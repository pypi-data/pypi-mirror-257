from .sc import sc_write


def write(self, filename, format=None, backend="obspy", **kwargs):
    if backend == "obspy":
        self.to_obspy().write(filename, format, **kwargs)
    elif backend == "shakecore":
        write_shakecore(self, filename, format)
    else:
        raise ValueError(f"Unrecognized backend: {backend}")


def write_shakecore(self, filename, format):
    if format == "sc":
        sc_write(self, filename)
    else:
        raise ValueError(f"Unrecognized format: {format}")
