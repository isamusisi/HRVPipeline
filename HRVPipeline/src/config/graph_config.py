from HRVPipeline.src.config.common_config import CommonConfig


class GraphConfig(CommonConfig):
    def __init__(self,eval_sampling_rate):
        super(GraphConfig, self).__init__(eval_sampling_rate)
