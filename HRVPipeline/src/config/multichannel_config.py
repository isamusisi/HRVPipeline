from HRVPipeline.src.config.common_config import CommonConfig


class MultichannelConfig(CommonConfig):
    def __init__(self,eval_sampling_rate):
        super(MultichannelConfig, self).__init__(eval_sampling_rate)