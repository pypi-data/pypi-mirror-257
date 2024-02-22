import copy
from collections.abc import MutableMapping

import numpy as np
from obspy import UTCDateTime

from shakecore.setting import MAX_DATA_THRESHOLD


def _all_numbers(lst):
    return all(isinstance(x, (int, float)) for x in lst)


def _all_strings(lst):
    return all(isinstance(x, str) for x in lst)


class Stats(MutableMapping):
    """
    Stats is a dictionary-like object that holds meta__dict__ for a Stream.

    Examples

    >>> from shakecore.core.stats import Stats
    >>> stats = Stats()
        starttime: 1970-01-01T00:00:00.000000Z
          endtime: 1970-01-01T00:00:00.000000Z
    sampling_rate: 1.0
            delta: 1.0
         interval: nan
             npts: 0
        trace_num: 0
             unit: "unknown"
          network: []
          station: []
          channel: []
         latitude: []
        longitude: []
        elevation: []
       processing: []
            notes: {}
    >>> stats["starttime"] = UTCDateTime(2018, 1, 1)
    """

    # set of read only attrs
    readonly = ["endtime"]

    # default values
    defaults = {
        "starttime": UTCDateTime(0),
        "endtime": UTCDateTime(0),
        "sampling_rate": 1.0,
        "delta": 1.0,
        "interval": np.nan,
        "npts": 0,
        "trace_num": 0,
        "type": "unknown",
        "network": [],
        "station": [],
        "channel": [],
        "latitude": [],
        "longitude": [],
        "elevation": [],
        "processing": [],
        "notes": {},
    }
    defaults_types = {
        "starttime": UTCDateTime,
        "endtime": UTCDateTime,
        "sampling_rate": float,
        "delta": float,
        "interval": float,
        "npts": int,
        "trace_num": int,
        "type": str,
        "network": list,
        "station": list,
        "channel": list,
        "latitude": list,
        "longitude": list,
        "elevation": list,
        "processing": list,
        "notes": dict,
    }

    # keys which need to refresh derived values
    refresh_keys = {"starttime", "sampling_rate", "delta", "npts"}

    def __init__(self, *args, **kwargs):
        self.__dict__.update(copy.deepcopy(self.defaults))
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        # check key type
        if key in self.defaults and not isinstance(value, self.defaults_types[key]):
            msg = "Value of %s must be %s!"
            raise TypeError(msg % (key, self.defaults_types[key]))

        # check key value type
        if key in ["network", "station", "channel"] and not _all_strings(value):
            raise TypeError(f"Expected header['{key}'] to be a list of strings.")
        elif key in ["latitude", "longitude", "elevation"] and not _all_numbers(value):
            raise TypeError(f"Expected header['{key}'] to be a list of numbers.")

        # refresh derived values
        if key in self.readonly:
            msg = 'Attribute "%s" in %s object is read only!'
            raise AttributeError(msg % (key, self.__class__.__name__))
        elif key in self.refresh_keys:
            # ensure correct __dict__ type
            if key == "delta":
                key = "sampling_rate"
                try:
                    value = 1.0 / float(value)
                except ZeroDivisionError:
                    value = 0.0
            elif key == "sampling_rate":
                value = float(value)
            elif key == "starttime":
                value = UTCDateTime(value)
            elif key == "npts":
                if not isinstance(value, int):
                    value = int(value)
            # set current key
            self.__dict__[key] = value
            # set derived value: delta
            try:
                delta = 1.0 / float(self.sampling_rate)
            except ZeroDivisionError:
                delta = 0.0
            self.__dict__["delta"] = delta
            # set derived value: endtime
            if self.npts == 0:
                timediff = 0
            else:
                timediff = float(self.npts - 1) * delta
            self.__dict__["endtime"] = self.starttime + timediff
        else:
            self.__dict__[key] = value

    __setattr__ = __setitem__

    def __delitem__(self, key):
        if key in self.defaults:
            pass
        else:
            del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.__dict__)

    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text(f"{self.__class__.__name__}(...)")
        else:
            p.text(str(self))

    def __str__(self, min_label_length=16):
        keys = list(self.keys())
        defaults_keys = list(self.defaults.keys())

        # sort keys with defaults first
        other_keys = [k for k in keys if k not in defaults_keys]
        sorted_keys = defaults_keys + sorted(other_keys)

        # determine longest key name for alignment of all items
        i = max(max([len(k) for k in keys]), min_label_length)
        pattern = "%%%ds: %%s" % (i)
        head = []
        for k in sorted_keys:
            if k in [
                "network",
                "station",
                "channel",
                "latitude",
                "longitude",
                "elevation",
            ]:
                info = np.array2string(
                    np.array(self.__dict__[k]),
                    threshold=MAX_DATA_THRESHOLD,
                    separator=", ",
                )
            else:
                info = self.__dict__[k]
            head.append(pattern % (k, info))

        return "\n".join(head)

    def __getstate__(self):
        state = self.__dict__.copy()
        # remove the unneeded entries
        state.pop("delta", None)
        state.pop("endtime", None)
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # trigger refreshing
        self.__setitem__("sampling_rate", state["sampling_rate"])

    def copy(self):
        return copy.deepcopy(self)

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).items():
            if key in self.readonly:
                pass
            else:
                self.__setitem__(key, value)
