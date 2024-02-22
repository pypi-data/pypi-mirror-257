import numpy as np
from scipy.fft import fft2, fftshift, ifft2, ifftshift


def fk_forward(data, dx, dt, new_shape=None, device="cpu"):
    """
    Forward 2D Fourier transform

    Parameters
    ----------
    data : ndarray
        2D array of shape (nx, nt) containing the data.
    dx : float
        Sampling rate in meters.
    dt : float
        Sampling rate in seconds.
    new_shape : tuple
        Shape of the output array.
    device : str
        Device to perform the computation on. Options are 'cpu' and 'cuda'.

    Returns
    -------
    fk_data : ndarray
        2D array of shape (nk, nf) containing the FK transform of the data.
    k_axis : ndarray
        1D array of shape (nk,) containing the wavenumber axis, and wave number is from negative to positive.
    f_axis : ndarray
        1D array of shape (nf,) containing the frequency axis, and frequency is from negative to positive.
    dk : float
        Wavenumber sampling rate.
    df : float
        Frequency sampling rate.
    """
    if data.ndim != 2:
        raise ValueError("Input data must be a 2D array")

    if new_shape is None:
        new_shape = data.shape

    if device == "cpu":
        # Perform the 2D Fourier Transform
        fk_data = fftshift(fft2(data, s=new_shape))

        # Calculate the frequency and wavenumber axes
        n_trace, npts = new_shape[0], new_shape[1]
        dk = 1 / (dx * n_trace)
        df = 1 / (dt * npts)
        k_axis = fftshift(np.fft.fftfreq(n_trace, dx))
        f_axis = fftshift(np.fft.fftfreq(npts, dt))
    elif device == "cuda":
        pass

    return fk_data, k_axis, f_axis, dk, df


def fk_inverse(fk_data, new_shape=None, device="cpu"):
    """
    Inverse 2D Fourier transform
    """
    if fk_data.ndim != 2:
        raise ValueError("Input data must be a 2D array")

    if new_shape is None:
        new_shape = fk_data.shape

    if device == "cpu":
        # Perform the 2D Fourier Transform
        data = ifft2(ifftshift(fk_data))
        data = data[: new_shape[0], : new_shape[1]]
    elif device == "cuda":
        pass

    return data
