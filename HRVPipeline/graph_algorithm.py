import numpy as np
import scipy.signal as signal
import networkx as nx
import cedalion.io
from HRVPipeline.src.hrv_methods import get_snirf_ppg_peaks
import matplotlib.pyplot as plt
import xarray as xr
import heartpy as hp
import neurokit2 as nk


# Band-pass filter function
def bandpass_filter(data, cutoff_freqs, fs):
    nyquist = 0.5 * fs
    low, high = cutoff_freqs[0] / nyquist, cutoff_freqs[1] / nyquist
    print('Bandpass filter params:', low, high, nyquist, fs)
    b, a = signal.butter(2, [low, high], btype='band')
    return signal.filtfilt(b, a, data)


# Band-pass filter using heartpy
def filter_signal(data, sr):
    # return hp.filter_signal(data, [0.5, 3], sample_rate=sr, order=2, filtertype='bandpass')
    return nk.signal_filter(data, sr, 0.5, 3, order=2)


# Feature extraction: systolic peaks, maximum slopes, and onset points
def extract_features(ppg):
    smoothed = signal.savgol_filter(ppg, 51, 3)  # 5th order smoothing spline
    peaks, _ = signal.find_peaks(smoothed)  # Systolic peaks
    slopes, _ = signal.find_peaks(np.gradient(smoothed))  # Maximum slopes
    onsets, _ = signal.find_peaks(np.gradient(np.gradient(smoothed)))  # Onset points
    return peaks, slopes, onsets


# Construct a directed acyclic graph (DAG) from features and average IBIs
def construct_dag(features, avg_ibis):
    G = nx.DiGraph()
    fs = list(reversed(features))
    ibis = list(reversed(avg_ibis))
    for i, v_i in enumerate(fs):
        v_i = v_i[0]
        avg_ibi = ibis[i]
        for j, v_j in enumerate(fs[i + 1:]):
            v_j = v_j[0]
            dis = abs(v_i - v_j)
            if dis < 1.5 * avg_ibi:
                w = np.pi * dis ** 5
                G.add_edge(v_i, v_j, weight=w)
    return G


# Greedy fusion of features to estimate IBIs
def greedy_fusion(features_list, avg_ibis):
    estimated_ibis = []
    for ind, key2 in enumerate(features_list):
        for key in features_list[key2]:
            if len(features_list[key2][key]) >= 3:
                for i in range(0, len(features_list[key2][key]), 3):
                    if i + 2 < len(features_list[key2][key]):
                        if len(features_list[key2][key]) >= 3:
                            feature = features_list[key2][key][i]
                            estimated_ibi = feature  # Adjust fusion logic as needed
                            estimated_ibis.append(estimated_ibi)
    return estimated_ibis


# Load SNIRF data
def load_snirf_data(path):
    elements = cedalion.io.read_snirf(path)
    amp3d = elements[0].data[0]
    amp3d = amp3d.sel(time=amp3d.time < 20)
    amp2d = amp3d.stack(flat_channel=["channel", "wavelength"])
    return amp2d, amp2d.cd.sampling_rate


# Preprocess SNIRF data by filtering
def preprocess_snirf_data(amp2d, sampling_rate):
    filtered_data_list = []
    channel_name_list = []
    for i, fc in enumerate(amp2d.flat_channel.values):
        channel_data = amp2d.sel(flat_channel=fc)
        filtered_data = filter_signal(channel_data.values, sampling_rate)
        # filtered_data = channel_data.values
        filtered_data_list.append(filtered_data)
        print('-------------channel ', i, ': ', fc, channel_data)
        channel_name_list.append(fc)
    return filtered_data_list, channel_name_list


# Calculate average heart rate from peak timestamps
def calculate_average_hr(peak_timestamps, peaks_dict):
    window_length = 8 * 1000  # Length of the window in milliseconds
    hr_estimates = []

    for item in peak_timestamps:
        timestamp = item[0]
        channel = item[1]
        peak_list = peaks_dict[channel]
        first = peak_list[0]
        last = peak_list[-1]

        if timestamp - first >= window_length and last - timestamp >= window_length:
            closest_window_start = timestamp - window_length / 2
            closest_window_end = closest_window_start + window_length
        elif timestamp - first < window_length:
            closest_window_start = first
            closest_window_end = closest_window_start + window_length
        else:
            closest_window_end = last
            closest_window_start = closest_window_end - window_length

        peaks = [i for i in peak_list if closest_window_start <= i <= closest_window_end]
        hr = (60 / 8 * len(peaks))
        # print('HR:', timestamp, closest_window_start, closest_window_end, hr, peaks)
        hr_estimate = 60000 / hr
        hr_estimates.append(hr_estimate)

    return hr_estimates


