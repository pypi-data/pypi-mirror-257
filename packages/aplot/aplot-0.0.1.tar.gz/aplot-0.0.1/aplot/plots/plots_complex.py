import typing as _t

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from .. import styles
from . import utils
from .plots_2d import imshow
from .plots_histograms import plot_2d_histograms


@utils.plot_decorator(styles.REIM)
def plot_z_parametric(ax: plt.Axes, z: np.ndarray, **kwargs):
    ax.plot(np.real(z), np.imag(z), **utils.filter_set_kwargs(mpl.lines.Line2D, **kwargs))

    utils.set_params(ax, **kwargs)

    return ax


def plot_z_1d(
    axes: _t.Tuple[plt.Axes, plt.Axes],
    x: np.ndarray,
    z: np.ndarray,
    plot_format: _t.Literal["bode", "real_imag"] = "bode",
    unwrap: bool = False,
    **kwargs,
):
    if plot_format == "bode":
        data1 = np.abs(z)
        data2 = np.angle(z) * 180 / np.pi
        if unwrap:
            data2 = np.unwrap(data2, period=360)
        axes[0].set_title("Amplitude")
        axes[1].set_title("Phase")
    elif plot_format == "real_imag":
        data1 = np.real(z)
        data2 = np.imag(z)
        axes[0].set_title("Real")
        axes[1].set_title("Imag")
    else:
        raise ValueError("Plot_format should be either bode or real_imag")

    kwargs_without_xlabel = utils.pop_from_dict(kwargs, "xlabel")
    axes[0].plot(x, data1, **utils.filter_set_kwargs(mpl.lines.Line2D, **kwargs_without_xlabel))
    axes[1].plot(x, data2, **utils.filter_set_kwargs(mpl.lines.Line2D, **kwargs))

    return axes


def plot_z_2d(
    axes: _t.Tuple[plt.Axes, plt.Axes],
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    plot_format: _t.Literal["bode", "real_imag"] = "bode",
    # cmap: _t.Optional[str] = None,
    **kwargs,
):
    if plot_format == "bode":
        data1 = 20 * np.log10(np.abs(z))
        data2 = np.angle(z) * 180 / np.pi
        data2 = np.unwrap(data2, period=360)
        axes[0].set_title("Amplitude")
        axes[1].set_title("Phase")
    elif plot_format == "real_imag":
        data1 = np.real(z)
        data2 = np.imag(z)
        axes[0].set_title("Real")
        axes[1].set_title("Imag")
    else:
        raise ValueError("Plot_format should be either bode or real_imag")

    kwargs_without_xlabel = utils.pop_from_dict(kwargs, "xlabel")
    imshow(axes[0], data1, x=x, y=y, **kwargs_without_xlabel)
    im = axes[1].pcolor(x, y, data2)
    plt.colorbar(im, ax=axes[1])
    return axes


@utils.plot_decorator(styles.IQquadrature)
def plot_z_histograms(ax, data, **kwargs):
    plot_2d_histograms(ax, data, **kwargs)
