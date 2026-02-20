"""Axis line, ticks, and year labels."""

from __future__ import annotations

from typing import Callable

import matplotlib.pyplot as plt


def render_axis(
    ax: plt.Axes,
    timeline_cfg: dict,
    theme: dict,
    date_to_x: Callable[[float], float],
    fig_height_pts: float,
    fig_width_pts: float,
    margin_pts: float,
) -> float:
    """
    Draw the horizontal axis line, major ticks with labels, and minor ticks.
    Returns the y-coordinate of the axis in points.
    """
    t = theme["axis"]
    axis_y = fig_height_pts * t["y_position"]

    start = timeline_cfg["start"]
    end = timeline_cfg["end"]
    x_left = date_to_x(start)
    x_right = date_to_x(end)

    # --- axis line ---
    ax.plot(
        [x_left, x_right],
        [axis_y, axis_y],
        color=t["line_color"],
        linewidth=t["line_width"],
        solid_capstyle="butt",
        zorder=2,
    )

    # --- major ticks + labels ---
    tick_interval = timeline_cfg.get("tick_interval", 50)
    first_major = _ceil_to(start, tick_interval)
    year = first_major
    while year <= end:
        x = date_to_x(year)
        half = t["major_tick_height"] / 2
        ax.plot(
            [x, x],
            [axis_y - half, axis_y + half],
            color=t["line_color"],
            linewidth=t["line_width"],
            zorder=2,
        )
        ax.text(
            x,
            axis_y - half - 4,
            str(int(year)),
            ha="center",
            va="top",
            fontsize=t["year_label_fontsize"],
            fontfamily=t["year_label_family"],
            color=t["line_color"],
            zorder=3,
        )
        year += tick_interval

    # --- minor ticks ---
    minor_interval = timeline_cfg.get("minor_interval", 10)
    if minor_interval:
        first_minor = _ceil_to(start, minor_interval)
        year = first_minor
        half_minor = t["minor_tick_height"] / 2
        while year <= end:
            # skip positions already drawn as major ticks
            if (year - first_major) % tick_interval != 0:
                x = date_to_x(year)
                ax.plot(
                    [x, x],
                    [axis_y - half_minor, axis_y + half_minor],
                    color=t["line_color"],
                    linewidth=max(t["line_width"] * 0.6, 0.8),
                    zorder=2,
                )
            year += minor_interval

    return axis_y


def _ceil_to(value: float, interval: float) -> float:
    """Round value up to nearest multiple of interval."""
    import math
    return math.ceil(value / interval) * interval
