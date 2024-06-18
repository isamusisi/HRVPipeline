import time
from datetime import datetime, timezone

import heartpy as hp
import neurokit2 as nk
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import xarray as xr

import HRVPipeline.src.util.plot as p


def make_noise(ppg, snr=0.1):
    noised = np.random.normal(0, 1, len(ppg))

    return noised + ppg


def get_sampling_rate_from_timestamps(ppg):
    # times = ppg["timestamp"]
    times = ppg.index.to_series()
    time_format = "%Y-%m-%d-%H:%M:%S"
    dt = [datetime.fromtimestamp(t / 1000).strftime(time_format) for t in times]
    sr = round(hp.get_samplerate_datetime(dt, time_format), 2)
    # print(f"---------get_sampling_rate_timestamps--------{sr}-{calc_sampling_rate(ppg)}")
    # calc_sampling_rate(ppg)
    print(f"calculated sampling rate: {sr}")
    return sr


def get_sampling_rate(times):
    print(f"pre calculated sampling rate: {times[0]}")
    sr = hp.get_samplerate_mstimer(times)
    # print(f"---------get_sampling_rate_timestamps--------{sr}-{calc_sampling_rate(ppg)}")
    # calc_sampling_rate(ppg)
    print(f"calculated sampling rate: {sr}")
    return round(sr, 2)


def resample_ppg(ppg):
    # sr = calc_sampling_rate(ppg)
    sr = get_sampling_rate_from_timestamps(ppg)
    # sr = 9
    resampled = pd.DataFrame()
    # print(f"---------resample_ppg columns--------{ppg.columns}""")
    for i, c in enumerate(ppg.columns):
        # resampled.insert()
        # print(f"---------resample_ppg column--------{c} {i}")
        resampled.insert(i, c, nk.signal_resample(ppg[c], sampling_rate=int(sr), desired_sampling_rate=25))
    sr = get_sampling_rate_from_timestamps(ppg)
    resampled_ppg = nk.signal_resample(ppg["green"], sampling_rate=int(sr), desired_sampling_rate=25)
    # resampled = nk.signal_resample(ppg, sampling_rate=int(sr), desired_sampling_rate=25)
    # print(f"---------resample_ppg---------{sr}-{resampled[0]}-")
    # return pd.DataFrame(resampled, columns=["green"])
    return resampled


def get_filtered_ppg(ppg):
    sr = 25  # get_sampling_rate_timestamps(ppg)
    filtered_ppg = ppg.apply(lambda x: hp.filter_signal(x, [0.5, 3],
                                                        sample_rate=sr,
                                                        order=2,
                                                        filtertype='bandpass'))
    return filtered_ppg


def get_mock_ppg(duration=10, sampling_rate=25, heart_rate=70):
    ppg = nk.ppg_simulate(duration=duration, sampling_rate=sampling_rate, heart_rate=heart_rate)
    # print(f"---------get_mock_ppg--------{ppg}")
    return ppg


def get_ppg_peaks(ppg):
    signals, info = nk.ppg_process(ppg["green"], sampling_rate=25)
    hr = signals["PPG_Rate"]
    peaks = np.array(signals["PPG_Peaks"])
    # df = DataFrame({'signal': signals, 'hr': hr})
    # df.insert()
    ppg.insert(ppg.shape[1], "peaks", peaks, True)
    # print(f"---------get_ppg_peaks-------- {peaks} {ppg}")


def get_snirf_ppg_peaks(ppg, sr):
    signals, info = nk.ppg_process(ppg, sampling_rate=sr)
    hr = signals["PPG_Rate"]
    peaks = xr.DataArray(signals["PPG_Peaks"].values, dims=['time'])
    # df = DataFrame({'signal': signals, 'hr': hr})
    # df.insert()
    # ppg.insert(ppg.shape[1], "peaks", peaks, True)
    result = xr.Dataset({'PPG': ppg, 'peaks': peaks})
    return result
