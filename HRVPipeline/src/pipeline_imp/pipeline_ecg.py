
from HRVPipeline.src.algorithm.ampd_peak_detection import ampd
from HRVPipeline.src.algorithm.graph_peak_detection import calc_features_list, calculate_average_hr, construct_dag
from HRVPipeline.src.data_model.multichannel_signal import MultiChannelRawSignal, MultiChannelProcessedSignal
from HRVPipeline.src.data_model.peak_signal import PeakSignal, IbisSignal
from HRVPipeline.src.hrv_methods import get_snirf_ppg_peaks
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
import numpy as np
import cedalion.io
import neurokit2 as nk
import matplotlib.pyplot as plt
import scipy.signal as signal
import xarray as xr
def load_snirf_data(path,length):
    elements = cedalion.io.read_snirf(path)
    amp3d = elements[0].aux['ExGa1']
    amp3d = amp3d.sel(time=amp3d.time < length)
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
    #print('resample_xarray :', xarray.coords)
    cords = {**xarray.coords}
    cords.pop('samples', None)
    return xr.DataArray(resampled_data, dims=xarray.dims, coords={**cords, 'time': new_time})
    # return xarray

class EcgBasePipelineStage(PipelineStage):
    def __init__(self, config):
        super(EcgBasePipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.INPUT

    def run(self, pipeline_input):
        path = pipeline_input
        length = self.config.sample_length
        ecg, sampling_rate = load_snirf_data(path,length)


        # target_sr = 25
        # amp2d_resampled = resample_xarray(ecg, target_sr)
        # sampling_rate = target_sr
        # amp2d_resampled = amp2d

        times = ecg.time.values * 1000

        proccessed = MultiChannelProcessedSignal(ecg, sampling_rate, channels=1, times=times)

        features_list = []
        peaks_dict = {}
        peaks_indices_all = []
        peaks_indices_dict = {}
        if self.config.plot:
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

        #print("ecg shape:", ecg.values.shape, sampling_rate)

        ecg_info, r_peaks = nk.ecg_process(ecg.values, sampling_rate=sampling_rate)
        peak_indices = ecg_info['ECG_R_Peaks']

        peak_times = times * peak_indices
        # print(f'############## peak_times shape {peak_times.shape}')
        peak_times = [pt for pt in peak_times if pt > 0]

        if self.config.plot:
            for peak in peak_times:
                ax.axvline(x=peak, color='black', linestyle='--', linewidth=1)

        estimated_ibis = np.diff(peak_times)

        #print("Estimated IBIs:", np.mean(estimated_ibis), np.std(estimated_ibis), estimated_ibis)

        if self.config.plot:
            ax.legend()
            ax.set_xlabel("Time (ms)")
            ax.set_ylabel("$\Delta c$ / $\mu M$")

        features_list.sort()
        if self.config.plot:
            plt.show()
        res = PeakSignal(signals=proccessed, peaks=peak_indices, ibis=estimated_ibis, name='ECG')
        return res