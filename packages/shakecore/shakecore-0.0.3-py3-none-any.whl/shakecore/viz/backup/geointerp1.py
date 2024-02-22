import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from shakecore.viz.backup.mapbox_2_matplotlib import plot_map, plotscale


def get_rgb_from_cmap(value, cmap_name="seismic"):
    cmap = plt.get_cmap(cmap_name)
    rgb = cmap(value)[:3]

    return mcolors.rgb2hex(rgb)


def sub_plot(
    ax,
    points,
    results,
    known_index,
    type,
    plot_sag_flag,
    sag_linewidth,
    sag_cmap,
    plot_results_line_flag,
    results_linewidth,
    results_line_color,
    plot_results_dot_flag,
    results_markersize,
    results_dot_color,
    plot_results_label_flag,
    results_label_gap,
    plot_points_dot_flag,
    points_markersize,
    points_dot_color,
    plot_points_label_flag,
    points_label_gap,
    results_points_label_fontsize,
    ticks_labelsize,
    axis_label_fontsize,
    ticks_format_latlon,
    ticks_format_altitude,
    ticks_lon_num,
    ticks_lat_num,
    ticks_altitude_num,
    ticks_lon_rotation,
    ticks_lat_rotation,
    ticks_altitude_rotation,
):
    # plot background using sag_ratio
    if plot_sag_flag:
        max_sag_ratio = np.max(np.abs(results[:, 4]))
        for i in range(0, len(results) - 1):
            if type == "lon2lat":  # 'lon2lat', 'lon2altitude', and 'lat2altitude'
                x = [results[i, 1], results[i + 1, 1]]  # lon
                y = [results[i, 0], results[i + 1, 0]]  # lat
            elif type == "lon2altitude":
                x = [results[i, 1], results[i + 1, 1]]  # lon
                y = [results[i, 2], results[i + 1, 2]]  # altitude
            elif type == "lat2altitude":
                x = [results[i, 2], results[i + 1, 2]]  # lat
                y = [results[i, 0], results[i + 1, 0]]  # altitude
            else:
                print("Wrong type!")
                exit()

            sag = results[i, 4]
            value = (sag / max_sag_ratio + 1) / 2.0
            color = get_rgb_from_cmap(value, sag_cmap.name)
            ax.plot(x, y, "-", color=color, linewidth=sag_linewidth, alpha=1)

    # plot results and points
    if type == "lon2lat":
        if plot_results_line_flag:
            ax.plot(
                results[:, 1],
                results[:, 0],
                "-",
                color=results_line_color,
                linewidth=results_linewidth,
            )

        if plot_results_dot_flag:
            ax.plot(
                results[:, 1],
                results[:, 0],
                "o",
                color=results_dot_color,
                markersize=results_markersize,
            )

        if plot_points_dot_flag:
            ax.plot(
                points[known_index, 1],
                points[known_index, 0],
                "o",
                color=points_dot_color,
                markersize=points_markersize,
            )

        if plot_results_label_flag:
            for i in range(0, len(results), results_label_gap):
                ax.annotate(
                    str(int(results[i, 3])),
                    xy=(results[i, 1], results[i, 0]),
                    color=results_dot_color,
                    fontsize=results_points_label_fontsize,
                )

        if plot_points_label_flag:
            for i in range(0, len(points), points_label_gap):
                if points[i, 3] != -999:
                    ax.annotate(
                        str(round(points[i, 3], 1)),
                        xy=(points[i, 1], points[i, 0]),
                        color=points_dot_color,
                        fontsize=results_points_label_fontsize,
                    )

        min_y, max_y = np.min(results[:, 0]), np.max(results[:, 0])
        min_x, max_x = np.min(results[:, 1]), np.max(results[:, 1])
        value_y = 0.3 * (max_y - min_y)
        value_x = 0.3 * (max_x - min_x)
        ax.set_xlim([min_x - value_x, max_x + value_x])
        ax.set_ylim([min_y - value_y, max_y + value_y])
        ax.set_xlabel("Longitude (°)", fontsize=axis_label_fontsize)
        ax.set_ylabel("Latitude (°)", fontsize=axis_label_fontsize)

        locator1 = ticker.MaxNLocator(nbins=ticks_lon_num)
        ax.xaxis.set_major_locator(locator1)
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(ticks_format_latlon))
        ax.tick_params(axis="x", rotation=ticks_lon_rotation, labelsize=ticks_labelsize)

        locator2 = ticker.MaxNLocator(nbins=ticks_lat_num)
        ax.yaxis.set_major_locator(locator2)
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(ticks_format_latlon))
        ax.tick_params(axis="y", rotation=ticks_lat_rotation, labelsize=ticks_labelsize)

    elif type == "lon2altitude":
        if plot_results_line_flag:
            ax.plot(
                results[:, 1],
                results[:, 2],
                "-",
                color=results_line_color,
                linewidth=results_linewidth,
            )

        if plot_results_dot_flag:
            ax.plot(
                results[:, 1],
                results[:, 2],
                "o",
                color=results_dot_color,
                markersize=results_markersize,
            )

        if plot_points_dot_flag:
            ax.plot(
                points[known_index, 1],
                points[known_index, 2],
                "o",
                color=points_dot_color,
                markersize=points_markersize,
            )

        if plot_results_label_flag:
            for i in range(0, len(results), results_label_gap):
                ax.annotate(
                    str(int(results[i, 3])),
                    xy=(results[i, 1], results[i, 2]),
                    color=results_dot_color,
                    fontsize=results_points_label_fontsize,
                )

        if plot_points_label_flag:
            for i in range(0, len(points), points_label_gap):
                if points[i, 3] != -999:
                    ax.annotate(
                        str(round(points[i, 3], 1)),
                        xy=(points[i, 1], points[i, 2]),
                        color=points_dot_color,
                        fontsize=results_points_label_fontsize,
                    )

        min_y, max_y = np.min(results[:, 2]), np.max(results[:, 2])
        min_x, max_x = np.min(results[:, 1]), np.max(results[:, 1])
        value_y = 0.3 * (max_y - min_y)
        value_x = 0.3 * (max_x - min_x)
        ax.set_xlim([min_x - value_x, max_x + value_x])
        ax.set_ylim([min_y - value_y, max_y + value_y])
        ax.set_ylabel("Altitude (m)", fontsize=axis_label_fontsize)

        locator1 = ticker.MaxNLocator(nbins=ticks_altitude_num)
        ax.yaxis.set_major_locator(locator1)
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(ticks_format_altitude))
        ax.tick_params(
            axis="y", rotation=ticks_altitude_rotation, labelsize=ticks_labelsize
        )

    elif type == "lat2altitude":
        if plot_results_line_flag:
            ax.plot(
                results[:, 2],
                results[:, 0],
                "-",
                color=results_line_color,
                linewidth=results_linewidth,
            )

        if plot_results_dot_flag:
            ax.plot(
                results[:, 2],
                results[:, 0],
                "o",
                color=results_dot_color,
                markersize=results_markersize,
            )

        if plot_points_dot_flag:
            ax.plot(
                points[known_index, 2],
                points[known_index, 0],
                "o",
                color=points_dot_color,
                markersize=points_markersize,
            )

        if plot_results_label_flag:
            for i in range(0, len(results), results_label_gap):
                ax.annotate(
                    str(int(results[i, 3])),
                    xy=(results[i, 2], results[i, 0]),
                    color=results_dot_color,
                    fontsize=results_points_label_fontsize,
                )

        if plot_points_label_flag:
            for i in range(0, len(points), points_label_gap):
                if points[i, 3] != -999:
                    ax.annotate(
                        str(round(points[i, 3], 1)),
                        xy=(points[i, 2], points[i, 0]),
                        color=points_dot_color,
                        fontsize=results_points_label_fontsize,
                    )

        min_y, max_y = np.min(results[:, 0]), np.max(results[:, 0])
        min_x, max_x = np.min(results[:, 2]), np.max(results[:, 2])
        value_y = 0.3 * (max_y - min_y)
        value_x = 0.3 * (max_x - min_x)
        ax.set_xlim([min_x - value_x, max_x + value_x])
        ax.set_ylim([min_y - value_y, max_y + value_y])
        ax.set_xlabel("Altitude (m)", fontsize=axis_label_fontsize)

        locator1 = ticker.MaxNLocator(nbins=ticks_altitude_num)
        ax.xaxis.set_major_locator(locator1)
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter(ticks_format_altitude))
        ax.tick_params(
            axis="x", rotation=ticks_altitude_rotation, labelsize=ticks_labelsize
        )

    else:
        print("Wrong type!")
        exit()


