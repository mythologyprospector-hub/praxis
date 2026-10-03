"""Explicit models keep calculations and simulations distinct from evidence and decisions."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json


@dataclass(frozen=True)
class Model:
    """A bounded calculation or simulation used to explore a defined problem."""

    id: str
    problem_id: str
    purpose: str
    method: str
    input_ids: tuple[str, ...] = field(default_factory=tuple)
    assumptions: tuple[str, ...] = field(default_factory=tuple)
    outputs: tuple[str, ...] = field(default_factory=tuple)
    uncertainty: str = ""

    def __post_init__(self) -> None:
        for name in ("id", "problem_id", "purpose", "method"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        if not isinstance(self.uncertainty, str):
            raise TypeError("uncertainty must be a string")

        for name in ("input_ids", "assumptions", "outputs"):
            values = getattr(self, name)
            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be a tuple of strings")
            cleaned = tuple(item.strip() for item in values)
            if any(not item for item in cleaned):
                raise ValueError(f"{name} must not contain empty items")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
