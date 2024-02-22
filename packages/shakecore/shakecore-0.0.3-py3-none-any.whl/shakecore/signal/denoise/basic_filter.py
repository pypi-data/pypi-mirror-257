import warnings

import numpy as np
import scipy

try:
    import cupy as cp
    import cupyx

    GUDA_MODE = True
except Exception:
    GUDA_MODE = False


def bandpass_cpu(data, freqmin, freqmax, df, corners=4, zerophase=False):
    fe = 0.5 * df
    low = freqmin / fe
    high = freqmax / fe
    # raise for some bad scenarios
    if high - 1.0 > -1e-6:
        msg = (
            "Selected high corner frequency ({}) of bandpass is at or "
            "above Nyquist ({}). Applying a high-pass instead."
        ).format(freqmax, fe)
        warnings.warn(msg)
        return highpass_cpu(
            data, freq=freqmin, df=df, corners=corners, zerophase=zerophase
        )
    if low > 1:
        msg = "Selected low corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = scipy.signal.iirfilter(
        corners, [low, high], btype="band", ftype="butter", output="zpk"
    )
    sos = scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = scipy.signal.sosfilt(sos, data, axis=1)
        out = scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def bandpass_cuda(data, freqmin, freqmax, df, corners=4, zerophase=False):
    fe = 0.5 * df
    low = freqmin / fe
    high = freqmax / fe
    # raise for some bad scenarios
    if high - 1.0 > -1e-6:
        msg = (
            "Selected high corner frequency ({}) of bandpass is at or "
            "above Nyquist ({}). Applying a high-pass instead."
        ).format(freqmax, fe)
        warnings.warn(msg)
        return highpass_cuda(
            data, freq=freqmin, df=df, corners=corners, zerophase=zerophase
        )
    if low > 1:
        msg = "Selected low corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = cupyx.scipy.signal.iirfilter(
        corners, [low, high], btype="band", ftype="butter", output="zpk"
    )
    sos = cupyx.scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        out = cupyx.scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = cupyx.scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def bandstop_cpu(data, freqmin, freqmax, df, corners=4, zerophase=False):
    fe = 0.5 * df
    low = freqmin / fe
    high = freqmax / fe
    # raise for some bad scenarios
    if high > 1:
        high = 1.0
        msg = (
            "Selected high corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    if low > 1:
        msg = "Selected low corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = scipy.signal.iirfilter(
        corners, [low, high], btype="bandstop", ftype="butter", output="zpk"
    )
    sos = scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = scipy.signal.sosfilt(sos, data, axis=1)
        out = scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def bandstop_cuda(data, freqmin, freqmax, df, corners=4, zerophase=False):
    fe = 0.5 * df
    low = freqmin / fe
    high = freqmax / fe
    # raise for some bad scenarios
    if high > 1:
        high = 1.0
        msg = (
            "Selected high corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    if low > 1:
        msg = "Selected low corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = cupyx.scipy.signal.iirfilter(
        corners, [low, high], btype="bandstop", ftype="butter", output="zpk"
    )
    sos = cupyx.scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        out = cupyx.scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = cupyx.scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def lowpass_cpu(data, freq, df, corners=4, zerophase=False):
    fe = 0.5 * df
    f = freq / fe
    # raise for some bad scenarios
    if f > 1:
        f = 1.0
        msg = (
            "Selected corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    z, p, k = scipy.signal.iirfilter(
        corners, f, btype="lowpass", ftype="butter", output="zpk"
    )
    sos = scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = scipy.signal.sosfilt(sos, data, axis=1)
        out = scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def lowpass_cuda(data, freq, df, corners=4, zerophase=False):
    fe = 0.5 * df
    f = freq / fe
    # raise for some bad scenarios
    if f > 1:
        f = 1.0
        msg = (
            "Selected corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    z, p, k = cupyx.scipy.signal.iirfilter(
        corners, f, btype="lowpass", ftype="butter", output="zpk"
    )
    sos = cupyx.scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        out = cupyx.scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = cupyx.scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def highpass_cpu(data, freq, df, corners=4, zerophase=False):
    fe = 0.5 * df
    f = freq / fe
    # raise for some bad scenarios
    if f > 1:
        msg = "Selected corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = scipy.signal.iirfilter(
        corners, f, btype="highpass", ftype="butter", output="zpk"
    )
    sos = scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = scipy.signal.sosfilt(sos, data, axis=1)
        out = scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def highpass_cuda(data, freq, df, corners=4, zerophase=False):
    fe = 0.5 * df
    f = freq / fe
    # raise for some bad scenarios
    if f > 1:
        msg = "Selected corner frequency is above Nyquist."
        raise ValueError(msg)
    z, p, k = cupyx.scipy.signal.iirfilter(
        corners, f, btype="highpass", ftype="butter", output="zpk"
    )
    sos = cupyx.scipy.signal.zpk2sos(z, p, k)
    if zerophase:
        ### obspy style
        firstpass = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        out = cupyx.scipy.signal.sosfilt(sos, firstpass[:, ::-1], axis=1)[:, ::-1]
        ### scipy style
        # out = cupyx.scipy.signal.sosfiltfilt(sos, data, axis=1)
        return out.astype(data.dtype)
    else:
        out = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
        return out.astype(data.dtype)


