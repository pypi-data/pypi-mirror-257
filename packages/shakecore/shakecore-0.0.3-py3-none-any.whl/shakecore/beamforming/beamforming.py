import pickle
import textwrap
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from obspy import UTCDateTime
from scipy.fft import rfft
from scipy.linalg import pinvh
from spectrum import dpss

from shakecore.setting import MAX_DATA_THRESHOLD
from shakecore.utils import latlon_2_utm
from shakecore.viz.utils.viz_tools import _get_ax, _get_cmap

"""
Compute the steering vectors for the specified parameter range.
Modified from https://github.com/solldavid/TwistPy

"""


def format_vel_tick(value, tick_number):
    return f"{value} m/s"


def format_inc_tick(value, tick_number):
    return f"{value} °"


def compute_steering_vectors(
    coordinates,
    reference_receiver,
    dest_epsg,
    frequency: float,
    velocity: Union[float, tuple] = 6000,
    inclination: Union[float, tuple] = (-90, 90, 1),
    azimuth: tuple = (0, 360, 1),
) -> None:
    r"""Precompute the steering vectors

    Compute the steering vectors for the specified parameter range. For parameters that are specified as a tuple,
    the grid search is performed over the range: (min_value, max_value, increment)

    Parameters
    ----------
        frequency : :obj:`float`
            Discrete frequency at which beamforming is performed
        velocity : :obj:`float` or :obj:`tuple`
            Specifies the velocity as a float (if known) or grid over which search is performed
        inclination : :obj:`tuple`
            Specifies inclination grid over which search is performed
        azimuth : :obj:`tuple`
            Specifies azimuth grid over which search is performed

    """
    # number of stations
    N = coordinates.shape[0]

    # compute inclination, azimuth and velocity vectors
    if isinstance(velocity, tuple):
        velocity_gridded = np.arange(
            velocity[0],
            velocity[1] + velocity[2],
            velocity[2],
        )
    else:
        velocity_gridded = np.array([velocity])

    if isinstance(inclination, tuple):
        inclination_gridded = np.radians(
            np.arange(
                inclination[0],
                inclination[1] + inclination[2],
                inclination[2],
            )
        )
    else:
        inclination_gridded = np.radians(np.array([inclination]))

    azimuth_gridded = np.radians(
        np.arange(azimuth[0], azimuth[1] + azimuth[2], azimuth[2])
    )
    n_vel = len(velocity_gridded)
    n_inc = len(inclination_gridded)
    n_azi = len(azimuth_gridded)

    # create grid
    inclination_gridded, azimuth_gridded, velocity_gridded = np.meshgrid(
        inclination_gridded, azimuth_gridded, velocity_gridded, indexing="ij"
    )

    # compute relative coordinates, and convert lat/lon/elev to y/x/z
    utm_x, utm_y = latlon_2_utm(
        coordinates[:, 0], coordinates[:, 1], dest_epsg=dest_epsg
    )
    coords_utm = np.column_stack((utm_x, utm_y, coordinates[:, 2]))
    coords = coords_utm - np.tile(coords_utm[reference_receiver, :], (N, 1))
    coords = np.asmatrix(coords)

    # compute wave vector and wave number
    wave_vector_x = (np.sin(inclination_gridded) * np.cos(azimuth_gridded)).ravel()
    wave_vector_y = (np.sin(inclination_gridded) * np.sin(azimuth_gridded)).ravel()
    wave_vector_z = (np.cos(inclination_gridded)).ravel()
    wave_vector_x, wave_vector_y, wave_vector_z = (
        np.asmatrix(wave_vector_x).T,
        np.asmatrix(wave_vector_y).T,
        np.asmatrix(wave_vector_z).T,
    )
    wave_number = (-2 * np.pi * frequency / velocity_gridded).ravel()
    wave_number = np.asmatrix(wave_number).T

    # compute steering vectors, steering_vectors = exp(i * k * np.dot(wave_vector * coords))
    steering_vectors: np.ndarray = np.exp(
        1j
        * np.multiply(
            np.tile(wave_number, (1, N)),
            (
                wave_vector_x * coords[:, 0].T
                + wave_vector_y * coords[:, 1].T
                + wave_vector_z * coords[:, 2].T
            ),
        )
    )

    # ensure that steering vectors are unit vectors
    steering_vectors = steering_vectors / np.sqrt(N)

    return n_vel, n_inc, n_azi, steering_vectors


