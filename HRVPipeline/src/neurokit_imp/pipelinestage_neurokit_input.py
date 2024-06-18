from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
from HRVPipeline.src.util.io import read_ppg
from HRVPipeline.src.util.io import read_snirf_ppg
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

        print(f"------------------------config_input_type----------------------{self.config}, {config_input_type}, {config_input_type.value == InputType.SNIRF.value} {self.config['input_type'].value > InputType.MCS_CSV.value}")

        if config_input_type.value == InputType.MCS_CSV.value:
            return read_ppg(pipeline_input)
        elif config_input_type.value is InputType.SNIRF.value:
            return read_snirf_ppg(pipeline_input)
        raise Exception("Unsupported Input Config")
