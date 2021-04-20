import matplotlib.pyplot as plt
from cycler import cycler

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
        self.std_pad_len = (7, 5)
        self.n_bins = 50
        if 'n_bins' in args and args['n_bins']:
            self.n_bins = args['n_bins']
        self.init_plot_config(args)

    def init_plot_config(self, args):
        """
        Initializes the style of matplotlib plots.
        """
        # TODO: customize this!
        self.std_plot_args = {'histtype':'stepfilled',
                              'fill': False,
                              'alpha':0.9,
                              'linewidth':3.5}
        new_colors = [plt.get_cmap('Paired')(i) for i in [0, 1, 4, 5, 2, 3, 6, 7]]
        mpl_cfg = {
            'xtick.top': True,
            'ytick.right': True,
            'hatch.linewidth':3.,
            'axes.prop_cycle': (
                cycler( 'edgecolor', new_colors) +
                cycler( 'color', new_colors) +
                cycler( 'facecolor', new_colors)),
            'font.size': 14}
        plt.rcParams.update(mpl_cfg)

    def plot_histogram(self, variable_name: str, ax, title: str = None) -> None:
        """
        Plots a 1D histogram on axis.
        """
        mrange = self.file_operator.get_dynamic_range(variable_name)
        plot_args = {'range': mrange,
                     'bins':self.n_bins}
        plot_args.update(self.std_plot_args)
        label = 'All entries'
        ax.hist(self.file_operator.get_df(variable_name), hatch='//', label=label, **plot_args)
        splitted = self.file_operator.get_split_by(variable_name)
        if not splitted is None:
            sec_label = self.file_operator.get_split_by_name(variable_name)
            ax.hist(splitted, hatch='//', label=sec_label, **plot_args)
        else:
            next(ax._get_lines.prop_cycler) 
            next(ax._get_lines.prop_cycler) 
        next(ax._get_lines.prop_cycler) 
        secondary = self.file_operator.get_df(variable_name, False)
        if not secondary is None:
            ax.hist(secondary, hatch='\\\\', label=label+' (alt.)', **plot_args)
        if title is None:
            title = self.file_operator.scheme.get_short_column_name(variable_name)
        ax.set_xlabel(title)

    def plot(self, variable_names: list):
        """
        Plots a canvas of n-plots.
        """
        # TODO: generalize this!
        fig, ax = plt.subplots(figsize=self.std_pad_len, dpi=100)
        for variable_name in variable_names:
            col_type =  str(self.file_operator.get_type(variable_name)).lower()
            if col_type.startswith('float'):
                self.plot_histogram(variable_name, ax=ax)
            else:
                self.plot_histogram(variable_name, ax=ax)
        fig.tight_layout()
        plt.legend(fancybox=True, framealpha=0.5)
        plt.show(block=False)
        self.ui.ask_continue_or_exit()