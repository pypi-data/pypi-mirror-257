import numpy as np
import scipy

from shakecore.core.utils import _add_processing_info

try:
    import cupy as cp

    GUDA_MODE = True
except Exception:
    GUDA_MODE = False

TYPES = {
    "unknown": "unknown",
    "displacement": "unknown",
    "velocity": "displacement",
    "acceleration": "velocity",
    "pressure": "unknown",
    "strain_rate": "strain_rate",
    "strain": "unknown",
    "deformation_rate": "unknown",
}


@_add_processing_info
def integrate(self, type="cumsum", device="cpu"):
    if device == "cpu":
        if type == "cumsum":
            self.data = cumsum_cpu(self.data, dx=self.stats.delta)
        elif type == "cumtrapz":
            self.data = cumtrapz_cpu(self.data, dx=self.stats.delta)
        else:
            raise ValueError(f"Unknown integrate type '{type}'.")
        self.stats.type = TYPES[self.stats.type]

    elif device == "cuda":
        if type == "cumsum":
            self.data = cumsum_cuda(self.data, dx=self.stats.delta)
        elif type == "cumtrapz":
            raise NotImplementedError("cumtrapz is not implemented for CUDA.")
        else:
            raise ValueError(f"Unknown integrate type '{type}'.")
        self.stats.type = TYPES[self.stats.type]

    else:
        raise ValueError(f"Unknown device '{device}'.")


def cumsum_cpu(data, dx):
    averages = (data[:, :-1] + data[:, 1:]) / 2
    zeroes = np.zeros((data.shape[0], 1), dtype=data.dtype)
    averages = np.concatenate((zeroes, averages), axis=1)
    out = np.cumsum(averages, axis=1) * dx

    return out


def cumsum_cuda(data, dx):
    # Ensure data is a cupy ndarray
    data = cp.asarray(data)
    averages = (data[:, :-1] + data[:, 1:]) / 2
    zeroes = cp.zeros((data.shape[0], 1), dtype=data.dtype)
    averages = cp.concatenate((zeroes, averages), axis=1)
    out = cp.cumsum(averages, axis=1) * dx

    return out


def cumtrapz_cpu(data, dx):
    # Integrate. Set first value to zero to avoid changing the total
    # length of the array.
    # (manually adding the zero and not using `cumtrapz(..., initial=0)` is a
    # backwards compatibility fix for scipy versions < 0.11.
    ret = scipy.integrate.cumtrapz(data, dx=dx, axis=1)
    zeroes = np.zeros((data.shape[0], 1), dtype=ret.dtype)
    out = np.concatenate([zeroes, ret], axis=1)

    return out
