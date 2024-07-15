from HRVPipeline.src.algorithm.ampd_peak_detection import ampd
from HRVPipeline.src.algorithm.graph_peak_detection import calc_features_list, calculate_average_hr, construct_dag
from HRVPipeline.src.data_model.multichannel_signal import MultiChannelRawSignal, MultiChannelProcessedSignal
from HRVPipeline.src.data_model.peak_signal import PeakSignal, IbisSignal
from HRVPipeline.src.hrv_methods import get_snirf_ppg_peaks
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
import numpy as np

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

        print(filtered_data_list.shape)
        filtered_data_list = filtered_data_list.transpose()
        for i, channel_data in enumerate(filtered_data_list):
            # print(f'############## channel_data shape {np.shape(channel_data)}')
            # channel_data = filtered_data_list[0]

            peaks = ampd(channel_data)

            peak_times = times[peaks]

            # print("ampd peaks :", peak_times)

            estimated_ibis = np.diff(peak_times)

            print(f"Estimated IBIs {i}:", np.mean(estimated_ibis), np.std(estimated_ibis))#, estimated_ibis)


        res = IbisSignal(signals=processed, ibis=estimated_ibis)
        return res



