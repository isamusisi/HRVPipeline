import numpy as np

import cedalion
import cedalion.nirs
import cedalion.sigproc.quality as quality
import cedalion.xrutils as xrutils
import cedalion.datasets as datasets
import xarray as xr
import matplotlib.pyplot as p
from functools import reduce
import numpy as np

from cedalion import Quantity, units

from HRVPipeline.src.algorithm.preprocessing import resample_xarray, preprocess_snirf_data
from HRVPipeline.src.data_model.multichannel_signal import MultiChannelProcessedSignal, MultiChannelRawSignal
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
from HRVPipeline.src.util.plot import plot_signal


class SnirfUpsamplingPipelineStage(PipelineStage):
    def __init__(self, config):
        super(SnirfUpsamplingPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def run(self, pipeline_input: MultiChannelProcessedSignal) -> MultiChannelProcessedSignal:
        raw = pipeline_input
        target_sr = self.config.target_sampling_rate

        amp2d_resampled = resample_xarray(raw.signals, target_sr)

        res = MultiChannelProcessedSignal(signals=amp2d_resampled,
                                          sampling_rate=target_sr,
                                          channels=raw.channels)
        return res


class SnirfFilterPipelineStage(PipelineStage):
    def __init__(self, config):
        super(SnirfFilterPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def run(self, pipeline_input: MultiChannelProcessedSignal) -> MultiChannelProcessedSignal:
        processed = pipeline_input

        amp2d_filtered = preprocess_snirf_data(processed.signals, processed.sampling_rate)

        times = processed.signals.time.values * 1000  # TODO not so nice
        if self.config.plot:
            plot_signal(np.transpose(amp2d_filtered.values))

        # print('filtered xarray', amp2d_filtered)

        res = MultiChannelProcessedSignal(signals=amp2d_filtered.values,
                                          sampling_rate=processed.sampling_rate,
                                          channels=processed.channels,
                                          times=times)
        return res


class SnirfPruningPipelineStage(PipelineStage):
    def __init__(self, config):
        super(SnirfPruningPipelineStage, self).__init__(config)
        self.accepted_in = [PipelineStageType.INPUT, PipelineStageType.PRE_PROCESSING]
        self.stage_type = PipelineStageType.PRE_PROCESSING

    def run(self, pipeline_input: MultiChannelRawSignal) -> MultiChannelProcessedSignal:
        raw = pipeline_input
        signals = raw.signals
        target_sr = self.config.target_sampling_rate

        # snr_thresh = self.config.snr_thresh  # 16  # the SNR (std/mean) of a channel.
        # sd_threshs = [1,
        #               4.5] * units.cm  # defines the lower and upper bounds for the source-detector separation that we would like to keep
        # amp_threshs = self.config.amp_threshs * units.volt # [0.1, 3] * units.volt  # define whether a channel's amplitude is within a certain range
        #
        # # then we calculate the masks for each metric: SNR, SD distance and mean amplitude
        # _, snr_mask = quality.snr(signals, snr_thresh)
        # # _, sd_mask = quality.sd_dist(signals, data.geo3d, sd_threshs)
        # _, amp_mask = quality.mean_amp(signals, amp_threshs)
        #
        # # put all masks in a list
        # masks = [snr_mask, amp_mask]
        #
        # # prune channels using the masks and the operator "all", which will keep only channels that pass all three metrics
        # amp_pruned, drop_list = quality.prune_ch(signals, masks, "all")

        # print list of dropped channels
        # print(f"List of pruned channels: {drop_list}")
        # display the new data xarray

        res = MultiChannelProcessedSignal(signals=raw.signals,
                                          sampling_rate=target_sr,
                                          channels=raw.channels)
        return res
