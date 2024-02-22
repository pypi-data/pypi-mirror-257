import datetime

import itables
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import pandas as pd
from matplotlib.patches import Rectangle
from obspy import UTCDateTime

from shakecore.core.stream import Stream
from shakecore.setting import TABLE_STYLES
from shakecore.viz.utils.viz_tools import (
    _format_time_axis,
    _get_ax,
    _get_cmap,
    cmap_gaps,
)


def _get_trace_start_end(t_start, t_end, trace_num, trace_info):
    trace_start = 0
    trace_end = trace_start + trace_num

    if len(trace_info) == 0:
        return trace_start, trace_end
    else:
        # Initialize a list to store the overlapping intervals
        overlapping_intervals = []
        trace_info = sorted(trace_info, key=lambda x: x[0])
        for interval in trace_info:
            if not (interval[1] <= t_start or interval[0] >= t_end):
                overlapping_intervals.append(interval)

        overlapping_intervals = sorted(overlapping_intervals, key=lambda x: x[2])
        for interval in overlapping_intervals:
            if not (interval[3] <= trace_start or interval[2] >= trace_end):
                trace_start = interval[3]
                trace_end = trace_start + trace_num

        return trace_start, trace_end


@property
def table(self):
    """_summary_"""
    info = []
    for i, stream in enumerate(self.streams):
        stats = stream.stats
        # set starttime and endtime
        starttime = str(stats.starttime)
        endtime = str(stats.endtime)
        # set duration
        d_time = datetime.timedelta(seconds=stats.endtime - stats.starttime)
        microseconds = d_time.microseconds
        d_time = d_time - datetime.timedelta(microseconds=microseconds)
        duration = f"{d_time.days} days<br>{(datetime.datetime.min + d_time).strftime('%H:%M:%S')}.{microseconds:06}"
        # set processing
        processing = "<br/>".join(
            [f"{[i+1]}: {s}" for i, s in enumerate(stats.processing)]
        )
        info.append(
            [
                f"S{i}",
                starttime[:10] + "<br>" + starttime[11:-1],
                endtime[:10] + "<br>" + endtime[11:-1],
                duration,
                stats.sampling_rate,
                stats.delta,
                stats.interval,
                stats.npts,
                stats.trace_num,
                stats.type,
                np.ma.isMaskedArray(stream.data),
                stream.id,
                stats.notes,
                processing,
            ]
        )

    table = pd.DataFrame(
        info,
        columns=[
            "index",
            "starttime",
            "endtime",
            "duration",
            "sampling_rate",
            "delta",
            "interval",
            "npts",
            "trace_num",
            "type",
            "data_masked",
            "id",
            "notes",
            "processing",
        ],
    )
    return table


def show(
    self,
    mode="table",
    show_masked=False,
    cmap=cmap_gaps,
    time_axis="x",
    invert_x=False,
    invert_y=False,
    time_minticks=5,
    time_maxticks=None,
    timetick_rotation=0,
    timetick_labelsize=10,
    text_labelsize=16,
    axis_labelsize=16,
    ax=None,
    figsize=(10, 5),
    show=True,
    save_path=None,
    dpi=100,
):
    if mode == "table":
        # ----- [widgets version] departed -----#
        # from ipywidgets import widgets
        # if rows is None:
        #     return self.table.style.set_table_styles(TABLE_STYLES)
        # else:
        #     self.rows = rows
        #     num_pages = int(np.ceil(len(self.streams) / rows))
        #     widgets.interact(self._show_page, page=(1, num_pages))
        # ----- [itables version] -----#
        return itables.show(self.table)

    elif mode == "figure":
        ax = self._show_figure(
            show_masked=show_masked,
            cmap=cmap,
            time_axis=time_axis,
            invert_x=invert_x,
            invert_y=invert_y,
            time_minticks=time_minticks,
            time_maxticks=time_maxticks,
            timetick_rotation=timetick_rotation,
            timetick_labelsize=timetick_labelsize,
            text_labelsize=text_labelsize,
            axis_labelsize=axis_labelsize,
            ax=ax,
            figsize=figsize,
            show=show,
            save_path=save_path,
            dpi=dpi,
        )
        return ax
    else:
        raise ValueError("mode must be 'table' or 'figure'")


# ----- [widgets version] departed -----#
# def _show_page(self, page=1):
#     start = (page - 1) * self.rows
#     end = start + self.rows
#     return self.table.iloc[start:end].style.set_table_styles(TABLE_STYLES)


