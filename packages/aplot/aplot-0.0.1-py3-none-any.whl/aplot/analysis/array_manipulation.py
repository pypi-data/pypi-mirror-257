import typing as _t

import numpy as np
import scipy


def argmin2d(
    d: np.ndarray,
    x_mask: _t.Optional[_t.Union[_t.Tuple[int, int], _t.List]] = None,
    y_mask: _t.Optional[_t.Union[_t.Tuple[int, int], _t.List]] = None,
    filter_: _t.Optional[int] = None,
) -> _t.Tuple[int, int]:
    """Find the indexes of the minimum of the specified 2d array. Ignores np.nan.

    Args:
        d (np.ndarray): Numpy array.
        x_mask (Optional[Union[Tuple[int, int], List]], optional): Limit where to look on x-axis.
            Can be tuple of the (start, end) indexes where to look or array of booleans of x-axis length.
            Defaults to None.
        y_mask (Optional[Union[Tuple[int, int], List]], optional): Limit where to look on y-axis.
            Can be tuple of the (start, end) indexes where to look or array of booleans of y-axis length.
            Defaults to None.
        filter (Optional[int], optional): Size of the window of the uniform_filter that is used on the data.
            Defaults to None.

    Returns:
        Tuple[int, int]: index_y, index_x, i.e. the min value is d[index_y, index_x]
    """
    if filter_ and filter_ > 1:
        d = scipy.ndimage.uniform_filter(d, size=3, mode="nearest")

    if x_mask is not None:
        if isinstance(x_mask, tuple):
            d[:, 0 : x_mask[0]] = np.nan
            d[:, x_mask[1] + 1 :] = np.nan
        else:
            d[:, ~x_mask] = np.nan
    if y_mask is not None:
        if isinstance(y_mask, tuple):
            d[0 : y_mask[0], :] = np.nan
            d[y_mask[1] + 1 :, :] = np.nan
        else:
            d[~y_mask, :] = np.nan

    shape = d.shape
    index = np.nanargmin(d)
    return index // shape[1], index % shape[1]


def array_from_bounds(
    start: float,
    stop: float,
    dstep: float,
    post_function: _t.Optional[_t.Callable] = None,
    to_list: bool = False,
) -> np.ndarray:
    """Generate an array of values centered around a given value with a specific span and step.

    Args:
        start (float): The initial point of the array.
        stop (float): The final point the center.
            If span or dstep is non-positive, returns an array with only the center.
        dstep (float): The spacing between consecutive values in the array.
        post_function (Callable, optional): An optional function to be applied element-wise
            to the resultant array. Defaults to None.
        to_list (bool, optional): If True, return the output as a Python list instead of
            a numpy array. Defaults to False.

    Returns:
        np.ndarray: Array of values starting from (center - span/2) to (center + span/2)
        with a step of dstep. If the post_function is provided, values will be transformed
        by this function.

    """
    res = (
        np.arange(
            start,
            stop + dstep / 2,
            dstep,
        )
        if ((stop - start > 0) and dstep > 0)
        else np.array([(start + stop) / 2])
    )
    if post_function:
        res = post_function(res)
    if to_list:
        res = res.tolist()
    return res


def array_from_span(
    center: float,
    span: float,
    dstep: float,
    post_function: _t.Optional[_t.Callable] = None,
    to_list: bool = False,
) -> np.ndarray:
    """Generate an array of values centered around a given value with a specific span and step.

    Args:
        center (float): The central value of the array.
        span (float): The total range of values around the center.
            If span or dstep is non-positive, returns an array with only the center.
        dstep (float): The spacing between consecutive values in the array.
        post_function (Callable, optional): An optional function to be applied element-wise
            to the resultant array. Defaults to None.
        to_list (bool, optional): If True, return the output as a Python list instead of
            a numpy array. Defaults to False.

    Returns:
        np.ndarray: Array of values starting from (center - span/2) to (center + span/2)
        with a step of dstep. If the post_function is provided, values will be transformed
        by this function.

    """
    res = (
        np.arange(
            center - span / 2,
            center + span / 2 + dstep / 2,
            dstep,
        )
        if (span > 0 and dstep > 0)
        else np.array([center])
    )
    if post_function:
        res = post_function(res)
    if to_list:
        res = res.tolist()
    return res


def get_z(I: np.ndarray, Q: np.ndarray) -> np.ndarray:  # pylint: disable=invalid-name # noqa: E741
    min_len = min(len(I), len(Q))
    return I[:min_len] + 1j * Q[:min_len]


def combine_arrays(datax, datay):
    length = min(len(datax), len(datay))
    combined = np.array([datax[:length], datay[:length]])
    return combined
