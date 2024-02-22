import os

import numpy as np
from numba import jit
from scipy.optimize import minimize

numba_threads = int(os.getenv("NUMBA_NUM_THREADS", "1"))
parallel = True if numba_threads != 1 else False

"""_summary_

Modified from https://github.com/msacchi/Radon_Py/tree/master and https://github.com/PyLops/pylops

Plan to use implement GPU acceleration using numba for `forward` and `adjoint` in the future.
"""


@jit(nopython=True)
def _linear(
    x: float,
    t: float,
    p: float,
) -> np.ndarray:
    return t + p * x


@jit(nopython=True)
def _parabolic(
    x: float,
    t: float,
    p: float,
) -> np.ndarray:
    return t + p * x**2


@jit(nopython=True)
def _hyperbolic(
    x: float,
    t: float,
    p: float,
) -> np.ndarray:
    return np.sqrt(t**2 + (x / p) ** 2)


@jit(nopython=True, parallel=parallel, nogil=True)
def _radon_adjoint(data, dt, dx, p_vec, func):
    p_num = len(p_vec)
    x_num, npts = data.shape
    model = np.zeros((p_num, npts))
    for itau in range(0, npts):
        for ix in range(0, x_num):
            for ip in range(0, p_num):
                t = func(float(ix * dx), float(itau * dt), float(p_vec[ip]))
                it = int(t / dt)
                if it >= 0 and it < npts:
                    model[ip, itau] += data[ix, it]

    return model


@jit(nopython=True, parallel=parallel, nogil=True)
def _radon_forward(model, dt, dx, x_num, p_vec, func):
    p_num, npts = model.shape
    data = np.zeros((x_num, npts))
    for itau in range(0, npts):
        for ix in range(0, x_num):
            for ip in range(0, p_num):
                t = func(float(ix * dx), float(itau * dt), float(p_vec[ip]))
                it = int(t / dt)
                if it >= 0 and it < npts:
                    data[ix, it] += model[ip, itau]

    return data


def radon_adjoint(data, dt, dx, p_vec, kind="linear"):
    if kind == "linear":
        func = _linear
    elif kind == "parabolic":
        func = _parabolic
    elif kind == "hyperbolic":
        func = _hyperbolic
    elif callable(kind):
        func = kind
    else:
        raise ValueError(
            "kind must be 'linear', 'parabolic', 'hyperbolic', or callable"
        )

    return _radon_adjoint(data, dt, dx, p_vec, func)


def radon_forward(model, dt, dx, x_num, p_vec, kind="linear"):
    if kind == "linear":
        func = _linear
    elif kind == "parabolic":
        func = _parabolic
    elif kind == "hyperbolic":
        func = _hyperbolic
    elif callable(kind):
        func = kind
    else:
        raise ValueError(
            "kind must be 'linear', 'parabolic', 'hyperbolic', or callable"
        )

    return _radon_forward(model, dt, dx, x_num, p_vec, func)


def obj_function(model_flat, data, dt, dx, p_vec, kind):
    x_num = data.shape[0]
    model = model_flat.reshape((-1, data.shape[1]))
    Lm = radon_forward(model, dt, dx, x_num, p_vec, kind)

    return np.sum(np.sum((Lm - data) ** 2))


def grad_function(model_flat, data, dt, dx, p_vec, kind):
    x_num = data.shape[0]
    model = model_flat.reshape((-1, data.shape[1]))
    Lm = radon_forward(model, dt, dx, x_num, p_vec, kind)
    residual = Lm - data
    grad = radon_adjoint(residual, dt, dx, p_vec, kind)  # L^T (Lm - d)
    grad_flat = grad.ravel()

    return grad_flat


def radon_inverse(data, dt, dx, p_vec, kind, method="CG", options={}):
    p_num = len(p_vec)
    npts = data.shape[1]
    model_0_flat = np.zeros((p_num, npts)).ravel()

    results = minimize(
        fun=obj_function,
        x0=model_0_flat,
        args=(data, dt, dx, p_vec, kind),
        method=method,
        jac=grad_function,
        options=options,
    )

    model = results.x.reshape((-1, npts))

    return model
