import scipy

from shakecore.core.utils import _add_processing_info

try:
    import cupy as cp
    import cupyx

    GUDA_MODE = True
except Exception:
    GUDA_MODE = False


@_add_processing_info
def resample(
    self,
    sampling_rate,
    window=None,
    device="cpu",
):
    if device == "cpu":
        new_npts = int(self.stats.npts * sampling_rate / self.stats.sampling_rate)
        self.data = scipy.signal.resample(
            self.data, num=new_npts, axis=1, window=window, domain="time"
        )
        self.stats.sampling_rate = sampling_rate

    elif device == "cuda":
        self.data = resample_cuda(
            self.data,
            raw_sampling_rate=self.stats.sampling_rate,
            sampling_rate=sampling_rate,
            window=window,
        )
        self.stats.sampling_rate = sampling_rate

    else:
        raise ValueError(f"Unknown device '{device}'.")


def resample_cuda(data, raw_sampling_rate, sampling_rate, window):
    x = data
    num = int(data.shape[1] * sampling_rate / raw_sampling_rate)
    t = None
    axis = 1
    window = window
    domain = "time"

    # ***************
    if domain not in ("time", "freq"):
        raise ValueError(
            "Acceptable domain flags are 'time' or"
            " 'freq', not domain={}".format(domain)
        )

    x = cp.asarray(x)
    Nx = x.shape[axis]

    # Check if we can use faster real FFT
    real_input = cp.isrealobj(x)

    if domain == "time":
        # Forward transform
        if real_input:
            X = cupyx.scipy.fft.rfft(x, axis=axis)
        else:  # Full complex FFT
            X = cupyx.scipy.fft.fft(x, axis=axis)
    else:  # domain == 'freq'
        X = x

    # Apply window to spectrum
    if window is not None:
        if callable(window):
            W = window(cupyx.scipy.fft.fftfreq(Nx))
        elif isinstance(window, cp.ndarray):
            if window.shape != (Nx,):
                raise ValueError("window must have the same length as data")
            W = window
        else:
            from scipy.signal import get_window

            W = cupyx.scipy.fft.ifftshift(cp.asarray(get_window(window, Nx)))

        newshape_W = [1] * x.ndim
        newshape_W[axis] = X.shape[axis]
        if real_input:
            # Fold the window back on itself to mimic complex behavior
            W_real = W.copy()
            W_real[1:] += W_real[-1:0:-1]
            W_real[1:] *= 0.5
            X *= W_real[: newshape_W[axis]].reshape(newshape_W)
        else:
            X *= W.reshape(newshape_W)

    # Copy each half of the original spectrum to the output spectrum, either
    # truncating high frequences (downsampling) or zero-padding them
    # (upsampling)

    # Placeholder array for output spectrum
    newshape = list(x.shape)
    if real_input:
        newshape[axis] = num // 2 + 1
    else:
        newshape[axis] = num
    Y = cp.zeros(newshape, X.dtype)

    # Copy positive frequency components (and Nyquist, if present)
    N = min(num, Nx)
    nyq = N // 2 + 1  # Slice index that includes Nyquist if present
    sl = [slice(None)] * x.ndim
    sl[axis] = slice(0, nyq)
    Y[tuple(sl)] = X[tuple(sl)]
    if not real_input:
        # Copy negative frequency components
        if N > 2:  # (slice expression doesn't collapse to empty array)
            sl[axis] = slice(nyq - N, None)
            Y[tuple(sl)] = X[tuple(sl)]

    # Split/join Nyquist component(s) if present
    # So far we have set Y[+N/2]=X[+N/2]
    if N % 2 == 0:
        if num < Nx:  # downsampling
            if real_input:
                sl[axis] = slice(N // 2, N // 2 + 1)
                Y[tuple(sl)] *= 2.0
            else:
                # select the component of Y at frequency +N/2,
                # add the component of X at -N/2
                sl[axis] = slice(-N // 2, -N // 2 + 1)
                Y[tuple(sl)] += X[tuple(sl)]
        elif Nx < num:  # upsampling
            # select the component at frequency +N/2 and halve it
            sl[axis] = slice(N // 2, N // 2 + 1)
            Y[tuple(sl)] *= 0.5
            if not real_input:
                temp = Y[tuple(sl)]
                # set the component at -N/2 equal to the component at +N/2
                sl[axis] = slice(num - N // 2, num - N // 2 + 1)
                Y[tuple(sl)] = temp

    # Inverse transform
    if real_input:
        y = cupyx.scipy.fft.irfft(Y, num, axis=axis)
    else:
        y = cupyx.scipy.fft.ifft(Y, axis=axis, overwrite_x=True)

    y *= float(num) / float(Nx)

    if t is None:
        return y
    else:
        new_t = cp.arange(0, num) * (t[1] - t[0]) * Nx / float(num) + t[0]
        return y, new_t
