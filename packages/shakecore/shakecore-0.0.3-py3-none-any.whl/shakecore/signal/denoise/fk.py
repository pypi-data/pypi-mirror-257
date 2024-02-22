import numpy as np
from scipy.ndimage import gaussian_filter, uniform_filter

from shakecore.transform import fk_forward, fk_inverse


def fk_cpu(
    data,
    dx,
    dt,
    vmin,
    vmax,
    polygon_mode="eliminate",
    nx=1,
    nt=1,
    smooth="no",  # no, guassian, uniform
    guassian_sigma=1,
    uniform_size=1,
):
    """
    Compute fk transform of a 2D array.

    Parameters
    ----------
    data : ndarray
        2D array of shape (nx, nt) containing the data.
    dx : float
        Sampling rate in meters.
    dt : float
        Sampling rate in seconds.
    vmin : float
        Minimum velocity in meters per second.
    vmax : float
        Maximum velocity in meters per second.
    polygon_mode : str
        If 'eliminate', the polygon is eliminated from the fk spectrum.
        If 'extract', the polygon is extracted in the fk spectrum.
    nx : int
        Dense x direction to improve the filter performance
    nt : int
        Dense t direction to improve the filter performance
    smooth : str
        If 'no', no smoothing is applied.
        If 'gaussian', a gaussian smoothing filter is applied.
        If 'uniform', a uniform smoothing filter is applied.
    guassian_sigma : float
        Sigma of the gaussian smoothing filter.
    uniform_size : int
        Size of the uniform smoothing filter.


    Returns
    -------
    filtered_data : ndarray
        2D array of shape (nx, nt) containing the filtered data.
    """
    # Compute the FK transform of the data
    raw_shape = data.shape
    new_shape = (nx * data.shape[0], nt * data.shape[1])
    fk_data, k_axis, f_axis, _, _ = fk_forward(data, dx, dt, new_shape, device="cpu")

    # Keep uniform with the positive direction from L to R
    fk_data = np.flip(fk_data, axis=0)

    # Create a velocity filter in the FK domain
    v_filter = np.ones_like(fk_data.real)
    f_grid, k_grid = np.meshgrid(f_axis, k_axis, indexing="xy")
    with np.errstate(divide="ignore", invalid="ignore"):
        v = f_grid / k_grid
        v[k_grid == 0] = np.inf
    v_filter[(v >= vmin) & (v <= vmax)] = 0

    # Smooth the filter
    if smooth == "gaussian":
        v_filter = gaussian_filter(v_filter, sigma=guassian_sigma)
    elif smooth == "uniform":
        v_filter = uniform_filter(v_filter, size=uniform_size)
    elif smooth == "no":
        pass
    else:
        raise ValueError(
            "Invalid value for smooth. Must be 'no', 'gaussian', or 'uniform'."
        )

    # Apply the velocity filter
    if polygon_mode == "eliminate":
        fk_data *= v_filter
    elif polygon_mode == "extract":
        fk_data *= 1 - v_filter
    else:
        raise ValueError(
            "Invalid value for polygon_mode. Must be 'eliminate' or 'extract'."
        )

    # Perform the inverse FK transform to get the filtered data
    fk_data = np.flip(fk_data, axis=0)
    filtered_data = fk_inverse(fk_data, raw_shape, device="cpu").real

    return filtered_data
