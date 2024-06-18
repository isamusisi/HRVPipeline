import unittest

from HRVPipeline.src.pipeline.pipeline import Pipeline, StageIncompatible
from HRVPipeline.src.pipeline.pipeline_stage import PipelineStage, PipelineStageType


class PipelineStageTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.pipeline = Pipeline()
        self.pipeline_stage_input = PipelineStage()
        self.pipeline_stage_preprocessing = PipelineStage()
        self.pipeline_stage_preprocessing.stage_type = PipelineStageType.PRE_PROCESSING

    def tearDown(self) -> None:
        pass


    def test_something(self):
        self.assertFalse(self.pipeline is None)  # add assertion here

    def test_add_stage_ok(self):

        self.pipeline.add_stage(self.pipeline_stage_input)
        self.assertEqual(True, True)  # TODO Throw no exception? return True?

    def test_add_stage_not_started_with_input(self):
        self.assertRaises(StageIncompatible,self.pipeline.add_stage,self.pipeline_stage_preprocessing)
    def test_add_stage_not_incompatible(self):
        self.pipeline.add_stage(self.pipeline_stage_input)

        self.assertRaises(StageIncompatible,self.pipeline.add_stage,self.pipeline_stage_input)


if __name__ == '__main__':
    unittest.main()
