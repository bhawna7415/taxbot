import unittest
import os
from unittest.mock import MagicMock
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from finetuning.classification import FineTuning  # Assuming the class is defined in finetuning.py
class TestFineTuning(unittest.TestCase):
    def setUp(self):
        # Get the path to the test data JSONL file relative to the current working directory
        test_file_dir = os.path.dirname(os.path.abspath(__file__))
        self.jsonl_file = os.path.join(test_file_dir, "trainingsample.jsonl")
        self.obj = FineTuning(self.jsonl_file)

    def test_uploadfile(self):
        # Upload the file
        self.obj.uploadfile()

        # Assertions
        self.assertIsNotNone(self.obj.file_id)

    def test_createjobs(self):
        # Upload the file first
        self.obj.uploadfile()

        # Create jobs
        self.obj.createjobs()

        # Assertions
        self.assertIsNotNone(self.obj.jobs_id)

    def test_retreivejobs(self):
        # Upload the file and create jobs first
        self.obj.uploadfile()
        self.obj.createjobs()

        # Retrieve jobs
        result = self.obj.retreivejobs()

        # Assertions
        self.assertIsNotNone(result)
       

if __name__ == '__main__':
    unittest.main()