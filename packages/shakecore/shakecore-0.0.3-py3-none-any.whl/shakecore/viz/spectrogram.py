import matplotlib.pyplot as plt
import numpy as np
import scipy
from matplotlib.colors import Normalize

from shakecore.transform import cwt_forward, s_forward

from .utils.viz_tools import _format_time_axis


def spectrogram(
    self,
    method="stft",  # 'stft', 'wavelet', and 'stockwell'
    trace=0,
    starttime=None,
    endtime=None,
    color="black",
    linewidth=1,
    linestyle="-",
    alpha=1,
    fillcolors=(None, None),
    fillalpha=0.5,
    cmap="viridis",  # "jet", "bwr", "seismic", "viridis"
    log=False,
    clip=[0.0, 1.0],
    time_minticks=5,
    time_maxticks=None,
    timetick_rotation=0,
    timetick_labelsize=10,
    figsize=(10, 5),
    show=True,
    save_path=None,
    dpi=100,
    **kwargs,
):
    # check starttime and endtime
    if starttime is None:
        starttime = self.stats.starttime
    if starttime < self.stats.starttime:
        raise ValueError("starttime must be greater than or equal to stream starttime.")
    if endtime is None:
        endtime = self.stats.endtime
    if endtime > self.stats.endtime:
        raise ValueError("endtime must be less than or equal to stream endtime.")

    # times
    starttime_npts = int((starttime - self.stats.starttime) * self.stats.sampling_rate)
    endtime_npts = int((endtime - self.stats.starttime) * self.stats.sampling_rate)
    total_npts_times = self.times(type="datetime")
    npts_times = total_npts_times[starttime_npts:endtime_npts]

    # check data
    data = self.data[trace, starttime_npts:endtime_npts].copy()
    data /= np.max(np.abs(data))

    # set figure
    fig, axs = plt.subplots(
        2, 1, figsize=figsize, sharex="col", gridspec_kw=dict(height_ratios=[2, 3])
    )
    fig.subplots_adjust(hspace=0)

    # plot waveform
    axs[0].plot(
        npts_times,
        data,
        linewidth=linewidth,
        color=color,
        alpha=alpha,
        linestyle=linestyle,
    )
    if fillcolors[0] is not None:
        axs[0].fill_between(
            npts_times,
            data,
            0,
            where=data > 0,
            facecolor=fillcolors[0],
            alpha=fillalpha,
        )
    if fillcolors[1] is not None:
        axs[0].fill_between(
            npts_times,
            data,
            0,
            where=data < 0,
            facecolor=fillcolors[1],
            alpha=fillalpha,
        )

    # signal spectrum
    if method == "stft":
        freqs, times, Sxx = scipy.signal.spectrogram(data, self.stats.sampling_rate)
    elif method == "wavelet":
        wave, scales, freqs, coi, fft, fftfreqs = cwt_forward(
            data, self.stats.delta, **kwargs
        )
        Sxx = np.abs(wave) ** 2
    elif method == "stockwell":
        Sxx, freqs = s_forward(data, self.stats.sampling_rate, **kwargs)
        freqs *= self.stats.sampling_rate
    else:
        raise ValueError("method must be one of 'stft', 'wavelet', or 'stockwell'.")

    # spect times
    npts_times_spect = [
        np.datetime64(starttime.datetime) + np.timedelta64(int(1e9 * ts), "ns")
        for ts in times
    ]

    # log scale
    if log:
        Sxx = 10 * np.log10(Sxx)
    else:
        Sxx = np.sqrt(Sxx)

    # clip
    vmin, vmax = clip
    _range = float(Sxx.max() - Sxx.min())
    vmin = Sxx.min() + vmin * _range
    vmax = Sxx.min() + vmax * _range
    norm = Normalize(vmin, vmax, clip=True)

    # plot spectrogram
    axs[1].pcolormesh(
        npts_times_spect, freqs, Sxx, norm=norm, cmap=cmap, shading="gouraud"
    )

    # format axis
    axs[0].margins(0, 0.1)
    axs[0].set_axis_off()
    axs[1].set_ylabel("Frequency [Hz]")
    axs[1].set_xlim(npts_times[0], npts_times[-1])
    if log:
        axs[1].set_ylim(freqs[1], freqs[-1])  # remove the first element to avoid zero
        axs[1].set_yscale("log")
    _format_time_axis(
        axs[1],
        axis="x",
        tick_rotation=timetick_rotation,
        minticks=time_minticks,
        maxticks=time_maxticks,
        labelsize=timetick_labelsize,
    )

    # show or save
    if not show:
        plt.close(fig)
    if save_path is not None:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
    else:
        return axs[0], axs[1]
