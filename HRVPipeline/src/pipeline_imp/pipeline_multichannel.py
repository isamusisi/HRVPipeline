from HRVPipeline.src.algorithm.ampd_peak_detection import ampd
from HRVPipeline.src.algorithm.graph_peak_detection import calc_features_list, calculate_average_hr, construct_dag
from HRVPipeline.src.data_model.multichannel_signal import MultiChannelRawSignal, MultiChannelProcessedSignal
from HRVPipeline.src.data_model.peak_signal import PeakSignal, IbisSignal
from HRVPipeline.src.hrv_methods import get_snirf_ppg_peaks
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
import numpy as np
from sklearn.cluster import KMeans

class MultiChannelPipelineStage(PipelineStage):
    def __init__(self, config):
        super(MultiChannelPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def run(self, pipeline_input: MultiChannelProcessedSignal) -> MultiChannelProcessedSignal:
        processed = pipeline_input

        filtered_data_list = processed.signals
        sampling_rate = processed.sampling_rate
        times = processed.times  # TODO

        print(filtered_data_list.shape)
        filtered_data_list = filtered_data_list.transpose()
        features_list = []
        peaks_dict = {}
        peaks_indices_all = []
        peaks_indices_dict = {}


        for i, filtered_data in enumerate(filtered_data_list):
            # print('filtered_data', i, filtered_data)
            print(filtered_data.shape)
            peaks = get_snirf_ppg_peaks(filtered_data, sampling_rate)

            peak_indices = np.array(peaks.peaks.values)
            peak_times = times * peak_indices
            # print(f'############## peak_times shape {peak_times.shape}')
            peak_times_raw = [pt for pt in peak_times if pt > 0]
            peak_times = [(pt, i) for pt in peak_times if pt > 0]
            # print('Extracted peaks:', peak_times)
            peaks_dict[i] = peak_times_raw
            peaks_indices_dict[i] = peak_indices
            peaks_indices_all.append(peak_indices)

            features_list.extend(peak_times_raw)

            peak_sums = np.stack(peaks_indices_all).sum(axis=0)
            # ax.plot(times, peak_sums)

            num_bin = np.stack(peaks_indices_all).sum(axis=1).max()

            # num_bin = np.max(num_bin)

            bins = np.histogram(peak_sums, bins=num_bin)
            bin_edges = bins[1]
            bin_counts = bins[0]
            print('Bins:', bin_edges)
            print('Bin counts:', bin_counts)
            print('num_bin:', num_bin)

            features_list = np.asarray(features_list)

            print('features_list:', features_list.min(), features_list.max(), features_list.shape)
            peak_sums_reshaped: np.array = features_list.reshape(-1, 1)
            # peak_sums_reshaped = features_list
            n_clusters = num_bin  # Adjust the number of clusters as needed
            kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(peak_sums_reshaped)
            clusters = kmeans.labels_
            aggregated_peaks = []
            # Plot the clusters
            for cluster in range(n_clusters):
                cluster_indices = np.where(clusters == cluster)[0]
                agg_mean = peak_sums_reshaped[cluster_indices].mean()
                aggregated_peaks.append(agg_mean)
                #ax.axvline(x=agg_mean, color='black', linestyle='--', linewidth=1)
                # ax.scatter(peak_sums_reshaped[cluster_indices], times[cluster_indices], label=f'Cluster {cluster}', s=50)

            aggregated_peaks.sort()
            estimated_ibis = np.diff(aggregated_peaks)

            print("Estimated IBIs:", np.mean(estimated_ibis), np.std(estimated_ibis), estimated_ibis)

            shift = 0.01
        res = IbisSignal(signals=processed, ibis=estimated_ibis)
        return res