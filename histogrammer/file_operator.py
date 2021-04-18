import sys
import numpy as np
import pandas as pd
import uproot
from histogrammer.textui_operator import TextUIOperator
from histogrammer.schemes import get_scheme


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
        self.scheme_name = None
        if 'scheme' in args and args['scheme']:
            self.scheme_name = args['scheme']
        self.scheme = get_scheme(self.scheme_name)
        self.split_by_cut = None
        if 'split_by' in args and args['split_by']:
            self.split_by_cut = args['split_by']
        self.table_name = None
        if 'table_name' in args and args['table_name']:
            self.table_name = args['table_name']
        self.secondary_filenames = None
        self.secondary_dataframe = None
        if 'versus_dataframe' in args and args['versus_dataframe']:
            self.secondary_filenames = args['versus_dataframe']

    def open_all(self):
        """
        Opens all files, main method to call
        """

        if not self.filenames:
            raise Exception('Filenames have not been provided!')
        self.prime_dataframe = self.open_files(self.filenames)
        self.scheme.initialize(self.get_df().columns)
        if self.secondary_filenames:
            self.secondary_dataframe = self.open_files(self.secondary_filenames)

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
                    selected_name = tree_names[0]
                    if self.table_name and self.table_name in tree_names:
                        selected_name = self.table_name
                    elif len(tree_names) > 1:
                        answer = self.ui.ask_user_choice('Please choose an object to open:', 
                            tree_names, ask_exit=True)
                        selected_name = tree_names[int(answer)]
                        # Remember the choice for other calls of the function:
                        self.table_name = selected_name
                    root_df = rootfile[selected_name].pandas.df()
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

    def get_dynamic_range(self, column_name: str) -> tuple:
        """
        Return a dynamic range for a column across all dataframes.
        """
        min1 = np.amin(self.prime_dataframe[column_name])
        max1 = np.amax(self.prime_dataframe[column_name])
        mrange = [min1, max1]
        """
        if self.secondary_dataframe is not None:
            min2 = np.amin(self.FileOperator.Tree2[column_name])
            max2 = np.amax(self.FileOperator.Tree2[column_name])
            mrange = [min(min1, min2), max(max1, max2)]
        """
        return mrange


    def get_split_by(self, column_name: str = None):
        """
        Returns a dataframe after a user selection cut
        """
        if not self.split_by_cut:
            split_column_name = self.scheme.get_split_column_name(column_name)
            #print(split_column_name)
            if not split_column_name:
                return None
            # TODO: this is a really simple functionality
            cut = f'{split_column_name} > 0'
            splitted_df = self.prime_dataframe.query(cut, engine='python')
            if len(splitted_df) < 1:
                return None
            return splitted_df[column_name]
        splitted_df = self.prime_dataframe.query(str(self.split_by_cut), engine='python')
        if len(splitted_df) < 1:
            return None
        if column_name:
            return splitted_df[column_name]
        return splitted_df

    def get_df(self, column_name: str or list = None, primary: bool = True):
        """
        Returns the converted dataframe or a column if name is provided.
        """
        if not primary:
            if self.secondary_dataframe is None:
                return None
            if column_name:
                return self.secondary_dataframe[column_name]
            return self.secondary_dataframe
        if column_name:
            return self.prime_dataframe[column_name]
        return self.prime_dataframe

    def get_type(self, column_name) -> str:
        """
        Returns the converted dataframe or a column if name is provided.
        """
        if not column_name in self.prime_dataframe.columns:
            return None
        return self.prime_dataframe[column_name].dtype