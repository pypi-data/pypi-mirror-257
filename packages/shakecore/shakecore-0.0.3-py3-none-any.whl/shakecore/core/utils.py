import inspect

import numpy as np
from decorator import decorator


@decorator
def _add_processing_info(func, *args, **kwargs):
    """
    This is a decorator that attaches information about a processing call as a
    string to the Stream.stats.processing list.
    """
    callargs = inspect.getcallargs(func, *args, **kwargs)
    callargs.pop("self")
    kwargs_ = callargs.pop("kwargs", {})
    from shakecore import __version__

    info = "shakecore {version}: {function}(%s)".format(
        version=__version__, function=func.__name__
    )
    arguments = []
    arguments += [
        "%s=%s" % (k, repr(v)) if not isinstance(v, str) else "%s='%s'" % (k, v)
        for k, v in callargs.items()
    ]
    arguments += [
        "%s=%s" % (k, repr(v)) if not isinstance(v, str) else "%s='%s'" % (k, v)
        for k, v in kwargs_.items()
    ]
    arguments.sort()
    info = info % ", ".join(arguments)
    self = args[0]
    result = func(*args, **kwargs)
    # Attach after executing the function to avoid having it attached
    # while the operation failed.
    self._internal_add_processing_info(info)
    return result


def _data_sanity_checks(value):
    """
    Check if a given input is suitable to be used for Stream.data. Raises the
    corresponding exception if it is not, otherwise silently passes.
    """
    if not isinstance(value, np.ndarray):
        msg = "Stream.data must be a NumPy array."
        raise ValueError(msg)
    if value.ndim != 2:
        msg = (
            "NumPy array for Stream.data has bad shape ('%s'). Only 2-d "
            "arrays are allowed for initialization."
        ) % str(value.shape)
        raise ValueError(msg)


def create_empty_data_chunk(trace_num, delta, dtype, fill_value=None):
    """
    Creates an NumPy array depending on the given data type and fill value.

    If no ``fill_value`` is given a masked array will be returned.

    :param delta: Number of samples for data chunk
    :param dtype: NumPy dtype for returned data chunk
    :param fill_value: If ``None``, masked array is returned, else the
        array is filled with the corresponding value

    .. rubric:: Example

    >>> create_empty_data_chunk(3, 'int', 10)
    array([10, 10, 10])

    >>> create_empty_data_chunk(
    ...     3, 'f')  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    masked_array(data = [-- -- --],
                 mask = ...,
                 ...)
    """
    if fill_value is None:
        temp = np.ma.masked_all((trace_num, delta), dtype=np.dtype(dtype))
        # fill with nan if float number and otherwise with a very small number
        if issubclass(temp.data.dtype.type, np.integer):
            temp.data[:] = np.iinfo(temp.data.dtype).min
        else:
            temp.data[:] = np.nan
    elif (isinstance(fill_value, list) or isinstance(fill_value, tuple)) and len(
        fill_value
    ) == 2:
        # if two values are supplied use these as samples bordering to our data
        # and interpolate between:
        ls = fill_value[0]
        rs = fill_value[1]
        # include left and right sample (delta + 2)
        interpolation = np.empty((trace_num, delta + 2))
        for i in range(0, trace_num):
            interpolation[i, :] = np.linspace(ls[i], rs[i], delta + 2)
        # cut ls and rs and ensure correct data type
        temp = np.require(interpolation[:, 1:-1], dtype=np.dtype(dtype))
    else:
        temp = np.ones((trace_num, delta), dtype=np.dtype(dtype))
        temp *= fill_value
    return temp


class FunctionDescriptor:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:

            def wrapper(*args, **kwargs):
                return self.func(instance.instance, *args, **kwargs)

            return wrapper
