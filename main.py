# from src.util.io import read_log
import pandas as pd
import xarray as xr
from matplotlib import pyplot as plt

import src.util.io as io
import src.util.plot as p
import src.util.process as proc
import src.hrv_methods as hrv
import neurokit2 as nk

if __name__ == '__main__':
    print('=' * 70)
    # ins = io.read_log('src/data/input/log_isa5.txt')
    # print(ins.max("green"))
    # print(ins.mean("green"))
    # print(ins.sel(green=slice(0)))
    # flat = xr.DataArray(ins-proc.baseline_flat(ins, 5, 0.1), dims=["green_flat"])
    # print(flat.max("green_flat"))
    # print(flat.mean("green_flat"))
    # p.plot_signal([ins, flat])

    ppg = io.read_ppg('src/data/input/ppg_isa3.csv')
    resampled = hrv.resample_ppg(ppg)
    # print(f"--------resampled: {resampled}")
    hrv.calc_sampling_rate(ppg)

    # # xppg = xr.DataArray(ppg)
    # # print(xppg)
    # hrv.get_sampling_rate_from_timestamps(ppg)
    # hrv.calc_sampling_rate(ppg)
    filtered_raw = hrv.get_filtered_ppg(ppg)
    filtered_resampled = hrv.get_filtered_ppg(resampled)
    #

    # p.plot_signal([ppg["green"]], 'ppg_avg-9Hz(25Hz)_raw')
    # p.plot_signal([resampled["green"]], 'ppg_resampled_25Hz')
    p.plot_signal([filtered_raw["green"]], 'ppg_avg-9Hz(25Hz)_filtered')
    # p.plot_signal([filtered_resampled["green"]], 'ppg_resampled_25Hz_filtered')
    # p.plot_signal([ppg["green"]])
    #
    # hrv.get_mock_ppg()
    hrv.get_ppg_peaks(ppg)
    hrv.get_ppg_peaks(resampled)
    hrv.get_ppg_peaks(filtered_raw)
    hrv.get_ppg_peaks(filtered_resampled)
    # #

    # flat = pd.DataFrame(ppg["green"]-proc.baseline_flat(ppg["green"], 5, 0.1), columns=["green"])
    # p.plot_signal([flat["green"]])
    # hrv.get_ppg_peaks(flat)
    # p.plot_ppg(flat)
    # p.plot_signal([ppg["green"]])
    # p.plot_signal([resampled["green"]])

    # p.plot_ppg(ppg, 'ppg_avg-9Hz(25Hz)_raw_peaks')
    # p.plot_ppg(resampled, 'ppg_resampled_25Hz_peaks')
    p.plot_ppg(filtered_raw, 'ppg_avg-9Hz(25Hz)_filtered_peaks')
    # p.plot_ppg(filtered_resampled, 'ppg_resampled_25Hz_filtered_peaks')
    # p.plot_ppg(filtered_ppg)
    #
    # ppg = nk.ppg_simulate(duration=60, sampling_rate=25, heart_rate=70)
    # for ppg_signal in [ppg, resampled]:
    #     sr = hrv.
    #     signals, info = nk.ppg_process(ppg_signal, sampling_rate=25)
    #
    #     nk.ppg_plot(signals, info)
    #

    # signals_raw, info_raw = nk.ppg_process(ppg["green"], sampling_rate=25)
    # signals, info = nk.ppg_process(ppg["green"], sampling_rate=25)
    # signals, info = nk.ppg_process(flat["green"], sampling_rate=25)
    # signals, info = nk.ppg_process(ppg, sampling_rate=25)

    # nk.ppg_plot(signals_raw, info_raw)
    # nk.ppg_plot(signals, info)

    plt.show()
    # plt.close()
