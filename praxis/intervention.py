"""Candidate interventions remain proposals distinct from evidence and results."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json


@dataclass(frozen=True)
class Intervention:
    """A proposed change intended to alter an outcome for a defined problem."""

    id: str
    problem_id: str
    description: str
    intended_outcome: str
    hypothesis_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "problem_id", "description", "intended_outcome"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        if not isinstance(self.hypothesis_ids, tuple):
            raise TypeError("hypothesis_ids must be a tuple of strings")
        cleaned = tuple(item.strip() for item in self.hypothesis_ids)
        if any(not item for item in cleaned):
            raise ValueError("hypothesis_ids must not contain empty items")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