def cmmt(data: np.ndarray, Nw: int, freq_band: tuple, fsamp: float) -> np.ndarray:
    """Compute array data covariance matrix using the multitaper method

    Parameters
    ----------
    data : :obj:`~numpy.ndarray`
        Data as an array of dimensions (NxNt) with N being the number of stations in the array and Nt the number of time
        samples.
    Nw : :obj:`int`
        Number of tapers to use for the multi-taper method
    freq_band : :obj:`tuple`
         Frequency band within which covariance matrices are averaged as (fmin, fmax)
    fsamp : :obj:`float`
        Sampling rate of the data in Hz

    Returns
    -------
    C : :obj:`~numpy.ndarray` of :obj:`~numpy.complex128`
        Covariance matrix averaged within specified frequency band.

    """
    # number of stations (N), time sampling points (Nx)
    N, Nt = data.shape

    # next power of 2 (for FFT)
    NFFT = 2 ** int(np.log2(Nt) + 1) + 1

    # for very short windows, the frequency resolution might suffer
    if NFFT < 257:
        NFFT = 257

    # demean data
    data = (data.T - np.mean(data, axis=1)).T

    # compute slepian sequences and eigenvalues
    tapers, eigenvalues = dpss(N=Nt, NW=Nw)
    tapers = np.tile(tapers.T, [N, 1, 1])
    tapers = np.swapaxes(tapers, 0, 1)

    # compute weights from eigenvalues
    weights = eigenvalues / (np.arange(int(2 * Nw)) + 1).astype(float)

    # mutitaper spectral estimation
    S = rfft(np.multiply(tapers, data), 2 * NFFT, axis=-1)

    # inverse of weighted power spectrum for scaling
    Sk_inv = 1 / np.sqrt(np.sum((np.abs(S) ** 2).T * weights, axis=-1).T)

    # only compute covariance matrices within the specified frequency band
    df = fsamp / (2 * NFFT)
    f = np.arange(0, NFFT + 1) * df
    ind = (f >= freq_band[0]) & (f < freq_band[1])

    S = S[:, :, ind]
    Sk_inv = Sk_inv[:, ind]

    S = np.moveaxis(S, 1, 2)
    Sk_inv = np.moveaxis(Sk_inv, 0, 1)
    scales = np.einsum("...i,...j->...ij", Sk_inv, Sk_inv, optimize=True)

    # compute covariance matrix
    C = scales * (
        np.einsum("...i,...j->...ij", S, S.conj(), optimize=True).astype("complex")
        * np.tile(
            np.moveaxis(weights[np.newaxis, np.newaxis, np.newaxis], 3, 0),
            (1, S.shape[1], N, N),
        )
    )

    # sum over tapers
    C = np.sum(C, axis=0)

    # average over frequency range
    C = np.nanmean(C, axis=0)

    return C


def arf(
    coordinates,
    reference_receiver,
    dest_epsg,
    freq_band,
    velocity,
    inclination,
    azimuth,
):
    # number of stations
    N = coordinates.shape[0]

    # compute steering_vectors
    frequency = np.mean(freq_band)
    n_vel, n_inc, n_azi, steering_vectors = compute_steering_vectors(
        coordinates,
        reference_receiver,
        dest_epsg,
        frequency,
        velocity,
        inclination,
        azimuth,
    )

    # compute covariance matrix
    C = np.ones((N, N), dtype=np.complex128)

    # compute beamforming power
    P: np.ndarray = np.einsum(
        "sn, nk, sk->s",
        steering_vectors.conj(),
        C,
        steering_vectors,
        optimize=True,
    )

    # reshape beamforming power
    P_reshape = np.reshape(P, (n_inc, n_azi, n_vel))
    P = np.real(P_reshape)

    # generate beamforming object
    Beamforming_Data = Beamforming(
        P,
        coordinates,
        reference_receiver,
        "arf",
        freq_band,
        velocity,
        inclination,
        azimuth,
        number_of_sources=1,
        starttime=UTCDateTime(0),
        endtime=UTCDateTime(1),
    )

    return Beamforming_Data


