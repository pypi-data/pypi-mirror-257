import matplotlib.pyplot as plt
import numpy as np

from shakecore.transform import radon_inverse

from .utils.viz_tools import _get_ax, _get_cmap


def radon(
    self,
    starttime=None,
    endtime=None,
    starttrace=None,
    endtrace=None,
    p_vec=np.linspace(-1.0, 1.0, 1000),  # s/m
    kind="parabolic",
    method="CG",
    options={},
    invert_y=True,
    ax=None,
    clip=[-1.0, 1.0],
    cmap="viridis",
    tracetick_rotation=0,
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

    # radon transform
    dt = self.stats.delta
    dx = self.stats.interval
    npts = data.shape[1]
    tau_vec = np.arange(0, npts) * dt
    model = radon_inverse(
        data,
        dt,
        dx,
        p_vec,
        kind,
        method,
        options,
    )

    # plot
    model /= np.max(np.abs(model))
    ax = _get_ax(ax, figsize=figsize)
    cmap = _get_cmap(cmap)
    im = ax.imshow(
        model.T,
        origin="lower",
        aspect="auto",
        cmap=cmap,
        extent=(p_vec.min(), p_vec.max(), tau_vec.min(), tau_vec.max()),
    )

    # clip
    im.set_clim(clip)

    # format
    fig = ax.figure
    ax.tick_params(axis="x", rotation=tracetick_rotation)
    ax.set_xlim(p_vec.min(), p_vec.max())
    ax.set_ylim(tau_vec.min(), tau_vec.max())
    ax.set_xlabel(f"P of `{kind}`")
    ax.set_ylabel("Tau (s)")
    if invert_y:
        ax.invert_yaxis()
    if not show:
        plt.close(fig)
    if save_path is not None:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
    else:
        return ax
