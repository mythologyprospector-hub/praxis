"""Core representation of a human-defined problem.

The Problem object is deliberately domain-local. Organs may transport or
coordinate it later, but runtime infrastructure must not become the owner of
Praxis's problem semantics.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json


def _clean_items(items: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    cleaned = tuple(item.strip() for item in items)
    if any(not item for item in cleaned):
        raise ValueError(f"{field_name} must not contain empty items")
    return cleaned


@dataclass(frozen=True)
class Problem:
    """An explicitly human-defined problem and the constraints that shape it."""

    id: str
    title: str
    goal: str
    constraints: tuple[str, ...] = field(default_factory=tuple)
    values: tuple[str, ...] = field(default_factory=tuple)
    non_negotiables: tuple[str, ...] = field(default_factory=tuple)
    stakeholders: tuple[str, ...] = field(default_factory=tuple)
    known_risks: tuple[str, ...] = field(default_factory=tuple)
    acceptable_tradeoffs: tuple[str, ...] = field(default_factory=tuple)
    unacceptable_tradeoffs: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "title", "goal"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        for name in (
            "constraints",
            "values",
            "non_negotiables",
            "stakeholders",
            "known_risks",
            "acceptable_tradeoffs",
            "unacceptable_tradeoffs",
        ):
            value = getattr(self, name)
            if not isinstance(value, tuple):
                raise TypeError(f"{name} must be a tuple of strings")
            _clean_items(value, name)

    def to_dict(self) -> dict[str, object]:
        """Return a stable JSON-compatible representation."""
        return asdict(self)

    def to_json(self) -> str:
        """Serialize deterministically for storage, transport, and tests."""
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
