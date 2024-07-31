from HRVPipeline.src.data_model.multichannel_signal import MultiChannelProcessedSignal
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
from HRVPipeline.src.algorithm.preprocessing import resample_xarray, preprocess_snirf_data


class AugmentationPipelineStage(PipelineStage):
    def __init__(self, config):
        super(AugmentationPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def run(self, pipeline_input: MultiChannelProcessedSignal) -> MultiChannelProcessedSignal:
        raw = pipeline_input
        target_sr = self.config.eval_sampling_rate

        amp2d_resampled = resample_xarray(raw.signals, target_sr)  # TODO skip if eval_mode = False

        res = MultiChannelProcessedSignal(signals=amp2d_resampled,
                                          sampling_rate=target_sr,
                                          channels=raw.channels)
        return res
