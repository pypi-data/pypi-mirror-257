import numpy as np

from shakecore.core.utils import _add_processing_info


def max(self, axis="all"):  # trace time all
    if axis == "trace":
        value = np.max(np.abs(self.data), axis=0)
        return value
    elif axis == "time":
        value = np.max(np.abs(self.data), axis=1)
        return value
    elif axis == "all":
        value = np.max(np.abs(self.data))
        return value
    else:
        raise ValueError("axis must be 'trace', 'time' or 'all'")


def std(self, axis="all"):  # trace time all
    if axis == "trace":
        return np.std(self.data, axis=0)
    elif axis == "time":
        return np.std(self.data, axis=1)
    elif axis == "all":
        return np.std(self.data)
    else:
        raise ValueError("axis must be 'trace', 'time' or 'all'")


def mean(self, axis="all"):  # trace time all
    if axis == "trace":
        return np.mean(self.data, axis=0)
    elif axis == "time":
        return np.mean(self.data, axis=1)
    elif axis == "all":
        return np.mean(self.data)
    else:
        raise ValueError("axis must be 'trace', 'time' or 'all'")


@_add_processing_info
def normalize(self, axis="all"):  # trace time all
    if axis == "trace":
        self.data = self.data / np.max(np.abs(self.data), axis=0, keepdims=True)
    elif axis == "time":
        self.data = self.data / np.max(np.abs(self.data), axis=1, keepdims=True)
    elif axis == "all":
        self.data = self.data / np.max(np.abs(self.data))
    else:
        raise ValueError("axis must be 'trace', 'time' or 'all'")
