import numpy as np
import scipy.signal as signal
import networkx as nx
from matplotlib import pyplot as plt
import xarray as xr
import heartpy as hp
import neurokit2 as nk

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


# Load SNIRF data
def load_snirf_data(path):
    elements = cedalion.io.read_snirf(path)
    amp3d = elements[0].data[0]
    amp3d = amp3d.sel(time=amp3d.time < 20)
    amp2d = amp3d.stack(flat_channel=["channel", "wavelength"])
    return amp2d, amp2d.cd.sampling_rate

def filter_signal(data, sr):
    # return hp.filter_signal(data, [0.5, 3], sample_rate=sr, order=2, filtertype='bandpass')
    return nk.signal_filter(data, sr, 0.5, 3, order=2)
# Preprocess SNIRF data
def preprocess_snirf_data(amp2d, sampling_rate):
    filtered_data_list = []
    channel_name_list = []
    for i, fc in enumerate(amp2d.flat_channel.values):
        channel_data = amp2d.sel(flat_channel=fc)
        filtered_data = filter_signal(channel_data.values, sampling_rate)
        # filtered_data = channel_data.values
        filtered_data_list.append(filtered_data)
        # print('-------------channel ', i, ': ', fc, channel_data)
        channel_name_list.append(fc)
    return filtered_data_list, channel_name_list


def normalize(sig):
    min_val = np.min(sig)
    max_val = np.max(sig)
    normalized_signal = (sig - min_val) / (max_val - min_val)
    return normalized_signal


def resample_xarray(xarray, new_sr):
    duration = xarray.time.values[-1] - xarray.time.values[0]
    new_length = int(duration * new_sr)

    resampled_data = signal.resample(xarray.values, new_length)
    new_time = np.linspace(xarray.time.values[0], xarray.time.values[-1], new_length)
    # print('resample_xarray :', xarray.coords)
    cords = {**xarray.coords}
    cords.pop('samples', None)
    return xr.DataArray(resampled_data, dims=xarray.dims, coords={**cords, 'time': new_time})
    # return xarray


# def ampd(y):
#     L = len(y)
#     Lh = int(np.ceil(L / 2.0))
#     m = np.zeros((Lh, Lh))
#     Lmin = np.zeros(L)
#
#     for k in range(1, Lh + 1):
#         m[k - 1, :] = (y[k - 1:L - k + 1] - y[:L - 2 * k + 2]) < 0
#
#     for j in range(Lh):
#         Lmin += m[j, :]
#
#     Lmin = Lmin[:Lh]
#     indices = np.where(Lmin == 0)[0]
#     peaks = indices + 1
#
#     return peaks

# Main processing

def ampd(signal):
    # Ensure the signal is a numpy array
    signal = np.asarray(signal, dtype=float)

    if signal.ndim != 1:
        raise ValueError("Input signal must be a one-dimensional array")

    # Detrend signal using a linear fit
    time = np.arange(len(signal))
    fit_polynomial = np.polyfit(time, signal, 1)
    fit_signal = np.polyval(fit_polynomial, time)
    dtr_signal = signal - fit_signal

    # Initialize variables
    N = len(dtr_signal)
    L = int(np.ceil(N / 2.0)) - 1
    LSM = np.ones((L, N)) + np.random.rand(L, N)

    # Generate Local Scalogram Matrix (LSM)
    for k in range(1, L + 1):
        for i in range(k + 1, N - k):
            if dtr_signal[i] > dtr_signal[i - k] and dtr_signal[i] > dtr_signal[i + k]:
                LSM[k - 1, i] = 0

    # Find the optimal scale (l) with the minimum G
    G = np.sum(LSM, axis=1)
    l = np.argmin(G) + 1

    # Use only the first 'l' rows of LSM
    LSM = LSM[:l, :]

    # Calculate standard deviation along the columns
    S = np.std(LSM, axis=0)

    # Find peaks where standard deviation is zero
    peaks = np.where(S == 0)[0]

    return peaks


def main():
    path = r"src\data\NIRxData_compact\2024-04-09_001\2024-04-09_001.snirf"
    amp2d, sampling_rate = load_snirf_data(path)
    target_sr = 500
    amp2d_resampled = resample_xarray(amp2d, target_sr)
    sampling_rate = target_sr
    # amp2d_resampled = amp2d

    filtered_data_list, channels = preprocess_snirf_data(amp2d_resampled, sampling_rate)

    times = amp2d_resampled.time.values * 1000
    # Extracting features from all channels
    features_list = []
    peaks_list = []
    # slopes_list = []
    # onsets_list = []
    # f, ax = p.subplots(1, 1, figsize=(24, 8))

    # for i, filtered_data in enumerate(filtered_data_list):
    #     pass
    fig, ax = plt.subplots(1, 1, figsize=(24, 8))
    for i, channel_data in enumerate(filtered_data_list):
        # print(f'############## channel_data shape {np.shape(channel_data)}')
    # channel_data = filtered_data_list[0]

        peaks = ampd(channel_data)

        peak_times = times[peaks]

        # print("ampd peaks :", peak_times)


        estimated_ibis = np.diff(peak_times)

        print("Estimated IBIs:", i, channels[i], np.mean(estimated_ibis), np.std(estimated_ibis))

        # Plot the results


        ax.plot(times, normalize(channel_data), label=channels[i])
        # for peak in peak_times:
        #     ax.axvline(x=peak, color='black', linestyle='--', linewidth=1)
    # plt.figure(figsize=(14, 7))
    plt.title('AMPD Peak Detection on SNIRF Data')
    plt.xlabel('time (ms)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
