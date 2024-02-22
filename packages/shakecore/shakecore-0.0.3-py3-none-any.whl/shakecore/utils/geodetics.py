import numpy as np
from obspy.geodetics import degrees2kilometers, locations2degrees
from pyproj import Transformer


def utm_2_latlon(utm_x, utm_y, source_epsg, dest_epsg="EPSG:4326"):
    transformer = Transformer.from_crs(source_epsg, dest_epsg)
    lat, lon = transformer.transform(utm_x, utm_y)

    return lat, lon


def latlon_2_utm(lat, lon, dest_epsg, source_epsg="EPSG:4326"):
    transformer = Transformer.from_crs(source_epsg, dest_epsg)
    utm_x, utm_y = transformer.transform(lat, lon)

    return utm_x, utm_y


def latlon_2_meter(lat1, lon1, lat2, lon2):
    dist = degrees2kilometers(locations2degrees(lat1, lon1, lat2, lon2)) * 1e3

    return dist


def projection(A, B, C):
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)

    if A.ndim == 1:
        A = A.reshape(1, -1)
    if B.ndim == 1:
        B = B.reshape(1, -1)
    if C.ndim == 1:
        C = C.reshape(1, -1)
        ndim = 1
    else:
        ndim = 2

    AB = B - A
    AC = C - A.reshape(1, -1)

    dot_product = np.sum(AC * AB, axis=1)
    length_squared = np.sum(AB**2)

    projection_length = dot_product / length_squared
    D = A + projection_length.reshape(-1, 1) * AB

    if ndim == 1:
        D = D[0]

    return D
