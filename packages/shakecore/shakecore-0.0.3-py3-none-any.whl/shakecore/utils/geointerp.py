from math import ceil, sqrt

import numpy as np
from geopy import Point
from geopy.distance import distance, geodesic
from obspy.geodetics import gps2dist_azimuth


def get_known_index(points):
    known_index = []

    if points.ndim == 1:
        points = points.reshape(1, -1)

    for i in range(0, len(points)):
        if points[i, 3] != -999:
            known_index.append(i)

    known_index = np.array(known_index)

    return known_index


def my_interpolate(
    points_part,
    chn_interp,
    chn_end_f,
    chn_start_f,
    lat0,
    lon0,
    altitude0,
    direaction,
    spacing_interval,
):
    # get dist_angles and dist_cumsum_gps
    dist_angles = np.empty((len(points_part), 4))
    for j in range(0, len(points_part)):
        if j == 0:
            lat1 = lat0
            lon1 = lon0
            altitude1 = altitude0
            lat2 = points_part[0, 0]
            lon2 = points_part[0, 1]
            altitude2 = points_part[0, 2]
            flat_d = distance((lat1, lon1), (lat2, lon2)).m
            real_d = 0
        else:
            lat1 = points_part[j - 1, 0]
            lon1 = points_part[j - 1, 1]
            altitude1 = points_part[j - 1, 2]
            lat2 = points_part[j, 0]
            lon2 = points_part[j, 1]
            altitude2 = points_part[j, 2]
            flat_d = distance((lat1, lon1), (lat2, lon2)).m
            real_d = sqrt(flat_d**2 + (altitude2 - altitude1) ** 2)

        if (altitude2 - altitude1) == 0:
            takeoff_angle = np.pi / 2
        else:
            takeoff_angle = np.arctan(flat_d / (altitude2 - altitude1))

        # for borehole
        if flat_d == 0:
            up_down = np.sign(altitude2 - altitude1)

        _, az, baz = gps2dist_azimuth(lat1, lon1, lat2, lon2)
        dist_angles[j, :] = np.array([real_d, az, baz, takeoff_angle])

    dist_cumsum_gps = np.cumsum(dist_angles[:, 0])

    # get dist_cumsum_chn and sag_ratio
    if direaction == "middle":
        dd = dist_cumsum_gps[-1] / (chn_end_f - chn_start_f)
        dist_cumsum_chn = (chn_interp - chn_start_f) * dd
    elif direaction == "head":
        dd = spacing_interval
        dist_cumsum_chn = (chn_start_f - chn_interp) * dd
    elif direaction == "tail":
        dd = spacing_interval
        dist_cumsum_chn = (chn_interp - chn_start_f) * dd
    else:
        print("direaction error!")
        exit()

    sag_ratio = (dd - spacing_interval) / spacing_interval

    # do interpolation
    results = np.empty((0, 5))
    for j in range(0, len(chn_interp)):
        # find the nearest point
        mark = -999
        dist_min = 0  # dist from the marked point
        for k in range(0, len(dist_cumsum_gps)):
            if dist_cumsum_chn[j] < dist_cumsum_gps[k]:
                mark = k - 1
                dist_min = dist_cumsum_chn[j] - dist_cumsum_gps[k - 1]
                break

        if mark == -999:
            mark = len(dist_cumsum_gps) - 1
            dist_min = dist_cumsum_chn[j] - dist_cumsum_gps[-1]

        lat = points_part[mark, 0]
        lon = points_part[mark, 1]
        altitude = points_part[mark, 2]

        if mark < (len(dist_cumsum_gps) - 1):
            angle_mark = mark + 1
        else:
            angle_mark = mark

        # get destination_altitude
        if dist_angles[angle_mark, 3] < 0:
            altitude_dist_min = dist_min * np.cos(dist_angles[angle_mark, 3])
        elif dist_angles[angle_mark, 3] == 0:
            if up_down == 1.0:
                altitude_dist_min = -dist_min
            else:
                altitude_dist_min = dist_min
        else:
            altitude_dist_min = -dist_min * np.cos(dist_angles[angle_mark, 3])

        destination_altitude = altitude - altitude_dist_min

        # get destination_latitude and destination_longitude
        flat_dist_min = abs(dist_min * np.sin(dist_angles[angle_mark, 3]))
        destination = geodesic(meters=flat_dist_min).destination(
            point=Point(lat, lon), bearing=dist_angles[angle_mark, 1]
        )

        results = np.vstack(
            (
                results,
                np.array(
                    [
                        destination.latitude,
                        destination.longitude,
                        destination_altitude,
                        chn_interp[j],
                        sag_ratio,
                    ]
                ),
            )
        )

    return results


