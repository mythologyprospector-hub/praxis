"""Explicit request boundary for recording an observed test result."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
import json

@dataclass(frozen=True)
class ResultRequest:
    """A bounded request to capture observations from a completed test."""

    id: str
    problem_id: str
    test_id: str
    expected_observation_ids: tuple[str, ...] = field(default_factory=tuple)
    intervention_ids: tuple[str, ...] = field(default_factory=tuple)
    constraints: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "problem_id", "test_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        for name in ("expected_observation_ids","intervention_ids","constraints"):
            values = getattr(self, name)
            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be a tuple of strings")
            cleaned = tuple(item.strip() for item in values)
            if any(not item for item in cleaned):
                raise ValueError(f"{name} must not contain empty items")
            if len(cleaned) != len(set(cleaned)):
                raise ValueError(f"{name} must contain unique items")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
