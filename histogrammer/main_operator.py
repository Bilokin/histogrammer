import histogrammer
from histogrammer.file_operator import FileOperator
from histogrammer.textui_operator import TextUIOperator
from histogrammer.schemes import get_scheme

class MainOperator():
    """
    Class that steers the program. 
    """
    def __init__(self, args):
        """
        Constructor method
        """
        self.ui = TextUIOperator()
        self.file_operator = FileOperator(args)
        self.scheme_name = args['scheme']
        self.to_exit = False

    def main_loop(self) -> None:
        """
        Creates an infinite loop until the user or an 
        external condition breaks it.
        """
        print('Hello world main loop!')
        self.file_operator.open_all()
        scheme = get_scheme(self.scheme_name)
        scheme.initialize(self.file_operator.get_df().columns)
        while(True):
            column = self.get_column_name_from_user(scheme)
            print(column)

    def get_column_name_from_user(self, scheme) -> str:
        """
        Asks user which column to use for plotting.
        """
        group_names = scheme.get_group_names()
        selected_group = None
        if len(group_names) > 1:
            answer = self.ui.ask_user_choice('Please select a column group:', group_names, True)
            selected_group = group_names[answer]
        short_columns = scheme.get_short_column_names(selected_group)
        answer = self.ui.ask_user_choice('Please select a column:', short_columns, True)
        return scheme.get_full_column_name(selected_group, short_columns[answer])