def head_interpolate(points, known_index, channel_start, channel_end, spacing_interval):
    results_head = np.empty((0, 5))
    direaction = "head"
    points_part = np.flipud(points[0 : known_index[0] + 1, :])

    if known_index[0] + 1 == len(points):
        lat0 = points[known_index[0], 0]
        lon0 = points[known_index[0], 1]
        altitude0 = points[known_index[0], 2]
    else:
        lat0 = points[known_index[0] + 1, 0]
        lon0 = points[known_index[0] + 1, 1]
        altitude0 = points[known_index[0] + 1, 2]

    chn_end_f = points[known_index[0], 3]
    chn_end_i = ceil(chn_end_f)  # save the last channel

    if chn_end_i >= channel_start:
        if chn_end_i > channel_end:
            chn_end_i = channel_end + 1

        chn_interp = np.flipud(np.arange(channel_start, chn_end_i + 1, 1, dtype=int))

        results_head = my_interpolate(
            points_part,
            chn_interp,
            channel_end,
            chn_end_f,
            lat0,
            lon0,
            altitude0,
            direaction,
            spacing_interval,
        )

        results_head = np.flipud(results_head)
        results_head = results_head[:-1, :]

    return results_head


def tail_interpolate(points, known_index, channel_start, channel_end, spacing_interval):
    results_tail = np.empty((0, 5))
    direaction = "tail"
    points_part = points[known_index[-1] :, :]

    if known_index[-1] == 0:
        lat0 = points[known_index[-1], 0]
        lon0 = points[known_index[-1], 1]
        altitude0 = points[known_index[-1], 2]
    else:
        lat0 = points[known_index[-1] - 1, 0]
        lon0 = points[known_index[-1] - 1, 1]
        altitude0 = points[known_index[-1] - 1, 2]

    chn_start_f = points[known_index[-1], 3]
    chn_start_i = ceil(chn_start_f)  # save the first channel
    if chn_start_i <= channel_end:
        if chn_start_i < channel_start:
            chn_start_i = channel_start

        chn_interp = np.arange(chn_start_i, channel_end + 1, 1, dtype=int)

        results_tail = my_interpolate(
            points_part,
            chn_interp,
            channel_end,
            chn_start_f,
            lat0,
            lon0,
            altitude0,
            direaction,
            spacing_interval,
        )

    return results_tail


def middle_interpolate(
    points, known_index, channel_start, channel_end, spacing_interval
):
    results_middle = np.empty((0, 5))
    known_num = len(known_index)
    for i in range(0, known_num - 1):
        direaction = "middle"
        points_part = points[known_index[i] : known_index[i + 1] + 1, :]
        lat0 = points[known_index[i] - 1, 0]
        lon0 = points[known_index[i] - 1, 1]
        altitude0 = points[known_index[i] - 1, 2]
        chn_start_f = points[known_index[i], 3]
        chn_end_f = points[known_index[i + 1], 3]
        chn_start_i = ceil(chn_start_f)  # save the first channel
        chn_end_i = (
            chn_end_f - 1 if int(chn_end_f) == chn_end_f else int(chn_end_f)
        )  # do not save the last channel

        if chn_start_i <= channel_end:
            if chn_end_i <= channel_end:
                chn_interp = np.arange(chn_start_i, chn_end_i + 1, 1, dtype=int)
            else:
                chn_interp = np.arange(chn_start_i, channel_end + 1, 1, dtype=int)

            results = my_interpolate(
                points_part,
                chn_interp,
                chn_end_f,
                chn_start_f,
                lat0,
                lon0,
                altitude0,
                direaction,
                spacing_interval,
            )

            results_middle = np.vstack((results_middle, results))

    return results_middle


def geointerp(points, channel_start, channel_end, spacing_interval):
    known_index = get_known_index(points)
    known_num = len(known_index)
    results_head, results_middle, results_tail = (
        np.empty((0, 5)),
        np.empty((0, 5)),
        np.empty((0, 5)),
    )

    if known_num == 0:
        print("No known points!")
        exit()
    elif known_num == 1:
        results_head = head_interpolate(
            points, known_index, channel_start, channel_end, spacing_interval
        )
        results_tail = tail_interpolate(
            points, known_index, channel_start, channel_end, spacing_interval
        )
    else:
        results_head = head_interpolate(
            points, known_index, channel_start, channel_end, spacing_interval
        )
        results_tail = tail_interpolate(
            points, known_index, channel_start, channel_end, spacing_interval
        )
        results_middle = middle_interpolate(
            points, known_index, channel_start, channel_end, spacing_interval
        )

    results = np.vstack((results_head, results_middle, results_tail))

    return results, known_index
