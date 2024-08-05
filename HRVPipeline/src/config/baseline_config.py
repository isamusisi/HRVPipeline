from HRVPipeline.src.config.common_config import CommonConfig


class BaselineConfig():
    def __init__(self, current_sampling_rate,plot=False):
        #super(BaselineConfig, self).__init__(eval_config)
        self.current_sampling_rate = current_sampling_rate
        self.plot =plot

        self.sample_length = CommonConfig.SAMPLE_LENGTH