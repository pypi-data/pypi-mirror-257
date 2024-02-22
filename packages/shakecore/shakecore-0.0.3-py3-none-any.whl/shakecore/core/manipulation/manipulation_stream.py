import copy
import datetime
import fnmatch
import hashlib
import math
import warnings

import itables
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import pandas as pd
from ipywidgets import widgets
from matplotlib.patches import Rectangle
from obspy import UTCDateTime

from shakecore.core.stats import Stats
from shakecore.core.utils import create_empty_data_chunk
from shakecore.setting import MAX_PROCESSING_INFO, TABLE_STYLES
from shakecore.viz.utils.viz_tools import (
    _format_time_axis,
    _format_trace_axis,
    _get_ax,
    _get_cmap,
    cmap_gaps,
)


def _internal_add_processing_info(self, info):
    """
    Add the given informational string to the `processing` field in the
    trace's :class:`~obspy.core.trace.Stats` object.
    """
    proc = self.stats.setdefault("processing", [])
    if len(proc) == MAX_PROCESSING_INFO - 1:
        msg = (
            "List of processing information in Stream.stats.processing "
            "reached maximal length of {} entries."
        )
        warnings.warn(msg.format(MAX_PROCESSING_INFO))
    if len(proc) < MAX_PROCESSING_INFO:
        proc.append(info)


@property
def id(self):
    """
    Return a unique identifier for the trace.

    The id is a hash of the header attributes.
    """
    info = (
        str(self.stats.network)
        + str(self.stats.station)
        + str(self.stats.channel)
        + str(self.stats.latitude)
        + str(self.stats.longitude)
        + str(self.stats.elevation)
    )
    hash_id = hashlib.sha256(info.encode()).hexdigest()
    return hash_id


@property
def table(self):
    """_summary_"""
    table = pd.DataFrame(
        {
            "trace": [f"T{i}" for i in range(self.stats.trace_num)],
            "network": self.stats.network,
            "station": self.stats.station,
            "channel": self.stats.channel,
            "latitude": self.stats.latitude,
            "longitude": self.stats.longitude,
            "elevation": self.stats.elevation,
        }
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
    trace_ticks=5,
    tracetick_rotation=0,
    tracetick_labelsize=10,
    axis_labelsize=16,
    ax=None,
    figsize=(10, 5),
    show=True,
    save_path=None,
    dpi=100,
):
    if mode == "table":
        # ----- [widgets version] departed -----#
        # if rows is None:
        #     return self.table.style.set_table_styles(TABLE_STYLES)
        # else:
        #     self.rows = rows
        #     num_pages = int(np.ceil(self.stats.trace_num / rows))
        #     widgets.interact(self._show_table, page=(1, num_pages))
        # ----- [itables version] -----#
        return itables.show(self.table)
    elif mode == "figure":
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        self._show_figure(
            show_masked=show_masked,
            cmap=cmap,
            time_axis=time_axis,
            invert_x=invert_x,
            invert_y=invert_y,
            time_minticks=time_minticks,
            time_maxticks=time_maxticks,
            timetick_rotation=timetick_rotation,
            timetick_labelsize=timetick_labelsize,
            trace_ticks=trace_ticks,
            tracetick_rotation=tracetick_rotation,
            tracetick_labelsize=tracetick_labelsize,
            axis_labelsize=axis_labelsize,
            ax=ax,
            figsize=figsize,
            show=show,
            save_path=save_path,
            dpi=dpi,
        )
    else:
        raise ValueError("mode must be 'table' or 'figure'")


