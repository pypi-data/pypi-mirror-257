import scipy

from shakecore.core.utils import _add_processing_info
from shakecore.signal.denoise import lowpass_cheby_2_cpu, lowpass_cheby_2_cuda


@_add_processing_info
def decimate(self, factor, type="simple", device="cpu", **options):
    """
    factor (int): Decimation factor.

    """
    if device == "cpu":
        if type == "simple":
            self.data = simple_cpu(
                self.data, factor, self.stats.sampling_rate, **options
            )
        elif type == "anti_aliasing":
            self.data = anti_aliasing_cpu(
                self.data, factor, self.stats.sampling_rate, **options
            )
        else:
            raise ValueError(f"Unknown filter type '{type}'.")
        self.stats.sampling_rate = self.stats.sampling_rate / float(factor)

    elif device == "cuda":
        if type == "simple":
            self.data = simple_cuda(
                self.data, factor, self.stats.sampling_rate, **options
            )
        elif type == "anti_aliasing":
            raise NotImplementedError
        else:
            raise ValueError(f"Unknown filter type '{type}'.")
        self.stats.sampling_rate = self.stats.sampling_rate / float(factor)

    else:
        raise ValueError(f"Unknown device '{device}'.")


# *************************************************************************************************
def simple_cpu(data, factor, sampling_rate, no_filter=False, strict_length=False):
    # check if end time changes and this is not explicitly allowed
    if strict_length and len(data) % factor:
        msg = "End time of trace would change and strict_length=True."
        raise ValueError(msg)

    # do automatic lowpass filtering
    if not no_filter:
        # be sure filter still behaves good
        if factor > 16:
            msg = (
                "Automatic filter design is unstable for decimation "
                + "factors above 16. Manual decimation is necessary."
            )
            raise ArithmeticError(msg)
        freq = sampling_rate * 0.5 / float(factor)
        data = lowpass_cheby_2_cpu(data, df=sampling_rate, freq=freq, maxorder=12)

    data = data[:, ::factor]

    return data


def anti_aliasing_cpu(data, factor, _):
    factor = int(factor)
    if factor > 13:
        msg = (
            "IRR filter is unstable for decimation factors above"
            " 13. Call decimate multiple times."
        )
        raise ValueError(msg)

    return scipy.signal.decimate(data, factor, ftype="iir", axis=1, zero_phase=True)


def simple_cuda(data, factor, sampling_rate, no_filter=False, strict_length=False):
    # check if end time changes and this is not explicitly allowed
    if strict_length and len(data) % factor:
        msg = "End time of trace would change and strict_length=True."
        raise ValueError(msg)

    # do automatic lowpass filtering
    if not no_filter:
        # be sure filter still behaves good
        if factor > 16:
            msg = (
                "Automatic filter design is unstable for decimation "
                + "factors above 16. Manual decimation is necessary."
            )
            raise ArithmeticError(msg)
        freq = sampling_rate * 0.5 / float(factor)
        data = lowpass_cheby_2_cuda(data, df=sampling_rate, freq=freq, maxorder=12)

    data = data[:, ::factor]

    return data
