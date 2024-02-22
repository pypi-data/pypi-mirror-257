import pycwt

"""
Refer to https://github.com/regeirk/pycwt

Plan to rewrite pycwt to use cupy for GPU acceleration in the future.
"""


def cwt_forward(signal, dt, dj=1 / 12, s0=-1, J=-1, wavelet="morlet", freqs=None):
    """Continuous wavelet transform of the signal at specified scales.

    Parameters
    ----------
    signal : numpy.ndarray, list
        Input signal array.
    dt : float
        Sampling interval.
    dj : float, optional
        Spacing between discrete scales. Default value is 1/12.
        Smaller values will result in better scale resolution, but
        slower calculation and plot.
    s0 : float, optional
        Smallest scale of the wavelet. Default value is 2*dt.
    J : float, optional
        Number of scales less one. Scales range from s0 up to
        s0 * 2**(J * dj), which gives a total of (J + 1) scales.
        Default is J = (log2(N * dt / so)) / dj.
    wavelet : instance of Wavelet class, or string
        Mother wavelet class. Default is Morlet wavelet.
    freqs : numpy.ndarray, optional
        Custom frequencies to use instead of the ones corresponding
        to the scales described above. Corresponding scales are
        calculated using the wavelet Fourier wavelength.

    Returns
    -------
    W : numpy.ndarray
        Wavelet transform according to the selected mother wavelet.
        Has (J+1) x N dimensions.
    sj : numpy.ndarray
        Vector of scale indices given by sj = s0 * 2**(j * dj),
        j={0, 1, ..., J}.
    freqs : array like
        Vector of Fourier frequencies (in 1 / time units) that
        corresponds to the wavelet scales.
    coi : numpy.ndarray
        Returns the cone of influence, which is a vector of N
        points containing the maximum Fourier period of useful
        information at that particular time. Periods greater than
        those are subject to edge effects.
    fft : numpy.ndarray
        Normalized fast Fourier transform of the input signal.
    fftfreqs : numpy.ndarray
        Fourier frequencies (in 1/time units) for the calculated
        FFT spectrum.

    Example
    -------
    >> mother = wavelet.Morlet(6.)
    >> wave, scales, freqs, coi, fft, fftfreqs = wavelet.cwt(signal,
           0.25, 0.25, 0.5, 28, mother)

    """
    wave, scales, freqs, coi, fft, fftfreqs = pycwt.cwt(
        signal, dt, dj, s0, J, wavelet, freqs
    )

    return wave, scales, freqs, coi, fft, fftfreqs


def cwt_inverse(W, sj, dt, dj=1 / 12, wavelet="morlet"):
    """Inverse continuous wavelet transform.

    Parameters
    ----------
    W : numpy.ndarray
        Wavelet transform, the result of the `cwt` function.
    sj : numpy.ndarray
        Vector of scale indices as returned by the `cwt` function.
    dt : float
        Sample spacing.
    dj : float, optional
        Spacing between discrete scales as used in the `cwt`
        function. Default value is 0.25.
    wavelet : instance of Wavelet class, or string
        Mother wavelet class. Default is Morlet

    Returns
    -------
    iW : numpy.ndarray
        Inverse wavelet transform.

    Example
    -------
    >> mother = wavelet.Morlet()
    >> wave, scales, freqs, coi, fft, fftfreqs = wavelet.cwt(var,
           0.25, 0.25, 0.5, 28, mother)
    >> iwave = wavelet.icwt(wave, scales, 0.25, 0.25, mother)

    """

    iW = pycwt.icwt(W, sj, dt, dj, wavelet)

    return iW