# ----- [widgets version] departed -----#
# def _show_table(self, page=1):
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
    trace_ticks,
    tracetick_rotation,
    tracetick_labelsize,
    axis_labelsize,
    ax,
    figsize,
    show,
    save_path,
    dpi,
):
    # get ax
    ax = _get_ax(ax, figsize=figsize)
    if cmap is None:
        cmap = cmap_gaps

    # set data
    if show_masked:
        facecolor = "none"
        data = self.data
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
    t_start = self.stats.starttime.datetime
    t_end = self.stats.endtime.datetime
    trace_start = 0
    trace_end = self.stats.trace_num

    # set box
    if time_axis == "x":
        trace_axis = "y"
        extents = [t_start, t_end, trace_start, trace_end]
        border = Rectangle(
            (t_start, trace_start),
            datetime.timedelta(seconds=(t_end - t_start).total_seconds()),
            trace_end - trace_start,
            edgecolor=(0.2, 0.2, 0.2),
            facecolor=facecolor,
            linewidth=0.5,
        )
    elif time_axis == "y":
        trace_axis = "x"
        extents = [trace_start, trace_end, t_start, t_end]
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

    # set ticks
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
        trace_label="trace",
        self=self,
        starttrace=trace_start,
        endtrace=trace_end,
        trace_ticks=trace_ticks,
        trace_axis=trace_axis,
        tracetick_rotation=tracetick_rotation,
        tracetick_labelsize=tracetick_labelsize,
    )
    fig = ax.figure
    if time_axis == "x":
        ax.set_xlim(t_start, t_end)
        ax.set_ylim(trace_start, trace_end)
        ax.set_ylabel("Traces", fontsize=axis_labelsize)
    elif time_axis == "y":
        ax.set_xlim(trace_start, trace_end)
        ax.set_ylim(t_start, t_end)
        ax.set_xlabel("Traces", fontsize=axis_labelsize)
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
    return ax


