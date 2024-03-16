from src.pipeline.pipeline_comperator import PipelineComperator
from src.pipeline.pipeline_factory import PipelineFactory
import matplotlib.pyplot as plt


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


pipeline_a = PipelineFactory.create_neurokit_pipeline()
pipeline_b = PipelineFactory.create_neurokit_pipeline_plus()
result = pipeline_a.run("src/data/input/ppg_isa3.csv")
print("pipeares",result)
pc = PipelineComperator(pipeline_a, pipeline_b,simple_compare_mse)
difs =pc.compare(["src/data/input/ppg_isa1.csv", "src/data/input/ppg_isa3.csv"])
dr = pc.plot_results(difs)
print(dr)
#plt.show()