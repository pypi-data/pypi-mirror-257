import matplotlib as mpl
import numpy as np

from . import utils


def plot_2d_histograms(ax, data, **kwargs):
    if isinstance(ax, (tuple, list, np.ndarray)):
        return utils.run_plot_on_axes_list(plot_2d_histograms, ax, data, **kwargs)

    bins = 100
    ax.hist2d(
        data[:, 0],
        data[:, 1],
        bins=bins,
        **utils.filter_set_kwargs(mpl.collections.QuadMesh, **kwargs),
    )
    ax.ticklabel_format(scilimits=(-1, 3))

    utils.set_params(ax, **kwargs)
