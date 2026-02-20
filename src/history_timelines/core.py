"""YAML loading utilities and coordinate helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_manifest(path: str | Path) -> dict[str, Any]:
    """Load and return the YAML manifest as a dict."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    _validate(data, path)
    return data


def _validate(data: dict, path: Path) -> None:
    """Basic structural validation — raises ValueError on problems."""
    required = ("metadata", "timeline", "events")
    for key in required:
        if key not in data:
            raise ValueError(f"Manifest {path} missing required key '{key}'")
    tl = data["timeline"]
    for key in ("start", "end"):
        if key not in tl:
            raise ValueError(f"timeline.{key} is required")
    if tl["start"] >= tl["end"]:
        raise ValueError("timeline.start must be less than timeline.end")


def make_date_to_x(timeline_cfg: dict, left_pts: float, right_pts: float):
    """Return a closure mapping a date (year number) → x in points."""
    start = timeline_cfg["start"]
    end = timeline_cfg["end"]
    span = end - start
    width = right_pts - left_pts

    def date_to_x(date: float) -> float:
        return left_pts + (date - start) / span * width

    return date_to_x
