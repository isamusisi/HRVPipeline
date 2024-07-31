from HRVPipeline.src.config.common_config import CommonConfig


class BaselineConfig(CommonConfig):
    def __init__(self,eval_sampling_rate):
        super(BaselineConfig, self).__init__(eval_sampling_rate)