def _show_figure(
    self,
    show_masked,
    cmap,
    time_axis,
    invert_x,
    invert_y,
    time_minticks,
    time_maxticks,
    timetick_rotation,
    timetick_labelsize,
    text_labelsize,
    axis_labelsize,
    ax,
    figsize,
    show,
    save_path,
    dpi,
):
    # set axis
    ax = _get_ax(ax, figsize=figsize)
    if cmap is None:
        cmap = cmap_gaps

    trace_info = []
    for i, stream in enumerate(self.streams):
        # set data
        if show_masked:
            facecolor = "none"
            data = stream.data
            if ma.isMaskedArray(data):
                mask = ma.getmask(data)
                data = np.where(mask, 0, 1)
            else:
                data = np.ones_like(data)
            if time_axis == "x":
                data = data
            elif time_axis == "y":
                data = data.T
            else:
                raise ValueError("time_axis must be 'x' or 'y'")
        else:
            facecolor = (0.92, 0.92, 0.92)

        # set times
        t_start = stream.stats.starttime.datetime
        t_end = stream.stats.endtime.datetime
        trace_start, trace_end = _get_trace_start_end(
            t_start, t_end, stream.stats.trace_num, trace_info
        )
        trace_info.append([t_start, t_end, trace_start, trace_end])

        # set text and box
        if time_axis == "x":
            # trace_axis = "y"
            extents = [t_start, t_end, trace_start, trace_end]
            x_center = datetime.datetime.fromtimestamp(
                (t_start.timestamp() + t_end.timestamp()) / 2
            )
            y_center = (trace_end + trace_start) / 2
            border = Rectangle(
                (t_start, trace_start),
                datetime.timedelta(seconds=(t_end - t_start).total_seconds()),
                trace_end - trace_start,
                edgecolor=(0.2, 0.2, 0.2),
                facecolor=facecolor,
                linewidth=0.5,
            )
        elif time_axis == "y":
            # trace_axis = "x"
            extents = [trace_start, trace_end, t_start, t_end]
            x_center = (trace_end + trace_start) / 2
            y_center = datetime.datetime.fromtimestamp(
                (t_start.timestamp() + t_end.timestamp()) / 2
            )
            border = Rectangle(
                (trace_start, t_start),
                trace_end - trace_start,
                datetime.timedelta(seconds=(t_end - t_start).total_seconds()),
                edgecolor=(0.1, 0.1, 0.1),
                facecolor=facecolor,
                linewidth=0.5,
            )
        else:
            raise ValueError("time_axis must be 'x' or 'y'")

        # plot
        if show_masked:
            cmap = _get_cmap(cmap)
            ax.imshow(
                data,
                extent=extents,
                vmin=0,
                vmax=1,
                aspect="auto",
                cmap=cmap,
                origin="lower",
            )
        ax.add_patch(border)
        ax.text(
            x_center,
            y_center,
            f"S{i}",
            color="black",
            ha="center",
            va="center",
            fontsize=text_labelsize,
        )

    # format
    _format_time_axis(
        ax,
        axis=time_axis,
        tick_rotation=timetick_rotation,
        minticks=time_minticks,
        maxticks=time_maxticks,
        labelsize=timetick_labelsize,
    )
    time_min = min([interval[0] for interval in trace_info])
    time_max = max([interval[1] for interval in trace_info])
    trace_min = min([interval[2] for interval in trace_info])
    trace_max = max([interval[3] for interval in trace_info])
    fig = ax.figure
    if time_axis == "x":
        ax.set_yticks([])
        ax.set_xlim(time_min, time_max)
        ax.set_ylim(trace_min, trace_max)
        ax.set_ylabel("streams", fontsize=axis_labelsize)
    elif time_axis == "y":
        ax.set_xticks([])
        ax.set_xlim(trace_min, trace_max)
        ax.set_ylim(time_min, time_max)
        ax.set_xlabel("streams", fontsize=axis_labelsize)
    if invert_x:
        ax.invert_xaxis()
    if invert_y:
        ax.invert_yaxis()
    if show:
        plt.show()
    else:
        plt.close(fig)
    if save_path is not None:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
    else:
        return ax


def append(self, stream):
    """
    Append a single Trace object to the current Stream object.

    """
    if isinstance(stream, Stream):
        self.streams.append(stream)
    else:
        msg = "Append only supports a single Stream object as an argument."
        raise TypeError(msg)
    return self


