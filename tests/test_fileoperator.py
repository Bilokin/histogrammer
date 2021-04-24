import pandas as pd
import pytest
import unittest
from histogrammer.file_operator import FileOperator

class TestFileOperator(unittest.TestCase):
    """Tests basic functions of FileOperator"""
    @pytest.fixture(autouse=True)
    def initdir(self, tmpdir):
        print(tmpdir)
        tmpdir.chdir()  # change to pytest-provided temporary directory
    def setUp(self):
        print('Setting up the test')
        prime_csv_df = pd.DataFrame({'a': [0,1,2], 
                               'b': [3,4,5],
                               'c': [0.1, 0.3, -0.8]})
        prime_csv_df.to_csv('temp1.csv')
        secondary_csv_df = pd.DataFrame({'a': [10,11,12,13], 
                               'b': [13,14,15,16] })
        secondary_csv_df.to_csv('temp2.csv')
        self.file_io = FileOperator(['temp1.csv'], {})
        self.file_io.open_all()
        self.file_io2 = FileOperator(['temp1.csv', 'temp2.csv'], {})
        self.file_io2.open_all()
        self.file_io3 = FileOperator(['temp1.csv'], {'versus_dataframe': ['temp2.csv']})
        self.file_io3.open_all()

    def test_openall(self):
        """
        Tests open_all method
        """

        self.assertIsNotNone(self.file_io.prime_dataframe)
        self.assertEqual(len(self.file_io.prime_dataframe), 3)

        self.assertIsNotNone(self.file_io2.prime_dataframe)
        self.assertEqual(len(self.file_io2.prime_dataframe), 7)
        self.assertIsNone(self.file_io2.secondary_dataframe)

        self.assertIsNotNone(self.file_io3.prime_dataframe)
        self.assertEqual(len(self.file_io3.prime_dataframe), 3)
        self.assertIsNotNone(self.file_io3.secondary_dataframe)
        self.assertEqual(len(self.file_io3.secondary_dataframe), 4)
        # Scheme test:
        self.assertIsNotNone(self.file_io.scheme)
        

    def test_get_dynamic_range(self):
        """
        Tests get_dynamic_range method
        """
        mrange = self.file_io.get_dynamic_range('a')
        self.assertListEqual(mrange, [0,2])
        mrange = self.file_io.get_dynamic_range('b')
        self.assertListEqual(mrange, [3,5])
        mrange = self.file_io.get_dynamic_range('c')
        self.assertListEqual(mrange, [-0.8, 0.3])
        mrange = self.file_io2.get_dynamic_range('a')
        self.assertListEqual(mrange, [0,13])
        mrange = self.file_io3.get_dynamic_range('a')
        self.assertListEqual(mrange, [0,13])

    def test_get_type(self):
        """
        Tests get_type method
        """
        self.assertEqual(str(self.file_io.get_type('a')), 'int64')
        self.assertEqual(str(self.file_io.get_type('b')), 'int64')
        self.assertEqual(str(self.file_io.get_type('c')), 'float64')