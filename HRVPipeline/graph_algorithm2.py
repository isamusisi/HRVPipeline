import numpy as np
import scipy.signal as signal
import networkx as nx
import cedalion.io
from HRVPipeline.src.hrv_methods import get_snirf_ppg_peaks
import matplotlib.pyplot as p

# Parameters
cutoff_freqs = (0.5, 15)


# Band-pass filter
def bandpass_filter(data, cutoff_freqs, fs):
    nyquist = 0.5 * fs
    low, high = cutoff_freqs[0] / nyquist, cutoff_freqs[1] / nyquist
    print('-------------------------bandpass_filter params', low, high, nyquist, fs)
    b, a = signal.butter(2, [low, high], btype='band')
    return signal.filtfilt(b, a, data)


# Feature extraction: systolic peaks, maximum slopes, and onset points
def extract_features(ppg):
    smoothed = signal.savgol_filter(ppg, 51, 3)  # 5th order smoothing spline
    peaks, _ = signal.find_peaks(smoothed)  # Systolic peaks
    slopes, _ = signal.find_peaks(np.gradient(smoothed))  # Maximum slopes
    onsets, _ = signal.find_peaks(np.gradient(np.gradient(smoothed)))  # Onset points
    return peaks, slopes, onsets


# Directed Acyclic Graph (DAG) construction and shortest path calculation
# def construct_dag_old(features, avg_ibi):
#     G = nx.DiGraph()
#     for feature in features:
#         for i, v_i in enumerate(feature):
#             for j in range(i + 1, len(feature)):
#                 v_j = feature[j]
#                 if v_j - v_i < 1.5 * avg_ibi:
#                     G.add_edge(v_i, v_j, weight=(v_j - v_i - avg_ibi) ** 2)
#     return G


# def construct_dag(features, avg_ibi):
#     G = nx.DiGraph()
#     # for feature in features:
#     for i, v_i in enumerate(features):
#         for j in range(i + 1, len(features)):
#             v_j = features[j]
#             if v_j - v_i < 1.5 * avg_ibi:
#                 G.add_edge(v_i, v_j, weight=(v_j - v_i - avg_ibi) ** 2)
#     return G
#

def construct_dag(features, avg_ibis):
    G = nx.DiGraph()
    # for feature in features:
    fs = list(reversed(features))
    ibis = list(reversed(avg_ibis))
    for i, v_i in enumerate(fs):
        avg_ibi = ibis[i]
        for j, v_j in enumerate(fs[i + 1:]):
            dis = abs(v_i - v_j)
            # print('++++++++++++++++++++++++++++construct_dag params', v_i, v_j, dis, avg_ibi, 1.5*avg_ibi)
            if dis < 1.5 * avg_ibi:
                w = np.pi * dis ** 2
                G.add_edge(v_i, v_j, weight=w)
    return G


# Greedy fusion method
def greedy_fusion_old(peaks_list, slopes_list, onsets_list, avg_ibis):
    fused_ibis = []
    for i in range(0, len(onsets_list[0]), 3):
        segment_candidates = []
        for peaks, slopes, onsets in zip(peaks_list, slopes_list, onsets_list):
            segment_candidates.extend(peaks[i:i + 3])
            segment_candidates.extend(slopes[i:i + 3])
            segment_candidates.extend(onsets[i:i + 3])

        segment_candidates = np.unique(segment_candidates)
        segment_candidates.sort()

        segment_ibis = []
        for j in range(2, len(segment_candidates)):
            ibi = segment_candidates[j] - segment_candidates[j - 1]
            if abs(ibi - avg_ibis) < avg_ibis * 0.2:
                segment_ibis.append(ibi)

        if segment_ibis:
            fused_ibis.extend(segment_ibis[:3])

    return fused_ibis


def greedy_fusion_old2(peaks_list, slopes_list, onsets_list, avg_ibis):
    estimated_ibis = []

    # Iterate over the keys of onsets_list instead of assuming 0
    for key2 in onsets_list:
        # Ensure the list for the current key has at least 3 elements
        for key in onsets_list[key2]:
            if len(onsets_list[key2][key]) >= 3:
                for i in range(0, len(onsets_list[key2][key]), 3):
                    if i + 2 < len(onsets_list[key2][key]):
                        # Example fusion logic (you may need to adjust this)
                        # print('-------------------------dag_onsets_list params', key2, key, onsets_list[key].values(),
                        #       onsets_list[key])
                        onset = onsets_list[key2][key][i]
                        slope = slopes_list[key2][key][i]
                        peak = peaks_list[key2][key][i]
                        estimated_ibi = onset + slope + peak - avg_ibis[key2]  # Adjust your fusion logic as needed
                        estimated_ibis.append(estimated_ibi)

    return estimated_ibis


