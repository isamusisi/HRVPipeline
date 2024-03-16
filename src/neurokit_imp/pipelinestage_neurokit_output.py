from src.pipeline.pipeline_stage import PipelineStage, PipelineStageType
import matplotlib
matplotlib.use('TkAgg')  # Use the 'agg' backend
import neurokit2 as nk
matplotlib.use('TkAgg')  # Use the 'agg' backend


class NeurokitPipelineStageOutput(PipelineStage):
    def __init__(self, config ={}):
        super().__init__(config)
        self.stage_type = PipelineStageType.OUTPUT
        self.accepted_in = [PipelineStageType.HRV_CALC]

        # TODO research ...
        # TODO neurokit names -> your names
        self.normalized_keys= [
            # most common as we know?
            'HRV_MeanNN', 'HRV_SDNN',
            #poincare
            'HRV_SD1', 'HRV_SD2',
            #freq
            'HRV_ULF','HRV_VLF', 'HRV_LF', 'HRV_HF', 'HRV_VHF'
        ]


    def __str__(self):
        return "NeurokitPipeline"

    # TODO needed ? accept_input? overwrite?

    def run(self, pipeline_input):
        out = {}
        for k in self.normalized_keys:

            out[k] = pipeline_input[k].values[0]# TODO your naming for out
        return out

 # ['HRV_MeanNN', 'HRV_SDNN', 'HRV_SDANN1', 'HRV_SDNNI1', 'HRV_SDANN2',
 #         'HRV_SDNNI2', 'HRV_SDANN5', 'HRV_SDNNI5', 'HRV_RMSSD', 'HRV_SDSD',
 #         'HRV_CVNN', 'HRV_CVSD', 'HRV_MedianNN', 'HRV_MadNN', 'HRV_MCVNN',
 #         'HRV_IQRNN', 'HRV_SDRMSSD', 'HRV_Prc20NN', 'HRV_Prc80NN', 'HRV_pNN50',
 #         'HRV_pNN20', 'HRV_MinNN', 'HRV_MaxNN', 'HRV_HTI', 'HRV_TINN', 'HRV_ULF',
 #         'HRV_VLF', 'HRV_LF', 'HRV_HF', 'HRV_VHF', 'HRV_TP', 'HRV_LFHF',
 #         'HRV_LFn', 'HRV_HFn', 'HRV_LnHF', 'HRV_SD1', 'HRV_SD2', 'HRV_SD1SD2',
 #         'HRV_S', 'HRV_CSI', 'HRV_CVI', 'HRV_CSI_Modified', 'HRV_PIP',
 #         'HRV_IALS', 'HRV_PSS', 'HRV_PAS', 'HRV_GI', 'HRV_SI', 'HRV_AI',
 #         'HRV_PI', 'HRV_C1d', 'HRV_C1a', 'HRV_SD1d', 'HRV_SD1a', 'HRV_C2d',
 #         'HRV_C2a', 'HRV_SD2d', 'HRV_SD2a', 'HRV_Cd', 'HRV_Ca', 'HRV_SDNNd',
 #         'HRV_SDNNa', 'HRV_DFA_alpha1', 'HRV_MFDFA_alpha1_Width',
 #         'HRV_MFDFA_alpha1_Peak', 'HRV_MFDFA_alpha1_Mean',
 #         'HRV_MFDFA_alpha1_Max', 'HRV_MFDFA_alpha1_Delta',
 #         'HRV_MFDFA_alpha1_Asymmetry', 'HRV_MFDFA_alpha1_Fluctuation',
 #         'HRV_MFDFA_alpha1_Increment', 'HRV_ApEn', 'HRV_SampEn', 'HRV_ShanEn',
 #         'HRV_FuzzyEn', 'HRV_MSEn', 'HRV_CMSEn', 'HRV_RCMSEn', 'HRV_CD',
 #         'HRV_HFD', 'HRV_KFD', 'HRV_LZC'],
 #        dtype = 'object')