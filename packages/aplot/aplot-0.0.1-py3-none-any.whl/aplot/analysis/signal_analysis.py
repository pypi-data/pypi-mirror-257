import typing as _t

import numpy as np
import scipy


def find_h_symmetry_axis(data: np.ndarray) -> int:
    """Find the horizontal symmetry axis for a given data.

    Args:
        data (np.ndarray): 2d np array.

    Returns:
        (int): x index of the symmetry axis.
    """
    data = (data - np.mean(data)) / np.std(data)
    # corr = scipy.signal.fftconvolve(
    #     data[:, : len(data[0]) // 2], data[:, ::-1], mode="full"
    # )
    corr = scipy.signal.fftconvolve(data, data[::-1], mode="full")
    return int((np.argmax(corr) % corr.shape[-1]) / 2)


def remove_background(data: np.ndarray, convolve_len: _t.Optional[int] = None):
    if convolve_len is None:
        convolve_len = min(50, len(data) // 15)
    data = (
        data
        - scipy.signal.convolve2d(data, np.ones((convolve_len, 1)), mode="same", boundary="symm")
        / convolve_len
    )
    return data - data.mean(axis=1)[:, np.newaxis]
