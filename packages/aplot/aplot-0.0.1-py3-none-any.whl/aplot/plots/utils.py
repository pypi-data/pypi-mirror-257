import functools
import typing as _t

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from ..code_utils import pop_from_dict  # pylint: disable=W0611 # noqa: F401


def push_labels_to_kwargs(labels: _t.Optional[_t.Dict[str, str]], kwargs: _t.Dict[str, str]):
    if labels is not None:
        for k, v in labels.items():
            kwargs.setdefault(k, v)


def plot_decorator(default_labels=None):
    """
    A decorator that can be used to add default labels to a plotting function.

    Parameters:
    - default_labels (callable or None): A callable that returns the default labels to be used,
        or None if no default labels are needed.

    Returns:
    - decorated_function (function): The decorated plotting function.

    Usage:
    @plot_decorator(default_labels=my_default_labels)
    def my_plot_function(*args, **kwargs):
        # Plotting logic here
        pass

    """
    if callable(default_labels):
        original_function, default_labels = default_labels, None
    else:
        original_function = None

    def _decorate(function):
        @functools.wraps(function)
        def wrapped_function(*args, **kwargs):
            if default_labels:
                kwargs.setdefault("labels", default_labels)

            if "labels" in kwargs:
                push_labels_to_kwargs(kwargs["labels"], kwargs)
            return function(*args, **kwargs)

        return wrapped_function

    if original_function:
        return _decorate(original_function)

    return _decorate


def suptitle(text, figure: _t.Optional[Figure] = None):
    if figure is None:
        figure = plt.gcf()
    text_before = figure._suptitle  # pylint: disable=protected-access
    if text_before:
        text_before = text_before.get_text()
        plt.suptitle(text + "\n" + text_before)
    else:
        plt.suptitle(text)


def run_map(func: _t.Callable, elements: _t.Iterable):
    for element in elements:
        func(element)


def run_plot_on_axes_list(func, axes, data, *args, **kwargs):
    for i, (a, d) in enumerate(zip(axes, data)):
        kwargs_one = kwargs.copy()
        for k in list(kwargs_one.keys()):
            if not k.startswith("list_"):
                continue
            v = kwargs_one.pop(k, None)
            if isinstance(v, (list, tuple, np.ndarray)):
                kwargs_one[k[5:]] = v[i]
        func(a, *args, data=d, **kwargs_one)
    return


def filter_set_kwargs(obj, **kwargs):
    """Filter kwargs to one that can be set with set_... method."""
    for k in list(kwargs.keys()):
        func = getattr(obj, f"set_{k}", None)
        if not callable(func):
            kwargs.pop(k)
    return kwargs


def set_params(ax: plt.Axes, **kwargs):
    """Set the parameters of the Axes if they exist.

    Args:
        ax (plt.Axes): Axes.
        kwargs (dict): Parameters to set.

    Returns:
        list: Lis of the parameters that were set.
    """
    kwargs = filter_set_kwargs(ax, **kwargs)
    return ax.set(**kwargs)
