from src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
import matplotlib
matplotlib.use('TkAgg')  # Use the 'agg' backend
import neurokit2 as nk
matplotlib.use('TkAgg')  # Use the 'agg' backend


class NeurokitPipelineStageHRV(PipelineStage):
    def __init__(self, config ={}):
        super().__init__(config)
        self.stage_type = PipelineStageType.HRV_CALC
        self.accepted_in = [PipelineStageType.PRE_PROCESSING]

    def __str__(self):
        return "NeurokitPipeline"

    # TODO needed ? accept_input? overwrite?

    def run(self, pipeline_input):
        # TODO interfaces between stages!!!!!!!!!!!
        df, info = pipeline_input
        signal = info["PPG_Peaks"]
        sr = info["sampling_rate"]
        return nk.hrv(peaks=signal,sampling_rate=sr,show=True) # TODO via config or better from stage before ...

