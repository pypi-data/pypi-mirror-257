import copy

import numpy as np

import shakecore.core.manipulation.manipulation_pool
import shakecore.core.operator.operator_pool
from shakecore.core.stream import Stream


def _all_streams(lst):
    return all(isinstance(x, Stream) for x in lst)


class Pool:
    def __init__(self, streams=[]):
        self.streams = []
        if isinstance(streams, Stream):
            self.streams.extend([streams])
        elif isinstance(streams, list) and _all_streams(streams):
            self.streams.extend(streams)
        else:
            raise TypeError

    def __str__(self):
        info = str(len(self.streams)) + " stream(s) in Pool:\n"
        for i, stream in enumerate(self.streams):
            # set out string
            out = f"{stream.stats.trace_num:7d} trace(s) "
            starttime = str(stream.stats.starttime)
            endtime = str(stream.stats.endtime)
            delta = stream.stats.delta
            sampling_rate = stream.stats.sampling_rate
            npts = stream.stats.npts
            if stream.stats.sampling_rate < 0.1:
                out += f"| {starttime} - {endtime} | {delta:1f} Hz, {npts:d} npts"
            else:
                out += (
                    f"| {starttime} - {endtime} | {sampling_rate:1f} Hz, {npts:d} npts"
                )
            if np.ma.count_masked(stream.data):
                out += " (masked)\n"
            else:
                out += "\n"
            # cut out if too long
            if len(self.streams) <= 20:
                info += out
            else:
                if i < 10:
                    info += out
                elif i == 10:
                    info += "...\n"
                elif i > len(self.streams) - 10:
                    info += out
        return info

    def __repr__(self):
        return str(self)

    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text(f"{self.__class__.__name__}(...)")
        else:
            p.text(str(self))

    def __add__(self, other):
        return shakecore.core.operator.operator_pool.__add__(self, other)

    def __iadd__(self, other):
        return shakecore.core.operator.operator_pool.__iadd__(self, other)

    def __mul__(self, other):
        return shakecore.core.operator.operator_pool.__mul__(self, other)

    def __iter__(self):
        return list(self.streams).__iter__()

    def __len__(self):
        return len(self.streams)

    def __eq__(self, other):
        return shakecore.core.operator.operator_pool.__eq__(self, other)

    def __ne__(self, other):
        return shakecore.core.operator.operator_pool.__ne__(self, other)

    def __lt__(self, other):
        return shakecore.core.operator.operator_pool.__lt__(self, other)

    def __le__(self, other):
        return shakecore.core.operator.operator_pool.__le__(self, other)

    def __gt__(self, other):
        return shakecore.core.operator.operator_pool.__gt__(self, other)

    def __ge__(self, other):
        return shakecore.core.operator.operator_pool.__ge__(self, other)

    def __setitem__(self, index, trace):
        return shakecore.core.operator.operator_pool.__setitem__(self, index, trace)

    def __getitem__(self, index):
        return shakecore.core.operator.operator_pool.__getitem__(self, index)

    def __delitem__(self, index):
        return shakecore.core.operator.operator_pool.__delitem__(self, index)

    def __getslice__(self, i, j, k=1):
        return shakecore.core.operator.operator_pool.__getslice__(self, i, j, k)

    def copy(self):
        """
        Return a deep copy of the Stream object.

        :returns: Deep copy of Stream object.
        :rtype: :class:`~shakecore.core.stream.Stream`
        """
        return copy.deepcopy(self)

    # --- manipulation funcs --- #
    table = shakecore.core.manipulation.manipulation_pool.table
    show = shakecore.core.manipulation.manipulation_pool.show
    # _show_page = shakecore.core.manipulation.manipulation_pool._show_page   # [widgets version] departed
    _show_figure = shakecore.core.manipulation.manipulation_pool._show_figure
    append = shakecore.core.manipulation.manipulation_pool.append
    extend = shakecore.core.manipulation.manipulation_pool.extend
    delete = shakecore.core.manipulation.manipulation_pool.delete
    select = shakecore.core.manipulation.manipulation_pool.select
    trim = shakecore.core.manipulation.manipulation_pool.trim
    aligntime = shakecore.core.manipulation.manipulation_pool.aligntime
    sort = shakecore.core.manipulation.manipulation_pool.sort
    merge = shakecore.core.manipulation.manipulation_pool.merge
