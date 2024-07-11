import networkx as nx
import numpy as np

from HRVPipeline.src.hrv_methods import get_snirf_ppg_peaks


def calc_features_list(filtered_data_list, sampling_rate, times):
    features_list = []
    peaks_dict = {}
    y_values = []
    shift = 0.01
    for i, filtered_data in enumerate(filtered_data_list):
        # print('filtered_data', i, filtered_data)
        peaks = get_snirf_ppg_peaks(filtered_data, sampling_rate)

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
    features_list.sort()
    return features_list, peaks_dict


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
