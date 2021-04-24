import pytest
import unittest
from histogrammer.schemes import BelleScheme

class TestSchemes(unittest.TestCase):
    """Tests basic functions of Scheme classes"""
    @pytest.fixture(autouse=True)
    def initdir(self, tmpdir):
        print(tmpdir)
        tmpdir.chdir()  # change to pytest-provided temporary directory

    def test_basic_belle(self):
        """
        Test a simple case without groups
        """
        columns = ['__index__',
                   '__weight__',
                   'p']
        scheme = BelleScheme()
        scheme.initialize(columns)
        self.assertEqual(len(scheme.groups), 1)
        self.assertDictEqual(scheme.groups, {'Parent':columns})

    def test_group_belle(self):
        """
        Test a simple case without groups
        """
        columns = ['__index__',
                   '__weight__',
                   'p',
                   'B0_p', 'B0_cosTheta',
                   'B0_D0_p', 'B0_D0_cosTheta',
                   'B0_pi0_p', 'B0_pi0_cosTheta',]
        scheme = BelleScheme()
        scheme.initialize(columns)
        self.assertEqual(len(scheme.groups), 4)
        self.assertListEqual(list(scheme.groups.keys()), ['Parent', 'B0', 'B0_D0', 'B0_pi0'])
        self.assertEqual(scheme.length, len(columns))
        # Test short/long names:

        self.assertEqual( scheme.get_full_column_name(None, '__index__'), '__index__' )
        self.assertEqual( scheme.get_full_column_name('Parent', '__index__'), '__index__' )
        self.assertEqual( scheme.get_full_column_name('B0', 'p'), 'B0_p' )
        self.assertEqual( scheme.get_full_column_name('B0_D0', 'cosTheta'), 'B0_D0_cosTheta' )
        with self.assertRaises(Exception):
            self.assertEqual( scheme.get_full_column_name('B0_D*0', 'cosTheta'), 'B0_D*0_cosTheta' )
        self.assertEqual(scheme.get_short_column_name('__index__'), '__index__')
        # This is not really desired, but acceptable so far:
        self.assertEqual(scheme.get_short_column_name('B0_D0_cosTheta'), 'D0_cosTheta')