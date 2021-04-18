import matplotlib.pyplot as plt

class PlotOperator():
    """
    Class that draws plots
    """
    def __init__(self, file_operator, ui_operator, args: dict):
        """
        Constructor method.
        """
        self.file_operator = file_operator
        self.ui = ui_operator
        self.std_pad_lenx = 6
        self.std_pad_leny = 5
        self.n_bins = 50
        if 'n_bins' in args and args['n_bins']:
            self.n_bins = args['n_bins']

    def plot_histogram(self, variable_name: str, ax, title: str = None) -> None:
        """
        Plots a 1D histogram on axis.
        """
        mrange = self.file_operator.get_dynamic_range(variable_name)
        plot_args = {'range': mrange,
                     'bins':self.n_bins}
        ax.hist(self.file_operator.get_df(variable_name), **plot_args)
        splitted = self.file_operator.get_split_by(variable_name)
        if not splitted is None:
            ax.hist(splitted, **plot_args)
        secondary = self.file_operator.get_df(variable_name, False)
        if not secondary is None:
            ax.hist(secondary,  **plot_args)
        if title is None:
            title = self.file_operator.scheme.get_short_column_name(variable_name)
        ax.set_xlabel(title)

    def plot(self, variable_names: list):
        """
        Plots a canvas of n-plots.
        """
        # TODO: generalize this!
        fig, ax = plt.subplots(figsize=(self.std_pad_lenx, self.std_pad_lenx), dpi=100)
        for variable_name in variable_names:
            col_type =  str(self.file_operator.get_type(variable_name)).lower()
            if col_type.startswith('float'):
                self.plot_histogram(variable_name, ax=ax)
            else:
                self.plot_histogram(variable_name, ax=ax)
        fig.tight_layout()
        plt.show(block=False)
        self.ui.ask_continue_or_exit()