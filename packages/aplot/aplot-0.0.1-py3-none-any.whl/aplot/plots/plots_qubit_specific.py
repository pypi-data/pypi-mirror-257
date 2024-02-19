import typing as _t

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from .. import fit, styles
from ..types import _MASK
from . import utils
from .plots_2d import imshow


@utils.plot_decorator(styles.RAMSEY)
def plot_ramsey_2_angles(
    axes: _t.Tuple[plt.Axes, plt.Axes],
    times: np.ndarray,
    data: np.ndarray,
    mask: _t.Optional[_MASK] = None,
    **kwargs,
) -> fit.ComplexSpiralParam:
    """
    Plot Ramsey 2 angles, both in-phase and in quadrature components, and their corresponding fits.

    Parameters:
    -----------
    axes : _t.Tuple[plt.Axes, plt.Axes]
        A tuple of two Axes objects where the data will be plotted.

    times : np.ndarray
        A 1D array of time values corresponding to the data.

    data : np.ndarray
        A 2D array where the first column corresponds to the real part and the second column
        to the imaginary part of the data.

    mask : _t.Optional[_t.Union[int, np.ndarray]], default=None
        Mask on the values that are fitted.
        If only integer is passed, then mask = times<mask.

    **kwargs:
        Additional keyword arguments which can be passed for styling and other purposes.
        These may include but are not limited to:
            - label: Label for the data.
            - fitlabel: Label for the fitted curve.
            - Any other styling attributes supported by `mpl.lines.Line2D`.

    Returns:
    --------
    res : fit.ComplexSpiral.fit result
        The result of the fit for the provided data.

    Notes:
    ------
    The function plots the real (in-phase) and imaginary (in quadrature) parts of the data on
    the provided axes. Additionally, it fits the data using
    `fit.ComplexSpiral.fit` and plots the fitted curves.

    """
    data = data.T[0] + 1j * data.T[1]
    start = np.average(data[:10])
    end = np.average(data[-10:])
    line = (end - start) * np.arange(len(data)) / len(data) + start
    res, res_func = fit.ComplexSpiral.fit(times, data - line, mask=mask)
    # line, line_func = fit.Line.fit(times, data, mask=mask)

    # times_fit = np.linspace(0, max(times), 1001)
    kwargs_fit = kwargs | styles.FIT
    kwargs_fit = (kwargs_fit - "label") | {"label": kwargs_fit.get("fitlabel")}
    kwargs_data = kwargs | styles.DATA

    for ax, func_, label in zip(axes, (np.real, np.imag), ("in-phase", "in quadrature")):
        ax.plot(
            times,
            func_(data),
            label=f'{kwargs_data.get("label", "")} {label}',
            **utils.filter_set_kwargs(mpl.lines.Line2D, **(kwargs_data - ("label"))),
        )
        ax.plot(
            times,
            func_(res_func(times) + line),
            **utils.filter_set_kwargs(mpl.lines.Line2D, **kwargs_fit),
        )
        utils.set_params(ax, **kwargs)
        ax.legend()
    return res


@utils.plot_decorator
def plot_ramsey_vs_flux(
    axes: _t.Tuple[plt.Axes, plt.Axes],
    voltages: np.ndarray,
    times: np.ndarray,
    data: np.ndarray,
    frequency_if: float,
    frequency_lo: float,
    ramsey_detuning: float,
    show_guess: bool = False,
    **kwargs,
) -> _t.Tuple[fit.HyperbolaParam, np.ndarray, np.ndarray]:
    fit_data = np.zeros(data.shape[:-1])

    frequencies = np.zeros(data.shape[0])
    t2_list = np.zeros(data.shape[0])
    cov_list = []  # np.zeros(data.shape[0])

    for i, d in enumerate(data):
        d = d[:, 0] + 1j * d[:, 1]
        res, res_func = fit.ComplexSpiral.fit(times, d)
        fit_data[i] = np.real(res_func(times))
        frequencies[i] = frequency_lo + frequency_if + (ramsey_detuning + res.freq) * 1e9
        t2_list[i] = res.tau
        error = fit.ComplexSpiral.error(res_func, times, d)
        cov_list.append(error)

    imshow(
        axes[0],
        data[:, :, 0].T,
        x=voltages,
        y=times * 1e-3,
        **(kwargs | styles.VOLT_TIME),
    )
    imshow(
        axes[1],
        fit_data.T,
        x=voltages,
        y=times * 1e-3,
        colorbar=False,
        **(kwargs | styles.VOLT_TIME),
    )
    lims = axes[0].get_ylim()
    axes[0].plot(voltages, t2_list * 1e-3, color=styles.colors[1], label="T2 from fit")
    axes[0].set_ylim(*lims)
    axes[0].legend()

    diff = np.abs(np.diff(frequencies))
    final_diff = np.abs(
        (np.insert(diff, 0, diff[0]) + np.insert(diff, -1, diff[-1])) / 2 / frequencies
    )

    mask = final_diff < 1e-3

    res, res_func = fit.Hyperbola.fit(voltages[2:-2], frequencies[2:-2], mask=mask[2:-2])
    # else:
    #     res = None

    if res is not None:
        second_ax1 = axes[1].twinx()
        second_ax1.plot(
            voltages,
            frequencies * 1e-9,
            color=styles.colors[1],
            label=kwargs.get("freq_label", "Frequency from fit"),
        )
        frequencies2 = frequencies.copy()
        frequencies2[mask] = np.nan
        second_ax1.plot(
            voltages,
            frequencies2 * 1e-9,
            color="k",
        )
        frequencies_fit = res_func(voltages) * 1e-9
        second_ax1.plot(
            voltages,
            frequencies_fit,
            linestyle="--",
            color=styles.colors[2],
            label=kwargs.get("freq_fit_label", "Hyperbola fit on freq"),
        )
        if show_guess:
            _, res_guess = fit.Hyperbola.guess(voltages, frequencies, mask=mask, direction=1)
            second_ax1.plot(
                voltages,
                res_guess(voltages) * 1e-9,
                linestyle="--",
                color=styles.colors[3],
                label=kwargs.get("freq_guess_label", "Hyperbola guess on freq"),
            )

        second_ax1.set_ylabel(kwargs.get("ylabel2", "Frequency, GHz"))
        lims = min(frequencies_fit), max(frequencies_fit)
        delta = lims[1] - lims[0]
        second_ax1.set_ylim(lims[0] - delta * 0.2, lims[1] + delta * 0.2)
        second_ax1.legend()

    return res, frequencies, t2_list, cov_list
