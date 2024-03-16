from src.pipeline.pipeline_stage import PipelineStage, PipelineStageType

import neurokit2 as nk


class NeurokitPipelineStagePreprocessing(PipelineStage):
    def __init__(self, config={}):
        super().__init__(config)
        self.stage_type = PipelineStageType.PRE_PROCESSING
        self.accepted_in = [PipelineStageType.INPUT]

    def __str__(self):
        return "NeurokitPipeline"

    # TODO needed ? accept_input? overwrite?

    def run(self, pipeline_input):
        # TODO interfaces between stages!!!!!!!!!!!

        sr = self.config["sampling_rate"]

        # filter raw signal
        filtered_input = pipeline_input.apply(lambda x: nk.signal_filter(x, sampling_rate=sr, lowcut=0.5, highcut=3,
                                                                         order=2))

        return nk.ppg_process(filtered_input["green"],
                              sampling_rate=sr)  # TODO via config or better from stage before ...
