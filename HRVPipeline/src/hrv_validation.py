import matplotlib
# matplotlib.use('TKAgg')

from HRVPipeline.src.config.ampd_config import AmpdConfig
from HRVPipeline.src.config.graph_config import GraphConfig
from HRVPipeline.src.config.multichannel_config import MultichannelConfig
from pipeline.pipeline_factory import PipelineFactory
from config.evaluation_config import EvaluationConfig

# Dataset
# configs
# parameters

# GRAPH PIPELINE
# AMPD PIPELINE
# MULTICHANNEL PIPELINE

# plotting


if __name__ == "__main__":
    print("Start evaluation")
    evaluation_config = EvaluationConfig()

    graph_config = GraphConfig()
    ampd_config = AmpdConfig()
    multichannel_config = MultichannelConfig()

    pipeline_ampd = PipelineFactory.create_ampd_pipeline(ampd_config)
    pipeline_graph = PipelineFactory.create_graph_pipeline(graph_config)
    pipeline_multi = PipelineFactory.create_multichannel_aggregation_pipeline(multichannel_config)

    #pipeline = pipeline_graph
    pipeline = pipeline_multi
    res = pipeline.run(evaluation_config.dataset_path)
