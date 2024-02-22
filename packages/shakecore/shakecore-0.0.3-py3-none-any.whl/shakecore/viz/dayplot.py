import math
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import date2num

from .utils.viz_tools import _format_time_axis, _get_ax


def dayplot(
    self,
    trace=0,
    interval=60 * 30,
    starttime=None,
    endtime=None,
    amp_scale=1,
    time_axis="x",
    invert_x=False,
    invert_y=False,
    time_minticks=5,
    time_maxticks=None,
    timetick_rotation=0,
    timetick_labelsize=10,
    win_minticks=5,
    win_maxticks=None,
    winstick_rotation=0,
    winstick_labelsize=10,
    ax=None,
    color=None,
    linewidth=1,
    linestyle="-",
    alpha=1,
    fillcolors=(None, None),
    fillalpha=0.5,
    grid_color="black",
    grid_linewidth=0.5,
    grid_linestyle=":",
    grid_alpha=1,
    figsize=(10, 5),
    show=True,
    save_path=None,
    dpi=100,
):
    """
    Plot the data in the stream.
    waveform
    wiggles
    """
    # check starttime and endtime
    if starttime is None:
        starttime = self.stats.starttime
    if starttime < self.stats.starttime:
        raise ValueError("starttime must be greater than or equal to stream starttime.")
    if endtime is None:
        endtime = self.stats.endtime
    if endtime > self.stats.endtime:
        raise ValueError("endtime must be less than or equal to stream endtime.")

    # init win_axis
    if time_axis == "x":
        win_axis = "y"
    elif time_axis == "y":
        win_axis = "x"
    else:
        raise ValueError("time_axis must be 'x' or 'y'")

    # set win
    win_num = math.ceil((endtime - starttime) / interval)
    win_npts = int(interval * self.stats.sampling_rate)
    date2num_real_start = date2num(self.stats.starttime.datetime)
    number_interval = 1
    date2num_internal = interval / 86400

    # set time
    npts_times_ns = (1e9 * np.arange(win_npts) / self.stats.sampling_rate).astype(
        np.int64
    )
    time_deltas_timedelta64 = npts_times_ns * np.timedelta64(1, "ns")
    datenpts_times = np.datetime64(starttime.datetime) + time_deltas_timedelta64
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        npts_times = pd.Series(datenpts_times).dt.to_pydatetime()
        npts_times = np.array(npts_times)

    # data normalization
    starttime_npts = int((starttime - self.stats.starttime) * self.stats.sampling_rate)
    endtime_npts = int((endtime - self.stats.starttime) * self.stats.sampling_rate)
    data_1d = self.data[trace, starttime_npts:endtime_npts].copy().flatten()
    data_1d = data_1d / (np.max(np.abs(data_1d)) * 2)
    data = np.full((win_num, win_npts), np.nan)
    data.flat[: data_1d.shape[0]] = data_1d

    # set color
    if color is None:
        color = ["#B2000F", "#004C12", "#847200", "#0E01FF"]
    elif type(color) is str:
        color = [color]

    # set ax
    ax = _get_ax(ax, figsize=figsize)

    # plot data
    for i in range(0, win_num):
        number_real = data[i, :] * amp_scale + i
        date2num_real = (
            date2num_internal * number_real / number_interval + date2num_real_start
        )

        date2num_real_standard = (
            date2num_internal * i / number_interval + date2num_real_start
        )
        if time_axis == "x":
            ax.plot(
                npts_times,
                date2num_real,
                linewidth=linewidth,
                color=color[i % len(color)],
                alpha=alpha,
                linestyle=linestyle,
            )
            if fillcolors[0] is not None:
                ax.fill_between(
                    npts_times,
                    date2num_real,
                    date2num_real_standard,
                    where=date2num_real > date2num_real_standard,
                    facecolor=fillcolors[0],
                    alpha=fillalpha,
                )
            if fillcolors[1] is not None:
                ax.fill_between(
                    npts_times,
                    date2num_real,
                    date2num_real_standard,
                    where=date2num_real < date2num_real_standard,
                    facecolor=fillcolors[1],
                    alpha=fillalpha,
                )
        elif time_axis == "y":
            ax.plot(
                date2num_real,
                npts_times,
                linewidth=linewidth,
                color=color[i % len(color)],
                alpha=alpha,
                linestyle=linestyle,
            )
            if fillcolors[0] is not None:
                ax.fill_betweenx(
                    npts_times,
                    date2num_real,
                    date2num_real_standard,
                    where=date2num_real > date2num_real_standard,
                    facecolor=fillcolors[0],
                    alpha=fillalpha,
                )
            if fillcolors[1] is not None:
                ax.fill_betweenx(
                    npts_times,
                    date2num_real,
                    date2num_real_standard,
                    where=date2num_real < date2num_real_standard,
                    facecolor=fillcolors[1],
                    alpha=fillalpha,
                )
        else:
            raise ValueError("time_axis must be 'x' or 'y'")
    # grid
    ax.grid(
        color=grid_color,
        linewidth=grid_linewidth,
        linestyle=grid_linestyle,
        alpha=grid_alpha,
    )

    # format axis
    _format_time_axis(
        ax,
        axis=time_axis,
        tick_rotation=timetick_rotation,
        minticks=time_minticks,
        maxticks=time_maxticks,
        labelsize=timetick_labelsize,
    )
    _format_time_axis(
        ax,
        axis=win_axis,
        tick_rotation=winstick_rotation,
        minticks=win_minticks,
        maxticks=win_maxticks,
        labelsize=winstick_labelsize,
    )
    fig = ax.figure
    if time_axis == "x":
        ax.set_xlim(npts_times[0], npts_times[-1])
    elif time_axis == "y":
        ax.set_ylim(npts_times[0], npts_times[-1])
    if invert_x:
        ax.invert_xaxis()
    if invert_y:
        ax.invert_yaxis()
    if not show:
        plt.close(fig)
    if save_path is not None:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
    else:
        return ax
