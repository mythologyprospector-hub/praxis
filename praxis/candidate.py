"""Candidate sets keep generated possibilities grouped without turning them into decisions."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json


@dataclass(frozen=True)
class CandidateSet:
    """A bounded set of candidate hypotheses and/or interventions for a problem."""

    id: str
    problem_id: str
    hypothesis_ids: tuple[str, ...] = field(default_factory=tuple)
    intervention_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "problem_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        for name in ("hypothesis_ids", "intervention_ids"):
            values = getattr(self, name)
            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be a tuple of strings")
            cleaned = tuple(item.strip() for item in values)
            if any(not item for item in cleaned):
                raise ValueError(f"{name} must not contain empty items")
            if len(cleaned) != len(set(cleaned)):
                raise ValueError(f"{name} must contain unique ids")

        if not self.hypothesis_ids and not self.intervention_ids:
            raise ValueError("candidate set must contain at least one candidate")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
