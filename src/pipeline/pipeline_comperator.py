from math import sqrt


class PipelineComperator:
    def __init__(self,pipelineA,pipelineB,compare_func):
        pass
        self.pipelineA = pipelineA
        self.pipelineB = pipelineB
        self.compare_func = compare_func

    def compare(self,pipeline_inputs): # TODO pipeline_inputs for each / shared / configs?
        difs = [] # TODO actually do in the comperator class and sth like MSE etc? weighted loss...
        for pipeline_input in pipeline_inputs:
            # TODO pipeline.reset()?
            result_a = self.pipelineA.run(pipeline_input)
            result_b = self.pipelineB.run(pipeline_input)
            dif = self.compare_func(result_a, result_b)
            difs.append(dif)

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

