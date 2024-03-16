from src.pipeline.pipeline import Pipeline




class NeurokitPipeline(Pipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "NeurokitPipeline"


