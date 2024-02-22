from shakecore.core.stream import Stream


def __add__(self, other):
    if isinstance(other, Stream):
        other = self.__class__([other])
    if not isinstance(other, type(self)):
        raise TypeError
    streams = self.streams + other.streams
    return self.__class__(streams=streams)


def __iadd__(self, other):
    if isinstance(other, Stream):
        self.append(other)
    elif isinstance(other, type(self)):
        self.streams += other.streams
    return self


def __mul__(self, other):
    """
    Too ambiguous, throw an Error.
    """
    raise NotImplementedError("Too ambiguous, therefore not implemented.")


def __iter__(self):
    return list(self.streams).__iter__()


def __len__(self):
    return len(self.streams)


def __eq__(self, other):
    return self.streams == other.streams


def __ne__(self, other):
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


def __setitem__(self, index, trace):
    """
    __setitem__ method of obspy.Stream objects.
    """
    self.streams.__setitem__(index, trace)


def __getitem__(self, index):
    """
    __getitem__ method of obspy.Stream objects.

    :return: Trace objects
    """
    if isinstance(index, slice):
        return self.__class__(streams=self.streams.__getitem__(index))
    else:
        return self.streams.__getitem__(index)


def __delitem__(self, index):
    """
    Passes on the __delitem__ method to the underlying list of streams.
    """
    return self.streams.__delitem__(index)
