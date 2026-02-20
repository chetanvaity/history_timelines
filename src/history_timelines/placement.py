"""Label placement: AABB collision detection and greedy resolver."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlacementElement:
    """A placed element with an axis-aligned bounding box (in points)."""
    id: str
    bbox: tuple[float, float, float, float]   # (x0, y0, x1, y1)
    group: str = ""


@dataclass
class LabelCandidate:
    """An element that needs placement, with ordered candidate positions."""
    id: str
    positions: list[PlacementElement]          # ordered preference
    priority: float = 0.0                      # higher = placed first
    metadata: dict[str, Any] = field(default_factory=dict)


class PlacementManager:
    """Tracks placed elements and resolves greedy placement."""

    def __init__(self) -> None:
        self._placed: list[PlacementElement] = []

    def add(self, element: PlacementElement) -> None:
        self._placed.append(element)

    def would_overlap(self, candidate: PlacementElement) -> bool:
        for placed in self._placed:
            if _bbox_intersects(candidate.bbox, placed.bbox):
                return True
        return False

    def resolve_greedy(
        self, candidates: list[LabelCandidate]
    ) -> dict[str, PlacementElement | None]:
        """
        Sort candidates by priority descending.
        For each candidate, pick the first position that doesn't overlap.
        Returns a mapping id → placed PlacementElement (or None if no room).
        """
        sorted_candidates = sorted(candidates, key=lambda c: c.priority, reverse=True)
        result: dict[str, PlacementElement | None] = {}

        for cand in sorted_candidates:
            placed = None
            for pos in cand.positions:
                if not self.would_overlap(pos):
                    self.add(pos)
                    placed = pos
                    break
            result[cand.id] = placed

        return result


def _bbox_intersects(
    b1: tuple[float, float, float, float],
    b2: tuple[float, float, float, float],
) -> bool:
    """Return True if two AABBs overlap (touching edges count as overlap)."""
    x0a, y0a, x1a, y1a = b1
    x0b, y0b, x1b, y1b = b2
    return x0a < x1b and x1a > x0b and y0a < y1b and y1a > y0b
