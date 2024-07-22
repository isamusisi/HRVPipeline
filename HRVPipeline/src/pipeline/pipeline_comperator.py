from math import sqrt


class PipelineComperator:
    def __init__(self,pipelineGroundTruth,pipelines,compare_func):
        pass
        self.pipelineGroundTruth = pipelineGroundTruth
        self.pipelines = pipelines
        self.compare_func = compare_func

    def compare(self, pipeline_inputs): # TODO pipeline_inputs for each / shared / configs?
        difs = [[] for x in self.pipelines]
        # TODO actually do in the comparator class and sth like MSE etc? weighted loss...
        for run, pipeline_input in enumerate(pipeline_inputs):
            # TODO pipeline.reset()?
            print(f"RUN {run} ...")
            result_a = self.pipelineGroundTruth.run(pipeline_input)
            for i, pipeline in enumerate(self.pipelines):
                result_b = pipeline.run(pipeline_input)
                dif = self.compare_func(result_a, result_b)
                difs[i].append(dif)
                print(f"{run};{i};{dif}")

        return difs

    def plot_results(self, dif):
        print("-"*70)
        print("COMPARISON")
        keys = dif[0].keys()
        n = len(dif)
        res = {}
        for k in keys:
            res[k] = 0
        for d in dif:
            for k in keys:
                res[k] = res[k]+d[k]

        for k in keys:
            res[k] = res[k]/n
            print(res[k],sqrt(res[k]))

        return res

