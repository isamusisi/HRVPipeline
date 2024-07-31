from HRVPipeline.src.algorithm.ampd_peak_detection import ampd
from HRVPipeline.src.algorithm.graph_peak_detection import calc_features_list, calculate_average_hr, construct_dag
from HRVPipeline.src.data_model.multichannel_signal import MultiChannelRawSignal, MultiChannelProcessedSignal
from HRVPipeline.src.data_model.peak_signal import PeakSignal, IbisSignal
from HRVPipeline.src.hrv_methods import get_snirf_ppg_peaks
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
import numpy as np
from threading import Thread


class OneChannelRunner(Thread):
    def __init__(self, i, channel_data, times):
        Thread.__init__(self)
        self.i = i
        self.channel_data = channel_data
        self.times = times
        self.estimated_ibis = None
        self.peak_indicies = None

    def run(self):
        peaks = ampd(self.channel_data)

        peak_times = self.times[peaks]

        self.peak_indicies = np.isin(self.times, peak_times).astype(int)

        # print("ampd peaks :", peak_times)

        self.estimated_ibis = np.diff(peak_times)

        # print(f"Estimated IBIs {self.i}:", np.mean(self.estimated_ibis), np.std(self.estimated_ibis))  # , estimated_ibis)


class AmpdPipelineStage(PipelineStage):
    def __init__(self, config):
        super(AmpdPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def run(self, pipeline_input: MultiChannelProcessedSignal) -> MultiChannelProcessedSignal:
        processed = pipeline_input

        filtered_data_list = processed.signals
        sampling_rate = processed.sampling_rate
        times = processed.times  # TODO

        # print(filtered_data_list.shape)
        filtered_data_list = filtered_data_list.transpose()
        runs = []

        for i, channel_data in enumerate(filtered_data_list):
            # print("starting ",i)
            # print(f'############## channel_data shape {np.shape(channel_data)}')
            # channel_data = filtered_data_list[0]
            run = OneChannelRunner(i, channel_data[:], times[:])
            run.start()
            run.join()  # run still consecutively
            runs.append(run)

        # run all in parallel
        # for run in runs:
        #    print("finished ",run.i)
        #    run.join()
        peak_indices = runs[0].peak_indicies  # TODO select proper
        estimated_ibis = runs[0].estimated_ibis
        # res = IbisSignal(signals=processed, ibis=estimated_ibis)
        res = PeakSignal(signals=processed, peaks=peak_indices, ibis=estimated_ibis, name='AMPD')
        return res
