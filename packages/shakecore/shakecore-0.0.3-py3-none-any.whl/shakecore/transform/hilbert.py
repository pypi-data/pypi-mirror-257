import numpy as np
from scipy.signal import hilbert as scipy_hilbert

"""
Plan to use implement GPU acceleration using cupy in the future.
"""


def hilbert(data, dt, device="cpu"):
    """
    Hilbert transform

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
    hilbert_data : ndarray
        2D array of shape (trace, npts) containing the hilbert transform of the data.
    amp_envelope : ndarray
        2D array of shape (trace, npts) containing the amplitude envelope of the data.
    instant_phase : ndarray
        2D array of shape (trace, npts) containing the instantaneous phase of the data.
    instant_freq : ndarray
        2D array of shape (trace, npts) containing the instantaneous frequency of the data.
    """
    if data.ndim != 2:
        raise ValueError("Input data must be a 2D array")

    if device == "cpu":
        analytic_data = scipy_hilbert(data, axis=1)
        amp_envelope = np.abs(analytic_data)
        instant_phase = np.unwrap(np.angle(analytic_data))
        instant_freq = np.diff(instant_phase) / (2.0 * np.pi) * (1 / dt)
    elif device == "cuda":
        pass

    return analytic_data, amp_envelope, instant_phase, instant_freq
