from HRVPipeline.src.data_model.multichannel_signal import MultiChannelProcessedSignal
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStageOutput


class PeakSignal(PipelineStageOutput):
    def __init__(self, signals, peaks):
        self.multi_channel_signals: MultiChannelProcessedSignal= signals
        self.peaks = peaks

class IbisSignal(PipelineStageOutput):
    def __init__(self, signals, ibis):
        self.multi_channel_signals: MultiChannelProcessedSignal= signals
        self.ibis = ibis


