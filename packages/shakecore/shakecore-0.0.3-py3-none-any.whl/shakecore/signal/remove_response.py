import numpy as np
from joblib import Parallel, delayed
from obspy.core.inventory import Inventory

from shakecore.core.utils import _add_processing_info


@_add_processing_info
def remove_response(
    self,
    inventory=None,
    output="VEL",
    water_level=60,
    pre_filt=None,
    zero_mean=True,
    taper=True,
    taper_fraction=0.05,
    plot=False,
    fig=None,
    device="cpu",
    jobs=1,
):
    if device == "cpu":
        st_obspy = self.to_obspy()
        if jobs == 1:
            traces = []
            if type(inventory) == Inventory:
                for i in range(0, len(st_obspy)):
                    tr = rm_response_obspy(
                        st_obspy[i],
                        inventory,
                        output,
                        water_level,
                        pre_filt,
                        zero_mean,
                        taper,
                        taper_fraction,
                        plot,
                        fig,
                    )
                    traces.append(tr)
            elif type(inventory) == list and len(inventory) == self.stats.trace_num:
                for i in range(0, len(st_obspy)):
                    tr = rm_response_obspy(
                        st_obspy[i],
                        inventory[i],
                        output,
                        water_level,
                        pre_filt,
                        zero_mean,
                        taper,
                        taper_fraction,
                        plot,
                        fig,
                    )
                    traces.append(tr)
            else:
                raise ValueError(
                    f"Unrecognized inventory: {inventory}."
                    "It should be an ObsPy Inventory object or a list of ObsPy Inventory objects."
                )
            self.data = np.array([tr.data for tr in traces])
        elif jobs > 1:
            if type(inventory) == Inventory:
                traces = Parallel(n_jobs=jobs, backend="loky")(
                    delayed(rm_response_obspy)(
                        st_obspy[i],
                        inventory,
                        output,
                        water_level,
                        pre_filt,
                        zero_mean,
                        taper,
                        taper_fraction,
                        plot,
                        fig,
                    )
                    for i in range(0, len(st_obspy))
                )
            elif type(inventory) == list and len(inventory) == self.stats.trace_num:
                traces = Parallel(n_jobs=jobs, backend="loky")(
                    delayed(rm_response_obspy)(
                        st_obspy[i],
                        inventory[i],
                        output,
                        water_level,
                        pre_filt,
                        zero_mean,
                        taper,
                        taper_fraction,
                        plot,
                        fig,
                    )
                    for i in range(0, len(st_obspy))
                )
            else:
                raise ValueError(
                    f"Unrecognized inventory: {inventory}."
                    "It should be an ObsPy Inventory object or a list of ObsPy Inventory objects."
                )
            self.data = np.array([tr.data for tr in traces])

    elif device == "cuda":
        raise NotImplementedError
    else:
        raise ValueError(f"Unknown device '{device}'.")


def rm_response_obspy(
    trace,
    inventory,
    output,
    water_level,
    pre_filt,
    zero_mean,
    taper,
    taper_fraction,
    plot,
    fig,
):
    trace.remove_response(
        inventory,
        output,
        water_level,
        pre_filt,
        zero_mean,
        taper,
        taper_fraction,
        plot,
        fig,
    )

    return trace
