import numpy as np
from scipy.signal import detrend as scipy_detrend

from shakecore.core.utils import _add_processing_info

try:
    import cupy as cp
    from cupyx.scipy.signal import detrend as cupy_detrend

    GUDA_MODE = True
except Exception:
    GUDA_MODE = False


@_add_processing_info
def detrend(self, type="linear", device="cpu", **options):
    """
    Detrend data.
    :param type: The type of detrending to perform. Can be one of ``'linear'``,
        ``'constant'``, or ``'polynomial'``.
    :param **options: Additional options is the 'order'.
    """
    if device == "cpu":
        if type == "linear":
            self.data = linear_cpu(self.data)
        elif type == "constant":
            self.data = constant_cpu(self.data)
        elif type == "polynomial":
            self.data = polynomial_cpu(self.data, **options)
        else:
            raise ValueError(f"Unknown detrend type '{type}'.")

    elif device == "cuda":
        if type == "linear":
            self.data = linear_cuda(self.data)
        elif type == "constant":
            self.data = constant_cuda(self.data)
        elif type == "polynomial":
            self.data = polynomial_cuda(self.data, **options)
        else:
            raise ValueError(f"Unknown detrend type '{type}'.")

    else:
        raise ValueError(f"Unknown device '{device}'.")


# *************************************************************************************************
def linear_cpu(data):
    return scipy_detrend(data, axis=1, type="linear", overwrite_data=False)


def linear_cuda(data):
    return cupy_detrend(data, axis=1, type="linear", overwrite_data=False)


def constant_cpu(data):
    return scipy_detrend(data, axis=1, type="constant", overwrite_data=False)


def constant_cuda(data):
    return cupy_detrend(data, axis=1, type="constant", overwrite_data=False)


def polynomial_cpu(data, order=3):
    fit = np.empty_like(data)
    x = np.arange(data.shape[1])
    for i in range(data.shape[0]):
        fit[i] = np.polyval(np.polyfit(x, data[i], deg=order), x)
    data -= fit
    return data


def polynomial_cuda(data, order=3):
    fit = cp.empty_like(data)
    x = cp.arange(data.shape[1])
    for i in range(data.shape[0]):
        fit[i] = cp.polyval(cp.polyfit(x, data[i], deg=order), x)
    data -= fit
    return data
