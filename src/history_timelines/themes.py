"""Theme definitions for history_timelines."""

from __future__ import annotations

from typing import Any

PARCHMENT: dict[str, Any] = {
    "figure": {
        "bg_color": "#F5E6C8",
        "margin_pts": 40,
    },
    "axis": {
        "line_color": "#3A2A1A",
        "line_width": 2.0,
        "major_tick_height": 12,
        "minor_tick_height": 6,
        "year_label_fontsize": 10,
        "year_label_family": "serif",
        "y_position": 0.5,   # fraction of figure height
    },
    "event": {
        "dot_radius": 5,
        "dot_color": "#3A2A1A",
        "leader_color": "#3A2A1A",
        "leader_width": 1.0,
        "label_fontsize": 9,
        "label_family": "serif",
        "label_color": "#1A0A00",
        "base_gap_pts": 20,       # min distance label baseline from axis
        "stagger_pts": 16,        # additional height per stagger level
        "max_levels": 4,
    },
    "period": {
        "height_pts": 18,
        "alpha": 0.35,
        "label_fontsize": 8,
        "label_family": "serif",
        "label_color": "#1A0A00",
        "track_gap_pts": 4,
    },
    "cartouche": {
        "outer_line_width": 3,
        "inner_line_width": 1,
        "line_gap": 4,
        "line_color": "#3A2A1A",
        "bg_color": "#FAF0DC",
        "padding": 12,
        "title_fontsize": 18,
        "subtitle_fontsize": 12,
        "font_family": "serif",
    },
    "narrative": {
        "fontsize": 8,
        "font_family": "serif",
        "text_color": "#2A1A0A",
        "bg_color": "#FAF0DC",
        "border_color": "#3A2A1A",
        "border_width": 1.0,
        "padding": 10,
        "reference_fontsize": 7,
        "reference_style": "italic",
    },
}

_THEMES: dict[str, dict] = {
    "parchment": PARCHMENT,
}


def get_theme(name: str) -> dict[str, Any]:
    """Return the theme dict for the given name. Raises KeyError if unknown."""
    try:
        return _THEMES[name]
    except KeyError:
        available = ", ".join(_THEMES)
        raise KeyError(f"Unknown theme '{name}'. Available: {available}")
