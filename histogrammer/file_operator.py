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
    def __init__(self, filenames: list, args: dict):
        """
        Constructor method.
        """
        self.ui = TextUIOperator()
        self.filenames = filenames
        self.datasets = []
        self.selection = None
        self.prime_dataframe = None
        self.secondary_dataframe = None
        if 'selection_cut' in args and args['selection_cut']:
            self.selection = args['selection_cut']
        self.scheme_name = None
        if 'scheme' in args and args['scheme']:
            self.scheme_name = args['scheme']
        self.scheme = get_scheme(self.scheme_name)
        self.split_by = None
        if 'split_by' in args and args['split_by']:
            self.split_by = args['split_by']
        self.table_name = None
        if 'table_name' in args and args['table_name']:
            self.table_name = args['table_name']
        self.secondary_filenames = None
        if 'versus_dataframe' in args and args['versus_dataframe']:
            self.secondary_filenames = args['versus_dataframe']

    def open_all(self):
        """
        Opens all files, main method to call
        """

        if not self.filenames:
            raise Exception('Filenames have not been provided!')
        self.prime_dataframe = self.open_files(self.filenames)
        self.datasets += [self.prime_dataframe]
        self.scheme.initialize(self.prime_dataframe.columns)
        if self.secondary_filenames:
            self.secondary_dataframe = self.open_files(self.secondary_filenames)
            self.datasets += [self.secondary_dataframe]

        # TODO: Compare the dataframes!

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
                    # Drop duplicated columns if any:
                    root_df = root_df.loc[:, ~root_df.columns.duplicated()]
                    if self.selection:
                        root_df = root_df.query(self.selection)
                    dfs += [root_df]
            else:
                sys.exit(f'File {filename} has an unsupported format!')
        return pd.concat(dfs, ignore_index=True)

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

    def get_dynamic_range(self, column_name: str) -> list:
        """
        Return a dynamic range for a column across all dataframes.
        """
        min1 = np.amin(self.prime_dataframe[column_name])
        max1 = np.amax(self.prime_dataframe[column_name])
        mrange = [min1, max1]
        
        if self.secondary_dataframe is not None:
            min2 = np.amin(self.secondary_dataframe[column_name])
            max2 = np.amax(self.secondary_dataframe[column_name])
            mrange = [min(min1, min2), max(max1, max2)]
        # Output dummy values in case of all NaNs
        if mrange[0] is np.nan and mrange[1] is np.nan:
            return [0,1]
        return mrange

    def get_split_by_name(self, column_name: str = None) -> str:
        """
        Returns split query or column name.
        """
        if self.split_by:
            return self.split_by
        else:
            return self.scheme.get_short_column_name(self.scheme.get_split_column_name(column_name))

    def get_split_by(self, column_name: str = None, for_primary: bool = True):
        """
        Returns a dataframe after a user selection cut
        """
        dataframe = self.prime_dataframe
        if not for_primary:
            dataframe = self.secondary_dataframe
        if not self.split_by:
            split_column_name = self.scheme.get_split_column_name(column_name)
            #print(split_column_name)
            if not split_column_name:
                return None
            # TODO: this is a really simple functionality
            cut = f'{split_column_name} > 0'
            splitted_df = dataframe.query(cut, engine='python')
            if len(splitted_df) < 1:
                return None
            return splitted_df[column_name]
        splitted_df = dataframe.query(str(self.split_by), engine='python')
        if len(splitted_df) < 1:
            return None
        if column_name:
            return splitted_df[column_name]
        return splitted_df

    def get_df(self, column_name: str or list = None, for_primary: bool = True):
        """
        Returns the converted dataframe or a column if name is provided.
        """
        if not for_primary:
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
    
    def has_secondary(self) -> bool:
        """
        Returns True, if there is a secondary dataframe.
        """
        return self.secondary_dataframe is not None

    def show_description(self, variable_names: list):
        """
        Prints out the moments and other properties of a distribution
        """
        descriptions = ['primary dataframe (blue)', 'secondary dataframe (red)']
        for variable_name in variable_names:
            split_by_cut = self.scheme.get_split_column_name(variable_name)
            if split_by_cut:
                split_by_cut += ' > 0'
            if self.split_by:
                split_by_cut = self.split_by

            for dataset, description in zip(self.datasets, descriptions):
                self.ui.separator()
                self.ui.say(f'Variable {variable_name} in {description}')
                total = len(dataset[variable_name])
                mean = dataset[variable_name].mean()
                std = dataset[variable_name].std()
                nans = dataset[variable_name].isna().sum()
                self.ui.say(f'Total entries: {total}')
                self.ui.say(f'Mean total: {mean:.4f} deviation: {std:.4f}')
                if (nans > 0):
                    self.ui.say(f'NaNs: {nans} ({nans/total*100:0.2f}%)')
                if split_by_cut:
                    splitted = dataset.query(split_by_cut)
                    total_split = len(splitted[variable_name])

                    self.ui.say(f'Split entries: {total_split} by {split_by_cut} (darker)')
                    if (total_split > 0):
                        mean = splitted[variable_name].mean()
                        std = splitted[variable_name].std()
                        self.ui.say(f'Mean split: {mean:.4f} deviation: {std:.4f} (darker)')                
                        self.ui.say(f'Ratio split: {total_split/total:.4f}')
                self.ui.separator()