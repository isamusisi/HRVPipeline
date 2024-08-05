from HRVPipeline.src.config.evaluation_config import EvaluationConfig


class CommonConfig:
    SAMPLE_LENGTH = 60*1
    def __init__(self, eval_config: EvaluationConfig):

        self.plot = False
        self.target_sampling_rate = 500
        self.snr_thresh = 16
        self.amp_threshs = [0.1, 3]

        self.sample_length = self.SAMPLE_LENGTH

        self.current_sampling_rate = eval_config.current_sampling_rate
        self.current_snr = eval_config.current_snr


