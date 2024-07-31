import matplotlib.pyplot as plt

from HRVPipeline.src.algorithm.ampd_peak_detection import ampd
from HRVPipeline.src.algorithm.graph_peak_detection import calc_features_list, calculate_average_hr, construct_dag
from HRVPipeline.src.data_model.multichannel_signal import MultiChannelRawSignal, MultiChannelProcessedSignal
from HRVPipeline.src.data_model.peak_signal import PeakSignal, IbisSignal
from HRVPipeline.src.hrv_methods import get_snirf_ppg_peaks
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
import numpy as np
import neurokit2 as nk


class HRVPipelineStage(PipelineStage):
    def __init__(self, config):
        super(HRVPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.HRV_CALC

    def run(self, pipeline_input: PeakSignal):
        processed = pipeline_input
        hrv = nk.hrv(peaks=processed.peaks,
                     sampling_rate=processed.multi_channel_signals.sampling_rate,
                     show=self.config.plot)
        # print("HRV", hrv.columns.shape, hrv.columns)
        return hrv, processed.ibis, processed.name
