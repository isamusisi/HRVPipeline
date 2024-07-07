import numpy as np
import scipy.signal as signal
import networkx as nx
import cedalion.io
from sklearn.cluster import KMeans

from HRVPipeline.src.hrv_methods import get_snirf_ppg_peaks
import matplotlib.pyplot as plt
import xarray as xr
import heartpy as hp
import neurokit2 as nk


# Band-pass filter function

def load_snirf_data(path):
    elements = cedalion.io.read_snirf(path)
    amp3d = elements[0].aux['ExGa1']
    amp3d = amp3d.sel(time=amp3d.time < 20)
    return amp3d, amp3d.cd.sampling_rate


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


# Main processing function
def main():
    path = r"src\data\NIRxData_compact\2024-04-09_001\2024-04-09_001.snirf"
    ecg, sampling_rate = load_snirf_data(path)
    # target_sr = 25
    # amp2d_resampled = resample_xarray(ecg, target_sr)
    # sampling_rate = target_sr
    # amp2d_resampled = amp2d

    times = ecg.time.values * 1000
    features_list = []
    peaks_dict = {}
    peaks_indices_all = []
    peaks_indices_dict = {}
    fig, ax = plt.subplots(1, 1, figsize=(24, 8))
    ax.plot(times, normalize(ecg), label='ECG')
    # for i, filtered_data in enumerate(filtered_data_list):
    #     # print('filtered_data', i, filtered_data)
    #     peaks = get_snirf_ppg_peaks(filtered_data, sampling_rate)
    #     line, = ax.plot(times, normalize(filtered_data), label=channels[i])
    #     peak_indices = np.array(peaks.peaks.values)
    #     peak_times = times * peak_indices
    #     # print(f'############## peak_times shape {peak_times.shape}')
    #     peak_times_raw = [pt for pt in peak_times if pt > 0]
    #     peak_times = [(pt, i) for pt in peak_times if pt > 0]
    #     # print('Extracted peaks:', peak_times)
    #     peaks_dict[i] = peak_times_raw
    #     peaks_indices_dict[i] = peak_indices
    #     peaks_indices_all.append(peak_indices)
    #
    #     features_list.extend(peak_times_raw)
    #     line_color = line.get_color()
    #
    #     shift = 0.01
    #
    #     for peak in peak_times:
    #         if peak[0] > 0:
    #             ax.scatter(x=peak[0], y=i * shift, color=line_color, edgecolor='black', s=100, zorder=5)

    print("ecg shape:", ecg.values.shape, sampling_rate)

    ecg_info, r_peaks = nk.ecg_process(ecg.values, sampling_rate=sampling_rate)
    peak_indices = ecg_info['ECG_R_Peaks']

    peak_times = times * peak_indices
    # print(f'############## peak_times shape {peak_times.shape}')
    peak_times = [pt for pt in peak_times if pt > 0]

    for peak in peak_times:
        ax.axvline(x=peak, color='black', linestyle='--', linewidth=1)

    estimated_ibis = np.diff(peak_times)

    print("Estimated IBIs:", np.mean(estimated_ibis), np.std(estimated_ibis), estimated_ibis)

    ax.legend()
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("$\Delta c$ / $\mu M$")

    features_list.sort()


    plt.show()


if __name__ == "__main__":
    main()

# baseline: 837.0633, 73.97581593910678
# multi: 831.9140470649988 82.96791028226616
# graph: 836.3294802831144 76.13971832081398
# ampd ch1: 842.2865454545455 71.52871875415893