import sys
import pandas as pd
import uproot
from histogrammer.textui_operator import TextUIOperator


class FileOperator():
    """
    Class that opens the file and converts it to a dataframe.
    """
    def __init__(self, args: dict):
        """
        Constructor method.
        """
        self.ui = TextUIOperator()
        self.filenames = args['filenames']
        self.selection = None
        if 'selection_cut' in args and args['selection_cut']:
            self.selection = args['selection_cut']
        self.prime_dataframe = None
    
    def open_all(self):
        """
        Opens all files, main method to call
        """
        if not self.filenames:
            raise Exception('Filenames have not been provided!')
        self.prime_dataframe = self.open_files(self.filenames)

    def open_files(self, filenames: list) -> pd.DataFrame:
        """
        Safely opens the files.
        """
        dfs = []
        for filename in filenames:
            self.ui.say(f'Opening a file {filename}')
            if filename.lower().endswith('csv'):
                csv_df = pd.read_csv(filename)
                if self.selection:
                    csv_df = csv_df.query(self.selection)
                dfs += [csv_df]
            elif filename.lower().endswith('root'):
                with uproot.open(filename) as rootfile:
                    tree_names = self.get_names(rootfile.classnames())
                    answer = self.ui.ask_user_choice('Please choose an object to open:', 
                        tree_names, ask_exit=True)
                    root_df = rootfile[tree_names[int(answer)]].pandas.df()
                    if self.selection:
                        root_df = root_df.query(self.selection)
                    dfs += [root_df]
            else:
                sys.exit(f'File {filename} has an unsupported format!')
        return pd.concat(dfs, ignore_index=True).convert_dtypes()

    def get_names(self, raw_names: list) -> list:
        """
        Outputs pretty names.
        """
        names = []
        for raw in raw_names:
            raw_name = raw[0].decode('utf-8')
            if ';' in raw_name:
                raw_name = raw_name.split(';')[0]
            names += [raw_name]
        return names

    def get_df(self) -> pd.DataFrame:
        """
        Returns the converted dataframe.
        """
        return self.prime_dataframe