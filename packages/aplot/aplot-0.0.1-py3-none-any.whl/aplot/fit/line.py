import typing as _t

import numpy as np

from .fit_logic import FitLogic


class LineParam(_t.NamedTuple):
    amplitude: float
    offset: float


class Line(FitLogic[LineParam]):
    param: _t.Tuple[LineParam] = LineParam

    @staticmethod
    def func(x, amplitude, offset):
        return amplitude * x + offset

    @staticmethod
    def _guess(x, z, **kwargs):
        average_size = max(len(z) // 10, 1)
        y1 = np.average(z[:average_size])
        y2 = np.average(z[-average_size:])

        amplitude = (y2 - y1) / (x[-1] - x[0])
        offset = y1 - x[0] * amplitude

        return [amplitude, offset]
