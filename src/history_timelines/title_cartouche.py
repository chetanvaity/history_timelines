"""Title cartouche with double-rule frame."""

from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.transforms import Bbox


_POSITIONS = {
    "top-left", "top-right", "top-center",
    "bottom-left", "bottom-right", "bottom-center",
}


def render_title_cartouche(
    ax: plt.Axes,
    manifest: dict,
    theme: dict,
    fig_width_pts: float,
    fig_height_pts: float,
    margin_pts: float,
) -> None:
    """Draw the title + optional subtitle inside a double-rule frame."""
    cfg = manifest.get("title_cartouche", {})
    position = cfg.get("position", "top-left")
    ct = theme["cartouche"]

    title_text = manifest.get("metadata", {}).get("title", "")
    subtitle_text = manifest.get("metadata", {}).get("subtitle", "")

    pad = ct["padding"]
    title_fs = ct["title_fontsize"]
    subtitle_fs = ct["subtitle_fontsize"]
    font_family = ct["font_family"]
    outer_lw = ct["outer_line_width"]
    inner_lw = ct["inner_line_width"]
    gap = ct["line_gap"]
    line_color = ct["line_color"]
    bg_color = ct["bg_color"]

    # Estimate box dimensions
    title_h = title_fs * 1.4
    subtitle_h = subtitle_fs * 1.4 if subtitle_text else 0
    text_h = title_h + subtitle_h + (4 if subtitle_text else 0)
    # Estimate width from longest line
    max_chars = max(len(title_text), len(subtitle_text))
    est_w = max(max_chars * title_fs * 0.6 + 2 * pad, 120)
    box_w = min(est_w, fig_width_pts * 0.4)
    box_h = text_h + 2 * pad + 2 * gap + outer_lw + inner_lw

    # Position the box
    h_margin = margin_pts
    v_margin = margin_pts

    if "left" in position:
        bx = h_margin
    elif "right" in position:
        bx = fig_width_pts - h_margin - box_w
    else:  # center
        bx = (fig_width_pts - box_w) / 2

    if "top" in position:
        by = fig_height_pts - v_margin - box_h
    else:  # bottom
        by = v_margin

    # Outer rectangle (background fill)
    outer = mpatches.FancyBboxPatch(
        (bx, by),
        box_w,
        box_h,
        boxstyle="square,pad=0",
        facecolor=bg_color,
        edgecolor=line_color,
        linewidth=outer_lw,
        zorder=8,
    )
    ax.add_patch(outer)

    # Inner rectangle (thin rule inset by gap + outer_lw/2)
    inset = gap + outer_lw / 2
    inner = mpatches.FancyBboxPatch(
        (bx + inset, by + inset),
        box_w - 2 * inset,
        box_h - 2 * inset,
        boxstyle="square,pad=0",
        facecolor="none",
        edgecolor=line_color,
        linewidth=inner_lw,
        zorder=9,
    )
    ax.add_patch(inner)

    # Text: centred inside inner box
    cx = bx + box_w / 2
    text_top = by + box_h - inset - pad

    if subtitle_text:
        ax.text(
            cx,
            text_top - title_h / 2,
            title_text,
            ha="center",
            va="center",
            fontsize=title_fs,
            fontfamily=font_family,
            fontweight="bold",
            color=line_color,
            zorder=10,
        )
        ax.text(
            cx,
            text_top - title_h - 4 - subtitle_h / 2,
            subtitle_text,
            ha="center",
            va="center",
            fontsize=subtitle_fs,
            fontfamily=font_family,
            style="italic",
            color=line_color,
            zorder=10,
        )
    else:
        # Vertically centre single title in box
        ax.text(
            cx,
            by + box_h / 2,
            title_text,
            ha="center",
            va="center",
            fontsize=title_fs,
            fontfamily=font_family,
            fontweight="bold",
            color=line_color,
            zorder=10,
        )
