import cedalion
from HRVPipeline.src.hrv_methods import get_snirf_ppg_peaks
from cedalion.io import read_snirf
import matplotlib.pyplot as p
import numpy as np
import xarray as xr
import cedalion.xrutils
import cedalion.xrutils as xrutils
# import src.hrv_methods as hrv
import neurokit2 as nk

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, find_peaks
from scipy.interpolate import splrep, splev
from scipy.ndimage import gaussian_filter1d
from heapq import heappop, heappush

cedalion.units.define("@alias ohm = Ohm")
cedalion.units.define("@alias degC = oC")
cedalion.units.define("ADU = dimensionless")


def bandpass_filter(signal, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)


def preprocess_ppg(ppg_signal, fs):
    ppg_signal = bandpass_filter(ppg_signal, 0.7, 15, fs, order=5)
    return ppg_signal


def find_candidate_peaks(ppg_signal, distance=1):
    peaks, _ = find_peaks(ppg_signal, distance=distance)
    return peaks


def create_graph(peaks_timestamps):
    graph = {}
    for i, t1 in enumerate(peaks_timestamps):
        graph[i] = []
        for j in range(i + 1, len(peaks_timestamps)):
            t2 = peaks_timestamps[j]
            interval = t2 - t1
            if interval <= 1.5 * np.mean(np.diff(peaks_timestamps)):
                graph[i].append((j, interval))
    return graph


def convex_penalty_function(interval, mean_ibi, alpha=2):
    return (interval - mean_ibi) ** alpha


def shortest_path(graph, start, end, mean_ibi):
    heap = [(0, start, [])]
    visited = set()
    while heap:
        (cost, u, path) = heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        path = path + [u]
        if u == end:
            return cost, path
        for v, weight in graph.get(u, ()):
            if v not in visited:
                heappush(heap, (cost + convex_penalty_function(weight, mean_ibi), v, path))
        print("visited nodes:", visited, heap)
    return float("inf"), []


def estimate_ibis(peaks_timestamps, path):
    return np.diff([peaks_timestamps[i] for i in path])


def main():
    path = r"src\data\NIRxData_compact\2024-04-09_001\2024-04-09_001.snirf"
    elements = cedalion.io.read_snirf(path)

    amp3d = elements[0].data[0]
    amp3d = amp3d.sel(time=amp3d.time[40:160])
    # stack channel and wavelength dims into a new dimension called flat_channel
    amp2d = amp3d.stack(flat_channel=["channel", "wavelength"])
    sr = amp2d.cd.sampling_rate
    mean_ibis = []
    peak_candidates = []
    for fc in amp2d.flat_channel.values:
        channel_data = amp2d.sel(flat_channel=fc)
        # print(fc, channel_data[:10])
        # Load your PPG signal data here
        # ppg_data should be a 1D numpy array of PPG signal values
        # ppg_data = pd.read_csv("ppg_signal.csv").values.flatten()
        # fs = 500  # Sampling frequency

        # Preprocess PPG signal
        # ppg_data = preprocess_ppg(channel_data.values, sr)

        peaks = get_snirf_ppg_peaks(channel_data, sr)

        peak_indices = np.array(peaks.peaks)
        peak_times = channel_data.time.values * peak_indices
        peak_times = [i for i in peak_times if i > 0]

        peak_candidates.extend(peak_times)
        print(f"peak_times: {len(peaks.peaks)} {peak_times}")

        # Find candidate peaks
        # peaks = find_candidate_peaks(ppg_data, distance=sr // 2)  # Assuming average HR around 60-120 bpm

        # Estimate average IBI
        mean_ibi = np.mean(np.diff(peak_times))
        mean_ibis.append(mean_ibi)

    # Create graph
    # peak_candidates = np.array(peak_candidates).flatten()
    peak_candidates.sort()
    print(f"peak_candidates: {len(peak_candidates)} {peak_candidates}")
    graph = create_graph(peak_candidates)
    # Find shortest path for IBI estimation
    start, end = 0, len(peak_candidates) - 1
    cost, path = shortest_path(graph, start, end, np.mean(mean_ibis))
    print("Estimation params:", np.mean(mean_ibis), cost, start, end, path)
    #
    # # Estimate IBIs
    estimated_ibis = estimate_ibis(peak_candidates, path)
    print("Estimated IBIs:", len(estimated_ibis), estimated_ibis)


if __name__ == "__main__":
    main()
