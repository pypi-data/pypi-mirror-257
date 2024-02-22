import numpy as np

from shakecore.core.utils import _add_processing_info
from shakecore.transform import fk_forward, fk_inverse


@_add_processing_info
def strain_rate_2_velocity(self, method="fk_scaling", sigma=1e-5, device="cpu"):
    # self.data = self.data / apparent_velocity
    """
    Method-1: FK
        a.transform to FK domain
        b.multiply by a scalar according to ...
        c.transform back to time domain

    Method-2: Slant Stack (determine the apparent velocity at each second)
        a...
    """
    if self.stats.type != "strain_rate":
        raise ValueError("Input data must be strain rate")

    if method == "fk_scaling":
        # convert strain rate to strain
        self.integrate(device=device)

        # fk transform
        fk_data, k_axis, f_axis, _, _ = fk_forward(
            self.data, self.stats.interval, self.stats.delta, device=device
        )

        # compute scaling factor
        f_grid, k_grid = np.meshgrid(f_axis, k_axis, indexing="xy")
        with np.errstate(divide="ignore", invalid="ignore"):
            scale = (f_grid + sigma) / (k_grid + sigma)

        # apply scaling factor
        fk_data *= scale

        # inverse fk transform
        self.data = fk_inverse(fk_data, device=device).real
    else:
        raise ValueError(f"Unknown method '{method}'")

    self.stats.type = "velocity"


@_add_processing_info
def velocity_2_strain_rate(self, gauge_length, device="cpu"):
    """
    Convert velocity to strain rate.
    """
    if self.stats.type != "velocity":
        raise ValueError("Input data must be velocity")

    gauge_samples = round(gauge_length / self.stats.interval)
    mid = gauge_samples // 2

    if device == "cpu":
        npts = self.data.shape[1]
        self.data[mid:-mid, :] = (
            self.data[gauge_samples - 1 : -1, :] - self.data[0:-gauge_samples, :]
        ) / gauge_length
        self.data[0:mid, :] = np.zeros((mid, npts), dtype=self.data.dtype)
        self.data[-mid:, :] = np.zeros((mid, npts), dtype=self.data.dtype)
    elif device == "cuda":
        pass

    self.stats.type = "strain_rate"


@_add_processing_info
def deformation_rate_2_strain_rate(self, gauge_length, device="cpu"):
    """
    Convert deformation rate to strain rate.
    """
    if self.stats.type != "deformation_rate":
        raise ValueError("Input data must be deformation rate")

    gauge_samples = round(gauge_length / self.stats.interval)
    mid = gauge_samples // 2

    if device == "cpu":
        npts = self.data.shape[1]
        self.data[mid:-mid, :] = (
            self.data[gauge_samples - 1 : -1, :] - self.data[0:-gauge_samples, :]
        ) / gauge_length
        self.data[0:mid, :] = np.zeros((mid, npts), dtype=self.data.dtype)
        self.data[-mid:, :] = np.zeros((mid, npts), dtype=self.data.dtype)
    elif device == "cuda":
        pass

    self.stats.type = "strain_rate"
