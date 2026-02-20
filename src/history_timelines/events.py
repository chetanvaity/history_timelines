"""Event collect / resolve / render pipeline."""

from __future__ import annotations

from typing import Callable

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from .placement import LabelCandidate, PlacementElement, PlacementManager

# Approximate character width at 9pt in points (used for bbox estimation)
_CHAR_WIDTH_PTS = 5.5
_LINE_HEIGHT_PTS = 11.0
_LABEL_PADDING = 3.0   # horizontal padding around label text


def collect_events(
    manifest: dict,
    theme: dict,
    date_to_x: Callable[[float], float],
    axis_y: float,
) -> list[LabelCandidate]:
    """
    For each event generate candidate PlacementElements at multiple stagger
    levels above and below the axis.  Returns a list of LabelCandidates.
    """
    et = theme["event"]
    base_gap = et["base_gap_pts"]
    stagger = et["stagger_pts"]
    max_levels = et["max_levels"]
    font_size = et["label_fontsize"]

    candidates: list[LabelCandidate] = []

    for idx, ev in enumerate(manifest.get("events", [])):
        date = float(ev["date"])
        label = ev.get("label", "")
        side = ev.get("side", "auto").lower()

        x = date_to_x(date)
        label_w = max(len(label) * _CHAR_WIDTH_PTS + 2 * _LABEL_PADDING, 40)
        label_h = _LINE_HEIGHT_PTS + 2 * _LABEL_PADDING

        positions: list[PlacementElement] = []

        # Build ordered list of (direction, level) pairs based on side hint
        if side == "above":
            combos = [("above", lv) for lv in range(1, max_levels + 1)]
            combos += [("below", lv) for lv in range(1, max_levels + 1)]
        elif side == "below":
            combos = [("below", lv) for lv in range(1, max_levels + 1)]
            combos += [("above", lv) for lv in range(1, max_levels + 1)]
        else:  # auto: interleave
            combos = []
            for lv in range(1, max_levels + 1):
                if idx % 2 == 0:
                    combos.append(("above", lv))
                    combos.append(("below", lv))
                else:
                    combos.append(("below", lv))
                    combos.append(("above", lv))

        for direction, level in combos:
            offset = base_gap + (level - 1) * stagger
            if direction == "above":
                label_y0 = axis_y + offset
                label_y1 = label_y0 + label_h
            else:
                label_y1 = axis_y - offset
                label_y0 = label_y1 - label_h

            # Centre label on event x
            lx0 = x - label_w / 2
            lx1 = x + label_w / 2

            elem = PlacementElement(
                id=f"event_{idx}_{direction}_{level}",
                bbox=(lx0, label_y0, lx1, label_y1),
                group="event_label",
            )
            positions.append(elem)

        candidates.append(
            LabelCandidate(
                id=f"event_{idx}",
                positions=positions,
                priority=float(len(manifest["events"]) - idx),
                metadata={"event": ev, "x": x},
            )
        )

    return candidates


def render_events(
    ax: plt.Axes,
    candidates: list[LabelCandidate],
    resolved: dict[str, PlacementElement | None],
    theme: dict,
    axis_y: float,
) -> None:
    """Draw dot on axis, leader line to label centre, and label text."""
    et = theme["event"]
    dot_r = et["dot_radius"]
    dot_color = et["dot_color"]
    leader_color = et["leader_color"]
    leader_lw = et["leader_width"]
    label_fontsize = et["label_fontsize"]
    label_family = et["label_family"]
    label_color = et["label_color"]

    for cand in candidates:
        placed = resolved.get(cand.id)
        ev = cand.metadata["event"]
        x = cand.metadata["x"]
        label = ev.get("label", "")

        # Dot on axis
        circle = mpatches.Circle(
            (x, axis_y),
            radius=dot_r,
            color=dot_color,
            zorder=5,
        )
        ax.add_patch(circle)

        if placed is None:
            continue  # no room for label

        bx0, by0, bx1, by1 = placed.bbox
        lx = (bx0 + bx1) / 2
        ly_center = (by0 + by1) / 2

        # Leader line from axis dot top/bottom to label edge
        if ly_center > axis_y:
            # label is above axis
            leader_y_start = axis_y + dot_r
            leader_y_end = by0
        else:
            # label is below axis
            leader_y_start = axis_y - dot_r
            leader_y_end = by1

        ax.plot(
            [x, lx],
            [leader_y_start, leader_y_end],
            color=leader_color,
            linewidth=leader_lw,
            zorder=4,
        )

        # Label text
        ax.text(
            lx,
            ly_center,
            label,
            ha="center",
            va="center",
            fontsize=label_fontsize,
            fontfamily=label_family,
            color=label_color,
            zorder=6,
        )
