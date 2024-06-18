from HRVPipeline.src.neurokit_imp.pipelinestage_neurokit_input import InputType
from HRVPipeline.src.pipeline.pipeline_comperator import PipelineComperator
from HRVPipeline.src.pipeline.pipeline_factory import PipelineFactory
import matplotlib.pyplot as plt
import cedalion
cedalion.units.define('Ohm = ohm')
cedalion.units.define('oC = °C')
cedalion.units.define('ADU = 1')


# Show the plot

# TODO file for those or class ...
def simple_compare_mse(resA,resB):
    keys= ['HRV_MeanNN', 'HRV_SDNN',
    # poincare
    'HRV_SD1', 'HRV_SD2',
    # freq
    'HRV_ULF', 'HRV_VLF', 'HRV_LF', 'HRV_HF', 'HRV_VHF']
    # TODO those should come from someehre?!
    # TODO how to deal with NANs
    res = {}
    for k in keys:
        a = resA[k]
        b = resB[k]
        se = (a-b)**2
        res[k] = se
    return res


pipeline_a = PipelineFactory.create_neurokit_pipeline({"input_type": InputType.SNIRF, "window": 60})
pipeline_b = PipelineFactory.create_neurokit_pipeline_plus()
# result = pipeline_a.run("src/data/input/ppg_isa3.csv")
result = pipeline_a.run("src/data/NIRxData_compact/2024-04-09_007/2024-04-09_007.snirf")
print("pipeares", result)
# pc = PipelineComperator(pipeline_a, pipeline_b, simple_compare_mse)
# difs = pc.compare(["src/data/input/ppg_isa1.csv", "src/data/input/ppg_isa3.csv"])
# dr = pc.plot_results(difs)
# print(dr)
#plt.show()