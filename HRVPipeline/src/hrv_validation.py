# import matplotlib
# from matplotlib import pyplot as plt
# import neurokit2 as nk
# import numpy as np
# import pandas as pd
# from scipy.spatial.distance import euclidean
# from scipy.stats import pearsonr, spearmanr
# from sklearn.metrics.pairwise import cosine_similarity
# # matplotlib.use('TKAgg')
#
# import pandas as pd
#
# from HRVPipeline.src.config.ampd_config import AmpdConfig
# from HRVPipeline.src.config.baseline_config import BaselineConfig
# from HRVPipeline.src.config.graph_config import GraphConfig
# from HRVPipeline.src.config.multichannel_config import MultichannelConfig
# from HRVPipeline.src.pipeline.pipeline_comperator import PipelineComperator
# from pipeline.pipeline_factory import PipelineFactory
# from config.evaluation_config import EvaluationConfig
#
#
# # Dataset
# # configs
# # parameters
#
# # GRAPH PIPELINE
# # AMPD PIPELINE
# # MULTICHANNEL PIPELINE
#
# # plotting
#
# def clean_data(df):
#     # Replace inf with NaN
#     df.replace([np.inf, -np.inf], np.nan, inplace=True)
#     # Drop rows with NaN values
#     df.dropna(axis=1, inplace=True)
#     return df
#
#
# def compare_pipelines(base_hrv, alg_hrv):
#     # Convert to DataFrame for ease of comparison
#     hrv_df1 = clean_data(pd.DataFrame(base_hrv, index=[0]))
#     hrv_df2 = clean_data(pd.DataFrame(alg_hrv, index=[0]))
#
#     # Calculate Euclidean Distance
#     euclidean_dist = euclidean(hrv_df1.values.flatten(), hrv_df2.values.flatten())
#
#     # Calculate Cosine Similarity
#     cos_sim = cosine_similarity(hrv_df1.values, hrv_df2.values)[0, 0]
#
#     # Calculate Pearson and Spearman correlation
#     pearson_corr, _ = pearsonr(hrv_df1.values.flatten(), hrv_df2.values.flatten())
#     spearman_corr, _ = spearmanr(hrv_df1.values.flatten(), hrv_df2.values.flatten())
#     return euclidean_dist,alg_hrv
#
# def append_row(df, row):
#     return pd.concat([
#                 df,
#                 pd.DataFrame([row], columns=row.index)]
#            ).reset_index(drop=True)
#
#
#
#
#
# if __name__ == "__main__":
#
#     evaluation_config = EvaluationConfig()
#
#
#
#     baseline_config = BaselineConfig()
#     pipeline_base = PipelineFactory.create_base_pipeline(baseline_config)
#     results = pd.DataFrame(columns=['SR', 'SNR', 'NO_CHANNELS',"DIF","HRV"])
#
#
#     for eval_config in evaluation_config:
#         print(eval_config)
#
#         graph_config = GraphConfig() #  for each graph config ... as is tradition (eval config)
#         ampd_config = AmpdConfig()
#         multichannel_config = MultichannelConfig()
#
#         pipeline_ampd = PipelineFactory.create_ampd_pipeline(ampd_config)
#         pipeline_graph = PipelineFactory.create_graph_pipeline(graph_config)
#         pipeline_multi = PipelineFactory.create_multichannel_aggregation_pipeline(multichannel_config)
#         # pipeline_ampd !!!
#         comparator = PipelineComperator(pipeline_base, [pipeline_graph, pipeline_multi], compare_pipelines)
#         difs = comparator.compare([evaluation_config.dataset_path])
#         dif_graph, dif_multi = difs #be carefull man
#         print('-----------------diffs:', difs)
#         print(eval_config.i,evaluation_config)
#         new_row = pd.Series({'SR': evaluation_config.current_sampling_rate,
#                              'SNR': eval_config.current_snr,
#                              'NO_CHANNELS': evaluation_config.current_no_channels,
#                              "PIPELINE": "GRAPH",
#                              "DIF": dif_graph[0][0],
#                              "HRV": dif_graph[0][1]["HRV_MeanNN"].values
#                              })
#         results = append_row(results, new_row)
#         new_row = pd.Series({'SR': evaluation_config.current_sampling_rate,
#                              'SNR': eval_config.current_snr,
#                              'NO_CHANNELS': evaluation_config.current_no_channels,
#                              "PIPELINE": "MULTICHANNEL",
#                              "DIF": dif_multi[0][0],
#                              "HRV": dif_multi[0][1]["HRV_MeanNN"].values
#                              })
#         results = append_row(results, new_row)
#     print("Start evaluation")
#
#
#     plt.show()
#     print(results.head())
#     print(results.shape)

