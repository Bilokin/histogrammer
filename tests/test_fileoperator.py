import pandas as pd
import pytest
import unittest
from histogrammer.file_operator import FileOperator

class TestFileOperator(unittest.TestCase):
    """Tests basic functions of Repositories"""
    @pytest.fixture(autouse=True)
    def initdir(self, tmpdir):
        print(tmpdir)
        tmpdir.chdir()  # change to pytest-provided temporary directory
    def setUp(self):
        print('Setting up the test')
        prime_csv_df = pd.DataFrame({'a': [0,1,2], 
                               'b': [3,4,5] })
        prime_csv_df.to_csv('temp1.csv')
        secondary_csv_df = pd.DataFrame({'a': [10,11,12,13], 
                               'b': [13,14,15,16] })
        secondary_csv_df.to_csv('temp2.csv')

    def test_openall(self):
        """
        Test open_all method
        """
        file_io = FileOperator(['temp1.csv'], {})
        print(file_io.prime_dataframe)
        self.assertIsNone(file_io.prime_dataframe)
        file_io.open_all()
        self.assertIsNotNone(file_io.prime_dataframe)
        self.assertEqual(len(file_io.prime_dataframe), 3)
        file_io2 = FileOperator(['temp1.csv', 'temp2.csv'], {})
        file_io2.open_all()
        self.assertIsNotNone(file_io2.prime_dataframe)
        self.assertEqual(len(file_io2.prime_dataframe), 7)
        self.assertIsNone(file_io2.secondary_dataframe)
        file_io2 = FileOperator(['temp1.csv'], {'versus_dataframe': ['temp2.csv']})
        file_io2.open_all()
        self.assertIsNotNone(file_io2.prime_dataframe)
        self.assertEqual(len(file_io2.prime_dataframe), 3)
        self.assertIsNotNone(file_io2.secondary_dataframe)
        self.assertEqual(len(file_io2.secondary_dataframe), 4)
