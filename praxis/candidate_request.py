"""Candidate-generation requests define bounded inputs without authorizing selection or action."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json


@dataclass(frozen=True)
class CandidateRequest:
    """A bounded request to generate candidate hypotheses and/or interventions."""

    id: str
    problem_id: str
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    gap_ids: tuple[str, ...] = field(default_factory=tuple)
    requested_types: tuple[str, ...] = ("hypothesis", "intervention")
    constraints: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "problem_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        for name in (
            "evidence_ids",
            "gap_ids",
            "requested_types",
            "constraints",
        ):
            values = getattr(self, name)
            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be a tuple of strings")
            cleaned = tuple(item.strip() for item in values)
            if any(not item for item in cleaned):
                raise ValueError(f"{name} must not contain empty items")
            if len(cleaned) != len(set(cleaned)):
                raise ValueError(f"{name} must contain unique items")

        allowed_types = {"hypothesis", "intervention"}
        if not self.requested_types:
            raise ValueError("requested_types must contain at least one type")
        if any(item not in allowed_types for item in self.requested_types):
            raise ValueError("requested_types contains an unsupported candidate type")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
