from shakecore.core.utils import FunctionDescriptor

from .dayplot import dayplot
from .fk import fk
from .geometry import geometry
from .plot import plot
from .radon import radon
from .spectrogram import spectrogram
from .waterfall import waterfall


class Viz:
    def __init__(self, instance):
        self.instance = instance

    fk = FunctionDescriptor(fk)
    plot = FunctionDescriptor(plot)
    radon = FunctionDescriptor(radon)
    dayplot = FunctionDescriptor(dayplot)
    waterfall = FunctionDescriptor(waterfall)
    spectrogram = FunctionDescriptor(spectrogram)
    geometry = FunctionDescriptor(geometry)
