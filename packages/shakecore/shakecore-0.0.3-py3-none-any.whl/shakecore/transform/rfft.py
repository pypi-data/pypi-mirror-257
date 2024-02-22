import numpy as np
from scipy.fft import irfft, rfft


def rfft_forward(data, dt, device="cpu"):
    """
    Forward Fourier transform

    Parameters
    ----------
    data : ndarray
        2D array of shape (trace, npts) containing the data.
    dt : float
        Sampling rate in seconds.
    device : str
        Device to perform the computation on. Options are 'cpu' and 'cuda'.

    Returns
    -------
    rfft_data : ndarray
        2D array of shape (trace, freq) containing the rfft transform of the data.
    f_axis : ndarray
        1D array of shape (freq) containing the frequency axis, and frequency is from zero to positive.
    df : float
        Frequency sampling rate.
    """
    if data.ndim != 2:
        raise ValueError("Input data must be a 2D array")

    if device == "cpu":
        # Perform the 2D Fourier Transform
        rfft_data = rfft(data, axis=1)

        # Calculate the frequency and wavenumber axes
        npts = data.shape[1]
        df = 1 / (dt * npts)
        f_axis = np.fft.rfftfreq(npts, dt)
    elif device == "cuda":
        pass

    return rfft_data, f_axis, df


def rfft_inverse(rfft_data, device="cpu"):
    """
    Inverse Fourier transform

    Parameters
    ----------
    rfft_data : ndarray
        2D array of shape (trace, freq) containing the data.
    df : float
        Frequency sampling rate.
    device : str
        Device to perform the computation on. Options are 'cpu' and 'cuda'.

    Returns
    -------
    data : ndarray
        2D array of shape (trace, npts) containing the FK transform of the data.
    """
    if rfft_data.ndim != 2:
        raise ValueError("Input data must be a 2D array")

    if device == "cpu":
        # Perform the 2D Fourier Transform
        data = irfft(rfft_data, axis=1)
    elif device == "cuda":
        pass

    return data