def greedy_fusion(features_list, avg_ibis):
    estimated_ibis = []

    # Iterate over the keys of onsets_list instead of assuming 0
    for ind, key2 in enumerate(features_list):
        # Ensure the list for the current key has at least 3 elements
        for key in features_list[key2]:
            if len(features_list[key2][key]) >= 3:
                for i in range(0, len(features_list[key2][key]), 3):
                    if i + 2 < len(features_list[key2][key]):
                        if len(features_list[key2][key]) >= 3:
                            # Example fusion logic (you may need to adjust this)
                            # print('-------------------------dag_onsets_list params', avg_ibis, key2, key,
                            #       features_list[key2][key])
                            feature = features_list[key2][key][i]
                            estimated_ibi = feature  # Adjust your fusion logic as needed
                            estimated_ibis.append(estimated_ibi)

    return estimated_ibis


# Load SNIRF data
def load_snirf_data(path):
    elements = cedalion.io.read_snirf(path)
    amp3d = elements[0].data[0]
    amp3d = amp3d.sel(time=amp3d.time[40:160])
    amp2d = amp3d.stack(flat_channel=["channel", "wavelength"])
    return amp2d, amp2d.cd.sampling_rate


# Preprocess SNIRF data
def preprocess_snirf_data(amp2d, sampling_rate):
    filtered_data_list = []
    channel_name_list = []
    for fc in amp2d.flat_channel.values:
        channel_data = amp2d.sel(flat_channel=fc).values
        # filtered_data = bandpass_filter(channel_data, cutoff_freqs, sampling_rate)
        filtered_data = channel_data
        filtered_data_list.append(filtered_data)
        channel_name_list.append(fc)
    return filtered_data_list, channel_name_list


def calculate_average_hr(peak_timestamps):
    # Initialize variables
    window_length = 8 * 1000 # Length of the window in seconds
    hr_estimates = []

    # Iterate through each peak timestamp
    first = peak_timestamps[0]
    last = peak_timestamps[-1]
    for timestamp in peak_timestamps:
        # Find HR estimate for the closest 8-second window around the timestamp
        if timestamp - first >= window_length and last - timestamp >= window_length:
            closest_window_start = timestamp - window_length / 2
            closest_window_end = closest_window_start + window_length
        elif timestamp - first < window_length:
            closest_window_start = first
            closest_window_end = closest_window_start + window_length
        else:
            closest_window_end = last
            closest_window_start = closest_window_end - window_length
        # closest_window_start = min(timestamp, timestamp - window_length / 2)
        # closest_window_end = closest_window_start + window_length

        peaks = [i for i in peak_timestamps if closest_window_start <= i <= closest_window_end]

        # Simulated HR estimation based on the peak timestamp
        # In a real implementation, this would involve actual processing and filtering
        # Assuming a simplistic approach of extracting HR from timestamps
        hr = (60/8 * len(peaks))
        # print('hr---------------', timestamp, closest_window_start, closest_window_end, hr, peaks)
        # hr_estimate = 60000 / hr
        hr_estimate = 60000 / 74

        hr_estimates.append(hr_estimate)

    # Calculate average heart rate
    return hr_estimates


def normalize(sig):
    min_val = np.min(sig)
    max_val = np.max(sig)
    normalized_signal = (sig - min_val) / (max_val - min_val)
    return normalized_signal


