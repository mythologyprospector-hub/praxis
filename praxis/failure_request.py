"""Failure-analysis requests make attack inputs explicit without making risk judgments."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
import json

@dataclass(frozen=True)
class FailureAnalysisRequest:
    """A bounded request to examine candidate interventions for failure modes."""

    id: str
    problem_id: str
    intervention_ids: tuple[str, ...] = field(default_factory=tuple)
    hypothesis_ids: tuple[str, ...] = field(default_factory=tuple)
    model_ids: tuple[str, ...] = field(default_factory=tuple)
    focus_areas: tuple[str, ...] = field(default_factory=tuple)
    constraints: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "problem_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        for name in ("intervention_ids", "hypothesis_ids", "model_ids", "focus_areas", "constraints"):
            values = getattr(self, name)
            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be a tuple of strings")
            cleaned = tuple(item.strip() for item in values)
            if any(not item for item in cleaned):
                raise ValueError(f"{name} must not contain empty items")
            if len(cleaned) != len(set(cleaned)):
                raise ValueError(f"{name} must contain unique items")
        if not self.intervention_ids:
            raise ValueError("failure analysis requires at least one intervention")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
