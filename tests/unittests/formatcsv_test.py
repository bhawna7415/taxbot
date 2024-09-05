import pytest
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from csvformatter.formatcsv import Formatter
import json
import unittest
from unittest.mock import MagicMock



class TestFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = Formatter()

    def test_basic_functionality(self):
        result = self.formatter.format_csv()
        self.assertEqual(result, "Done")



if __name__ == '__main__':
    unittest.main()