import copy

import numpy as np

from shakecore.core.utils import create_empty_data_chunk


def __eq__(self, other):
    """
    Implements rich comparison of Stream objects for "==" operator.
    """
    # check if other is a Stream object
    if not isinstance(other, type(self)):
        return False
    # comparison of Stats objects is supported by underlying AttribDict
    if not self.stats == other.stats:
        return False
    # comparison of ndarrays is supported by NumPy
    if not np.array_equal(self.data, other.data):
        return False

    return True


def __ne__(self, other):
    """
    Implements rich comparison of Stream objects for "!=" operator.
    """
    return not self.__eq__(other)


def __lt__(self, other):
    """
    Too ambiguous, throw an Error.
    """
    raise NotImplementedError("Too ambiguous, therefore not implemented.")


def __le__(self, other):
    """
    Too ambiguous, throw an Error.
    """
    raise NotImplementedError("Too ambiguous, therefore not implemented.")


def __gt__(self, other):
    """
    Too ambiguous, throw an Error.
    """
    raise NotImplementedError("Too ambiguous, therefore not implemented.")


def __ge__(self, other):
    """
    Too ambiguous, throw an Error.
    """
    raise NotImplementedError("Too ambiguous, therefore not implemented.")


def __nonzero__(self):
    """
    No data means no trace.
    """
    return bool(len(self.data))


def __sub__(self, num):
    """
    Subtract a scalar from stream.
    """
    if not isinstance(num, (int, float)):
        raise TypeError("Only numbers can be subtracted with traces.")
    new = self.copy()
    new.data -= num
    return new


def __truediv__(self, num):
    """
    Divide stream by a scalar.
    """
    if not isinstance(num, (int, float)):
        raise TypeError("Only numbers can be divided with traces.")
    new = self.copy()
    new.data /= num
    return new


def __floordiv__(self, num):
    """
    Divide stream by a scalar.
    """
    if not isinstance(num, (int, float)):
        raise TypeError("Only numbers can be divided with traces.")
    new = self.copy()
    new.data //= num
    return new


def __pow__(self, num):
    """
    Divide stream by a scalar.
    """
    if not isinstance(num, (int, float)):
        raise TypeError("Only numbers can be divided with traces.")
    new = self.copy()
    new.data **= num
    return new


def __mul__(self, num):
    """
    Multiply stream with a scalar.
    """
    if not isinstance(num, (int, float)):
        raise TypeError("Only numbers can be multiplied with traces.")
    new = self.copy()
    new.data *= num
    return new


