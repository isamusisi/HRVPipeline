import matplotlib
from matplotlib import pyplot as plt
import neurokit2 as nk
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics.pairwise import cosine_similarity
# matplotlib.use('TKAgg')

from HRVPipeline.src.config.ampd_config import AmpdConfig
from HRVPipeline.src.config.baseline_config import BaselineConfig
from HRVPipeline.src.config.graph_config import GraphConfig
from HRVPipeline.src.config.multichannel_config import MultichannelConfig
from HRVPipeline.src.pipeline.pipeline_comperator import PipelineComperator
from pipeline.pipeline_factory import PipelineFactory
from config.evaluation_config import EvaluationConfig


# Dataset
# configs
# parameters

# GRAPH PIPELINE
# AMPD PIPELINE
# MULTICHANNEL PIPELINE

# plotting

def clean_data(df):
    # Replace inf with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    # Drop rows with NaN values
    df.dropna(axis=1, inplace=True)
    return df


def compare_pipelines(base_hrv, alg_hrv):
    # Convert to DataFrame for ease of comparison
    hrv_df1 = clean_data(pd.DataFrame(base_hrv, index=[0]))
    hrv_df2 = clean_data(pd.DataFrame(alg_hrv, index=[0]))

    # Calculate Euclidean Distance
    euclidean_dist = euclidean(hrv_df1.values.flatten(), hrv_df2.values.flatten())

    # Calculate Cosine Similarity
    cos_sim = cosine_similarity(hrv_df1.values, hrv_df2.values)[0, 0]

    # Calculate Pearson and Spearman correlation
    pearson_corr, _ = pearsonr(hrv_df1.values.flatten(), hrv_df2.values.flatten())
    spearman_corr, _ = spearmanr(hrv_df1.values.flatten(), hrv_df2.values.flatten())
    return euclidean_dist


if __name__ == "__main__":

    evaluation_config = EvaluationConfig()

    graph_config = GraphConfig()
    ampd_config = AmpdConfig()
    multichannel_config = MultichannelConfig()
    baseline_config = BaselineConfig()

    pipeline_ampd = PipelineFactory.create_ampd_pipeline(ampd_config)
    pipeline_graph = PipelineFactory.create_graph_pipeline(graph_config)
    pipeline_multi = PipelineFactory.create_multichannel_aggregation_pipeline(multichannel_config)

    pipeline_base = PipelineFactory.create_base_pipeline(baseline_config)

    # res = pipeline_graph.run(evaluation_config.dataset_path)
    # res = pipeline_ampd.run(evaluation_config.dataset_path) #!!!
    # res = pipeline_multi.run(evaluation_config.dataset_path)

    # res = pipeline_base.run(evaluation_config.dataset_path)
    #pipeline_ampd # too much memory
    comparator = PipelineComperator(pipeline_base, [pipeline_graph,pipeline_multi], compare_pipelines)
    print("Start evaluation")
    difs = comparator.compare([evaluation_config.dataset_path])
    print(difs)
    plt.show()
