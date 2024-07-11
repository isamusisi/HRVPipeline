import numpy as np

from HRVPipeline.src.algorithm.preprocessing import resample_xarray, preprocess_snirf_data
from HRVPipeline.src.data_model.multichannel_signal import MultiChannelProcessedSignal, MultiChannelRawSignal
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
from HRVPipeline.src.util.plot import plot_signal


class SnirfUpsamplingPipelineStage(PipelineStage):
    def __init__(self, config):
        super(SnirfUpsamplingPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def run(self, pipeline_input: MultiChannelRawSignal) -> MultiChannelProcessedSignal:
        raw = pipeline_input
        target_sr = 500

        amp2d_resampled = resample_xarray(raw.signals, target_sr)

        res = MultiChannelProcessedSignal(signals=amp2d_resampled,
                                          sampling_rate=target_sr,
                                          channels=raw.channels)
        return res


class SnirfFilterPipelineStage(PipelineStage):
    def __init__(self, config):
        super(SnirfFilterPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def run(self, pipeline_input: MultiChannelProcessedSignal) -> MultiChannelProcessedSignal:
        processed = pipeline_input

        amp2d_filtered = preprocess_snirf_data(processed.signals, processed.sampling_rate)

        times = processed.signals.time.values * 1000  # TODO not so nice

        plot_signal(np.transpose(amp2d_filtered.values))

        print('filtered xarray', amp2d_filtered)

        res = MultiChannelProcessedSignal(signals=amp2d_filtered.values,
                                          sampling_rate=processed.sampling_rate,
                                          channels=processed.channels,
                                          times=times)
        return res
