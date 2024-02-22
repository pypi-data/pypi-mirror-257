import numpy as np


def to_obspy(self):
    from obspy.core.stream import Stream
    from obspy.core.trace import Trace

    trace_all = []
    for i in range(0, self.stats.trace_num):
        trace_all.append(
            Trace(
                data=self.data[i, :],
                header={
                    "network": self.stats.network[i],
                    "station": self.stats.station[i],
                    "channel": self.stats.channel[i],
                    "starttime": self.stats.starttime,
                    "sampling_rate": self.stats.sampling_rate,
                    "delta": self.stats.delta,
                    "npts": self.stats.npts,
                    "_format": "sc",
                    "sc": {
                        "interval": self.stats.interval,
                        "type": self.stats.type,
                        "processing": self.stats.processing,
                        "notes": self.stats.notes,
                    },
                },
            )
        )

    return Stream(traces=trace_all)


def obspy_2_shakecore(
    stream, mode="strict", fill_value=None, interval=0.0, type="unknown", notes={}
):
    """
    Convert an ObsPy Stream object to a ShakeCore Stream object.

    Parameters
    ----------
    stream : obspy.core.stream.Stream
        ObsPy Stream object.
    mode : str
        Mode of conversion. Default is "strict". Options are "strict", "cutting" and "padding".
    fill_value : float
        Fill value for padding. Default is None.
    interval : float
        Interval between traces. Default is 0.0.
    type : str
        Type of the stream. Default is "unknown".
    notes : dict
        Notes of the stream. Default is {}.

    Returns
    -------
    stream : shakecore.core.stream.Stream
        ShakeCore Stream object.
    """
    from shakecore.core.stream import Stream

    sampling_rate_0 = stream[0].stats.sampling_rate
    for trace in stream:
        if trace.stats.sampling_rate != sampling_rate_0:
            raise ValueError("Sampling rate is not the same for all traces.")

    starttime = stream[0].stats.starttime
    if mode == "strict":
        is_same = True
        starttime_0 = stream[0].stats.starttime
        endtime_0 = stream[0].stats.endtime
        for trace in stream:
            if trace.stats.starttime != starttime_0 or trace.stats.endtime != endtime_0:
                is_same = False
                break
        if is_same:
            data = np.array([tr.data for tr in stream])
            starttime = starttime_0
        else:
            raise ValueError("Starttime and endtime are not the same for all traces.")
    elif mode == "cutting":
        is_same = True
        max_starttime_0 = stream[0].stats.starttime
        min_endtime_0 = stream[0].stats.endtime
        for trace in stream:
            if (
                trace.stats.starttime != max_starttime_0
                or trace.stats.endtime != min_endtime_0
            ):
                is_same = False
            if trace.stats.starttime > max_starttime_0:
                max_starttime_0 = trace.stats.starttime
            if trace.stats.endtime < min_endtime_0:
                min_endtime_0 = trace.stats.endtime
        if is_same:
            data = np.array([tr.data for tr in stream])
            starttime = max_starttime_0
        else:
            for trace in stream:
                trace.trim(starttime=max_starttime_0, endtime=min_endtime_0)
            data = np.array([tr.data for tr in stream])
            starttime = max_starttime_0
    elif mode == "padding":
        is_same = True
        min_starttime_0 = stream[0].stats.starttime
        max_endtime_0 = stream[0].stats.endtime
        for trace in stream:
            if (
                trace.stats.starttime != min_starttime_0
                or trace.stats.endtime != max_endtime_0
            ):
                is_same = False
            if trace.stats.starttime < min_starttime_0:
                min_starttime_0 = trace.stats.starttime
            if trace.stats.endtime > min_endtime_0:
                max_endtime_0 = trace.stats.endtime
        if is_same:
            data = np.array([tr.data for tr in stream])
            starttime = min_starttime_0
        else:
            for trace in stream:
                trace.trim(
                    starttime=min_starttime_0,
                    endtime=max_endtime_0,
                    pad=True,
                    fill_value=fill_value,
                )
            data = np.array([tr.data for tr in stream])
            starttime = max_starttime_0

    sampling_rate = float(stream[0].stats.sampling_rate)
    delta = float(stream[0].stats.delta)
    network = [str(tr.stats.network) for tr in stream]
    station = [str(tr.stats.station) for tr in stream]
    channel = [str(tr.stats.channel) for tr in stream]
    latitude = []
    longitude = []
    elevation = []
    for tr in stream:
        if hasattr(tr.stats, "_format"):
            if tr.stats._format == "SAC":
                if "stla" in tr.stats.sac:
                    latitude.append(float(tr.stats.sac["stla"]))
                else:
                    latitude.append(np.nan)
                if "stlo" in tr.stats.sac:
                    longitude.append(float(tr.stats.sac["stlo"]))
                else:
                    longitude.append(np.nan)
                if "stel" in tr.stats.sac:
                    elevation.append(float(tr.stats.sac["stel"]))
                else:
                    elevation.append(np.nan)
            elif tr.stats._format == "MSEED":
                latitude.append(np.nan)
                longitude.append(np.nan)
                elevation.append(np.nan)
            elif tr.stats._format == "SEGY":
                latitude.append(np.nan)
                longitude.append(np.nan)
                elevation.append(np.nan)
            else:
                latitude.append(np.nan)
                longitude.append(np.nan)
                elevation.append(np.nan)
        else:
            latitude.append(np.nan)
            longitude.append(np.nan)
            elevation.append(np.nan)

    header = {
        "starttime": starttime,
        "sampling_rate": sampling_rate,
        "delta": delta,
        "interval": float(interval),
        "type": type,
        "network": network,
        "station": station,
        "channel": channel,
        "latitude": latitude,
        "longitude": longitude,
        "elevation": elevation,
        "notes": notes,
    }

    return Stream(data, header)
