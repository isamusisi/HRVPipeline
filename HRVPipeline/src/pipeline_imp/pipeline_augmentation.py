from HRVPipeline.src.algorithm.ppg_augmentation import add_noise, add_artefacts, add_artefacts_b, add_artefacts_c, \
    add_artefacts_d
from HRVPipeline.src.data_model.multichannel_signal import MultiChannelProcessedSignal
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
from HRVPipeline.src.algorithm.preprocessing import resample_xarray, preprocess_snirf_data


class AugmentationPipelineStage(PipelineStage):
    def __init__(self, config):
        super(AugmentationPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def augment_sampling_rate(self, raw_signals, target_sr):
        amp2d_resampled = resample_xarray(raw_signals, target_sr)  # TODO skip if eval_mode = False
        return amp2d_resampled

    def run(self, pipeline_input: MultiChannelProcessedSignal) -> MultiChannelProcessedSignal:
        raw = pipeline_input
        target_sr = self.config.current_sampling_rate
        target_snr =  self.config.current_snr
        augmented_signal = raw.signals
        if target_sr is not None:
            augmented_signal = self.augment_sampling_rate(augmented_signal,target_sr)
        #augmented_signal = add_artefacts_d(augmented_signal,0.01,0.07)

        if target_snr is not None:
            augmented_signal = add_noise(augmented_signal,target_snr)



        print("SHAPE", augmented_signal.shape)

        res = MultiChannelProcessedSignal(signals=augmented_signal,
                                          sampling_rate=target_sr,
                                          channels=raw.channels)
        return res
