import histogrammer
from histogrammer.file_operator import FileOperator
from histogrammer.textui_operator import TextUIOperator
from histogrammer.plot_operator import PlotOperator

class MainOperator():
    """
    Class that steers the program. 
    """
    def __init__(self, args):
        """
        Constructor method
        """
        self.ui = TextUIOperator()
        self.file_operator = FileOperator(args['filenames'], args)
        self.plt = PlotOperator(self.file_operator, self.ui, args)
        self.to_exit = False

    def main_loop(self) -> None:
        """
        Creates an infinite loop until the user or an 
        external condition breaks it.
        """
        self.file_operator.open_all()
        while(True):
            column = self.get_column_name_from_user()
            self.plt.plot([column])
            self.ui.ask_continue_or_exit()


    def get_column_name_from_user(self) -> str:
        """
        Asks user which column to use for plotting.
        """
        group_names = self.file_operator.scheme.get_group_names()
        selected_group = None
        if len(group_names) > 1:
            answer = self.ui.ask_user_choice('Please select a column group:', group_names, True)
            selected_group = group_names[answer]
        short_columns = self.file_operator.scheme.get_short_column_names(selected_group)
        answer = self.ui.ask_user_choice('Please select a column:', short_columns, True)
        return self.file_operator.scheme.get_full_column_name(selected_group, short_columns[answer])