import glob
from pathlib import PosixPath

import numpy as np
import obspy

from shakecore.io.utils import obspy_2_shakecore

from .sc import sc_read
from .tdms import tdms_read
from .terra15 import terra15_read


def read(
    filepaths=None,
    format=None,
    headonly=False,
    starttrace=None,
    endtrace=None,
    steptrace=1,
    starttime=None,
    endtime=None,
    nearest_sample=True,
    dtype=None,
    apply_calib=False,
    check_compression=True,
    backend="obspy",
    interval=np.nan,
    type="unknown",
    notes={},
    mode="strict",
    fill_value=None,
    **kwargs,
):
    if isinstance(filepaths, str):
        files = sorted(glob.glob(filepaths))
    elif isinstance(filepaths, PosixPath):
        files = sorted(glob.glob(str(filepaths)))
    elif isinstance(filepaths, list):
        files = sorted(filepaths)
    else:
        raise ValueError(f"Unrecognized filepaths: {filepaths}")

    if len(files) == 0:
        raise ValueError("No files found.")
    else:
        from shakecore.core.pool import Pool

        streams = []
        for file in files:
            pathname_or_url = file
            if backend == "obspy":
                stream = read_obspy(
                    pathname_or_url,
                    format,
                    headonly,
                    starttime,
                    endtime,
                    nearest_sample,
                    dtype,
                    apply_calib,
                    check_compression,
                    interval,
                    type,
                    notes,
                    mode,
                    fill_value,
                    **kwargs,
                )
            elif backend == "shakecore":
                stream = read_shakecore(
                    pathname_or_url,
                    format,
                    headonly,
                    starttrace,
                    endtrace,
                    steptrace,
                    starttime,
                    endtime,
                )
            else:
                raise ValueError(f"Unrecognized backend: {backend}")

            # append stream
            if stream is not None:
                streams.append(stream)

        return Pool(streams)


def read_obspy(
    pathname_or_url=None,
    format=None,
    headonly=False,
    starttime=None,
    endtime=None,
    nearest_sample=True,
    dtype=None,
    apply_calib=False,
    check_compression=True,
    interval=np.nan,
    type="unknown",
    notes=dict(),
    mode="strict",
    fill_value=None,
    **kwargs,
):
    stream_obspy = obspy.read(
        pathname_or_url,
        format,
        headonly,
        starttime,
        endtime,
        nearest_sample,
        dtype,
        apply_calib,
        check_compression,
        **kwargs,
    )
    stream_shakecore = obspy_2_shakecore(
        stream_obspy, mode, fill_value, interval, type, notes
    )

    return stream_shakecore


def read_shakecore(
    pathname_or_url,
    format,
    headonly,
    starttrace,
    endtrace,
    steptrace,
    starttime,
    endtime,
):
    if format == "sc":
        stream = sc_read(
            pathname_or_url,
            headonly,
            starttrace,
            endtrace,
            steptrace,
            starttime,
            endtime,
        )
    elif format == "tdms":
        stream = tdms_read(
            pathname_or_url,
            headonly,
            starttrace,
            endtrace,
            steptrace,
            starttime,
            endtime,
        )
    elif format == "terra15":
        stream = terra15_read(
            pathname_or_url,
            headonly,
            starttrace,
            endtrace,
            steptrace,
            starttime,
            endtime,
        )
    else:
        raise ValueError(f"Unrecognized format: {format}")

    return stream
