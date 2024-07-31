from HRVPipeline.src.data_model.multichannel_signal import MultiChannelProcessedSignal
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStageOutput


class PeakSignal(PipelineStageOutput):
    def __init__(self, signals, peaks, ibis=None, name=''):
        if ibis is None:
            ibis = []
        self.multi_channel_signals: MultiChannelProcessedSignal = signals
        self.peaks = peaks
        self.ibis = ibis
        self.name = name


class IbisSignal(PipelineStageOutput):
    def __init__(self, signals, ibis):
        self.multi_channel_signals: MultiChannelProcessedSignal = signals
        self.ibis = ibis
