import sys
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
        self.all_choices = ['New plot', 'Weight with', 'Scatter plot against']
        self.choice = 0

    def main_loop(self) -> None:
        """
        Creates an infinite loop until the user or an 
        external condition breaks it.
        """
        self.file_operator.open_all()
        column = ''
        while(True):
            if self.choice == 0:
                self.ui.say('\nPlotting a new histogram')
                column = self.get_column_name_from_user()
                self.plt.plot([column])
                self.choice = self.ui.ask_user_choice('Please select an action:', self.all_choices, True)
            elif self.choice == 1:
                self.ui.say('Plotting the same histogram with weight')
                weight_column = self.get_column_name_from_user(name='weight')
                self.plt.plot([column], weight_column=weight_column)
                self.choice = 0
            elif self.choice == 2:
                self.ui.say('Plotting the scatter plot')
                second_column = self.get_column_name_from_user()
                self.plt.plot([(column, second_column)])
                self.choice = 0

            elif self.choice > len(self.all_choices) or self.choice < 0:
                sys.exit('Something unexpected happened!')


    def get_column_name_from_user(self, name: str = 'plot') -> str:
        """
        Asks user which column to use for plotting.
        """
        group_names = self.file_operator.scheme.get_group_names()
        selected_group = None
        if len(group_names) > 1:
            answer = self.ui.ask_user_choice('Please select a column group:', group_names, True)
            selected_group = group_names[answer]
        short_columns = self.file_operator.scheme.get_short_column_names(selected_group)
        answer = self.ui.ask_user_choice(f'Please select a {name} column:', short_columns, True)
        return self.file_operator.scheme.get_full_column_name(selected_group, short_columns[answer])