def beamforming_load(filename):
    with open(filename, "rb") as f:
        beamforming_data = pickle.load(f)

    return beamforming_data


def beamforming_compute(
    data,
    sampling_rate,
    coordinates,
    reference_receiver,
    dest_epsg,
    method,
    freq_band,
    velocity,
    inclination,
    azimuth,
    number_of_sources,
):
    # number of stations
    N = coordinates.shape[0]

    # compute steering_vectors
    frequency = np.mean(freq_band)
    n_vel, n_inc, n_azi, steering_vectors = compute_steering_vectors(
        coordinates,
        reference_receiver,
        dest_epsg,
        frequency,
        velocity,
        inclination,
        azimuth,
    )

    # compute covariance matrix
    npts = data.shape[1]
    Nw = max(
        1,
        int(2 * (npts / sampling_rate) * (0.2 * freq_band[1])),
    )
    if method == "arf":
        C = np.ones((N, N), dtype=np.complex128)
    else:
        C = cmmt(data, Nw, freq_band=freq_band, fsamp=sampling_rate)

    # compute beamforming power
    if method == "music":
        evalues, evectors = np.linalg.eigh(C)
        noise_space: np.ndarray = (evectors[:, : N - number_of_sources]).dot(
            np.matrix.getH(evectors[:, : N - number_of_sources])
        )
        P: np.ndarray = 1 / np.einsum(
            "sn, nk, sk->s",
            steering_vectors.conj(),
            noise_space,
            steering_vectors,
            optimize=True,
        )
    elif method == "mvdr":
        P: np.ndarray = 1 / np.einsum(
            "sn, nk, sk->s",
            steering_vectors.conj(),
            pinvh(C),
            steering_vectors,
            optimize=True,
        )
    elif method == "bartleft":
        P: np.ndarray = np.einsum(
            "sn, nk, sk->s",
            steering_vectors.conj(),
            C,
            steering_vectors,
            optimize=True,
        )
    elif method == "arf":
        P: np.ndarray = np.einsum(
            "sn, nk, sk->s",
            steering_vectors.conj(),
            C,
            steering_vectors,
            optimize=True,
        )
    else:
        raise Exception(
            f"Unknown beam-forming method: '{method}'!. Available methods are: 'music', 'mvdr', 'bartleft'."
        )

    # reshape beamforming power
    P_reshape = np.reshape(P, (n_inc, n_azi, n_vel))

    return np.real(P_reshape)


