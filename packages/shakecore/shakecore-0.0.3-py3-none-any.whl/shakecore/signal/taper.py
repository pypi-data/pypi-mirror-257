import warnings

import numpy as np
import scipy

from shakecore.core.utils import _add_processing_info

try:
    import cupy as cp

    GUDA_MODE = True
except Exception:
    GUDA_MODE = False


@_add_processing_info
def taper(self, max_percentage=0.05, type="hann", side="both", device="cpu"):
    if device == "cpu":
        self.data = taper_cpu(self.data, max_percentage, type, side)
    elif device == "cuda":
        self.data = taper_cuda(self.data, max_percentage, type, side)
    else:
        raise ValueError(f"Unknown device '{device}'.")


def taper_cpu(data, max_percentage, type, side):
    side_valid = ["both", "left", "right"]
    npts = data.shape[1]
    if side not in side_valid:
        raise ValueError("'side' has to be one of: %s" % side_valid)

    # max_half_lenghts_1
    max_half_lenghts_1 = None
    if max_percentage is not None:
        max_half_lenghts_1 = int(max_percentage * npts)

    if 2 * max_half_lenghts_1 > npts:
        msg = (
            "The requested taper is longer than the data. "
            "The taper will be shortened to data length."
        )
        warnings.warn(msg)

    # max_half_lenghts_2
    max_half_lenghts_2 = int(npts / 2)
    if max_half_lenghts_1 is None:
        wlen = max_half_lenghts_2
    else:
        wlen = min(max_half_lenghts_1, max_half_lenghts_2)

    if type == "bartlett":
        taper_sides = scipy.signal.bartlett(2 * wlen + 1)
    elif type == "blackman":
        taper_sides = scipy.signal.blackman(2 * wlen + 1)
    elif type == "hamming":
        taper_sides = scipy.signal.hamming(2 * wlen + 1)
    elif type == "hann":
        taper_sides = scipy.signal.hann(2 * wlen + 1)
    elif type == "kaiser":
        taper_sides = scipy.signal.kaiser(2 * wlen + 1, 14)
    else:
        raise ValueError("Unknown taper type '%s'." % type)

    if side == "left":
        taper = np.hstack((taper_sides[:wlen], np.ones(npts - wlen)))
    elif side == "right":
        taper = np.hstack(
            (np.ones(npts - wlen), taper_sides[len(taper_sides) - wlen :])
        )
    else:
        taper = np.hstack(
            (
                taper_sides[:wlen],
                np.ones(npts - 2 * wlen),
                taper_sides[len(taper_sides) - wlen :],
            )
        )

    # Convert data and taper type.
    if not np.issubdtype(data.dtype, np.floating):
        data = np.require(data, dtype=np.float64)
    taper = taper.astype(data.dtype)

    out = data * taper

    return out


def taper_cuda(data, max_percentage, type, side):
    side_valid = ["both", "left", "right"]
    npts = data.shape[1]
    if side not in side_valid:
        raise ValueError("'side' has to be one of: %s" % side_valid)

    # max_half_lenghts_1
    max_half_lenghts_1 = None
    if max_percentage is not None:
        max_half_lenghts_1 = int(max_percentage * npts)

    if 2 * max_half_lenghts_1 > npts:
        msg = (
            "The requested taper is longer than the data. "
            "The taper will be shortened to data length."
        )
        warnings.warn(msg)

    # max_half_lenghts_2
    max_half_lenghts_2 = int(npts / 2)
    if max_half_lenghts_1 is None:
        wlen = max_half_lenghts_2
    else:
        wlen = min(max_half_lenghts_1, max_half_lenghts_2)

    if type == "bartlett":
        taper_sides = cp.bartlett(2 * wlen + 1)
    elif type == "blackman":
        taper_sides = cp.blackman(2 * wlen + 1)
    elif type == "hamming":
        taper_sides = cp.hamming(2 * wlen + 1)
    elif type == "hann":
        taper_sides = cp.hann(2 * wlen + 1)
    elif type == "kaiser":
        taper_sides = cp.kaiser(2 * wlen + 1, 14)
    else:
        raise ValueError("Unknown taper type '%s'." % type)

    if side == "left":
        taper = cp.hstack((taper_sides[:wlen], cp.ones(npts - wlen)))
    elif side == "right":
        taper = cp.hstack(
            (cp.ones(npts - wlen), taper_sides[len(taper_sides) - wlen :])
        )
    else:
        taper = cp.hstack(
            (
                taper_sides[:wlen],
                cp.ones(npts - 2 * wlen),
                taper_sides[len(taper_sides) - wlen :],
            )
        )

    # Convert data if it's not a floating point type.
    if not cp.issubdtype(data.dtype, cp.floating):
        data = cp.require(data, dtype=cp.float64)

    out = data * taper

    return out