def times(self, type="relative", reftime=None):
    type = type.lower()
    time_array = np.arange(self.stats.npts)
    time_array = time_array / self.stats.sampling_rate

    if type == "relative":
        if reftime is not None:
            time_array += self.stats.starttime - reftime
    elif type == "timestamp":
        time_array = time_array + self.stats.starttime.timestamp
    elif type == "utcdatetime":
        time_array = np.vectorize(
            lambda t: self.stats.starttime + t, otypes=[UTCDateTime]
        )(time_array)
    elif type == "datetime":
        time_deltas_ns = (time_array * 1e9).astype(np.int64)
        time_deltas_timedelta64 = time_deltas_ns * np.timedelta64(1, "ns")
        datetime_array = (
            np.datetime64(self.stats.starttime.datetime) + time_deltas_timedelta64
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            time_array = pd.Series(datetime_array).dt.to_pydatetime()
            time_array = np.array(time_array)
    else:
        msg = "Invalid `type`: {}".format(type)
        raise ValueError(msg)

    return time_array


def add(
    self,
    stream,
    method=0,
    interpolation_samples=0,
    fill_value=None,
    sanity_checks=True,
):
    out = self.__add__(stream, method, interpolation_samples, fill_value, sanity_checks)

    return out


def extend(self, stream):
    """
    Extend the current Stream with the given Stream object.

    :param Stream: Stream object to extend the current Stream object with.
    :type Stream: :class:`~obspy.core.stream.Stream`

    .. rubric:: Example

    >>> from obspy import read
    >>> st = read()
    >>> st.extend(st)
    >>> len(st)
    2
    """
    # check if other object is a Stream
    if not isinstance(stream, type(self)):
        raise TypeError("Can only extend Stream with another Stream object.")
    # check starttime
    if self.stats.starttime != stream.stats.starttime:
        raise TypeError(
            "Starttime differs: %s vs %s"
            % (self.stats.starttime, stream.stats.starttime)
        )
    # check endtime
    if self.stats.endtime != stream.stats.endtime:
        raise TypeError(
            "Endtime differs: %s vs %s" % (self.stats.endtime, stream.stats.endtime)
        )
    #  check sample rate
    if self.stats.sampling_rate != stream.stats.sampling_rate:
        raise TypeError(
            "Sampling rate differs: %s vs %s"
            % (self.stats.sampling_rate, stream.stats.sampling_rate)
        )
    # check npts
    if self.stats.npts != stream.stats.npts:
        raise TypeError(
            "Number of samples differs: %s vs %s" % (self.stats.npts, stream.stats.npts)
        )
    # check type
    if self.stats.type != stream.stats.type:
        raise TypeError("Type differs: %s vs %s" % (self.stats.type, stream.stats.type))
    # check data type
    if self.data.dtype != stream.data.dtype:
        raise TypeError(
            "Data type differs: %s vs %s" % (self.data.dtype, stream.data.dtype)
        )
    # extend data
    self.data = np.concatenate([self.data, stream.data], axis=0)
    # extend stats
    self.stats.network.extend(stream.stats.network)
    self.stats.station.extend(stream.stats.station)
    self.stats.channel.extend(stream.stats.channel)
    self.stats.latitude.extend(stream.stats.latitude)
    self.stats.longitude.extend(stream.stats.longitude)
    self.stats.elevation.extend(stream.stats.elevation)
    # clear notes
    self.stats.notes = {}


def delete(self, index=[]):
    """
    Pop a trace from the Stream object.

    :param index: Index of trace to pop.
    :type index: int
    :returns: Popped trace.
    :rtype: :class:`~obspy.core.trace.Trace`

    .. rubric:: Example

    >>> from obspy import read
    >>> st = read()
    >>> tr = st.pop(0)
    >>> len(st)
    2
    """
    # check if trace is valid
    if len(index) > 0:
        trace_num = self.stats.trace_num
        if index[0] >= trace_num or index[-1] < 0:
            raise IndexError("Trace index out of range.")
        # delete stats
        attributes = [
            "network",
            "station",
            "channel",
            "latitude",
            "longitude",
            "elevation",
        ]
        for attr in attributes:
            original_list = getattr(self.stats, attr)
            new_list = [original_list[i] for i in range(trace_num) if i not in index]
            setattr(self.stats, attr, new_list)
        # delete data
        self.data = np.delete(self.data, np.array(index), axis=0)


def _ltrim(self, starttime, pad=False, nearest_sample=True, fill_value=None):
    org_dtype = self.data.dtype
    if isinstance(starttime, float) or isinstance(starttime, int):
        starttime = UTCDateTime(self.stats.starttime) + starttime
    elif not isinstance(starttime, UTCDateTime):
        raise TypeError
    # check if in boundary
    if nearest_sample:
        delta = round((starttime - self.stats.starttime) * self.stats.sampling_rate)
        if delta < 0 and pad:
            npts = abs(delta) + 10  # use this as a start
            newstarttime = self.stats.starttime - npts / float(self.stats.sampling_rate)
            newdelta = round((starttime - newstarttime) * self.stats.sampling_rate)
            delta = newdelta - npts
        delta = int(delta)
    else:
        delta = -1 * int(
            math.floor(
                round(
                    (self.stats.starttime - starttime) * self.stats.sampling_rate,
                    7,
                )
            )
        )
    # Adjust starttime only if delta is greater than zero or if the values
    # are padded with masked arrays.
    if delta > 0 or pad:
        self.stats.starttime += delta * self.stats.delta
    if delta == 0 or (delta < 0 and not pad):
        return self
    elif delta < 0 and pad:
        try:
            gap = create_empty_data_chunk(
                self.stats.trace_num, abs(delta), self.data.dtype, fill_value
            )
        except ValueError:
            # create_empty_data_chunk returns negative ValueError ?? for
            # too large number of points, e.g. 189336539799
            raise Exception(
                "Time offset between starttime and " "Stream.starttime too large"
            )
        self.data = np.ma.concatenate((gap, self.data), axis=1)
        return self
    elif starttime > self.stats.endtime:
        self.data = np.empty((0, 0), dtype=org_dtype)
        return self
    elif delta > 0:
        try:
            self.data = self.data[:, delta:]
        except IndexError:
            # a huge numbers for delta raises an IndexError
            # here we just create empty array with same dtype
            self.data = np.empty((0, 0), dtype=org_dtype)
    return self


def _rtrim(self, endtime, pad=False, nearest_sample=True, fill_value=None):
    org_dtype = self.data.dtype
    if isinstance(endtime, float) or isinstance(endtime, int):
        endtime = UTCDateTime(self.stats.endtime) - endtime
    elif not isinstance(endtime, UTCDateTime):
        raise TypeError
    # check if in boundary
    if nearest_sample:
        delta = (
            round((endtime - self.stats.starttime) * self.stats.sampling_rate)
            - self.stats.npts
            + 1
        )
        delta = int(delta)
    else:
        # solution for #127, however some tests need to be changed
        # delta = -1*int(math.floor(compatibility.round_away(
        #     (self.stats.endtime - endtime) * \
        #     self.stats.sampling_rate, 7)))
        delta = int(
            math.floor(
                round((endtime - self.stats.endtime) * self.stats.sampling_rate, 7)
            )
        )
    if delta == 0 or (delta > 0 and not pad):
        return self
    if delta > 0 and pad:
        try:
            gap = create_empty_data_chunk(
                self.stats.trace_num, delta, self.data.dtype, fill_value
            )
        except ValueError:
            # create_empty_data_chunk returns negative ValueError ?? for
            # too large number of points, e.g. 189336539799
            raise Exception(
                "Time offset between starttime and " + "Stream.starttime too large"
            )
        self.data = np.ma.concatenate((self.data, gap), axis=1)
        return self
    elif endtime < self.stats.starttime:
        self.stats.starttime = self.stats.endtime + delta * self.stats.delta
        self.data = np.empty((0, 0), dtype=org_dtype)
        return self
    # cut from right
    delta = abs(delta)
    total = self.data.shape[1] - delta
    if endtime == self.stats.starttime:
        total = 1
    self.data = self.data[:, :total]
    return self


def trim(
    self,
    starttime=None,
    endtime=None,
    pad=False,
    nearest_sample=True,
    fill_value=None,
):
    # check time order and swap eventually
    if (
        isinstance(starttime, UTCDateTime)
        and isinstance(endtime, UTCDateTime)
        and starttime > endtime
    ):
        raise ValueError("startime is larger than endtime")
    # cut it
    if starttime:
        self._ltrim(
            starttime, pad, nearest_sample=nearest_sample, fill_value=fill_value
        )
    if endtime:
        self._rtrim(endtime, pad, nearest_sample=nearest_sample, fill_value=fill_value)
    # if pad=True and fill_value is given convert to NumPy ndarray
    if pad is True and fill_value is not None:
        try:
            self.data = self.data.filled()
        except AttributeError:
            # numpy.ndarray object has no attribute 'filled' - ignoring
            pass


def select(
    self,
    trace=[None, None],
    network="",
    station="",
    channel="",
    latitude=[None, None],
    longitude=[None, None],
    elevation=[None, None],
):
    # copy
    stream = self.copy()
    # trace
    if (trace[0] is not None) or (trace[1] is not None):
        index = []
        min_trace = trace[0] or 0
        max_trace = trace[1] or stream.stats.trace_num
        for i in range(0, stream.stats.trace_num):
            if i < min_trace or i > max_trace:
                index.append(i)
        stream.delete(index)
    # network
    if network != "":
        index = []
        for i in range(0, stream.stats.trace_num):
            if not fnmatch.fnmatch(stream.stats.network[i], network):
                index.append(i)
        stream.delete(index)
    # station
    if station != "":
        index = []
        for i in range(0, stream.stats.trace_num):
            if not fnmatch.fnmatch(stream.stats.station[i], station):
                index.append(i)
        stream.delete(index)
    # channel
    if channel != "":
        index = []
        for i in range(0, stream.stats.trace_num):
            if not fnmatch.fnmatch(stream.stats.channel[i], channel):
                index.append(i)
        stream.delete(index)
    # latitude
    if (latitude[0] is not None) or (latitude[1] is not None):
        index = []
        lat_min = latitude[0] or -90
        lat_max = latitude[1] or 90
        for i in range(0, stream.stats.trace_num):
            if type(stream.stats.latitude[i]) == str:
                index.append(i)
            elif (
                stream.stats.latitude[i] < lat_min or stream.stats.latitude[i] > lat_max
            ):
                index.append(i)
        stream.delete(index)
    # longitude
    if (longitude[0] is not None) or (longitude[1] is not None):
        index = []
        lon_min = longitude[0] or -180
        lon_max = longitude[1] or 180
        for i in range(0, stream.stats.trace_num):
            if type(stream.stats.longitude[i]) == str:
                index.append(i)
            elif (
                stream.stats.longitude[i] < lon_min
                or stream.stats.longitude[i] > lon_max
            ):
                index.append(i)
        stream.delete(index)
    # elevation
    if (elevation[0] is not None) or (elevation[1] is not None):
        index = []
        ele_min = elevation[0] or -1e20
        ele_max = elevation[1] or 1e20
        for i in range(0, stream.stats.trace_num):
            if type(stream.stats.elevation[i]) == str:
                index.append(i)
            elif (
                stream.stats.elevation[i] < ele_min
                or stream.stats.elevation[i] > ele_max
            ):
                index.append(i)
        stream.delete(index)

    # delete processing info in stats
    stream.stats["processing"] = []

    return stream


def sort(
    self,
    keys=["network", "station", "channel", "latitude", "longitude", "elevation"],
    reverse=False,
):
    # check if list
    default_keys = [
        "network",
        "station",
        "channel",
        "latitude",
        "longitude",
        "elevation",
    ]

    msg = "keys must be a list of strings."
    if not isinstance(keys, list):
        raise TypeError(msg)

    # Loop over all keys in reversed order.
    key_list = []
    for _i in keys[::-1]:
        key_list.append(self.stats[_i])
    indexs = np.array(key_list)

    for i in range(0, len(keys)):
        if reverse:
            sort_order = np.argsort(indexs[i, :])[::-1]
        else:
            sort_order = np.argsort(indexs[i, :])
        indexs = indexs[:, sort_order]
        self.data = self.data[sort_order, :]
        for j in range(0, len(default_keys)):
            self.stats[default_keys[j]] = [
                self.stats[default_keys[j]][k] for k in sort_order
            ]

    return self


def split(self, n=2):
    from shakecore.core.pool import Pool

    # check n
    if n > self.stats.trace_num:
        raise ValueError("n must be smaller than the number of traces.")
    # split data
    data = np.array_split(self.data, n, axis=0)
    split_positions = np.cumsum([subarray.shape[0] for subarray in data])
    split_positions = np.insert(split_positions, 0, 0)
    # split stats
    base_stats = Stats(
        header={
            "starttime": self.stats.starttime,
            "sampling_rate": self.stats.sampling_rate,
            "delta": self.stats.delta,
            "type": self.stats.type,
        }
    )
    stats = [base_stats.copy() for _ in range(n)]
    for i in range(0, n):
        stats[i].network = self.stats.network[
            split_positions[i] : split_positions[i + 1]
        ]
        stats[i].station = self.stats.station[
            split_positions[i] : split_positions[i + 1]
        ]
        stats[i].channel = self.stats.channel[
            split_positions[i] : split_positions[i + 1]
        ]
        stats[i].latitude = self.stats.latitude[
            split_positions[i] : split_positions[i + 1]
        ]
        stats[i].longitude = self.stats.longitude[
            split_positions[i] : split_positions[i + 1]
        ]
        stats[i].elevation = self.stats.elevation[
            split_positions[i] : split_positions[i + 1]
        ]
    # create new streams
    streams = []
    for i in range(0, n):
        streams.append(self.__class__(data[i], header=stats[i]))
    return Pool(streams)


def slide(self, n=2):
    from shakecore.core.pool import Pool

    # check n
    if n > self.stats.npts:
        raise ValueError("n must be smaller than the number of samples.")
    # slide data
    data = np.array_split(self.data, n, axis=1)
    split_positions = np.cumsum([subarray.shape[1] for subarray in data])
    split_positions = np.insert(split_positions, 0, 0)
    stats = [self.stats.copy() for _ in range(n)]
    for i in range(0, n):
        stats[i].starttime = (
            self.stats.starttime + (split_positions[i]) * self.stats.delta
        )
        stats[i].processing = []
    # create new streams
    streams = []
    for i in range(0, n):
        streams.append(self.__class__(data[i], header=stats[i]))
    return Pool(streams)


def aligntime(self, method="nearest_sample"):
    # should be token place by interpolate and resample
    if method == "nearest_sample":
        self.stats.starttime = (
            UTCDateTime(0)
            + round((self.stats.starttime - UTCDateTime(0)) * self.stats.sampling_rate)
            / self.stats.sampling_rate
        )
    else:
        raise ValueError("method must be 'nearest_sample'.")