import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt
import neurokit2 as nk
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics.pairwise import cosine_similarity

from HRVPipeline.src.config.baseline_config import BaselineConfig

from HRVPipeline.src.config.common_config import CommonConfig
from HRVPipeline.src.pipeline.pipeline_comperator import PipelineComperator
from pipeline.pipeline_factory import PipelineFactory
from config.evaluation_config import EvaluationConfig


def clean_data(df):
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.replace([np.nan], 0, inplace=True)
    # df.dropna(axis=1, inplace=True)
    return df


def compare_pipelines(base_hrv, alg_hrv):
    hrv_df1 = clean_data(pd.DataFrame(base_hrv, index=[0]))
    hrv_df2 = clean_data(pd.DataFrame(alg_hrv, index=[0]))

    euclidean_dist = euclidean(hrv_df1.values.flatten(), hrv_df2.values.flatten())
    cos_sim = cosine_similarity(hrv_df1.values, hrv_df2.values)[0, 0]
    pearson_corr, _ = pearsonr(hrv_df1.values.flatten(), hrv_df2.values.flatten())
    spearman_corr, _ = spearmanr(hrv_df1.values.flatten(), hrv_df2.values.flatten())

    return euclidean_dist, alg_hrv


def append_row(df, row):
    return pd.concat([df, pd.DataFrame([row], columns=row.index)]).reset_index(drop=True)


if __name__ == "__main__":
    evaluation_config = EvaluationConfig()
    baseline_config = BaselineConfig(500)
    pipeline_base = PipelineFactory.create_base_pipeline(baseline_config)
    results = pd.DataFrame(columns=['SR', 'SNR', 'NO_CHANNELS', "PIPELINE", "DIF"])

    res = pipeline_base.run(evaluation_config.dataset_path)
    new_row = {
        'SR': 500,
        'SNR': 0,
        'NO_CHANNELS': 1,
        "PIPELINE": "BASE_LINE",
        "DIF": 0
    }
    # Add HRV parameters to the new row
    for key, value in res[0].items():
        new_row[key] = value.values[0] if isinstance(value, pd.Series) else value

    results = append_row(results, pd.Series(new_row))
    # print(results)
    # print(results.shape)
    # exit(0)

    for eval_config in evaluation_config:
        print(eval_config)

        common_config = CommonConfig(eval_config)

        pipeline_ampd = PipelineFactory.create_ampd_pipeline(common_config)
        pipeline_graph = PipelineFactory.create_graph_pipeline(common_config)
        pipeline_multi = PipelineFactory.create_multichannel_aggregation_pipeline(common_config)

        comparator = PipelineComperator(pipeline_base, [pipeline_graph, pipeline_multi], compare_pipelines)
        difs = comparator.compare([evaluation_config.dataset_path])
        dif_graph, dif_multi = difs

        for dif, pipeline_name in zip([dif_graph, dif_multi], ["GRAPH", "MULTICHANNEL"]):
            new_row = {
                'SR': evaluation_config.current_sampling_rate,
                'SNR': eval_config.current_snr,
                'NO_CHANNELS': evaluation_config.current_no_channels,
                "PIPELINE": pipeline_name,
                "DIF": dif[0][0]
            }
            # Add HRV parameters to the new row

            for key, value in dif[0][1].items():
                if key == "HRV_SD1":
                    print(value)
                new_row[key] = value.values[0] if isinstance(value, pd.Series) else value

            results = append_row(results, pd.Series(new_row))

    print("Start evaluation")

    plt.show()

    print(results.head())
    print(results.shape)
    print(results.columns)

    plt.figure(figsize=(10, 6))

    X_AXIS = "SR" #"HRV_SD1"
    Y_AXIS = "HRV_SDNN" # "HRV_SD2"
    custom_palette = sns.color_palette(["#FF5733", "#33FF57", "#3357FF"])
    sns.set_palette(custom_palette)
    #results =  results[results['PIPELINE'] =='GRAPH' ]
    sns.scatterplot(data=results, x=X_AXIS, y=Y_AXIS, hue='PIPELINE')#, palette='viridis'

    # Add labels and title
    plt.xlabel(X_AXIS)
    plt.ylabel(Y_AXIS)
    plt.show()

