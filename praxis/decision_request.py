"""Explicit request boundary for reviewing a proposed decision."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
import json

@dataclass(frozen=True)
class DecisionRequest:
    """A bounded request to formulate a decision for human consideration."""

    id: str
    problem_id: str
    subject_id: str
    candidate_ids: tuple[str, ...] = field(default_factory=tuple)
    test_ids: tuple[str, ...] = field(default_factory=tuple)
    result_ids: tuple[str, ...] = field(default_factory=tuple)
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    constraints: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "problem_id", "subject_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        for name in ("candidate_ids","test_ids","result_ids","evidence_ids","constraints"):
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
