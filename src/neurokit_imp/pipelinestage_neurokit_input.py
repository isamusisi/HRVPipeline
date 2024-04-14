from src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
from src.util.io import read_ppg
from src.pipeline_input.snirf_reader import read_snirf
from enum import Enum

class InputType(Enum):
    MCS_CSV = 0
    SNIRF = 1

class NeurokitPipelineStageInput(PipelineStage):
    def __init__(self,config ={}):
        super().__init__(config)

        self.stage_type = PipelineStageType.INPUT

    def __str__(self):
        return "NeurokitPipeline"

    # TODO needed ? accept_input? overwrite?

    def run(self, pipeline_input):
        config_input_type = self.config["input_type"] # TODO Better to have two seperate classes?(and a wrapper?)

        if config_input_type == InputType.MCS_CSV:
            return read_ppg(pipeline_input)
        elif config_input_type == InputType.SNIRF:
            return read_snirf(pipeline_input) #[:,0] which of the 40
        raise Exception("Unsupported Input Config")
