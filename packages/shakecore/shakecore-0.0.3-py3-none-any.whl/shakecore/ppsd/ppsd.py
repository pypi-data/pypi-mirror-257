import pickle
import textwrap
import warnings

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.signal import detrend as scipy_detrend
from scipy.signal import get_window, savgol_filter, welch

from shakecore.setting import MAX_DATA_THRESHOLD
from shakecore.viz.utils.viz_tools import _format_time_axis, _get_ax, _get_cmap


def ppsd_load(filename):
    with open(filename, "rb") as f:
        ppsd = pickle.load(f)

    return ppsd


def ppsd_all_load(filename):
    with open(filename, "rb") as f:
        ppsd_all = pickle.load(f)

    return ppsd_all


def ppsd_compute(data, fs, ppsd_len, ppsd_step, method):
    """_summary_

    Args:
        data (_type_): _description_
        fs (_type_): _description_
        ppsd_len (_type_): _description_
        ppsd_step (_type_): _description_
        method (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_

    Note:
        _note_
        Do need divide nperseg, because we divide the window power before???
    """
    npts = data.shape[1]
    trace_num = data.shape[0]
    nperseg = int(ppsd_len * fs)
    noverlap = int(ppsd_step * fs)

    if method == "welch":
        f_axis, ppsd_data = welch(
            data,
            fs=fs,
            nperseg=nperseg,
            noverlap=noverlap,
            axis=1,
        )
        ppsd_data = 10 * np.log10(ppsd_data)
    elif method == "fft":
        f_axis = scipy.fft.rfftfreq(nperseg, 1 / fs)
        scipy_detrend(data, axis=1, type="linear", overwrite_data=True)
        window = get_window("hann", nperseg)
        step = nperseg - noverlap
        win_num = (npts - noverlap) // step
        ppsd_data = np.zeros((trace_num, nperseg // 2 + 1))
        for i in range(win_num):
            npts1 = i * step
            npts2 = npts1 + nperseg
            seg = data[:, npts1:npts2]
            seg_window = seg * window
            seg_rfft = scipy.fft.rfft(seg_window, n=nperseg, axis=1)
            ppsd_data += np.abs(seg_rfft) ** 2

        ppsd_data = ppsd_data / win_num / (fs * (window**2).sum())
        ppsd_data = 10 * np.log10(ppsd_data)
    else:
        raise ValueError("method must be 'welch' or 'fft'")

    return ppsd_data, f_axis


def ppsd(
    self,
    ppsd_len,
    ppsd_step,
    starttrace=None,
    endtrace=None,
    starttime=None,
    endtime=None,
    method="welch",  # welch or fft
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

    # check starttrace and endtrace
    if starttrace is None:
        starttrace = int(0)
    if starttrace < 0:
        raise ValueError("starttrace must be greater than or equal to 0.")
    if endtrace is None:
        endtrace = int(self.stats.trace_num)
    if endtrace > self.stats.trace_num:
        raise ValueError("endtrace must be less than or equal to stream trace_num.")

    # set times
    starttime_npts = int((starttime - self.stats.starttime) * self.stats.sampling_rate)
    endtime_npts = int((endtime - self.stats.starttime) * self.stats.sampling_rate)

    # data
    data = self.data[starttrace:endtrace, starttime_npts:endtime_npts].copy()
    network = self.stats.network[starttrace:endtrace]
    station = self.stats.station[starttrace:endtrace]
    channel = self.stats.channel[starttrace:endtrace]

    # ppsd compute
    ppsd_data, f_axis = ppsd_compute(
        data, self.stats.sampling_rate, ppsd_len, ppsd_step, method
    )

    # generate ppsd object
    PPSD_Data = PPSD(
        ppsd_data,
        f_axis,
        network,
        station,
        channel,
        starttrace,
        endtrace,
        starttime,
        endtime,
        ppsd_len,
        ppsd_step,
        method,
    )

    return PPSD_Data


class PPSD(object):
    def __init__(
        self,
        data,
        f_axis,
        network,
        station,
        channel,
        starttrace,
        endtrace,
        starttime,
        endtime,
        ppsd_len,
        ppsd_step,
        method,
    ):
        self.data = data
        self.f_axis = f_axis
        self.network = network
        self.station = station
        self.channel = channel
        self.starttrace = starttrace
        self.endtrace = endtrace
        self.starttime = starttime
        self.endtime = endtime
        self.ppsd_len = ppsd_len
        self.ppsd_step = ppsd_step
        self.method = method

    def __str__(self):
        stats = (
            "* Stats:\n"
            f"      starttime: {str(self.starttime)}\n"
            f"      endtime: {str(self.endtime)}\n"
            f"      starttrace: {self.starttrace}\n"
            f"      endtrace: {self.endtrace}\n"
            f"      ppsd_len: {self.ppsd_len}\n"
            f"      ppsd_step: {self.ppsd_step}\n"
            f"      method: '{self.method}'\n"
            f"      frequency samples: {len(self.f_axis)}\n"
        )
        data = (
            "* Data:\n"
            f"       shape: {self.data.shape} || (trace, freq_axis)\n"
            f"       dtype: {self.data.dtype}\n"
            f"{textwrap.indent(np.array2string(self.data, threshold=MAX_DATA_THRESHOLD), '      ')}"
        )
        info = "\n".join([stats, data])
        return info

    def __repr__(self):
        return str(self)

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def plot(
        self,
        starttrace=0,
        endtrace=1,
        freq_range=[None, None],
        freq_log=True,
        db_range=[None, None],
        mode="mesh",  # mesh or line
        mesh_line=True,
        xbins=50,
        ybins=50,
        window_length=201,
        polyorder=2,
        ax=None,
        figsize=(10, 5),
        linewidth=1,
        linestyle="-",
        alpha=0.8,
        cmap="CMRmap_r",
        show_legend=True,
        show=True,
        save_path=None,
        dpi=100,
    ):
        # check starttrace and endtrace
        trace_num = self.data.shape[0]
        if starttrace < 0:
            raise ValueError("starttrace must be greater than or equal to 0.")
        if endtrace > trace_num:
            raise ValueError("endtrace must be less than or equal to stream trace_num.")

        # check freq_range
        if freq_range[0] is None:
            freq_range[0] = self.f_axis[1]  # skip 0 Hz to avoid log(0)
        if freq_range[1] is None:
            freq_range[1] = self.f_axis[-1]

        # data & smooth
        data = self.data[starttrace:endtrace].copy()
        data = np.nan_to_num(
            data, nan=0.0, posinf=0.0, neginf=0.0
        )  # replace nan, inf to 0
        data = savgol_filter(data, window_length, polyorder, axis=1)

        # plot
        ax = _get_ax(ax, figsize=figsize)
        cmap = _get_cmap(cmap)
        color = list(mcolors.TABLEAU_COLORS.keys())
        color_num = len(color)
        if mode == "line":
            for i in range(0, data.shape[0]):
                # skip all zero trace
                if not data[i].all() == 0:
                    ax.plot(
                        self.f_axis,
                        data[i],
                        color=color[i % color_num],
                        linewidth=linewidth,
                        linestyle=linestyle,
                        alpha=alpha,
                        label=f"Trace:{i+starttrace}",
                    )
        elif mode == "mesh":
            # remove all zero rows
            data = data[~np.all(data == 0, axis=1)]
            # mesh grid
            x_edges = np.linspace(self.f_axis[0], self.f_axis[-1], xbins)
            y_edges = np.linspace(data.min(), data.max(), ybins)
            X, Y = np.meshgrid(x_edges[:-1], y_edges[:-1])
            density = np.zeros(X.shape)
            for curve in data:
                H, _, _ = np.histogram2d(self.f_axis, curve, bins=(x_edges, y_edges))
                density += H.T
            density /= np.max(density)
            im = ax.pcolormesh(X, Y, density, cmap=cmap, shading="auto")
            # mean line
            if mesh_line:
                mean = np.mean(data, axis=0)
                ax.plot(
                    self.f_axis,
                    mean,
                    color="gray",
                    linewidth=linewidth,
                    linestyle=linestyle,
                    alpha=alpha,
                )
        else:
            raise ValueError("mode must be 'mesh' or 'line'")

        # format
        fig = ax.figure
        if mode == "mesh":
            cbar = fig.colorbar(im, ax=ax, extend="both")
            cbar.set_label("Probability")
        if mode == "line" and show_legend:
            ax.legend(loc="upper right", fontsize=8, shadow=False)
        if freq_log:
            ax.set_xscale("log")
        ax.set_xlim(freq_range)
        if db_range[0] is not None and db_range[1] is not None:
            ax.set_ylim(db_range)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("PSD (dB)")
        if show:
            plt.show()
        else:
            plt.close(fig)
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax

    def plot_spatial(
        self,
        starttrace=0,
        endtrace=1,
        freq_range=[None, None],
        freq_lines=[],  # list of frequency
        linewidth=1,
        linestyle="-",
        alpha=0.8,
        lines_scale=0.2,
        window_length=201,
        polyorder=2,
        trace_axis="x",
        trace_ticks=5,
        invert_x=False,
        invert_y=False,
        ax=None,
        cmap="viridis",
        clip=[None, None],
        figsize=(10, 6),
        show=True,
        save_path=None,
        dpi=100,
    ):
        # check starttrace and endtrace
        trace_num = self.data.shape[0]
        if starttrace < 0:
            raise ValueError("starttrace must be greater than or equal to 0.")
        if endtrace > trace_num:
            raise ValueError("endtrace must be less than or equal to stream trace_num.")

        # check freq_range
        freq_min = self.f_axis[0]
        freq_max = self.f_axis[-1]
        if freq_range[0] is None:
            freq_range[0] = self.f_axis[0]
        if freq_range[1] is None:
            freq_range[1] = self.f_axis[-1]

        # data & smooth
        data = self.data[starttrace:endtrace].copy()
        data = savgol_filter(data, window_length, polyorder, axis=1)

        # data freq lines
        if len(freq_lines) != 0:
            trace_num = endtrace - starttrace
            freq_lines_data = np.full((len(freq_lines), trace_num), np.nan)
            for i in range(0, len(freq_lines)):
                # find freq band from f_axis
                freq_min_index = np.argmin(np.abs(self.f_axis - freq_lines[i][0]))
                freq_max_index = np.argmin(np.abs(self.f_axis - freq_lines[i][1]))
                freq_lines_data[i, :] = np.mean(
                    data[:, freq_min_index:freq_max_index], axis=1
                )
            freq_lines_data += -np.nanmin(freq_lines_data)  # shift to positive from dB

        # clip
        if clip[0] is None:
            clip[0] = np.nanmin(data)
        if clip[1] is None:
            clip[1] = np.nanmax(data)

        # plot
        ax = _get_ax(ax, figsize=figsize)
        cmap = _get_cmap(cmap)
        if trace_axis == "x":
            im = ax.imshow(
                data.T,
                extent=[starttrace, endtrace, freq_min, freq_max],
                aspect="auto",
                cmap=cmap,
                origin="lower",
            )
        elif trace_axis == "y":
            im = ax.imshow(
                data,
                extent=[freq_min, freq_max, starttrace, endtrace],
                aspect="auto",
                cmap=cmap,
                origin="lower",
            )
        else:
            raise ValueError("time_axis must be 'x' or 'y'")

        # plot freq lines
        if len(freq_lines) != 0:
            traces_axis = np.linspace(starttrace, endtrace - 1, num=trace_num)
            for i in range(0, len(freq_lines)):
                y_shift = (freq_lines[i][1] + freq_lines[i][0]) / 2
                line_data = np.abs(freq_lines_data[i, :]) - np.nanmin(
                    np.abs(freq_lines_data[i, :])
                )
                if np.nanmax(line_data) == 0:
                    line_data = np.full(line_data.shape, y_shift)
                else:
                    line_data = (
                        line_data / np.nanmax(line_data) * lines_scale
                        - lines_scale / 2
                        + y_shift
                    )
                if trace_axis == "x":
                    ax.plot(
                        traces_axis,
                        line_data,
                        color="black",
                        linewidth=linewidth,
                        linestyle=linestyle,
                        alpha=alpha,
                    )
                elif trace_axis == "y":
                    ax.plot(
                        line_data,
                        traces_axis,
                        color="black",
                        linewidth=linewidth,
                        linestyle=linestyle,
                        alpha=alpha,
                    )
        # clip
        im.set_clim(clip)

        # format axis
        if trace_ticks > (endtrace - starttrace - 1):
            trace_ticks = round(endtrace - starttrace - 1)
        ticks = np.linspace(starttrace, endtrace - 1, num=trace_ticks)
        labels = np.round(
            np.linspace(starttrace, endtrace - 1, num=trace_ticks)
        ).astype(int)
        if trace_axis == "x":
            ax.set_ylim(freq_range)
            ax.set_xticks(ticks)
            ax.set_xticklabels(labels)
            ax.set_xlabel("Trace")
            ax.set_ylabel("Frequency (Hz)")
        elif trace_axis == "y":
            ax.set_xlim(freq_range)
            ax.set_yticks(ticks)
            ax.set_yticklabels(labels)
            ax.set_ylabel("Trace")
            ax.set_xlabel("Frequency (Hz)")
        else:
            raise ValueError("trace_axis must be 'x' or 'y'")

        # format figure
        fig = ax.figure
        cbar = fig.colorbar(im, ax=ax, extend="both")
        cbar.set_label("PSD (dB)")
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


class PPSD_ALL(object):
    def __init__(self, ppsds):
        # check ppsds
        if not isinstance(ppsds, list) or not all(isinstance(x, PPSD) for x in ppsds):
            raise ValueError("ppsds must be a list of PPSD objects.")

        # check ppsds parameters
        for ppsd in ppsds:
            if not np.all(np.isclose(ppsd.f_axis, ppsds[0].f_axis, atol=1e-6)):
                raise ValueError("ppsds must have the same f_axis.")
            if ppsd.network != ppsds[0].network:
                raise ValueError("ppsds must have the same network.")
            if ppsd.station != ppsds[0].station:
                raise ValueError("ppsds must have the same station.")
            if ppsd.channel != ppsds[0].channel:
                raise ValueError("ppsds must have the same channel.")
            if ppsd.starttrace != ppsds[0].starttrace:
                raise ValueError("ppsds must have the same starttrace.")
            if ppsd.endtrace != ppsds[0].endtrace:
                raise ValueError("ppsds must have the same endtrace.")

        # init parameters
        self.ppsds = ppsds
        self.f_axis = ppsds[0].f_axis
        self.network = ppsds[0].network
        self.station = ppsds[0].station
        self.channel = ppsds[0].channel
        self.starttrace = ppsds[0].starttrace
        self.endtrace = ppsds[0].endtrace
        self.trace_num = ppsds[0].endtrace - ppsds[0].starttrace

        # accemble all starttimes and endtimes into a 2-d array
        self.times = np.array([[ppsd.starttime, ppsd.endtime] for ppsd in ppsds])
        sorted_indices = np.argsort(self.times[:, 0])
        self.times = self.times[sorted_indices]
        self.ppsds = [self.ppsds[i] for i in sorted_indices]

    def __str__(self):
        info = str(len(self.ppsds)) + " ppsd(s) in ppsd_all:\n"
        for i, ppsd in enumerate(self.ppsds):
            # set out string
            out = f"    {ppsd.starttime} - {ppsd.endtime}\n"
            # cut out if too long
            if len(self.ppsds) <= 20:
                info += out
            else:
                if i < 10:
                    info += out
                elif i == 10:
                    info += "    ...\n"
                elif i > len(self.ppsds) - 10:
                    info += out
        return info

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return list(self.ppsds).__iter__()

    def __len__(self):
        return len(self.ppsds)

    def __eq__(self, other):
        return self.ppsds == other.ppsds

    def __ne__(self, other):
        return not self.__eq__(other)

    def __setitem__(self, index, trace):
        self.ppsds.__setitem__(index, trace)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.__class__(ppsds=self.ppsds.__getitem__(index))
        else:
            return self.ppsds.__getitem__(index)

    def __delitem__(self, index):
        return self.ppsds.__delitem__(index)

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def plot(
        self,
        starttrace=0,
        endtrace=1,
        freq_range=[None, None],
        freq_log=True,
        db_range=[None, None],
        mode="mesh",  # mesh or line
        mesh_line=True,
        xbins=50,
        ybins=50,
        window_length=201,
        polyorder=2,
        figsize=(10, 5),
        ax=None,
        linewidth=1,
        linestyle="-",
        alpha=0.8,
        cmap="CMRmap_r",
        show_legend=True,
        show=True,
        save_path=None,
        dpi=100,
    ):
        # check starttrace and endtrace
        if starttrace < 0:
            raise ValueError("starttrace must be greater than or equal to 0.")
        if endtrace > self.trace_num:
            raise ValueError("endtrace must be less than or equal to stream trace_num.")

        # check freq_range
        if freq_range[0] is None:
            freq_range[0] = self.f_axis[1]  # skip 0 Hz to avoid log(0)
        if freq_range[1] is None:
            freq_range[1] = self.f_axis[-1]

        # data & smooth, average data from all ppsds
        data = np.zeros((endtrace - starttrace, len(self.f_axis)))
        valid_num = np.zeros(endtrace - starttrace)
        for ppsd in self.ppsds:
            dd = ppsd.data[starttrace:endtrace].copy()
            nan_rows = np.isnan(dd).any(axis=1)
            inf_rows = np.isinf(dd).any(axis=1)
            invalid_rows = nan_rows | inf_rows
            valid_num += np.where(invalid_rows, 0, 1)
            data += np.nan_to_num(dd, nan=0.0, posinf=0.0, neginf=0.0)

        data /= valid_num[:, np.newaxis]
        data = np.nan_to_num(data, nan=0.0, posinf=0.0, neginf=0.0)
        data = savgol_filter(data, window_length, polyorder, axis=1)

        # plot
        ax = _get_ax(ax, figsize=figsize)
        cmap = _get_cmap(cmap)
        color = list(mcolors.TABLEAU_COLORS.keys())
        color_num = len(color)
        if mode == "line":
            for i in range(0, data.shape[0]):
                # skip all zero trace
                if not data[i].all() == 0:
                    ax.plot(
                        self.f_axis,
                        data[i],
                        color=color[i % color_num],
                        linewidth=linewidth,
                        linestyle=linestyle,
                        alpha=alpha,
                        label=f"Trace:{i+starttrace}",
                    )
        elif mode == "mesh":
            # remove all zero rows
            data = data[~np.all(data == 0, axis=1)]
            # mesh grid
            x_edges = np.linspace(self.f_axis[0], self.f_axis[-1], xbins)
            y_edges = np.linspace(data.min(), data.max(), ybins)
            X, Y = np.meshgrid(x_edges[:-1], y_edges[:-1])
            density = np.zeros(X.shape)
            for curve in data:
                H, _, _ = np.histogram2d(self.f_axis, curve, bins=(x_edges, y_edges))
                density += H.T
            density /= np.max(density)
            im = ax.pcolormesh(X, Y, density, cmap=cmap, shading="auto")
            # mean line
            if mesh_line:
                mean = np.mean(data, axis=0)
                ax.plot(
                    self.f_axis,
                    mean,
                    color="gray",
                    linewidth=linewidth,
                    linestyle=linestyle,
                    alpha=alpha,
                )
        else:
            raise ValueError("mode must be 'mesh' or 'line'")

        # format
        fig = ax.figure
        if mode == "mesh":
            cbar = fig.colorbar(im, ax=ax, extend="both")
            cbar.set_label("Probability")
        if mode == "line" and show_legend:
            ax.legend(loc="upper right", fontsize=8, shadow=False)
        if freq_log:
            ax.set_xscale("log")
        ax.set_xlim(freq_range)
        if db_range[0] is not None and db_range[1] is not None:
            ax.set_ylim(db_range)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("PSD (dB)")
        if show:
            plt.show()
        else:
            plt.close(fig)
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax

    def plot_spatial(
        self,
        starttrace=0,
        endtrace=1,
        freq_range=[None, None],
        freq_lines=[],  # list of frequency
        linewidth=1,
        linestyle="-",
        alpha=0.8,
        lines_scale=0.2,
        window_length=201,
        polyorder=2,
        trace_axis="x",
        trace_ticks=5,
        invert_x=False,
        invert_y=False,
        ax=None,
        cmap="viridis",
        clip=[None, None],
        figsize=(10, 6),
        show=True,
        save_path=None,
        dpi=100,
    ):
        # check starttrace and endtrace
        if starttrace < 0:
            raise ValueError("starttrace must be greater than or equal to 0.")
        if endtrace > self.trace_num:
            raise ValueError("endtrace must be less than or equal to stream trace_num.")

        # check freq_range
        freq_min = self.f_axis[0]
        freq_max = self.f_axis[-1]
        if freq_range[0] is None:
            freq_range[0] = self.f_axis[0]
        if freq_range[1] is None:
            freq_range[1] = self.f_axis[-1]

        # data & smooth, average data from all ppsd
        data = np.zeros((endtrace - starttrace, len(self.f_axis)))
        valid_num = np.zeros(endtrace - starttrace)
        for ppsd in self.ppsds:
            dd = ppsd.data[starttrace:endtrace].copy()
            nan_rows = np.isnan(dd).any(axis=1)
            inf_rows = np.isinf(dd).any(axis=1)
            invalid_rows = nan_rows | inf_rows
            valid_num += np.where(invalid_rows, 0, 1)
            data += np.nan_to_num(dd, nan=0.0, posinf=0.0, neginf=0.0)

        data /= valid_num[:, np.newaxis]
        data = savgol_filter(data, window_length, polyorder, axis=1)

        # data freq lines
        if len(freq_lines) != 0:
            trace_num = endtrace - starttrace
            freq_lines_data = np.full((len(freq_lines), trace_num), np.nan)
            for i in range(0, len(freq_lines)):
                # find freq band from f_axis
                freq_min_index = np.argmin(np.abs(self.f_axis - freq_lines[i][0]))
                freq_max_index = np.argmin(np.abs(self.f_axis - freq_lines[i][1]))
                freq_lines_data[i, :] = np.mean(
                    data[:, freq_min_index:freq_max_index], axis=1
                )
            freq_lines_data += -np.nanmin(freq_lines_data)  # shift to positive from dB

        # clip
        if clip[0] is None:
            clip[0] = np.nanmin(data)
        if clip[1] is None:
            clip[1] = np.nanmax(data)

        # plot
        ax = _get_ax(ax, figsize=figsize)
        cmap = _get_cmap(cmap)

        if trace_axis == "x":
            im = ax.imshow(
                data.T,
                extent=[starttrace, endtrace, freq_min, freq_max],
                aspect="auto",
                cmap=cmap,
                origin="lower",
            )
        elif trace_axis == "y":
            im = ax.imshow(
                data,
                extent=[freq_min, freq_max, starttrace, endtrace],
                aspect="auto",
                cmap=cmap,
                origin="lower",
            )
        else:
            raise ValueError("time_axis must be 'x' or 'y'")

        # plot freq lines
        if len(freq_lines) != 0:
            traces_axis = np.linspace(starttrace, endtrace - 1, num=trace_num)
            for i in range(0, len(freq_lines)):
                y_shift = (freq_lines[i][1] + freq_lines[i][0]) / 2
                line_data = np.abs(freq_lines_data[i, :]) - np.nanmin(
                    np.abs(freq_lines_data[i, :])
                )
                if np.nanmax(line_data) == 0:
                    line_data = np.full(line_data.shape, y_shift)
                else:
                    line_data = (
                        line_data / np.nanmax(line_data) * lines_scale
                        - lines_scale / 2
                        + y_shift
                    )
                if trace_axis == "x":
                    ax.plot(
                        traces_axis,
                        line_data,
                        color="black",
                        linewidth=linewidth,
                        linestyle=linestyle,
                        alpha=alpha,
                    )
                elif trace_axis == "y":
                    ax.plot(
                        line_data,
                        traces_axis,
                        color="black",
                        linewidth=linewidth,
                        linestyle=linestyle,
                        alpha=alpha,
                    )

        # clip
        im.set_clim(clip)

        # format axis
        if trace_ticks > (endtrace - starttrace - 1):
            trace_ticks = round(endtrace - starttrace - 1)
        ticks = np.linspace(starttrace, endtrace - 1, num=trace_ticks)
        labels = np.round(
            np.linspace(starttrace, endtrace - 1, num=trace_ticks)
        ).astype(int)
        if trace_axis == "x":
            ax.set_ylim(freq_range)
            ax.set_xticks(ticks)
            ax.set_xticklabels(labels)
            ax.set_xlabel("Trace")
            ax.set_ylabel("Frequency (Hz)")
        elif trace_axis == "y":
            ax.set_xlim(freq_range)
            ax.set_yticks(ticks)
            ax.set_yticklabels(labels)
            ax.set_ylabel("Trace")
            ax.set_xlabel("Frequency (Hz)")
        else:
            raise ValueError("trace_axis must be 'x' or 'y'")

        # format figure
        fig = ax.figure
        cbar = fig.colorbar(im, ax=ax, extend="both")
        cbar.set_label("PSD (dB)")
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

    def plot_temporal(
        self,
        starttrace=0,
        endtrace=1,
        freq_range=[None, None],
        freq_lines=[],  # list of frequency
        linewidth=1,
        linestyle="-",
        alpha=0.8,
        lines_scale=0.2,
        window_length=201,
        polyorder=2,
        time_minticks=5,
        time_maxticks=None,
        timetick_rotation=0,
        timetick_labelsize=10,
        ax=None,
        cmap="viridis",
        clip=[None, None],
        figsize=(10, 6),
        show=True,
        save_path=None,
        dpi=100,
    ):
        # check starttrace and endtrace
        if starttrace < 0:
            raise ValueError("starttrace must be greater than or equal to 0.")
        if endtrace > self.trace_num:
            raise ValueError("endtrace must be less than or equal to stream trace_num.")

        # check freq_range
        freq_min = self.f_axis[0]
        freq_max = self.f_axis[-1]
        if freq_range[0] is None:
            freq_range[0] = self.f_axis[0]
        if freq_range[1] is None:
            freq_range[1] = self.f_axis[-1]

        # data & smooth, average data from all ppsds
        time_min = min(self.times[:, 0])
        time_max = max(self.times[:, 1])
        total_seconds = time_max - time_min
        min_interval = np.min(self.times[:, 1] - self.times[:, 0])
        time_bins = int(total_seconds / min_interval)
        data = np.full((time_bins, len(self.f_axis)), np.nan)
        for i in range(0, len(self.ppsds)):
            dd = self.ppsds[i].data[starttrace:endtrace, :].copy()
            dd[np.isinf(dd)] = np.nan
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                dd = np.nanmean(dd, axis=0)
            index1 = int((self.times[i, 0] - time_min) / min_interval)
            index2 = int((self.times[i, 1] - time_min) / min_interval)
            data[index1:index2, :] = dd
        data = savgol_filter(data, window_length, polyorder, axis=1)

        # data freq lines
        if len(freq_lines) != 0:
            freq_lines_data = np.full((len(freq_lines), time_bins), np.nan)
            for i in range(0, len(freq_lines)):
                # find freq band from f_axis
                freq_min_index = np.argmin(np.abs(self.f_axis - freq_lines[i][0]))
                freq_max_index = np.argmin(np.abs(self.f_axis - freq_lines[i][1]))
                freq_lines_data[i, :] = np.mean(
                    data[:, freq_min_index:freq_max_index], axis=1
                )
            freq_lines_data += -np.nanmin(freq_lines_data)  # shift to positive from dB

        # clip
        if clip[0] is None:
            clip[0] = np.nanmin(data)
        if clip[1] is None:
            clip[1] = np.nanmax(data)

        # plot data
        ax = _get_ax(ax, figsize=figsize)
        cmap = _get_cmap(cmap)
        im = ax.imshow(
            data.T,
            extent=[time_min.datetime, time_max.datetime, freq_min, freq_max],
            aspect="auto",
            cmap=cmap,
            origin="lower",
        )

        # plot freq lines
        if len(freq_lines) != 0:
            times_axis = np.empty(time_bins, dtype=object)
            for i in range(0, time_bins):
                times_axis[i] = (
                    time_min + i * min_interval + 0.5 * min_interval
                ).datetime
            for i in range(0, len(freq_lines)):
                y_shift = (freq_lines[i][1] + freq_lines[i][0]) / 2
                line_data = np.abs(freq_lines_data[i, :]) - np.nanmin(
                    np.abs(freq_lines_data[i, :])
                )
                if np.nanmax(line_data) == 0:
                    line_data = np.full(line_data.shape, y_shift)
                else:
                    line_data = (
                        line_data / np.nanmax(line_data) * lines_scale
                        - lines_scale / 2
                        + y_shift
                    )
                ax.plot(
                    times_axis,
                    line_data,
                    color="black",
                    linewidth=linewidth,
                    linestyle=linestyle,
                    alpha=alpha,
                )

        # clip
        im.set_clim(clip)

        # format axis
        _format_time_axis(
            ax,
            axis="x",
            tick_rotation=timetick_rotation,
            minticks=time_minticks,
            maxticks=time_maxticks,
            labelsize=timetick_labelsize,
        )
        ax.set_ylim(freq_range)
        ax.set_ylabel("Frequency (Hz)")

        # format figure
        fig = ax.figure
        cbar = fig.colorbar(im, ax=ax, extend="both")
        cbar.set_label("PSD (dB)")
        if show:
            plt.show()
        else:
            plt.close(fig)
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        else:
            return ax
