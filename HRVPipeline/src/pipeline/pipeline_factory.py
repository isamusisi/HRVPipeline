from HRVPipeline.src.neurokit_imp.pipelinestage_neurokit_hrv import NeurokitPipelineStageHRV
from HRVPipeline.src.neurokit_imp.pipelinestage_neurokit_input import NeurokitPipelineStageInput
from HRVPipeline.src.neurokit_imp.pipelinestage_neurokit_output import NeurokitPipelineStageOutput
from HRVPipeline.src.neurokit_imp.pipelinestage_neurokit_preprocessing import NeurokitPipelineStagePreprocessing
from HRVPipeline.src.pipeline.pipeline import Pipeline
from HRVPipeline.src.pipeline_imp.pipeline_ampd import AmpdPipelineStage
from HRVPipeline.src.pipeline_imp.pipeline_graph import GraphPipelineStage
from HRVPipeline.src.pipeline_imp.pipeline_multichannel import MultiChannelPipelineStage

from HRVPipeline.src.pipeline_imp.pipeline_snirf_input import *
from HRVPipeline.src.pipeline_imp.pipeline_snirf_preprocessing import SnirfUpsamplingPipelineStage, \
    SnirfFilterPipelineStage


class PipelineFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_neurokit_pipeline(config):
        pipeline = Pipeline(config)
        pipeline.add_stage(NeurokitPipelineStageInput())
        pipeline.add_stage(NeurokitPipelineStagePreprocessing())
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

    @staticmethod
    def create_snirf_input_pipeline(config):
        pipeline_input = SnirfInputPipelineStage(config)
        pipeline_upsampling = SnirfUpsamplingPipelineStage(config)
        pipeline_filtering = SnirfFilterPipelineStage(config)
        #pipeline_imp = SnirfInputPipelineStage(config)

        return [pipeline_input,pipeline_upsampling,pipeline_filtering]

    @staticmethod
    def create_pipeline_from_stages(stages,config={}):
        pipeline = Pipeline(config)
        for stage in stages:
            pipeline.add_stage(stage)
        return pipeline

    @staticmethod
    def create_graph_pipeline(config):

        stages = []
        stages.extend(PipelineFactory.create_snirf_input_pipeline(config))
        stages.extend([GraphPipelineStage(config)])

        return PipelineFactory.create_pipeline_from_stages(stages)


    @staticmethod
    def create_ampd_pipeline(config):
        stages = []
        stages.extend(PipelineFactory.create_snirf_input_pipeline(config))
        stages.extend([AmpdPipelineStage(config)])
        return PipelineFactory.create_pipeline_from_stages(stages)

    @staticmethod
    def create_multichannel_aggregation_pipeline(config):
        stages = []
        stages.extend(PipelineFactory.create_snirf_input_pipeline(config))
        stages.extend([MultiChannelPipelineStage(config)])
        return PipelineFactory.create_pipeline_from_stages(stages)