def __add__(
    self,
    stream,
    method=0,
    interpolation_samples=0,
    fill_value=None,
    sanity_checks=True,
):
    if isinstance(stream, (int, float)):
        new = self.copy()
        new.data += stream
        return new
    elif isinstance(stream, type(self)):
        if sanity_checks:
            #  check id
            if self.id != stream.id:
                raise TypeError("stream ID differs: %s vs %s" % (self.id, stream.id))
            #  check sample rate
            if self.stats.sampling_rate != stream.stats.sampling_rate:
                raise TypeError(
                    "Sampling rate differs: %s vs %s"
                    % (self.stats.sampling_rate, stream.stats.sampling_rate)
                )
            if self.stats.type != stream.stats.type:
                raise TypeError(
                    "Data type differs: %s vs %s" % (self.stats.type, stream.stats.type)
                )
            # check data type
            if self.data.dtype != stream.data.dtype:
                raise TypeError(
                    "Data type differs: %s vs %s" % (self.data.dtype, stream.data.dtype)
                )
        # check times
        if self.stats.starttime <= stream.stats.starttime:
            lt = self
            rt = stream
        else:
            rt = self
            lt = stream
        trace_num = lt.data.shape[0]
        # check whether to use the latest value to fill a gap
        if fill_value == "latest":
            fill_value = lt.data[:, -1]
        elif fill_value == "interpolate":
            fill_value = (lt.data[:, -1], rt.data[:, 0])
        sr = self.stats.sampling_rate
        delta = (rt.stats.starttime - lt.stats.endtime) * sr
        delta = round(delta) - 1
        delta_endtime = lt.stats.endtime - rt.stats.endtime

        # check if overlap or gap
        if delta < 0 and delta_endtime < 0:  # 右边的部分在里面了
            # overlap
            delta = abs(delta)
            if np.all(np.equal(lt.data[:, -delta:], rt.data[:, :delta])):
                # check if data are the same
                data = [lt.data[:, :-delta], rt.data]
            elif method == 0:
                overlap = create_empty_data_chunk(
                    trace_num, delta, lt.data.dtype, fill_value
                )
                data = [lt.data[:, :-delta], overlap, rt.data[:, delta:]]
            elif method == 1 and interpolation_samples >= -1:
                try:
                    ls = lt.data[:, -delta - 1]
                except Exception:
                    ls = lt.data[:, 0]
                if interpolation_samples == -1:
                    interpolation_samples = delta
                elif interpolation_samples > delta:
                    interpolation_samples = delta
                try:
                    rs = rt.data[:, interpolation_samples]
                except IndexError:
                    # contained trace
                    data = [lt.data]
                else:
                    # include left and right sample (delta + 2)
                    interpolation = np.empty((trace_num, interpolation_samples + 2))
                    for i in range(0, trace_num):
                        interpolation[i, :] = np.linspace(
                            ls[i], rs[i], interpolation_samples + 2
                        )
                    # cut ls and rs and ensure correct data type
                    interpolation = np.require(interpolation[:, 1:-1], lt.data.dtype)
                    data = [
                        lt.data[:, :-delta],
                        interpolation,
                        rt.data[:, interpolation_samples:],
                    ]
            else:
                raise NotImplementedError
        elif delta < 0 and delta_endtime >= 0:  # 右边的全包在里面了
            # contained trace
            delta = abs(delta)
            lenrt = rt.data.shape[1]
            t1 = lt.data.shape[1] - delta
            t2 = t1 + lenrt
            data = np.empty((trace_num, lt.data.shape[1]))
            for i in range(0, trace_num):
                # check if data are the same
                data_equal = lt.data[i, t1:t2] == rt.data[i, :]
                # force a masked array and fill it for check of equality of valid data points
                dd = None
                if np.all(np.ma.masked_array(data_equal).filled()):
                    if isinstance(data_equal, np.ma.masked_array):
                        x = np.ma.masked_array(lt.data[i, t1:t2])
                        y = np.ma.masked_array(rt.data[i, :])
                        data_same = np.choose(x.mask, [x, y])
                        dd = np.choose(x.mask & y.mask, [data_same, np.nan])
                        if np.any(np.isnan(dd)):
                            dd = np.ma.masked_invalid(dd)
                        # convert back to maximum dtype of original data
                        dtype = np.max((x.dtype, y.dtype))
                        dd = dd.astype(dtype)
                        dd = np.concatenate(
                            [lt.data[i, :t1], dd, lt.data[i, t2:]], axis=0
                        )
                    else:
                        dd = lt.data[i, :]
                elif method == 0:
                    gap = create_empty_data_chunk(1, lenrt, lt.data.dtype, fill_value)
                    dd = np.concatenate(
                        [lt.data[i, :t1], gap[0], lt.data[i, t2:]], axis=0
                    )
                elif method == 1:
                    dd = lt.data[i, :]
                else:
                    raise NotImplementedError
                data[i, :] = dd
            data = [data]
        elif delta == 0:
            # exact fit - merge both traces
            data = [lt.data, rt.data]
        else:
            # gap
            # use fixed value or interpolate in between
            gap = create_empty_data_chunk(trace_num, delta, lt.data.dtype, fill_value)
            data = [lt.data, gap, rt.data]
        # merge traces depending on NumPy array type
        if True in [isinstance(_i, np.ma.masked_array) for _i in data]:
            data = np.ma.concatenate(data, axis=1)
        else:
            data = np.concatenate(data, axis=1)
            data = np.require(data, dtype=lt.data.dtype)
        # Check if we can downgrade to normal ndarray
        if isinstance(data, np.ma.masked_array) and np.ma.count_masked(data) == 0:
            data = data.compressed()
        # create the returned trace
        out = self.__class__(data=data, header=copy.deepcopy(lt.stats))
        return out
    else:
        raise TypeError("Cannot add Stream and %s" % type(stream))
