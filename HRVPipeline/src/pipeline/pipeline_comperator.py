from math import sqrt

import numpy as np

from HRVPipeline.violin_plots_test import violin_plots, ViolinPlotInput


class PipelineComperator:
    def __init__(self, pipelineGroundTruth, pipelines, compare_func):
        pass
        self.pipelineGroundTruth = pipelineGroundTruth
        self.pipelines = pipelines
        self.compare_func = compare_func

    def compare(self, pipeline_inputs):  # TODO pipeline_inputs for each / shared / configs?
        difs = [[] for x in self.pipelines]
        # TODO actually do in the comparator class and sth like MSE etc? weighted loss...
        for run, pipeline_input in enumerate(pipeline_inputs):
            # TODO pipeline.reset()?
            print(f"RUN {run} ...")
            hrv_a, ibis_a, name_a = self.pipelineGroundTruth.run(pipeline_input)
            compare_signals = [ViolinPlotInput(name_a, ibis_a)]
            print(name_a, "Estimated IBIs:", np.mean(ibis_a), np.std(ibis_a))
            for i, pipeline in enumerate(self.pipelines):
                hrv_b, ibis_b, name_b = pipeline.run(pipeline_input)
                print(name_b, "Estimated IBIs:", np.mean(ibis_b), np.std(ibis_b))
                dif = self.compare_func(hrv_a, hrv_b)
                compare_signals.append(ViolinPlotInput(name_b, ibis_b))
                difs[i].append(dif)
                print(f"{run};{i};{dif}")
            # violin_plots(compare_signals)

        return difs

    def plot_results(self, dif):
        print("-" * 70)
        print("COMPARISON")
        keys = dif[0].keys()
        n = len(dif)
        res = {}
        for k in keys:
            res[k] = 0
        for d in dif:
            for k in keys:
                res[k] = res[k] + d[k]

        for k in keys:
            res[k] = res[k] / n
            print(res[k], sqrt(res[k]))

        return res