def medfilt_cpu(data, traces=[None, None], slidesize=None):
    if slidesize is None:
        tr1, tr2 = traces
        if tr1 is None:
            tr1 = 0
        if tr2 is None:
            tr2 = data.shape[0]

        stacking = data[tr1:tr2, :].mean(axis=0, keepdims=True)
        data = np.subtract(data, stacking)
    else:
        slidesize = int(slidesize)
        for i in range(0, data.shape[0], slidesize):
            tr1 = i
            tr2 = i + slidesize
            stacking = data[tr1:tr2, :].mean(axis=0, keepdims=True)
            data[tr1:tr2, :] = np.subtract(data[tr1:tr2, :], stacking)

    return data


def medfilt_cuda(data, traces=[None, None]):
    tr1, tr2 = traces
    if tr1 is None:
        tr1 = 0
    if tr2 is None:
        tr2 = data.shape[0]

    stacking = data[tr1:tr2, :].mean(axis=0, keepdims=True)
    data = np.subtract(data, stacking)

    return data


# def medfilt_cpu(data, kernel_size=3):
#     out = scipy.signal.medfilt2d(data, kernel_size)
#     return out.astype(data.dtype)


# def medfilt_cuda(data, kernel_size=3):
#     out = cupyx.scipy.signal.medfilt2d(data, kernel_size)
#     return out.astype(data.dtype)


def lowpass_cheby_2_cpu(data, freq, df, maxorder=12, ba=False, freq_passband=False):
    nyquist = df * 0.5
    # rp - maximum ripple of passband, rs - attenuation of stopband
    rp, rs, order = 1, 96, 1e99
    ws = freq / nyquist  # stop band frequency
    wp = ws  # pass band frequency
    # raise for some bad scenarios
    if ws > 1:
        ws = 1.0
        msg = (
            "Selected corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    while True:
        if order <= maxorder:
            break
        wp = wp * 0.99
        order, wn = scipy.signal.cheb2ord(wp, ws, rp, rs, analog=0)
    if ba:
        out = scipy.signal.cheby2(order, rs, wn, btype="low", analog=0, output="ba")
        return out.astype(data.dtype)
    sos = scipy.signal.cheby2(order, rs, wn, btype="low", analog=0, output="sos")
    if freq_passband:
        out = scipy.signal.sosfilt(sos, data, axis=1), wp * nyquist
        return out.astype(data.dtype)
    out = scipy.signal.sosfilt(sos, data, axis=1)
    return out.astype(data.dtype)


def lowpass_cheby_2_cuda(data, freq, df, maxorder=12, ba=False, freq_passband=False):
    nyquist = df * 0.5
    # rp - maximum ripple of passband, rs - attenuation of stopband
    rp, rs, order = 1, 96, 1e99
    ws = freq / nyquist  # stop band frequency
    wp = ws  # pass band frequency
    # raise for some bad scenarios
    if ws > 1:
        ws = 1.0
        msg = (
            "Selected corner frequency is above Nyquist. "
            + "Setting Nyquist as high corner."
        )
        warnings.warn(msg)
    while True:
        if order <= maxorder:
            break
        wp = wp * 0.99
        order, wn = cupyx.scipy.signal.cheb2ord(wp, ws, rp, rs, analog=0)
    if ba:
        out = cupyx.scipy.signal.cheby2(
            order, rs, wn, btype="low", analog=0, output="ba"
        )
        return out.astype(data.dtype)
    sos = cupyx.scipy.signal.cheby2(order, rs, wn, btype="low", analog=0, output="sos")
    if freq_passband:
        out = cupyx.scipy.signal.sosfilt(sos, data, axis=1), wp * nyquist
        return out.astype(data.dtype)
    out = cupyx.scipy.signal.sosfilt(sos, data, axis=1)
    return out.astype(data.dtype)
