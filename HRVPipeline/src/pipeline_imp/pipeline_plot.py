from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
from HRVPipeline.src.util.plot import plot_signal

VIS_CHANNEL = 7
class XarrayPlottingPipelineStage(PipelineStage):
    def __init__(self, config):
        super(XarrayPlottingPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def run(self, pipeline_input):
        raw = pipeline_input
        plot_signal([raw.signals.values[:,VIS_CHANNEL].transpose()])


        return pipeline_input


class NumpyArrayPlottingPipelineStage(PipelineStage):
    def __init__(self, config):
        super(NumpyArrayPlottingPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def run(self, pipeline_input):
        raw = pipeline_input
        plot_signal([raw.signals.transpose()[VIS_CHANNEL]])


        return pipeline_input