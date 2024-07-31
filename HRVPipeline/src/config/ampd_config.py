from HRVPipeline.src.config.common_config import CommonConfig


class AmpdConfig(CommonConfig):
    def __init__(self,eval_sampling_rate):
        super(AmpdConfig, self).__init__(eval_sampling_rate)