def beamforming(
    self,
    dest_epsg,
    starttrace=None,
    endtrace=None,
    starttime=None,
    endtime=None,
    reference_receiver=0,
    method="music",
    freq_band=(0, None),
    velocity=6000,
    inclination=(0, 90, 1),
    azimuth=(0, 360, 1),
    number_of_sources=1,
):
    # check frequency band
    if freq_band[0] < 0:
        raise ValueError("fmin must be greater than or equal to 0.")
    if freq_band[1] is None:
        freq_band = (freq_band[0], self.stats.sampling_rate / 2)
    if freq_band[1] > self.stats.sampling_rate / 2:
        raise ValueError(
            f"fmax must be less than or equal to {self.stats.sampling_rate / 2}."
        )

    # check starttime and endtime
    if starttime is None:
        starttime = self.stats.starttime
    if starttime < self.stats.starttime:
        raise ValueError("starttime must be greater than or equal to stream starttime.")
    if endtime is None:
        endtime = self.stats.endtime
    if endtime > self.stats.endtime:
        raise ValueError("endtime must be less than or equal to stream endtime.")

    # check starttrace and endtrace
    if starttrace is None:
        starttrace = int(0)
    if starttrace < 0:
        raise ValueError("starttrace must be greater than or equal to 0.")
    if endtrace is None:
        endtrace = int(self.stats.trace_num)
    if endtrace > self.stats.trace_num:
        raise ValueError("endtrace must be less than or equal to stream trace_num.")

    # set times
    starttime_npts = int((starttime - self.stats.starttime) * self.stats.sampling_rate)
    endtime_npts = int((endtime - self.stats.starttime) * self.stats.sampling_rate)

    # data and coordinates
    data = self.data[starttrace:endtrace, starttime_npts:endtime_npts].copy()
    latitude = self.stats.latitude[starttrace:endtrace]
    longitude = self.stats.longitude[starttrace:endtrace]
    elevation = self.stats.elevation[starttrace:endtrace]
    coordinates = np.column_stack((latitude, longitude, elevation))

    # compute beamforming
    P = beamforming_compute(
        data,
        self.stats.sampling_rate,
        coordinates,
        reference_receiver,
        dest_epsg,
        method,
        freq_band,
        velocity,
        inclination,
        azimuth,
        number_of_sources,
    )

    # generate beamforming object
    Beamforming_Data = Beamforming(
        P,
        coordinates,
        reference_receiver,
        method,
        freq_band,
        velocity,
        inclination,
        azimuth,
        number_of_sources,
        starttime,
        endtime,
    )

    return Beamforming_Data


