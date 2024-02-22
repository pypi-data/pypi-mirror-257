import datetime

import numpy as np
from nptdms import TdmsFile
from obspy import UTCDateTime


def tdms_read(
    pathname_or_url,
    headonly,
    starttrace,
    endtrace,
    steptrace,
    starttime,
    endtime,
):
    tf = TdmsFile.read(pathname_or_url)
    group_name = tf.groups()[0].name
    raw_data = np.array(tf[group_name].as_dataframe()).T
    sampling_rate = tf.properties["SamplingFrequency[Hz]"]
    trace_num = raw_data.shape[0]
    raw_npts = raw_data.shape[1]
    starttime_raw = UTCDateTime(tf.properties["GPSTimeStamp"].astype(datetime.datetime))
    endtime_raw = starttime_raw + raw_npts / sampling_rate

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
    interval = tf.properties["SpatialResolution[m]"] * steptrace
    type = "unknown"  # idas
    # network =
    # station =
    channel = [str(i) for i in range(starttrace + 1, endtrace + 1, steptrace)]
    # latitude =
    # longitude =
    # elevation =
    # processing =
    # notes =

    if headonly:
        data = np.empty((0, 0))
    else:
        data = raw_data[starttrace:endtrace:steptrace, npts_start : npts_end + 1]

    from shakecore.core.stream import Stream

    header = {
        "starttime": starttime,
        "sampling_rate": sampling_rate,
        "interval": float(interval),
        "type": type,
        # "network": network,
        # "station": station,
        "channel": channel,
        # "latitude": latitude,
        # "longitude": longitude,
        # "elevation": elevation,
        # "processing": processing,
        # "notes": notes,
        "_format": "tdms",
        "tdms": dict(tf.properties),
    }

    return Stream(data, header)
