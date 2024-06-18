import cedalion
from cedalion.io import read_snirf
import matplotlib.pyplot as p
import numpy as np
import xarray as xr
import cedalion.xrutils
import cedalion.xrutils as xrutils
# import src.hrv_methods as hrv
import neurokit2 as nk


def get_snirf_ppg_peaks(ppg, sr):
    signals, info = nk.ppg_process(ppg, sampling_rate=sr)
    peaks = xr.DataArray(signals["PPG_Peaks"].values, dims=['time'])
    result = xr.Dataset({'PPG': ppg, 'peaks': peaks})
    return result


def normalize(signal):
    min_val = np.min(signal)
    max_val = np.max(signal)
    normalized_signal = (signal - min_val) / (max_val - min_val)
    return normalized_signal


if __name__ == "__main__":
    path = r"src\data\NIRxData_compact\2024-04-09_001\2024-04-09_001.snirf"

    elements = read_snirf(path)
    element = elements[0]  # there is only one NirsElement in this snirf file...
    amp = element.data[0]  # ... which holds amplitude data

    # restrict to first 60 seconds and fill in missing units
    amp = amp.sel(time=amp.time[40:160])
    amp = amp.pint.dequantify().pint.quantify("V")
    geo3d = element.geo3d

    dists = xrutils.norm(geo3d.loc[amp.source] - geo3d.loc[amp.detector], dim="pos")

    dpf = xr.DataArray([6., 6.], dims="wavelength", coords={"wavelength": [760., 850.]})

    E = cedalion.nirs.get_extinction_coefficients("prahl", amp.wavelength)
    Einv = cedalion.xrutils.pinv(E)

    optical_density = -np.log(amp / amp.mean("time"))

    conc = Einv @ (optical_density / (dists * dpf))

    channels = ['S1D1', 'S1D2', 'S2D1', 'S2D3', 'S3D2', 'S3D3', 'S3D4', 'S4D2', 'S4D4', 'S4D5', 'S5D3', 'S5D4', 'S5D6',
                'S6D4', 'S6D5', 'S6D6', 'S7D5', 'S7D7', 'S8D6', 'S8D7']
    # num_channels = len(channels)
    # num_rows = (num_channels + 1) // 2  # Round up if there's an odd number of channels
    # num_cols = 2
    f, ax = p.subplots(1, 1, figsize=(24, 8))
    # fig, axs = p.subplots(num_rows, num_cols, figsize=(24, 8 * num_rows), sharex='all')
    amp2d = amp.stack(flat_channel=["channel", "wavelength"])
    sr = amp2d.cd.sampling_rate
    mean_ibis = []
    peak_candidates = []
    peak_times_all = []
    for i, fc in enumerate(amp2d.flat_channel.values):
        channel_data = amp2d.sel(flat_channel=fc)

    # for i, channel in enumerate(channels):
    #     # ind = i // 2
    #     # ax = axs[ind][0 if i % 2 == 0 else 1]
    #     data = conc.sel(channel=channel, chromo="HbO").pint.to("micromolar")
    #     sr = conc.cd.sampling_rate
        channel = fc
        data = channel_data.values
        peaks = get_snirf_ppg_peaks(data, sr)

        peak_indices = np.array(peaks.peaks)
        peak_times = conc.time.values * peak_indices
        peak_times_all.extend(peak_times)
        # Plot the normalized signal
        line, = ax.plot(conc.time, normalize(data), label=channel)

        line_color = line.get_color()

        shift = 0.01

        for peak in peak_times:
            if peak > 0:
                ax.axvline(x=peak, color=line_color, linestyle='--', linewidth=1)
                ax.scatter(x=peak, y=i * shift, color=line_color, edgecolor='black', s=100, zorder=5)

        ax.legend()
        ax.set_xlabel("time / s")
        ax.set_ylabel("$\Delta c$ / $\mu M$")

    peak_times_all = list(set(peak_times_all))
    peak_times_all.sort()
    print('peak_times_all', len(peak_times_all), peak_times_all)

    p.show()
