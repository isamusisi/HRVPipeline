import numpy as np

from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
import matplotlib

import neurokit2 as nk

matplotlib.use('TkAgg')  # Use the 'agg' backend

matplotlib.use('TkAgg')  # Use the 'agg' backend


class NeurokitPipelineStageHRV(PipelineStage):
    def __init__(self, config={}):
        super().__init__(config)
        self.stage_type = PipelineStageType.HRV_CALC
        self.accepted_in = [PipelineStageType.PRE_PROCESSING]

    def __str__(self):
        return "NeurokitPipeline"

    # TODO needed ? accept_input? overwrite?

    def run(self, pipeline_input):
        # TODO interfaces between stages!!!!!!!!!!!
        peaks, sr, peaks_all, peaks_all_raw = pipeline_input
        peaks = [a for a in peaks if np.isfinite(a).all()]
        print(f'---------NeurokitPipelineStageHRV-------- input {len(peaks)} {len(peaks[0])} {peaks[0].sum()} {peaks[0]}')
        vals = peaks_all
        print(f'---------NeurokitPipelineStageHRV-------- input all {vals.sum()} {len(vals)} {vals}')
        result = [nk.hrv(peaks=x.values, sampling_rate=sr, show=False) for x in
                  peaks]  # TODO via config or better from stage before ...

        result2 = nk.hrv(peaks=vals, sampling_rate=sr, show=True)
        result3 = nk.hrv(peaks=peaks_all_raw, sampling_rate=int(sr/5), show=True)
        result.append(result2)
        result.append(result3)
        print(f'hrv list {len(result)} {result}')
        matplotlib.pyplot.show()

        return result
