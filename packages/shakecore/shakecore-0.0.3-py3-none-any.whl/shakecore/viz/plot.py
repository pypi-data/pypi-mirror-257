import matplotlib.pyplot as plt
import numpy as np

from .utils.viz_tools import _format_time_axis, _format_trace_axis, _get_ax


def plot(
    self,
    starttime=None,
    endtime=None,
    starttrace=None,
    endtrace=None,
    norm_method="stream",  # trace or stream
    amp_scale=1,
    time_axis="x",
    invert_x=False,
    invert_y=False,
    time_minticks=5,
    time_maxticks=None,
    timetick_rotation=0,
    timetick_labelsize=10,
    trace_ticks=5,
    tracetick_rotation=0,
    tracetick_labelsize=10,
    trace_label="trace",  # 'trace'  "interval", or 'distance'
    ax=None,
    color="black",
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

    # check starttrace and endtrace
    if starttrace is None:
        starttrace = int(0)
    if starttrace < 0:
        raise ValueError("starttrace must be greater than or equal to 0.")
    if endtrace is None:
        endtrace = int(self.stats.trace_num)
    if endtrace > self.stats.trace_num:
        raise ValueError("endtrace must be less than or equal to stream trace_num.")

    # init win_axis
    if time_axis == "x":
        trace_axis = "y"
    elif time_axis == "y":
        trace_axis = "x"
    else:
        raise ValueError("trace_axis must be 'x' or 'y'")

    # check trace_label
    if trace_label not in ["trace", "interval", "distance"]:
        raise ValueError("trace_label must be 'trace', 'interval' or 'distance'")

    # set times
    total_npts_times = self.times(type="datetime")
    starttime_npts = int((starttime - self.stats.starttime) * self.stats.sampling_rate)
    endtime_npts = int((endtime - self.stats.starttime) * self.stats.sampling_rate)
    npts_times = total_npts_times[starttime_npts:endtime_npts]

    # data
    data = self.data[starttrace:endtrace, starttime_npts:endtime_npts].copy()
    if norm_method == "trace":
        data = data / (np.max(np.abs(data), axis=1, keepdims=True) * 2)
    elif norm_method == "stream":
        data = data / (np.max(np.abs(data)) * 2)
    else:
        raise ValueError("norm_method must be 'trace' or 'stream'")

    # set ax
    ax = _get_ax(ax, figsize=figsize)
    # plot data
    for i in range(0, endtrace - starttrace):
        shift = i + starttrace
        if time_axis == "x":
            ax.plot(
                npts_times,
                data[i, :] * amp_scale + shift,
                linewidth=linewidth,
                color=color,
                alpha=alpha,
                linestyle=linestyle,
            )
            if fillcolors[0] is not None:
                ax.fill_between(
                    npts_times,
                    data[i, :] * amp_scale + shift,
                    shift,
                    where=data[i, :] * amp_scale + shift > shift,
                    facecolor=fillcolors[0],
                    alpha=fillalpha,
                )
            if fillcolors[1] is not None:
                ax.fill_between(
                    npts_times,
                    data[i, :] * amp_scale + shift,
                    shift,
                    where=data[i, :] * amp_scale + shift < shift,
                    facecolor=fillcolors[1],
                    alpha=fillalpha,
                )
        elif time_axis == "y":
            ax.plot(
                data[i, :] * amp_scale + shift,
                npts_times,
                linewidth=linewidth,
                color=color,
                alpha=alpha,
                linestyle=linestyle,
            )
            if fillcolors[0] is not None:
                ax.fill_betweenx(
                    npts_times,
                    data[i, :] * amp_scale + shift,
                    shift,
                    where=data[i, :] * amp_scale + shift > shift,
                    facecolor=fillcolors[0],
                    alpha=fillalpha,
                )
            if fillcolors[1] is not None:
                ax.fill_betweenx(
                    npts_times,
                    data[i, :] * amp_scale + shift,
                    shift,
                    where=data[i, :] * amp_scale + shift < shift,
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
    _format_trace_axis(
        ax,
        trace_label,
        self,
        starttrace,
        endtrace,
        trace_ticks,
        trace_axis,
        tracetick_rotation,
        tracetick_labelsize,
    )

    fig = ax.figure
    if time_axis == "x":
        ax.set_xlim(starttime.datetime, endtime.datetime)
        if trace_label == "trace":
            ax.set_ylabel("Trace")
        elif trace_label == "distance":
            ax.set_ylabel("Distance(m)")
        elif trace_label == "interval":
            ax.set_ylabel("Interval(m)")
    elif time_axis == "y":
        ax.set_ylim(starttime.datetime, endtime.datetime)
        if trace_label == "trace":
            ax.set_xlabel("Trace")
        elif trace_label == "distance":
            ax.set_xlabel("Distance(m)")
        elif trace_label == "interval":
            ax.set_xlabel("Interval(m)")
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
