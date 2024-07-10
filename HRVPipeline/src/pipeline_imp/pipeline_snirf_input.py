from HRVPipeline.src.data_model.multichannel_signal import MultiChannelRawSignal
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage
from HRVPipeline.src.algorithm.snirf_reader import *


class SnirfInputPipelineStage(PipelineStage):
    def __init__(self, config):
        super(SnirfInputPipelineStage, self).__init__(config)


    def run(self, pipeline_input)->MultiChannelRawSignal:
        path = pipeline_input
        amp2d, sampling_rate = load_snirf_data(path)
        res = MultiChannelRawSignal(signals=amp2d,
                                    sampling_rate=sampling_rate,
                                    channels=len(amp2d.flat_channel))
        return res