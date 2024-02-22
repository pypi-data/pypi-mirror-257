import matplotlib.pyplot as plt
import numpy as np


def ricker(dt, f0):
    # Ricker wavelet of central frequency f0 sampled every dt seconds

    nw = 2.5 / f0 / dt
    nw = 2 * int(nw / 2)
    nc = int(nw / 2)
    a = f0 * dt * 3.14159265359
    n = a * np.arange(-nc, nc)
    b = n**2
    return (1 - 2 * b) * np.exp(-b)


def wigb(data, dt, h, scale, color):
    # Plot wiggle seismic plot (python version of Xin-gong Li faumous wigb.m)

    nx, nt = data.shape
    dmax = np.max(data)
    data = data / dmax
    t = np.linspace(0, (nt - 1) * dt, nt)
    tmax = np.amax(t)
    hmin = np.amin(h)
    hmax = np.amax(h)

    c = scale * np.mean(np.diff(h))

    plt.axis([hmin - 2 * c, hmax + 2 * c, tmax, 0.0])
    data[:, nt - 1] = 0
    data[:, 0] = 0
    for k in range(0, nx):
        s = data[k, :] * c
        plt.plot(s + h[k], t, color, linewidth=1)
        b = h[k] + s.clip(min=0)
        plt.fill(b, t, color)

    return
