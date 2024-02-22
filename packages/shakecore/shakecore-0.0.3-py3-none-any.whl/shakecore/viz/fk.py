import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from shakecore.transform import fk_forward

from .utils.viz_tools import _get_ax, _get_cmap


def fk(
    self,
    starttime=None,
    endtime=None,
    starttrace=None,
    endtrace=None,
    velocity=[],  # m/s
    linewidth=1,
    linestyle="--",
    ax=None,
    clip=[0.0, 1.0],
    cmap="viridis",
    figsize=(10, 5),
    show=True,
    save_path=None,
    dpi=100,
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

    # fk transform
    fk_data, k_axis, f_axis, _, _ = fk_forward(
        data,
        dx=self.stats.interval,
        dt=self.stats.delta,
        device="cpu",
    )
    fk_data = np.abs(fk_data)

    # flip to keep uniform with the positive direction from L to R
    fk_data = np.flip(fk_data, axis=0)

    # plot
    fk_data /= np.max(np.abs(fk_data))
    ax = _get_ax(ax, figsize=figsize)
    cmap = _get_cmap(cmap)
    colors = list(mcolors.TABLEAU_COLORS.keys())
    im = ax.imshow(
        fk_data.T,
        origin="lower",
        aspect="auto",
        cmap=cmap,
        extent=(k_axis.min(), k_axis.max(), f_axis.min(), f_axis.max()),
    )

    # plot velocity
    for i in range(0, len(velocity)):
        x = k_axis
        y = velocity[i] * x
        ax.plot(
            x,
            y,
            color=colors[i],
            linestyle=linestyle,
            linewidth=linewidth,
            label=str(velocity[i]) + "m/s",
        )

    # clip
    im.set_clim(clip)

    # format
    fig = ax.figure
    ax.set_xlim(k_axis.min(), k_axis.max())
    ax.set_ylim(0, f_axis.max())
    ax.set_xlabel("Wave number (1/m)")
    ax.set_ylabel("Frequency (Hz)")
    if len(velocity) != 0:
        ax.legend(loc="upper right", fontsize=8, shadow=False)
    if not show:
        plt.close(fig)
    if save_path is not None:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
    else:
        return ax
