import networkx as nx
import numpy as np

from HRVPipeline.src.algorithm.graph_peak_detection import calc_features_list, calculate_average_hr, construct_dag
from HRVPipeline.src.data_model.multichannel_signal import MultiChannelRawSignal, MultiChannelProcessedSignal
from HRVPipeline.src.data_model.peak_signal import PeakSignal, IbisSignal
from HRVPipeline.src.hrv_methods import get_snirf_ppg_peaks
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType


class GraphPipelineStage(PipelineStage):
    def __init__(self, config):
        super(GraphPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def run(self, pipeline_input: MultiChannelProcessedSignal) -> MultiChannelProcessedSignal:
        processed = pipeline_input

        filtered_data_list = processed.signals
        sampling_rate = processed.sampling_rate
        times = processed.times  # TODO

        features_list, peaks_dict = calc_features_list(filtered_data_list, sampling_rate, times)

        avg_hrs = calculate_average_hr(features_list, peaks_dict)

        dag_features_list = construct_dag(features_list, avg_hrs)

        # plot_graph(dag_features_list)

        nodes = list(dag_features_list.nodes)
        shortest_path_features = nx.shortest_path(dag_features_list, source=nodes[0], target=nodes[-1])
        estimated_ibis = []

        shortest_path_times = list(shortest_path_features)
        shortest_path_times.reverse()
        ibis = np.diff(shortest_path_times)


        shortest_path_times.sort()

        for i, time in enumerate(shortest_path_times):
            if i > 0:
                estimated_ibis.append(time - shortest_path_times[i - 1])

        print("Estimated IBIs 1:", np.mean(estimated_ibis), np.std(estimated_ibis), estimated_ibis)
        print("Estimated IBIs 2:", np.mean(ibis), np.std(ibis), ibis)

        peaks_graph = None
        res = IbisSignal(signals=processed, ibis=estimated_ibis)
        return res