def extend(self, stream_list):
    """
    Extend the current Stream object with a list of Trace objects.

    :param trace_list: list of :class:`~obspy.core.trace.Trace` objects or
        :class:`~obspy.core.stream.Stream`.

    .. rubric:: Example

    >>> from obspy import read, Trace
    >>> st = read()
    >>> tr1 = Trace()
    >>> tr1.stats.station = 'TEST1'
    >>> tr2 = Trace()
    >>> tr2.stats.station = 'TEST2'
    >>> st.extend([tr1, tr2])  # doctest: +ELLIPSIS
    <...Stream object at 0x...>
    >>> print(st)  # doctest: +ELLIPSIS
    5 Trace(s) in Stream:
    BW.RJOB..EHZ | 2009-08-24T00:20:03.000000Z ... | 100.0 Hz, 3000 samples
    BW.RJOB..EHN | 2009-08-24T00:20:03.000000Z ... | 100.0 Hz, 3000 samples
    BW.RJOB..EHE | 2009-08-24T00:20:03.000000Z ... | 100.0 Hz, 3000 samples
    .TEST1..     | 1970-01-01T00:00:00.000000Z ... | 1.0 Hz, 0 samples
    .TEST2..     | 1970-01-01T00:00:00.000000Z ... | 1.0 Hz, 0 samples
    """
    if isinstance(stream_list, list):
        for _i in stream_list:
            # Make sure each item in the list is a stream.
            if not isinstance(_i, Stream):
                msg = "Extend only accepts a list of Trace objects."
                raise TypeError(msg)
        self.streams.extend(stream_list)
    elif isinstance(stream_list, type(self)):
        self.streams.extend(stream_list.streams)
    else:
        msg = "Extend only supports a list of Stream objects as argument."
        raise TypeError(msg)
    return self


def delete(self, index=[]):
    # sort index
    index = sorted(index)

    # delete
    for i in range(0, len(index)):
        del self.streams[index[i] - i]
    return self


def select(
    self,
    stream=[None, None],
    time=[None, None],
    network="",
    station="",
    channel="",
    latitude=[None, None],
    longitude=[None, None],
    elevation=[None, None],
):
    # copy
    pool = self.copy()

    # stream
    if (stream[0] is not None) or (stream[1] is not None):
        index = []
        min_stream = stream[0] or 0
        max_stream = stream[1] or len(pool.streams)
        for i in range(0, len(pool.streams)):
            if i < min_stream or i > max_stream:
                index.append(i)
        print(index)
        pool.delete(index)

    # time
    if (time[0] is not None) or (time[1] is not None):
        for stream in pool.streams:
            t_min = time[0] or UTCDateTime(0)
            t_max = time[1] or UTCDateTime("9999-12-31T23:59:59")
            if stream.stats.starttime >= t_min and stream.stats.starttime <= t_max:
                stream.select(
                    network=network,
                    station=station,
                    channel=channel,
                    latitude=latitude,
                    longitude=longitude,
                    elevation=elevation,
                )
    else:
        for stream in pool.streams:
            stream.select(
                network=network,
                station=station,
                channel=channel,
                latitude=latitude,
                longitude=longitude,
                elevation=elevation,
            )

    return pool


def trim(
    self,
    starttime=None,
    endtime=None,
    pad=False,
    nearest_sample=True,
    fill_value=None,
):
    for stream in self.streams:
        stream.trim(
            starttime=starttime,
            endtime=endtime,
            pad=pad,
            nearest_sample=nearest_sample,
            fill_value=fill_value,
        )


def sort(
    self,
    keys=["type", "starttime", "sampling_rate", "interval", "trace_num", "npts"],
    reverse=False,
):
    """
    Sort the stream by the given keys.

    :param keys: list of keys to sort by
    :type keys: list of str
    """
    # Loop over all keys in reversed order.
    for _i in keys[::-1]:
        self.streams.sort(key=lambda x: x.stats[_i], reverse=reverse)
    return self


def aligntime(self, method="nearest_sample"):
    """
    Align the starttime of all traces in the stream.

    :param starttime: starttime to align to
    :type starttime: :class:`~obspy.core.utcdatetime.UTCDateTime`
    :param method: Method to use for alignment. Options are
        ``"nearest_sample"``, ``"zero_phase"``, ``"first_sample"``,
        ``"last_sample"``. Default is ``"nearest_sample"``.
    :type method: str
    """
    for stream in self.streams:
        stream.aligntime(method=method)


def merge(
    self,
    axis="time",
    method=0,
    interpolation_samples=0,
    fill_value=None,
):
    if axis == "time":
        self.sort(keys=["starttime"])
        # check starttime
        for i in range(0, len(self.streams) - 1):
            if self[i].stats.starttime == self[i + 1].stats.starttime:
                raise TypeError(
                    "Stream starttime must be different: %s vs %s"
                    % (self[i].stats.starttime, self[i + 1].stats.starttime)
                )
        out = self.streams[0].copy()
        for stream in self.streams[1:]:
            out = out.__add__(
                stream, method, interpolation_samples, fill_value, sanity_checks=True
            )
        return out
    elif axis == "trace":
        out = self.streams[0].copy()
        for stream in self.streams[1:]:
            out.extend(stream)
        return out
    else:
        raise ValueError("axis must be 'time' or 'trace'")
