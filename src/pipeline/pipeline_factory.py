
from src.neurokit_imp.pipelinestage_neurokit_hrv import NeurokitPipelineStageHRV
from src.neurokit_imp.pipelinestage_neurokit_input import NeurokitPipelineStageInput
from src.neurokit_imp.pipelinestage_neurokit_output import NeurokitPipelineStageOutput
from src.neurokit_imp.pipelinestage_neurokit_preprocessing import NeurokitPipelineStagePreprocessing
from src.pipeline.pipeline import Pipeline


class PipelineFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_neurokit_pipeline():
        config = {"sampling_rate":25}
        pipeline = Pipeline()
        pipeline.add_stage(NeurokitPipelineStageInput())
        pipeline.add_stage(NeurokitPipelineStagePreprocessing(config))
        pipeline.add_stage(NeurokitPipelineStageHRV())
        pipeline.add_stage(NeurokitPipelineStageOutput())
        return pipeline

    @staticmethod
    def create_neurokit_pipeline_plus():
        config = {"sampling_rate": 26}
        pipeline = Pipeline()
        pipeline.add_stage(NeurokitPipelineStageInput())
        pipeline.add_stage(NeurokitPipelineStagePreprocessing(config))
        pipeline.add_stage(NeurokitPipelineStageHRV())
        pipeline.add_stage(NeurokitPipelineStageOutput())
        return pipeline