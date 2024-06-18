from enum import Enum
from typing import List


class PipelineStageType(Enum):
    INPUT = 0
    PRE_PROCESSING = 1
    FEATURE_EXTRACTION = 2
    HRV_CALC = 3
    OUTPUT = 4


# class PipelineStage:
#    pass

class PipelineStage:  # TODO inherit (ABC) == abstract class so it can not be constrcut
    def __init__(self, config={}):
        self.stage_type: PipelineStageType = PipelineStageType.INPUT
        self.config = config

        self.accepted_in: List[PipelineStageType] = []
        # TODO make sense? self.outs= []

    def __str__(self):
        # TODO format nicely
        return f"PIPELINE_STAGE {str(self.stage_type)}"

    def accept_as_input(self, stage: "PipelineStage") -> bool:
        # TODO think about adding list and objects / as input/output
        # TODO nicer
        if self.stage_type == PipelineStageType.INPUT:  # TODO well assert None?
            return stage.stage_type != PipelineStageType.INPUT
        else:
            return stage.stage_type in self.accepted_in

    # TODO call //run / invoke =?....
    def run(self, pipeline_input):  # TODO what about output types?!
        """put description here"""
        # TODO add hooks? like visual on_before_stage or rather in stage ...
        # result = stage.run(result) # TODO cache result?
        # TODO add hooks? like visual on_after_stage (like plot)
        pass