# Normalize signal
def normalize(sig):
    min_val = np.min(sig)
    max_val = np.max(sig)
    return (sig - min_val) / (max_val - min_val)


# Resample xarray data to a new sampling rate
def resample_xarray(xarray, new_sr):
    duration = xarray.time.values[-1] - xarray.time.values[0]
    new_length = int(duration * new_sr)

    resampled_data = signal.resample(xarray.values, new_length)
    new_time = np.linspace(xarray.time.values[0], xarray.time.values[-1], new_length)
    print('resample_xarray :', xarray.coords)
    cords = {**xarray.coords}
    cords.pop('samples', None)
    return xr.DataArray(resampled_data, dims=xarray.dims, coords={**cords, 'time': new_time})
    # return xarray


def plot_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=500)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, arrowstyle='->', arrowsize=20)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

    # Show edge weights
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title('Graph Representation of IBI')
    plt.show()

# Main processing function
def main():
    path = r"src\data\NIRxData_compact\2024-04-09_001\2024-04-09_001.snirf"
    amp2d, sampling_rate = load_snirf_data(path)
    target_sr = 500
    amp2d_resampled = resample_xarray(amp2d, target_sr)
    sampling_rate = target_sr
    # amp2d_resampled = amp2d

    filtered_data_list, channels = preprocess_snirf_data(amp2d_resampled, sampling_rate)

    times = amp2d_resampled.time.values * 1000
    features_list = []
    peaks_dict = {}
    fig, ax = plt.subplots(1, 1, figsize=(24, 8))
    y_values = []
    shift = 0.01
    for i, filtered_data in enumerate(filtered_data_list):
        # print('filtered_data', i, filtered_data)
        peaks = get_snirf_ppg_peaks(filtered_data, sampling_rate)
        line, = ax.plot(times, normalize(filtered_data), label=channels[i])
        # line, = ax.plot(times, normalize(filtered_data))
        # line, = ax.plot([])
        y_value = i * shift
        y_values.append(y_value)
        peak_indices = np.array(peaks.peaks.values)
        peak_times = times * peak_indices
        # print(f'############## peak_times shape {peak_times.shape}')
        peak_times_raw = [pt for pt in peak_times if pt > 0]
        peak_times = [(pt, i) for pt in peak_times if pt > 0]
        # print('Extracted peaks:', peak_times)
        peaks_dict[i] = peak_times_raw
        features_list.extend(peak_times)
        line_color = line.get_color()



        for peak in peak_times:
            if peak[0] > 0:
                ax.scatter(x=peak[0], y=y_value, color=line_color, edgecolor='black', s=100, zorder=5)

    ax.legend(loc='right', bbox_to_anchor=(1.1, 0.5), ncol=1, fancybox=True)
    plt.title('40 channels peaks and estimated real peaks (dotted line)', fontdict={'fontsize': 16})
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("$\Delta c$ / $\mu M$")
    # ax.set_ylabel("Channel / Wavelength")
    # ax.set_yticks(y_values)
    # ax.set_yticklabels(channels)
    # plt.show()
    # exit(0)
    features_list.sort()

    avg_hrs = calculate_average_hr(features_list, peaks_dict)

    dag_features_list = construct_dag(features_list, avg_hrs)

    # plot_graph(dag_features_list)

    nodes = list(dag_features_list.nodes)
    shortest_path_features = nx.shortest_path(dag_features_list, source=nodes[0], target=nodes[-1])
    estimated_ibis = []

    shortest_path_times = list(shortest_path_features)
    shortest_path_times.reverse()
    ibis = np.diff(shortest_path_times)

    for time in shortest_path_times:
        if time > 0:
            ax.axvline(x=time, color='black', linestyle='--', linewidth=1)
    shortest_path_times.sort()

    for i, time in enumerate(shortest_path_times):
        if i > 0:
            estimated_ibis.append(time - shortest_path_times[i - 1])

    print("Estimated IBIs 1:", np.mean(estimated_ibis), np.std(estimated_ibis), estimated_ibis)
    print("Estimated IBIs 2:", np.mean(ibis), np.std(ibis), ibis)

    plt.show()


if __name__ == "__main__":
    main()

#  I now have a complete implementation of the graph algorithm through all steps.
#
# 1.) Preprocess the PPG Signal
#
# In this step i first apply a filter on the signal for each channel
#
# import heartpy as hp
#
# hp.filter_signal(channel, [0.5, 3], sample_rate=sr, order=2, filtertype='bandpass')
#
#
# and than i resample it to a higher sampling rate. In this case fron 20Hz to 500Hz since that is the sampling rate of the reference PPG/ECG signal.
#
# import scipy.signal as signal
#
# target_sr = 500
#
# duration = data.time.values[-1] - data.time.values[0]
# new_length = int(duration * new_sr)
#
# resampled_data = signal.resample(data.values, new_length)
