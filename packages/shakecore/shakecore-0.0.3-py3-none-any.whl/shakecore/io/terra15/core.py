import numpy as np
from obspy import UTCDateTime


def terra15_read(
    pathname_or_url,
    headonly,
    starttrace,
    endtrace,
    steptrace,
    starttime,
    endtime,
):
    data = np.empty((0, 0))

    from shakecore.core.stream import Stream

    header = {
        "starttime": starttime,
    }

    return Stream(data, header)
