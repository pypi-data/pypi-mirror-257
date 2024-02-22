from shakecore.core.utils import _add_processing_info

from .denoise import (
    afk_cpu,
    bandpass_cpu,
    bandpass_cuda,
    bandstop_cpu,
    bandstop_cuda,
    curvelet_cpu,
    fk_cpu,
    highpass_cpu,
    highpass_cuda,
    lowpass_cpu,
    lowpass_cuda,
    medfilt_cpu,
    medfilt_cuda,
    radon_cpu,
)


@_add_processing_info
def filter(self, type="bandpass", device="cpu", **options):
    if device == "cpu":
        if type == "bandpass":
            self.data = bandpass_cpu(self.data, df=self.stats.sampling_rate, **options)
        elif type == "lowpass":
            self.data = lowpass_cpu(self.data, df=self.stats.sampling_rate, **options)
        elif type == "highpass":
            self.data = highpass_cpu(self.data, df=self.stats.sampling_rate, **options)
        elif type == "bandstop":
            self.data = bandstop_cpu(self.data, df=self.stats.sampling_rate, **options)
        elif type == "medfilt":
            self.data = medfilt_cpu(self.data, **options)
        elif type == "fk":
            self.data = fk_cpu(
                self.data, dx=self.stats.interval, dt=self.stats.delta, **options
            )
        elif type == "radon":
            self.data = radon_cpu(
                self.data,
                dx=self.stats.interval,
                dt=self.stats.delta,
                **options,
            )
        elif type == "curvelet":
            self.data = curvelet_cpu(self.data, **options)
        elif type == "afk":
            self.data = afk_cpu(self.data, **options)
        else:
            raise ValueError(f"Unknown filter type '{type}'.")

    elif device == "cuda":
        if type == "bandpass":
            self.data = bandpass_cuda(self.data, df=self.stats.sampling_rate, **options)
        elif type == "lowpass":
            self.data = lowpass_cuda(self.data, df=self.stats.sampling_rate, **options)
        elif type == "highpass":
            self.data = highpass_cuda(self.data, df=self.stats.sampling_rate, **options)
        elif type == "bandstop":
            self.data = bandstop_cuda(self.data, df=self.stats.sampling_rate, **options)
        elif type == "medfilt":
            self.data = medfilt_cuda(self.data, **options)
        else:
            raise ValueError(f"Unknown filter type '{type}'.")
    else:
        raise ValueError(f"Unknown device '{device}'.")
