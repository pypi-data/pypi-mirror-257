import typing as _t

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from .. import analysis, fit, styles
from ..types import _MASK
from . import utils


@utils.plot_decorator
def plot_sin(
    ax: plt.Axes, x: np.ndarray, data: np.ndarray, mask: _t.Optional[_MASK] = None, **kwargs
) -> fit.CosParam:
    """
    Plot sinusoidal data along with its cosine fit on a given axis.

    Parameters:
    -----------
    ax : plt.Axes
        An Axes object on which the data and its fit will be plotted.

    x : np.ndarray
        A 1D array of x-values corresponding to the data.

    data : np.ndarray
        A 1D array of data values corresponding to x.

    mask : _MASK, optional
        Mask on the values that are fitted.
        If only integer is passed, then mask = x<mask.

    **kwargs:
        Additional keyword arguments for styling and other purposes. These can include:
            - label: Label for the data.
            - fitlabel: Label for the fitted curve.
            - Any other styling attributes supported by `mpl.lines.Line2D`.

    Returns:
    --------
    res : fit.Cos.fit result
        The result of the cosine fit for the provided data.

    Notes:
    ------
    The function plots the given sinusoidal data on the specified axis and fits it using `fit.Cos.fit`.
    It then overlays the fitted cosine curve on the same axis. The legend of the fit includes
    the half period and the amplitude offset of the fit.

    """
    res, res_func = fit.Cos.fit(x, data, mask=mask)
    ax.plot(x, data, "o-", **utils.filter_set_kwargs(mpl.lines.Line2D, **kwargs))
    kwargs.pop("label", None)
    kwargs.setdefault("fitlabel", "fit")

    x_masked = analysis.mask_data(x, mask=mask)
    ax.plot(
        x_masked,
        res_func(x_masked),
        label=f"{kwargs['fitlabel']}: half_period = {res.period/2:.5f},\n offset={abs(2*res.offset):.3e}",
        **utils.filter_set_kwargs(mpl.lines.Line2D, **kwargs),
    )
    ax.legend()
    utils.set_params(ax, **kwargs)
    return res


@utils.plot_decorator(styles.AMPLITUDE_TIME)
def plot_damp_exp(
    ax: plt.Axes, x: np.ndarray, data: np.ndarray, mask: _t.Optional[_MASK] = None, **kwargs
) -> fit.DampedExpParam:
    """
    Plot data along with its damped exponential fit on a given axis.

    Parameters:
    -----------
    ax : plt.Axes
        An Axes object on which the data and its fit will be plotted.

    x : np.ndarray
        A 1D array of x-values corresponding to the data.

    data : np.ndarray
        A 1D array of data values corresponding to x.

    mask : np.ndarray, default=None
        Mask on the values that are fitted.
        If only integer is passed, then mask = x<mask.

    **kwargs:
        Additional keyword arguments for styling and other purposes. These may include but are not limited to:
            - label: Label for the data.
            - fitlabel: Label for the fitted curve.
            - Any other styling attributes supported by `mpl.lines.Line2D`.

    Returns:
    --------
    res : fit.DampedExp.fit result
        The result of the fit for the provided data.

    Notes:
    ------
    The function plots the given data on the specified axis and fits it using `fit.DampedExp.fit`.
    It then overlays the fitted damped exponential curve on the same axis. The legend of the fit
    includes the time constant 'tau' and the asymptotic offset of the fit.

    """
    res, res_func = fit.DampedExp.fit(x, data, mask=mask)
    ax.plot(
        x,
        data,
        **utils.filter_set_kwargs(mpl.lines.Line2D, **(kwargs | styles.DATA)),
    )

    kwargs.pop("label", None)
    kwargs.setdefault("fitlabel", "fit")

    x_masked = analysis.mask_data(x, mask=mask)
    ax.plot(
        x_masked,
        res_func(x_masked),
        label=f"{kwargs['fitlabel']}: tau = {res.tau*1e-3:.3f} us,\n asymp.={res.offset:.3f}",
        # **filter_set_kwargs(mpl.lines.Line2D, **(kwargs | styles.FIT)),
    )
    ax.legend()
    utils.set_params(ax, **kwargs)
    return res
