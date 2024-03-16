from src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
from src.util.io import read_ppg


class NeurokitPipelineStageInput(PipelineStage):
    def __init__(self,config ={}):
        super().__init__(config)
        self.stage_type = PipelineStageType.INPUT

    def __str__(self):
        return "NeurokitPipeline"

    # TODO needed ? accept_input? overwrite?

    def run(self, pipeline_input):
        return read_ppg(pipeline_input)

