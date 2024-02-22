from shakecore.core.utils import FunctionDescriptor

from .das import (
    deformation_rate_2_strain_rate,
    strain_rate_2_velocity,
    velocity_2_strain_rate,
)
from .hydrophone import pressure_2_velocity, velocity_2_pressure
from .map import map


class Conv:
    def __init__(self, instance):
        self.instance = instance

    map = FunctionDescriptor(map)
    deformation_rate_2_strain_rate = FunctionDescriptor(deformation_rate_2_strain_rate)
    strain_rate_2_velocity = FunctionDescriptor(strain_rate_2_velocity)
    velocity_2_strain_rate = FunctionDescriptor(velocity_2_strain_rate)
    velocity_2_pressure = FunctionDescriptor(velocity_2_pressure)
    pressure_2_velocity = FunctionDescriptor(pressure_2_velocity)
