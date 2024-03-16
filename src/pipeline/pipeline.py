from src.pipeline.pipeline_stage import PipelineStage, PipelineStageType



class StageIncompatible(Exception):
    # TODO move to a meaningfull place?
    def __init__(self, message="Stage is incompatible"):
        self.message = message
        super().__init__(self.message)


class Pipeline:
    def __init__(self):
        self.stages: PipelineStage = []

    def __str__(self):
        # TODO format nicely
        return f"PIPELINE"

    def run(self, pipeline_input):
        # assumption stage_0 is inpout only input
        # TODO better to somehow track inputs and somehow who needs them ...

        # TODO write tests
        result = self.stages[0].run(pipeline_input)

        for stage in self.stages[1:]:
            # TODO add hooks? like visual on_before_stage or rather in stage ...
            result = stage.run(result)
            # TODO add hooks? like visual on_after_stage (like plot)
        return result

    def add_stage(self, pipeline_stage: PipelineStage):

        if len(self.stages) == 0:  # empty ... should start with input stage...
            if pipeline_stage.stage_type != PipelineStageType.INPUT:
                raise StageIncompatible("Stages are incompatible")  # TODO more specific Exception?
            self.stages.append(pipeline_stage)
        else:
            if pipeline_stage.accept_as_input(self.stages[-1]):
                # ok is compatible
                self.stages.append(pipeline_stage)
            else:
                raise StageIncompatible("Stages are incompatible")
