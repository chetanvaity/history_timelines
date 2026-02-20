"""Period span (colored band) rendering."""

from __future__ import annotations

from typing import Callable

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from .placement import PlacementElement, PlacementManager


def render_periods(
    ax: plt.Axes,
    manifest: dict,
    theme: dict,
    date_to_x: Callable[[float], float],
    axis_y: float,
    pm: PlacementManager,
) -> None:
    """
    Draw colored band for each period, stacked by track number.
    track=1 → innermost (closest to axis), track=2 → next outward, etc.
    Registers bboxes with the PlacementManager so event labels avoid them.
    """
    pt = theme["period"]
    band_h = pt["height_pts"]
    track_gap = pt["track_gap_pts"]
    alpha = pt["alpha"]
    label_fontsize = pt["label_fontsize"]
    label_family = pt["label_family"]
    label_color = pt["label_color"]

    for idx, period in enumerate(manifest.get("periods", [])):
        start_date = float(period["start"])
        end_date = float(period["end"])
        label = period.get("label", "")
        color = period.get("color", "#888888")
        track = int(period.get("track", 1))

        x0 = date_to_x(start_date)
        x1 = date_to_x(end_date)

        # Band is centred on axis; track stacks outward on both sides
        offset = (track - 1) * (band_h + track_gap)
        y0 = axis_y - band_h / 2 - offset
        y1 = axis_y + band_h / 2 + offset

        rect = mpatches.FancyBboxPatch(
            (x0, y0),
            x1 - x0,
            y1 - y0,
            boxstyle="square,pad=0",
            facecolor=color,
            edgecolor=color,
            alpha=alpha,
            zorder=1,
        )
        ax.add_patch(rect)

        # Register with placement manager
        elem = PlacementElement(
            id=f"period_{idx}",
            bbox=(x0, y0, x1, y1),
            group="period",
        )
        pm.add(elem)

        # Period label centred inside the band
        band_width = x1 - x0
        if band_width > 20:  # only draw if there's reasonable space
            ax.text(
                (x0 + x1) / 2,
                (y0 + y1) / 2,
                label,
                ha="center",
                va="center",
                fontsize=label_fontsize,
                fontfamily=label_family,
                color=label_color,
                alpha=min(alpha + 0.4, 1.0),
                clip_on=True,
                zorder=2,
            )
