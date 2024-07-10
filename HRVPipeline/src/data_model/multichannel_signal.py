from HRVPipeline.src.pipeline.pipeline_stage import PipelineStageOutput
import xarray as xr


class MultiChannelRawSignal(PipelineStageOutput):
    def __init__(self, signals, sampling_rate=0, channels=0):
        self.signals: xr.DataArray = signals
        self.sampling_rate: float = sampling_rate
        self.channels: int = channels


class MultiChannelProcessedSignal(MultiChannelRawSignal):
    def __init__(self, signals, sampling_rate=0, channels=0):
        super().__init__(signals, sampling_rate, channels)


