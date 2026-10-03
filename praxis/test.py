"""Bounded test objects remain separate from interventions and results."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json


@dataclass(frozen=True)
class Test:
    """A bounded method for learning about a candidate intervention."""

    id: str
    problem_id: str
    objective: str
    expected_observations: tuple[str, ...]
    safety_constraints: tuple[str, ...]
    reversibility: str
    decision_criteria: tuple[str, ...]
    intervention_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "problem_id", "objective", "reversibility"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        for name in (
            "expected_observations",
            "safety_constraints",
            "decision_criteria",
            "intervention_ids",
        ):
            value = getattr(self, name)
            if not isinstance(value, tuple):
                raise TypeError(f"{name} must be a tuple of strings")
            cleaned = tuple(item.strip() for item in value)
            if any(not item for item in cleaned):
                raise ValueError(f"{name} must not contain empty items")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