# Main processing
def main():
    path = r"src\data\NIRxData_compact\2024-04-09_001\2024-04-09_001.snirf"
    amp2d, sampling_rate = load_snirf_data(path)
    filtered_data_list, channels = preprocess_snirf_data(amp2d, sampling_rate)

    times = amp2d.time.values * 1000
    # Extracting features from all channels
    features_list = []
    peaks_list = []
    # slopes_list = []
    # onsets_list = []
    f, ax = p.subplots(1, 1, figsize=(24, 8))

    for i, filtered_data in enumerate(filtered_data_list):
        # peaks, slopes, onsets = extract_features(filtered_data)
        peaks = get_snirf_ppg_peaks(filtered_data, sampling_rate)
        line, = ax.plot(times, normalize(filtered_data), label=channels[i])
        peak_indices = np.array(peaks.peaks.values)
        peak_times = times * peak_indices
        peak_times = [i for i in peak_times if i > 0]
        print('-------------------------extract_features peaks', peak_times)
        peaks_list.append(peak_times)
        features_list.extend(peak_times)
        # features_list.append(slopes)
        # features_list.append(onsets)
        # slopes_list.append(slopes)
        # onsets_list.append(onsets)
        line_color = line.get_color()

        shift = 0.01

        for peak in peak_times:
            if peak > 0:
                # ax.axvline(x=peak, color=line_color, linestyle='--', linewidth=1)
                ax.scatter(x=peak, y=i * shift, color=line_color, edgecolor='black', s=100, zorder=5)

        ax.legend()
        ax.set_xlabel("time / s")
        ax.set_ylabel("$\Delta c$ / $\mu M$")

    features_list = list(set(features_list))
    features_list.sort()

    # Estimating average heart rate and IBI
    hr_avg_list = [60000 / np.mean(np.diff(peaks)) for peaks in peaks_list if len(peaks) > 1]
    avg_ibis = np.mean(hr_avg_list) if hr_avg_list else 1000  # Default to 1000ms if hr_avg_list is empty

    print('-------------------------feature params', avg_ibis, len(features_list), features_list)
    # Constructing DAG for each feature set from each channel
    # dag_peaks_list = [construct_dag(peaks, avg_ibis) for peaks in peaks_list]
    # dag_slopes_list = [construct_dag(slopes, avg_ibis) for slopes in slopes_list]
    # dag_onsets_list = [construct_dag(onsets, avg_ibis) for onsets in onsets_list]
    avg_hrs = calculate_average_hr(features_list)

    print('-------------------------avg_hrs', len(avg_hrs), avg_hrs, avg_ibis)
    dag_features_list = construct_dag(features_list, avg_hrs)
    nodes = list(dag_features_list.nodes)
    print('-------------------------dag_features_list params', dag_features_list.nodes)
    print('-------------------------dag_features_list nodes', nodes[0])
    # dag_peaks_list = construct_dag(peaks_list, avg_ibis)
    # dag_slopes_list = construct_dag(slopes_list, avg_ibis)
    # dag_onsets_list = construct_dag(onsets_list, avg_ibis)
    # Finding shortest paths for each DAG
    # shortest_path_peaks = [nx.shortest_path(dag, weight='weight') for dag in dag_peaks_list]
    # shortest_path_slopes = [nx.shortest_path(dag, weight='weight') for dag in dag_slopes_list]
    # shortest_path_onsets = [nx.shortest_path(dag, weight='weight') for dag in dag_onsets_list]
    # shortest_path_features = nx.shortest_path(dag_features_list, weight='weight')
    shortest_path_features = nx.shortest_path(dag_features_list, source=nodes[0], target=nodes[-1])
    # shortest_path_peaks = nx.shortest_path(dag_peaks_list, weight='weight')
    # shortest_path_slopes = nx.shortest_path(dag_slopes_list, weight='weight')
    # shortest_path_onsets = nx.shortest_path(dag_onsets_list, weight='weight')

    # print('-------------------------shortest_path_features params', list(reversed(shortest_path_features.keys())))
    print('-------------------------shortest_path_features params', shortest_path_features)
    # Apply greedy fusion method to combine IBI sequences
    # estimated_ibis = greedy_fusion(shortest_path_peaks, shortest_path_slopes, shortest_path_onsets, avg_ibis)
    # estimated_ibis = greedy_fusion(shortest_path_features, avg_ibis)
    estimated_ibis = []

    # shortest_path_times = list(shortest_path_features.keys())
    shortest_path_times = list(shortest_path_features)

    for time in shortest_path_times:
        if time > 0:
            ax.axvline(x=time, color='black', linestyle='--', linewidth=1)
            # ax.scatter(x=peak, y=i * shift, color=line_color, edgecolor='black', s=100, zorder=5)
    shortest_path_times.sort()

    for i, time in enumerate(shortest_path_times):
        if i > 0:
            estimated_ibis.append(time - shortest_path_times[i - 1])

    print("Estimated IBIs: ", estimated_ibis)

    p.show()


if __name__ == "__main__":
    main()
