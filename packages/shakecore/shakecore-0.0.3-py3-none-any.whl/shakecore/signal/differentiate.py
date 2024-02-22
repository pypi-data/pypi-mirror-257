import numpy as np

from shakecore.core.utils import _add_processing_info

try:
    import cupy as cp

    GUDA_MODE = True
except Exception:
    GUDA_MODE = False

TYPES = {
    "unknown": "unknown",
    "displacement": "velocity",
    "velocity": "acceleration",
    "acceleration": "unknown",
    "pressure": "unknown",
    "strain_rate": "unknown",
    "strain": "strain_rate",
    "deformation_rate": "unknown",
}


@_add_processing_info
def differentiate(self, type="gradient", edge_order=2, device="cpu"):
    if device == "cpu":
        if type == "gradient":
            self.data = gradient_cpu(
                self.data,
                dx=self.stats.delta,
                edge_order=edge_order,
            )
        else:
            raise ValueError(f"Unknown differentiate type '{type}'.")
        self.stats.type = TYPES[self.stats.type]

    elif device == "cuda":
        if type == "gradient":
            self.data = gradient_cuda(
                self.data,
                dx=self.stats.delta,
                edge_order=edge_order,
            )
        else:
            raise ValueError(f"Unknown differentiate type '{type}'.")
        self.stats.type = TYPES[self.stats.type]

    else:
        raise ValueError(f"Unknown device '{device}'.")


# *************************************************************************************************
def gradient_cpu(data, dx, edge_order):
    out = np.gradient(data, dx, axis=-1, edge_order=edge_order)

    return out


def gradient_cuda(data, dx, edge_order):
    # Ensure data is a cupy ndarray
    data = cp.asarray(data)
    out = cp.gradient(data, dx, axis=-1, edge_order=edge_order)

    return out