def geointerp(
    points,
    results,
    known_index,
    plot_ax_right_flag=True,
    ax_right_size=0.7,
    plot_ax_top_flag=True,
    ax_top_size=0.7,
    plot_map_flag=True,
    map_style=3,
    compasssize=1,
    compass_accuracy=2,
    compass_textsize=4,
    compass_unit="m",
    rect=[0.1, 0.05],
    colorbar_size=0.2,
    colorbar_ticks_labelsize=6,
    colorbar_label_fontsize=8,
    legend_fontsize=6,
    save_flag=True,
    save_path="./interp_map.pdf",
    plot_sag_flag=True,
    sag_linewidth=6,
    sag_cmap=plt.colormaps["bwr"],
    plot_results_line_flag=True,
    results_linewidth=1,
    results_line_color="gray",
    plot_results_dot_flag=True,
    results_markersize=3,
    results_dot_color="orange",
    plot_results_label_flag=True,
    results_label_gap=1,
    plot_points_dot_flag=True,
    points_markersize=3,
    points_dot_color="k",
    plot_points_label_flag=True,
    points_label_gap=1,
    results_points_label_fontsize=6,
    ticks_labelsize=6,
    axis_label_fontsize=8,
    ticks_format_latlon="%0.4f",
    ticks_format_altitude="%0.1f",
    ticks_lon_num=5,
    ticks_lat_num=5,
    ticks_altitude_num=3,
    ticks_lon_rotation=0,
    ticks_lat_rotation=0,
    ticks_altitude_rotation=0,
):
    fig, ax = plt.subplots()
    plt.tight_layout()
    ax.set_aspect(1.0)
    ax.set_aspect("equal")
    divider = make_axes_locatable(ax)

    # set aspect of the main axes.
    if plot_ax_top_flag:
        ax_top = divider.append_axes("top", size=ax_top_size, pad=0.0, sharex=ax)
        ax_top.xaxis.set_tick_params(labelbottom=False)

    if plot_ax_right_flag:
        ax_right = divider.append_axes("right", size=ax_right_size, pad=0.0, sharey=ax)
        ax_right.yaxis.set_tick_params(labelleft=False)

    # plot map
    if plot_map_flag:
        min_y, max_y = np.min(results[:, 0]), np.max(results[:, 0])
        min_x, max_x = np.min(results[:, 1]), np.max(results[:, 1])
        value_y = 0.3 * (max_y - min_y)
        value_x = 0.3 * (max_x - min_x)
        bounds = [min_x - value_x, min_y - value_y, max_x + value_x, max_y + value_y]

        plot_map(ax, bounds, style=map_style)  # zoom = 30,

        plotscale(
            ax,
            bounds=bounds,
            textsize=compass_textsize,
            compasssize=compasssize,
            accuracy=compass_accuracy,
            unit=compass_unit,
            rect=rect,
            style=1,
            zorder=10,
        )

    sub_plot(
        ax,
        points=points,
        results=results,
        known_index=known_index,
        type="lon2lat",
        plot_sag_flag=plot_sag_flag,
        sag_linewidth=sag_linewidth,
        sag_cmap=sag_cmap,
        plot_results_line_flag=plot_results_line_flag,
        results_linewidth=results_linewidth,
        results_line_color=results_line_color,
        plot_results_dot_flag=plot_results_dot_flag,
        results_markersize=results_markersize,
        results_dot_color=results_dot_color,
        plot_results_label_flag=plot_results_label_flag,
        results_label_gap=results_label_gap,
        plot_points_dot_flag=plot_points_dot_flag,
        points_markersize=points_markersize,
        points_dot_color=points_dot_color,
        plot_points_label_flag=plot_points_label_flag,
        points_label_gap=points_label_gap,
        results_points_label_fontsize=results_points_label_fontsize,
        ticks_labelsize=ticks_labelsize,
        axis_label_fontsize=axis_label_fontsize,
        ticks_format_latlon=ticks_format_latlon,
        ticks_format_altitude=ticks_format_altitude,
        ticks_lon_num=ticks_lon_num,
        ticks_lat_num=ticks_lat_num,
        ticks_altitude_num=ticks_altitude_num,
        ticks_lon_rotation=ticks_lon_rotation,
        ticks_lat_rotation=ticks_lat_rotation,
        ticks_altitude_rotation=ticks_altitude_rotation,
    )

    if plot_ax_top_flag:
        sub_plot(
            ax_top,
            points=points,
            results=results,
            known_index=known_index,
            type="lon2altitude",
            plot_sag_flag=plot_sag_flag,
            sag_linewidth=sag_linewidth,
            sag_cmap=sag_cmap,
            plot_results_line_flag=plot_results_line_flag,
            results_linewidth=results_linewidth,
            results_line_color=results_line_color,
            plot_results_dot_flag=plot_results_dot_flag,
            results_markersize=results_markersize,
            results_dot_color=results_dot_color,
            plot_results_label_flag=plot_results_label_flag,
            results_label_gap=results_label_gap,
            plot_points_dot_flag=plot_points_dot_flag,
            points_markersize=points_markersize,
            points_dot_color=points_dot_color,
            plot_points_label_flag=plot_points_label_flag,
            points_label_gap=points_label_gap,
            results_points_label_fontsize=results_points_label_fontsize,
            ticks_labelsize=ticks_labelsize,
            axis_label_fontsize=axis_label_fontsize,
            ticks_format_latlon=ticks_format_latlon,
            ticks_format_altitude=ticks_format_altitude,
            ticks_lon_num=ticks_lon_num,
            ticks_lat_num=ticks_lat_num,
            ticks_altitude_num=ticks_altitude_num,
            ticks_lon_rotation=ticks_lon_rotation,
            ticks_lat_rotation=ticks_lat_rotation,
            ticks_altitude_rotation=ticks_altitude_rotation,
        )

    if plot_ax_right_flag:
        sub_plot(
            ax_right,
            points=points,
            results=results,
            known_index=known_index,
            type="lat2altitude",
            plot_sag_flag=plot_sag_flag,
            sag_linewidth=sag_linewidth,
            sag_cmap=sag_cmap,
            plot_results_line_flag=plot_results_line_flag,
            results_linewidth=results_linewidth,
            results_line_color=results_line_color,
            plot_results_dot_flag=plot_results_dot_flag,
            results_markersize=results_markersize,
            results_dot_color=results_dot_color,
            plot_results_label_flag=plot_results_label_flag,
            results_label_gap=results_label_gap,
            plot_points_dot_flag=plot_points_dot_flag,
            points_markersize=points_markersize,
            points_dot_color=points_dot_color,
            plot_points_label_flag=plot_points_label_flag,
            points_label_gap=points_label_gap,
            results_points_label_fontsize=results_points_label_fontsize,
            ticks_labelsize=ticks_labelsize,
            axis_label_fontsize=axis_label_fontsize,
            ticks_format_latlon=ticks_format_latlon,
            ticks_format_altitude=ticks_format_altitude,
            ticks_lon_num=ticks_lon_num,
            ticks_lat_num=ticks_lat_num,
            ticks_altitude_num=ticks_altitude_num,
            ticks_lon_rotation=ticks_lon_rotation,
            ticks_lat_rotation=ticks_lat_rotation,
            ticks_altitude_rotation=ticks_altitude_rotation,
        )

    # create a ax for legend and colorbar
    ax_colorbar = divider.append_axes("right", colorbar_size, pad=0.2, sharey=ax)
    ax_colorbar.spines["top"].set_visible(False)
    ax_colorbar.spines["right"].set_visible(False)
    ax_colorbar.spines["bottom"].set_visible(False)
    ax_colorbar.spines["left"].set_visible(False)
    ax_colorbar.get_xaxis().set_visible(False)
    ax_colorbar.get_yaxis().set_visible(False)

    # legend
    if plot_points_dot_flag:
        ax_colorbar.plot([], [], "o", color=points_dot_color, label="Known points")

    if plot_results_dot_flag:
        ax_colorbar.plot(
            [], [], "o", color=results_dot_color, label="Interpolated points"
        )

    if plot_results_line_flag:
        ax_colorbar.plot(
            [], [], "-", color=results_line_color, label="Interpolated line"
        )

    ax_colorbar.legend(loc="upper left", fontsize=legend_fontsize, frameon=False)

    # colorbar
    if plot_sag_flag:
        cbar_ax = inset_axes(
            ax_colorbar, width="50%", height="40%", loc="lower left"
        )  # cbar_ax = fig.add_axes([0.85, 0.15, 0.03, 0.4])

        font = {
            "family": "serif",
            "color": "black",
            "weight": "normal",
            "size": colorbar_label_fontsize,
        }

        max_sag_ratio = np.max(np.abs(results[:, 4]))
        cb = fig.colorbar(
            plt.cm.ScalarMappable(
                norm=Normalize(-max_sag_ratio, max_sag_ratio), cmap=sag_cmap
            ),
            cax=cbar_ax,
        )
        cb.set_label(label="Sag Ratio", fontdict=font)
        cb.ax.tick_params(labelsize=colorbar_ticks_labelsize)

    # save
    if save_flag:
        fig.savefig(save_path, dpi=800, format="pdf", bbox_inches="tight")
    else:
        plt.show()
