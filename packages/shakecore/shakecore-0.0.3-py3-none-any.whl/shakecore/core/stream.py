import copy
import textwrap

import numpy as np

import shakecore.beamforming
import shakecore.core.manipulation.manipulation_stream
import shakecore.core.operator.operator_stream
import shakecore.io
import shakecore.ppsd
import shakecore.signal
from shakecore.conv import Conv
from shakecore.core.stats import Stats
from shakecore.core.utils import _data_sanity_checks
from shakecore.setting import MAX_DATA_THRESHOLD
from shakecore.viz import Viz


class Stream:
    """
    A Stream object is a collection of Trace objects. It is initialized with
    a list of Trace objects or a single Trace object.

    Examples
    --------
    >>> import numpy as np
    >>> from shakecore.core.stream import Stream
    >>> data = np.ones((10, 100))
    >>> stream = Stream(data)
    >>> stream
    * ID:
          157b3c147eae3f4fef26d8f660f8549debaae2ae17bbc91b629b1adeca2bfac0
    * STATS:
             starttime: 1970-01-01T00:00:00.000000Z
               endtime: 1970-01-01T00:01:39.000000Z
         sampling_rate: 1.0
                 delta: 1.0
              interval: nan
                  npts: 100
             trace_num: 10
                  type: unknown
               network: ['', '', '', '', '', '', '', '', '', '']
               station: ['', '', '', '', '', '', '', '', '', '']
               channel: ['', '', '', '', '', '', '', '', '', '']
              latitude: [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
             longitude: [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
             elevation: [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
            processing: []
                 notes: {}
    * DATA:
           shape: (10, 100)
           dtype: float64
          masked: False
          [[1. 1. 1. ... 1. 1. 1.]
           [1. 1. 1. ... 1. 1. 1.]
           [1. 1. 1. ... 1. 1. 1.]
           ...
           [1. 1. 1. ... 1. 1. 1.]
           [1. 1. 1. ... 1. 1. 1.]
           [1. 1. 1. ... 1. 1. 1.]]
    """

    def __init__(self, data=np.empty((0, 0)), header={}):
        # check data, and copy header
        _data_sanity_checks(data)
        header = copy.deepcopy(header)

        # set trace_num and npts according to data shape
        header["npts"] = data.shape[1]
        header["trace_num"] = data.shape[0]

        # set default list in header if not set yet
        trace_num = header["trace_num"]
        for k in [
            "network",
            "station",
            "channel",
            "latitude",
            "longitude",
            "elevation",
        ]:
            if k in header:  # check the length
                if len(header[k]) != trace_num:
                    raise ValueError(
                        f"Expected the length of header['{k}'] to be {trace_num}."
                    )
            else:  # init with default value
                if k in ["latitude", "longitude", "elevation"]:
                    header[k] = [np.nan for _ in range(trace_num)]
                elif k in ["network", "station", "channel"]:
                    header[k] = ["" for _ in range(trace_num)]

        # set other default parameters
        self.stats = Stats(header)

        # set data without changing npts in stats object
        super().__setattr__("data", data)

    def __setattr__(self, key, value):
        """
        any change in Stream.data will dynamically set Stream.stats.npts and Stream.stats.trace_num
        """
        if key == "data":
            _data_sanity_checks(value)
            self.stats.npts = value.shape[1]
            self.stats.trace_num = value.shape[0]
        return super().__setattr__(key, value)

    def __str__(self):
        id = f"* ID:\n      {self.id}"
        stats = f"* STATS:\n{textwrap.indent(str(self.stats), '  ')}"
        data = (
            "* DATA:\n"
            f"       shape: {self.data.shape}\n"
            f"       dtype: {self.data.dtype}\n"
            f"      masked: {np.ma.isMaskedArray(self.data)}\n"
            f"{textwrap.indent(np.array2string(self.data, threshold=MAX_DATA_THRESHOLD), '      ')}"
        )
        info = "\n".join([id, stats, data])
        return info

    def __repr__(self):
        return str(self)

    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text(f"{self.__class__.__name__}(...)")
        else:
            p.text(str(self))

    def __eq__(self, other):
        return shakecore.core.operator.operator_stream.__eq__(self, other)

    def __ne__(self, other):
        return shakecore.core.operator.operator_stream.__ne__(self, other)

    def __lt__(self, other):
        return shakecore.core.operator.operator_stream.__lt__(self, other)

    def __le__(self, other):
        return shakecore.core.operator.operator_stream.__le__(self, other)

    def __gt__(self, other):
        return shakecore.core.operator.operator_stream.__gt__(self, other)

    def __ge__(self, other):
        return shakecore.core.operator.operator_stream.__ge__(self, other)

    def __nonzero__(self):
        return shakecore.core.operator.operator_stream.__nonzero__(self)

    def __mul__(self, num):
        return shakecore.core.operator.operator_stream.__mul__(self, num)

    def __sub__(self, other):
        return shakecore.core.operator.operator_stream.__sub__(self, other)

    def __floordiv__(self, other):
        return shakecore.core.operator.operator_stream.__floordiv__(self, other)

    def __truediv__(self, other):
        return shakecore.core.operator.operator_stream.__truediv__(self, other)

    def __pow__(self, other):
        return shakecore.core.operator.operator_stream.__pow__(self, other)

    def __add__(
        self,
        stream,
        method=0,
        interpolation_samples=0,
        fill_value=None,
        sanity_checks=True,
    ):
        return shakecore.core.operator.operator_stream.__add__(
            self, stream, method, interpolation_samples, fill_value, sanity_checks
        )

    def copy(self):
        """
        Return a deep copy of the Stream object.

        :returns: Deep copy of Stream object.
        :rtype: :class:`~shakecore.core.stream.Stream`
        """
        return copy.deepcopy(self)

    # --- io funcs --- #
    write = shakecore.io.write
    to_obspy = shakecore.io.to_obspy

    # --- manipulation funcs --- #
    _internal_add_processing_info = (
        shakecore.core.manipulation.manipulation_stream._internal_add_processing_info
    )
    id = shakecore.core.manipulation.manipulation_stream.id
    table = shakecore.core.manipulation.manipulation_stream.table
    show = shakecore.core.manipulation.manipulation_stream.show
    # _show_table = shakecore.core.manipulation.manipulation_stream._show_table   # [widgets version] departed
    _show_figure = shakecore.core.manipulation.manipulation_stream._show_figure
    times = shakecore.core.manipulation.manipulation_stream.times
    add = shakecore.core.manipulation.manipulation_stream.add
    extend = shakecore.core.manipulation.manipulation_stream.extend
    delete = shakecore.core.manipulation.manipulation_stream.delete
    select = shakecore.core.manipulation.manipulation_stream.select
    _rtrim = shakecore.core.manipulation.manipulation_stream._rtrim
    _ltrim = shakecore.core.manipulation.manipulation_stream._ltrim
    trim = shakecore.core.manipulation.manipulation_stream.trim
    aligntime = shakecore.core.manipulation.manipulation_stream.aligntime
    sort = shakecore.core.manipulation.manipulation_stream.sort
    split = shakecore.core.manipulation.manipulation_stream.split
    slide = shakecore.core.manipulation.manipulation_stream.slide

    # --- signal funcs --- #
    max = shakecore.signal.max
    std = shakecore.signal.std
    mean = shakecore.signal.mean
    normalize = shakecore.signal.normalize
    integrate = shakecore.signal.integrate
    differentiate = shakecore.signal.differentiate
    taper = shakecore.signal.taper
    detrend = shakecore.signal.detrend
    filter = shakecore.signal.filter
    resample = shakecore.signal.resample
    decimate = shakecore.signal.decimate
    remove_response = shakecore.signal.remove_response
    rotate = shakecore.signal.rotate
    interpolate = shakecore.signal.interpolate

    # --- ppsd funcs --- #
    ppsd = shakecore.ppsd.ppsd

    # --- beamforming funcs --- #
    beamforming = shakecore.beamforming.beamforming

    # --- convert funcs --- #
    @property
    def conv(self):
        """The Convertion namespace"""
        return Conv(self)

    # --- viz funcs --- #
    @property
    def viz(self):
        """The Visualization namespace"""
        return Viz(self)
