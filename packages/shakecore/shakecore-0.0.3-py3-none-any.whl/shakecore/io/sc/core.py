import json

import h5py
import numpy as np
from obspy import UTCDateTime


def sc_read(
    pathname_or_url,
    headonly,
    starttrace,
    endtrace,
    steptrace,
    starttime,
    endtime,
):
    with h5py.File(pathname_or_url, "r") as f:
        group = f["sc"]
        starttime_raw = UTCDateTime(group.attrs["starttime"])
        endtime_raw = UTCDateTime(group.attrs["endtime"])
        trace_num = group.attrs["trace_num"]
        sampling_rate = group.attrs["sampling_rate"]
        # raw_npts = group.attrs["npts"]

        if starttrace is None:
            starttrace = 0
        if endtrace is None:
            endtrace = trace_num
        if starttime is None:
            starttime = starttime_raw
        if endtime is None:
            endtime = endtime_raw

        if starttime > endtime_raw or endtime < starttime_raw:
            return None
        else:
            if starttime < starttime_raw:
                starttime = starttime_raw
            if endtime > endtime_raw:
                endtime = endtime_raw
            npts_start = round((starttime - starttime_raw) * sampling_rate)
            npts_end = round((endtime - starttime_raw) * sampling_rate)

        # npts = npts_end - npts_start
        interval = group.attrs["interval"] * steptrace
        type = group.attrs["type"]
        network = group.attrs["network"].tolist()[starttrace:endtrace:steptrace]
        station = group.attrs["station"].tolist()[starttrace:endtrace:steptrace]
        channel = group.attrs["channel"].tolist()[starttrace:endtrace:steptrace]
        latitude = group.attrs["latitude"].tolist()[starttrace:endtrace:steptrace]
        longitude = group.attrs["longitude"].tolist()[starttrace:endtrace:steptrace]
        elevation = group.attrs["elevation"].tolist()[starttrace:endtrace:steptrace]
        processing = group.attrs["processing"].tolist()
        notes = json.loads(group.attrs["notes"])

        if headonly:
            data = np.empty((0, 0))
        else:
            data = group["data"][
                starttrace:endtrace:steptrace, npts_start : npts_end + 1
            ]

    from shakecore.core.stream import Stream

    header = {
        "starttime": starttime,
        "sampling_rate": sampling_rate,
        "interval": float(interval),
        "type": type,
        "network": network,
        "station": station,
        "channel": channel,
        "latitude": latitude,
        "longitude": longitude,
        "elevation": elevation,
        "processing": processing,
        "notes": notes,
        "_format": "sc",
        "sc": dict(),
    }

    return Stream(data, header)


def sc_write(
    self,
    filename,
):
    with h5py.File(filename, "w") as f:
        group = f.create_group("sc")
        group.attrs["starttime"] = str(self.stats.starttime)
        group.attrs["endtime"] = str(self.stats.endtime)
        group.attrs["sampling_rate"] = self.stats.sampling_rate
        group.attrs["delta"] = self.stats.delta
        group.attrs["interval"] = self.stats.interval
        group.attrs["npts"] = self.stats.npts
        group.attrs["trace_num"] = self.stats.trace_num
        group.attrs["type"] = self.stats.type
        group.attrs["network"] = self.stats.network
        group.attrs["station"] = self.stats.station
        group.attrs["channel"] = self.stats.channel
        group.attrs["latitude"] = self.stats.latitude
        group.attrs["longitude"] = self.stats.longitude
        group.attrs["elevation"] = self.stats.elevation
        group.attrs["processing"] = self.stats.processing
        group.attrs["notes"] = json.dumps(self.stats.notes)
        group.create_dataset("data", data=self.data)
