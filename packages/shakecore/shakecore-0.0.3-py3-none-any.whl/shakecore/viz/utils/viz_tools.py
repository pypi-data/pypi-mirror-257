from math import ceil, sqrt

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from geopy.distance import distance
from matplotlib.colors import LinearSegmentedColormap

cmap_gaps = LinearSegmentedColormap.from_list(
    "custom_cmap", [(0, "red"), (1, (0.92, 0.92, 0.92))]
)


def _get_cmap(cmap):
    """Return a color map from a colormap or string."""
    if isinstance(cmap, str):  # get color map if a string was passed
        cmap = plt.get_cmap(cmap)
    return cmap


def _get_ax(ax, figsize=None, **kwargs):
    """Get an axis if ax is None"""
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=figsize, **kwargs)
    return ax


def _format_time_axis(
    ax, axis="x", tick_rotation=0, minticks=5, maxticks=None, labelsize=10
):
    locator = mdates.AutoDateLocator(tz="UTC", minticks=minticks, maxticks=maxticks)
    formatter = mdates.ConciseDateFormatter(locator)
    formatter.formats = [
        "%y",  # ticks are mostly years
        "%b",  # ticks are mostly months
        "%d",  # ticks are mostly days
        "%H:%M",  # hrs
        "%H:%M",  # min
        "%H:%M:%S.%f",
    ]  # secs

    formatter.zero_formats = [
        "",
        "%Y",
        "%b",
        "%b-%d",
        "%H:%M",
        "%H:%M:%S.%f",
    ]

    formatter.offset_formats = [
        "",
        "%Y",
        "%Y-%m",
        "%Y-%m-%d",
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
    ]
    if axis.lower() == "x":
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
    elif axis.lower() == "y":
        ax.yaxis.set_major_locator(locator)
        ax.yaxis.set_major_formatter(formatter)
    ax.tick_params(axis=axis.lower(), rotation=tick_rotation, labelsize=labelsize)


def _format_trace_axis(
    ax,
    trace_label,
    self,
    starttrace,
    endtrace,
    trace_ticks,
    trace_axis,
    tracetick_rotation,
    tracetick_labelsize,
):
    if trace_ticks > (endtrace - starttrace - 1):
        trace_ticks = round(endtrace - starttrace - 1)
    ticks = np.linspace(starttrace, endtrace - 1, num=trace_ticks)

    if trace_label == "trace":
        labels = np.round(
            np.linspace(starttrace, endtrace - 1, num=trace_ticks)
        ).astype(int)
    elif trace_label == "interval":
        interval = self.stats.interval
        labels = (
            np.round(np.linspace(starttrace, endtrace - 1, num=trace_ticks)).astype(int)
            * interval
        )
    elif trace_label == "distance":
        dists = []
        for i in np.floor(
            np.linspace(starttrace, endtrace - 1, num=trace_ticks)
        ).astype(int):
            lat1 = self.stats.latitude[0]
            lon1 = self.stats.longitude[0]
            elev1 = self.stats.elevation[0]
            lat2 = self.stats.latitude[i]
            lon2 = self.stats.longitude[i]
            elev2 = self.stats.elevation[i]
            flat_d = distance((lat1, lon1), (lat2, lon2)).m
            real_d = sqrt(flat_d**2 + (elev2 - elev1) ** 2)
            dists.append(real_d)
        labels = np.array(dists)
    else:
        raise ValueError("trace_label must be 'trace', 'interval', or 'distance'")

    if trace_axis == "x":
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels)
    elif trace_axis == "y":
        ax.set_yticks(ticks)
        ax.set_yticklabels(labels)
    else:
        raise ValueError("trace_axis must be 'x' or 'y'")

    ax.tick_params(
        axis=trace_axis, rotation=tracetick_rotation, labelsize=tracetick_labelsize
    )
