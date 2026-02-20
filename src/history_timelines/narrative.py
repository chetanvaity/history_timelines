"""Narrative text box."""

from __future__ import annotations

import textwrap

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def render_narrative(
    ax: plt.Axes,
    manifest: dict,
    theme: dict,
    fig_width_pts: float,
    fig_height_pts: float,
    margin_pts: float,
) -> None:
    """Draw the narrative text box with optional reference line."""
    cfg = manifest.get("narrative")
    if not cfg:
        return

    nt = theme["narrative"]
    position = cfg.get("position", "bottom-right")
    width_frac = cfg.get("width", 0.25)
    text = cfg.get("text", "")
    reference = cfg.get("reference", "")

    pad = nt["padding"]
    fontsize = nt["fontsize"]
    font_family = nt["font_family"]
    text_color = nt["text_color"]
    bg_color = nt["bg_color"]
    border_color = nt["border_color"]
    border_lw = nt["border_width"]
    ref_fs = nt["reference_fontsize"]

    box_w = fig_width_pts * width_frac
    # Wrap text to fit box width (rough char estimate)
    chars_per_line = max(int((box_w - 2 * pad) / (fontsize * 0.55)), 10)
    wrapped_lines = textwrap.wrap(text, width=chars_per_line)

    line_height = fontsize * 1.4
    ref_height = (ref_fs * 1.4 + 4) if reference else 0
    box_h = (
        len(wrapped_lines) * line_height
        + ref_height
        + 2 * pad
    )

    h_margin = margin_pts
    v_margin = margin_pts

    if "left" in position:
        bx = h_margin
    elif "right" in position:
        bx = fig_width_pts - h_margin - box_w
    else:
        bx = (fig_width_pts - box_w) / 2

    if "top" in position:
        by = fig_height_pts - v_margin - box_h
    else:
        by = v_margin

    rect = mpatches.FancyBboxPatch(
        (bx, by),
        box_w,
        box_h,
        boxstyle="square,pad=0",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=border_lw,
        zorder=8,
    )
    ax.add_patch(rect)

    # Draw wrapped text top-to-bottom inside box
    y_cursor = by + box_h - pad - line_height / 2
    for line in wrapped_lines:
        ax.text(
            bx + pad,
            y_cursor,
            line,
            ha="left",
            va="center",
            fontsize=fontsize,
            fontfamily=font_family,
            color=text_color,
            zorder=9,
        )
        y_cursor -= line_height

    if reference:
        ax.text(
            bx + pad,
            by + pad + ref_fs * 0.7,
            reference,
            ha="left",
            va="center",
            fontsize=ref_fs,
            fontfamily=font_family,
            style="italic",
            color=text_color,
            zorder=9,
        )
