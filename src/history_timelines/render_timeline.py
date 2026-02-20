"""CLI entry point and main rendering pipeline for history_timelines."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .core import load_manifest, make_date_to_x
from .themes import get_theme
from .placement import PlacementManager
from .axis import render_axis
from .events import collect_events, render_events
from .periods import render_periods
from .title_cartouche import render_title_cartouche
from .narrative import render_narrative


def render(manifest_path: str | Path, output: str | None = None, dpi: int = 150) -> Path:
    """
    Full collect → resolve → render pipeline.
    Returns the path of the saved PNG.
    """
    manifest_path = Path(manifest_path)
    manifest = load_manifest(manifest_path)

    meta = manifest["metadata"]
    theme_name = meta.get("theme", "parchment")
    theme = get_theme(theme_name)

    dimensions = meta.get("dimensions", [3600, 1200])
    fig_w_px, fig_h_px = dimensions[0], dimensions[1]
    fig_w_in = fig_w_px / dpi
    fig_h_in = fig_h_px / dpi

    # Points (1/72 inch)
    fig_w_pts = fig_w_in * 72
    fig_h_pts = fig_h_in * 72
    margin_pts = theme["figure"]["margin_pts"]

    # --- Figure setup ---
    fig, ax = plt.subplots(figsize=(fig_w_in, fig_h_in), dpi=dpi)
    fig.patch.set_facecolor(theme["figure"]["bg_color"])
    ax.set_facecolor(theme["figure"]["bg_color"])

    # Use points as the data coordinate system
    ax.set_xlim(0, fig_w_pts)
    ax.set_ylim(0, fig_h_pts)
    ax.set_aspect("equal")
    ax.axis("off")

    # --- Coordinate helpers ---
    date_to_x = make_date_to_x(
        manifest["timeline"],
        left_pts=margin_pts,
        right_pts=fig_w_pts - margin_pts,
    )

    # Axis y in points
    axis_y = fig_h_pts * theme["axis"]["y_position"]

    # --- Placement manager ---
    pm = PlacementManager()

    # ── COLLECT ──────────────────────────────────────────────────────────────

    # Periods: fixed positions, register bboxes with pm
    render_periods(ax, manifest, theme, date_to_x, axis_y, pm)

    # Events: build candidates
    event_candidates = collect_events(manifest, theme, date_to_x, axis_y)

    # ── RESOLVE ──────────────────────────────────────────────────────────────
    resolved = pm.resolve_greedy(event_candidates)

    # ── RENDER ───────────────────────────────────────────────────────────────
    render_axis(ax, manifest["timeline"], theme, date_to_x, fig_h_pts, fig_w_pts, margin_pts)
    render_events(ax, event_candidates, resolved, theme, axis_y)
    render_title_cartouche(ax, manifest, theme, fig_w_pts, fig_h_pts, margin_pts)
    render_narrative(ax, manifest, theme, fig_w_pts, fig_h_pts, margin_pts)

    # --- Save ---
    out_name = output or meta.get("output", "timeline.png")
    # Resolve relative to manifest directory
    out_path = Path(out_name)
    if not out_path.is_absolute():
        out_path = manifest_path.parent / out_path

    fig.savefig(
        out_path,
        dpi=dpi,
        bbox_inches=None,
        facecolor=fig.get_facecolor(),
    )
    plt.close(fig)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="history-timeline",
        description="Render a history timeline from a YAML manifest.",
    )
    parser.add_argument("manifest", help="Path to the manifest YAML file")
    parser.add_argument("--output", "-o", default=None, help="Output PNG path")
    parser.add_argument("--dpi", type=int, default=150, help="Output DPI (default 150)")
    args = parser.parse_args()

    try:
        out = render(args.manifest, output=args.output, dpi=args.dpi)
        print(f"Saved: {out}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
