import numpy as np
import scipy

from shakecore.core.utils import _add_processing_info


@_add_processing_info
def interpolate(self, sampling_rate, method="slinear", device="cpu"):
    if device == "cpu":
        starttime = self.stats.starttime
        endtime = self.stats.endtime
        npts = self.stats.npts
        times = np.linspace(
            starttime.timestamp,
            endtime.timestamp,
            num=npts,
            endpoint=True,
        )

        new_npts = int(self.stats.npts * sampling_rate / self.stats.sampling_rate)
        new_endtime = self.stats.starttime + new_npts / sampling_rate
        new_times = np.linspace(
            starttime.timestamp,
            new_endtime.timestamp,
            num=new_npts,
            endpoint=True,
        )

        self.data = scipy.interpolate.interp1d(
            times, self.data, axis=1, kind=method, fill_value="extrapolate"
        )(new_times)

        self.stats.sampling_rate = float(sampling_rate)

    elif device == "cuda":
        pass

    else:
        raise ValueError(f"Unknown device '{device}'.")
