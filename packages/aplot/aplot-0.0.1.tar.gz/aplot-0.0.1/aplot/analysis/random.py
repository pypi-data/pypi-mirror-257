import typing as _t

import numpy as np


def mask_data(data, mask: _t.Optional[_t.Union[np.ndarray, float]] = None):
    if mask is None:
        mask = [True] * len(data)
    elif isinstance(mask, (int, float)):
        mask = data < mask
    return data[mask]
