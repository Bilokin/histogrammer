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
        self.truncate_str_length = 30
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

    def plot_scatter(self, variable_names: list or tuple, ax, title: str = None, 
                     for_primary: bool = True) -> None:
        """
        Plots a 2D scatter plot on axis.
        """
        primary = self.file_operator.get_df(variable_names[0], for_primary=for_primary)
        secondary = self.file_operator.get_df(variable_names[1], for_primary=for_primary)
        ax.scatter(primary, secondary, alpha=self.std_plot_args['alpha'])
        splitted_primary = self.file_operator.get_split_by(variable_names[0], for_primary=for_primary)
        if splitted_primary is not None:
            splitted_secondary = self.file_operator.get_split_by(variable_names[1], for_primary=for_primary)
            if len(splitted_primary) == len(splitted_secondary):
                ax.scatter(splitted_primary, splitted_secondary, alpha=self.std_plot_args['alpha'])
            else:
                self.ui.say('Skipping splitted scatter plots, '
                           f'dimension mismatch ({len(splitted_primary)} vs {len(splitted_secondary)})')
                ax.scatter([], [])
        else:
            ax.scatter([], [])
        ax.set_xlabel(variable_names[0])
        ax.set_ylabel(variable_names[1])
            
    def plot_histogram(self, variable_name: str, ax, title: str = None, 
                    weight_column: str = None, for_primary: bool = True) -> None:
        """
        Plots a 1D histogram on axis.
        """
        mrange = self.file_operator.get_dynamic_range(variable_name)
        primary = self.file_operator.get_df(variable_name, for_primary=for_primary)
        primary_weights = None
        if weight_column:
            primary_weights = self.file_operator.get_df(weight_column, for_primary=for_primary)
        plot_args = {'range': mrange,
                     'bins':self.n_bins}
        plot_args.update(self.std_plot_args)
        label = 'All entries'
        plot_args['hatch'] = '//'
        plot_args['alpha'] = 0.9
        if not for_primary:
            plot_args['hatch'] = r'\\'
            plot_args['alpha'] = 0.7

        ax.hist(primary, label=label, weights=primary_weights, **plot_args)
        splitted = self.file_operator.get_split_by(variable_name, for_primary=for_primary)
        if not splitted is None:
            sec_label = self.file_operator.get_split_by_name(variable_name)
            sec_label = (sec_label[:self.truncate_str_length] + '..') if len(sec_label) > self.truncate_str_length else sec_label
            ax.hist(splitted, label=sec_label, **plot_args)
        else:
            # Empty plot to switch the color:
            ax.hist([],**plot_args)
        if title is None:
            title = self.file_operator.scheme.get_short_column_name(variable_name)
        ax.set_xlabel(title)
        ax.legend(fancybox=True, framealpha=0.5)

    def plot(self, variable_names: list, weight_column=None):
        """
        Plots a canvas of n-plots.
        """
        # TODO: generalize this!
        fig, ax = plt.subplots(figsize=self.std_pad_len, dpi=100)
        for variable_name in variable_names:
            if isinstance(variable_name, tuple) or isinstance(variable_name, list):
                self.plot_scatter(variable_name, ax=ax)
                if self.file_operator.has_secondary():
                    self.plot_scatter(variable_name, ax=ax, for_primary=False)
                continue
            col_type =  str(self.file_operator.get_type(variable_name)).lower()
            if col_type.startswith('float'):
                self.plot_histogram(variable_name, ax=ax, weight_column=weight_column)
                if self.file_operator.has_secondary():
                    self.plot_histogram(variable_name, ax=ax, weight_column=weight_column,
                        for_primary=False)

            else:
                self.plot_histogram(variable_name, ax=ax, weight_column=weight_column)
                if self.file_operator.has_secondary():
                    self.plot_histogram(variable_name, ax=ax, weight_column=weight_column,
                        for_primary=False)
        fig.tight_layout()
        plt.show(block=False)
