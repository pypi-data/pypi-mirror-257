import abc
import typing as _t

import numpy as np
from scipy import optimize

_T = _t.TypeVar("_T")
_R = _t.TypeVar("_R")


def param_len(cls):
    return len(cls.__annotations__)


class FitResult(_t.Tuple[_t.Optional[_R], _t.Callable]):
    """
    Represents the result of a fit operation.

    Attributes:
        res: The result of the fit operation.
        res_func: A callable function that takes a numpy array as input and returns a numpy array as output.
    """

    res: _t.Optional[_R]
    res_func: _t.Optional[_t.Callable[[np.ndarray], np.ndarray]]

    def __init__(
        self,
        res: _t.Optional[_R] = None,
        res_func: _t.Optional[_t.Callable] = None,
        **kwargs,
    ):
        """
        Initialize the Main class.

        Args:
            res: Optional result value.
            res_func: Optional callable function for result.
            **kwargs: Additional keyword arguments.
        """
        del kwargs
        self.res = res
        self.res_func = res_func if res_func is not None else (lambda _: None)

    def __new__(
        cls,
        res: _t.Optional[_R] = None,
        res_func: _t.Optional[_t.Callable] = None,
        **kwargs,
    ):
        if res_func is None:
            res_func = lambda _: None  # noqa: E731

        new = super().__new__(cls, (res, res_func))
        return new


class FitLogic(_t.Generic[_T]):
    """
    A generic class for fitting logic.

    Parameters:
    - param: The parameter type for the fit.

    Methods:
    - __init__: Initializes the FitLogic instance.
    - func: Abstract method for the fitting function.
    - _guess: Abstract method for guessing initial fit parameters.
    - fit: Fits the data using the specified fitting function.
    - sfit: Fits the data using the specified fitting function with simulated annealing.
    - guess: Guesses the initial fit parameters.
    - error: Calculates the error between the fitted function and the data.
    - get_mask: Returns a mask array based on the provided mask or threshold.

    Attributes:
    - param: The parameter type for the fit.
    """

    param: abc.ABCMeta

    def __init__(self, *args, **kwargs):
        """Initialize the FitLogic instance.

        Parameters:
        - args: Positional arguments.
        - kwargs: Keyword arguments.
        """
        del args
        for k, v in kwargs.items():
            setattr(self, f"_{k}", v)

    @abc.abstractmethod
    @staticmethod
    def func(x, *args, **kwargs):
        """Abstract method for the fitting function.

        Parameters:
        - x: The independent variable.
        - args: Positional arguments.
        - kwargs: Keyword arguments.
        """

    @abc.abstractmethod
    @staticmethod
    def _guess(x, y, **kwargs):
        """Abstract method for guessing initial fit parameters.

        Parameters:
        - x: The independent variable.
        - y: The dependent variable.
        - kwargs: Keyword arguments.
        """

    @classmethod
    def fit(
        cls,
        x: np.ndarray,
        data: np.ndarray,
        mask: _t.Optional[_t.Union[np.ndarray, float]] = None,
        guess: _t.Optional[_T] = None,
        **kwargs,
    ) -> FitResult[_T]:  # Tuple[_T, _t.Callable, np.ndarray]:
        """Fit the data using the specified fitting function.

        Parameters:
        - x: The independent variable.
        - data: The dependent variable.
        - mask: The mask array or threshold for data filtering (optional).
        - guess: The initial guess for fit parameters (optional).
        - kwargs: Additional keyword arguments.

        Returns:
        - FitResult: The result of the fit, including the fitted parameters and the fitted function.
        """
        mask = cls.get_mask(mask, x)

        if np.sum(mask) < param_len(cls.param):
            return FitResult()

        def to_minimize(args):
            return np.abs(cls.func(x[mask], *args) - data[mask])

        if guess is None:
            guess = cls._guess(x[mask], data[mask], **kwargs)

        res, _ = optimize.leastsq(to_minimize, guess, maxfev=5000)  # full_output=True)
        # res, _, infodict, _, _ = leastsq(to_minimize, guess, full_output=True)

        return FitResult(cls.param(*res), lambda x: cls.func(x, *res))

    @classmethod
    def sfit(
        cls,
        x: np.ndarray,
        data: np.ndarray,
        mask: _t.Optional[_t.Union[np.ndarray, float]] = None,
        guess: _t.Optional[_T] = None,
        T: int = 1,
        **kwargs,
    ) -> FitResult[_T]:
        """Fit the data using the specified fitting function with simulated annealing.

        Parameters:
        - x: The independent variable.
        - data: The dependent variable.
        - mask: The mask array or threshold for data filtering (optional).
        - guess: The initial guess for fit parameters (optional).
        - T: The temperature parameter for simulated annealing (default: 1).
        - kwargs: Additional keyword arguments.

        Returns:
        - FitResult: The result of the fit, including the fitted parameters and the fitted function.
        """
        mask = cls.get_mask(mask, x)

        def to_minimize(args):
            return np.abs(np.sum((cls.func(x[mask], *args) - data[mask]) ** 2))

        if guess is None:
            guess = cls._guess(x[mask], data[mask], **kwargs)

        res = optimize.basinhopping(
            func=to_minimize,
            x0=guess,
            T=T,
            # minimizer_kwargs={"jac": lambda params: chisq_jac(sin_jac, x, y_data, params)}
        ).x

        return FitResult(cls.param(*res), lambda x: cls.func(x, *res))

    @classmethod
    def guess(
        cls, x, y, mask: _t.Optional[_t.Union[np.ndarray, float]] = None, **kwargs
    ) -> _t.Tuple[_T, _t.Callable]:
        """Guess the initial fit parameters.

        Parameters:
        - x: The independent variable.
        - y: The dependent variable.
        - mask: The mask array or threshold for data filtering (optional).
        - kwargs: Additional keyword arguments.

        Returns:
        - Tuple[_T, _t.Callable]: The guessed fit parameters and the fitted function.
        """
        mask = cls.get_mask(mask, x)
        guess_param = cls._guess(x[mask], y[mask], **kwargs)
        return cls.param(*guess_param), lambda x: cls.func(x, *guess_param)

    @classmethod
    def error(cls, func, x, y, **kwargs):
        """Calculate the error between the fitted function and the data.

        Parameters:
        - func: The fitted function.
        - x: The independent variable.
        - y: The dependent variable.
        - kwargs: Additional keyword arguments.

        Returns:
        - float: The error between the fitted function and the data.
        """
        del kwargs
        return np.sum(np.abs(func(x) - y) ** 2) / len(x)

    @staticmethod
    def get_mask(
        mask: _t.Optional[_t.Union[np.ndarray, float]] = None,
        x: _t.Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Return a mask array based on the provided mask or threshold.

        Parameters:
        - mask: The mask array or threshold (optional).
        - x: The independent variable (optional).

        Returns:
        - np.ndarray: The mask array.
        """
        if mask is None:
            return [True] * len(x)
        elif isinstance(mask, (int, float)) and x is not None:
            return x < mask
        return mask