class Beamforming(object):
    def __init__(
        self,
        data,
        coordinates,
        reference_receiver,
        method,
        freq_band,
        velocity,
        inclination,
        azimuth,
        number_of_sources,
        starttime,
        endtime,
    ):
        # initialize
        self.data = data
        self.coordinates = coordinates
        self.reference_receiver = reference_receiver
        self.method = method
        self.freq_band = freq_band
        self.velocity = velocity
        self.inclination = inclination
        self.azimuth = azimuth
        self.number_of_sources = number_of_sources
        self.starttime = starttime
        self.endtime = endtime

        # number of stations
        self.number_of_traces = self.coordinates.shape[0]

    def __str__(self):
        stats = (
            "* Stats:\n"
            f"      starttime: {str(self.starttime)}\n"
            f"      endtime: {str(self.endtime)}\n"
            f"      reference_receiver: {self.reference_receiver}\n"
            f"      method: '{self.method}'\n"
            f"      freq_band: {self.freq_band}\n"
            f"      velocity: {self.velocity}\n"
            f"      inclination: {self.inclination}\n"
            f"      azimuth: {self.azimuth}\n"
            f"      number_of_sources: {self.number_of_sources}\n"
            f"      number_of_traces: {self.number_of_traces}\n"
        )
        data = (
            "* Data:\n"
            f"       shape: {self.data.shape} || (inclination, azimuth, velocity)\n"
            f"       dtype: {self.data.dtype}\n"
            f"       data[:,:,0]:\n"
            f"{textwrap.indent(np.array2string(self.data[:,:,0], threshold=MAX_DATA_THRESHOLD), '      ')}"
        )
        info = "\n".join([stats, data])
        return info

    def __repr__(self):
        return str(self)

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def plot(
        self,
        polar_axis=True,
        y_axis="velocity",  # 'inclination', 'velocity'
        velocity_index=0,
        inclination_index=0,
        ax=None,
        figsize=(10, 5),
        cmap="gnuplot2_r",  # 'CMRmap', 'viridis', 'gnuplot2_r'
        ticks_color="black",
        ticks_size=8,
        show=True,
        save_path=None,
        dpi=100,
    ):
        if polar_axis:
            azi_plot = np.arange(
                self.azimuth[0],
                self.azimuth[1] + self.azimuth[2],
                self.azimuth[2],
            )
            ax = _get_ax(ax, figsize=figsize, subplot_kw=dict(polar=True))
            cmap = _get_cmap(cmap)
            if y_axis == "velocity":
                dd = self.data[inclination_index, :, :].T.squeeze()
                dd = dd / np.max(dd)
                if self.method == "arf":
                    dd = 10 * np.log10(dd**2)
                vel_plot = np.arange(
                    self.velocity[0],
                    self.velocity[1] + self.velocity[2],
                    self.velocity[2],
                )
                azi_grid, vel_grid = np.meshgrid(np.radians(azi_plot), vel_plot)
                im = ax.pcolormesh(
                    azi_grid,
                    vel_grid,
                    dd,
                    cmap=cmap,
                )
                ax.yaxis.set_major_formatter(FuncFormatter(format_vel_tick))
            elif y_axis == "inclination":
                dd = self.data[:, :, velocity_index].squeeze()
                dd = dd / np.max(dd)
                if self.method == "arf":
                    dd = 10 * np.log10(dd**2)
                inc_plot = np.arange(
                    self.inclination[0],
                    self.inclination[1] + self.inclination[2],
                    self.inclination[2],
                )
                azi_grid, inc_grid = np.meshgrid(np.radians(azi_plot), inc_plot)
                im = ax.pcolormesh(
                    azi_grid,
                    inc_grid,
                    dd,
                    cmap=cmap,
                )
                ax.yaxis.set_major_formatter(FuncFormatter(format_inc_tick))
            else:
                raise Exception(
                    f"Unknown y_axis: '{y_axis}'!. Available methods are: 'inclination', 'velocity'."
                )

            # format axis
            fig = ax.figure
            ax.set_theta_direction(-1)
            ax.set_theta_offset(np.pi / 2.0)
            ax.grid(color="gray", ls="--")
            ax.tick_params(axis="y", colors=ticks_color, labelsize=ticks_size)
            cbar = fig.colorbar(im, ax=ax, extend="both", shrink=0.75, pad=0.05)
            if self.method == "arf":
                cbar.set_label("Beam power (dB)")
            else:
                cbar.set_label("Normalized Spectral Power")
            if show:
                plt.show()
            else:
                plt.close(fig)
            if save_path is not None:
                fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
            else:
                return ax
        else:
            ax = _get_ax(ax, figsize=figsize, subplot_kw=dict(polar=False))
            cmap = _get_cmap(cmap)
            if y_axis == "velocity":
                dd = self.data[inclination_index, :, :].T.squeeze()
                dd = dd / np.max(dd)
                if self.method == "arf":
                    dd = 10 * np.log10(dd**2)
                im = ax.imshow(
                    dd,
                    extent=[
                        self.azimuth[0],
                        self.azimuth[1],
                        self.velocity[0],
                        self.velocity[1],
                    ],
                    origin="lower",
                    cmap=cmap,
                    aspect="auto",
                )
                ax.set_xlabel("Azimuth (°)")
                ax.set_ylabel("Velocity (m/s)")
            elif y_axis == "inclination":
                dd = self.data[:, :, velocity_index].squeeze()
                dd = dd / np.max(dd)
                if self.method == "arf":
                    dd = 10 * np.log10(dd**2)
                im = ax.imshow(
                    dd,
                    extent=[
                        self.azimuth[0],
                        self.azimuth[1],
                        self.inclination[0],
                        self.inclination[1],
                    ],
                    origin="lower",
                    cmap=cmap,
                    aspect="auto",
                )
                ax.set_xlabel("Azimuth (°)")
                ax.set_ylabel("Inclination (°)")
            else:
                raise Exception(
                    f"Unknown y_axis: '{y_axis}'!. Available methods are: 'inclination', 'velocity'."
                )

            # format axis
            fig = ax.figure
            ax.tick_params(colors=ticks_color, labelsize=ticks_size)
            cbar = fig.colorbar(im, ax=ax, extend="both", shrink=0.75, pad=0.05)
            if self.method == "arf":
                cbar.set_label("Beam power (dB)")
            else:
                cbar.set_label("Normalized Spectral Power")
            if show:
                plt.show()
            else:
                plt.close(fig)
            if save_path is not None:
                fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
            else:
                return ax
