from shakecore.core.utils import _add_processing_info


@_add_processing_info
def pressure_2_velocity(self, media_density=1000, media_velocity=1450, device="cpu"):
    """
    velocity = pressure / (media_density * media_velocity)

    For water, media_density = 1000 kg/m^3, media_velocity = 1450 m/s
    """
    if device == "cpu":
        velocity = self.data / (media_density * media_velocity)
    elif device == "cuda":
        pass

    self.data = velocity
    self.stats.type = "velocity"


@_add_processing_info
def velocity_2_pressure(self, media_density=1000, media_velocity=1450, device="cpu"):
    """
    pressure = velocity * media_density * media_velocity

    For water, media_density = 1000 kg/m^3, media_velocity = 1450 m/s
    """
    if device == "cpu":
        pressure = self.data * media_density * media_velocity
    elif device == "cuda":
        pass

    self.data = pressure
    self.stats.type = "pressure"
