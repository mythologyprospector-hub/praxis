"""Explicit hypotheses keep proposed explanations separate from evidence."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json


@dataclass(frozen=True)
class Hypothesis:
    """A proposed explanation or mechanism, not an evidence claim."""

    id: str
    problem_id: str
    statement: str
    rationale: str
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "problem_id", "statement", "rationale"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        if not isinstance(self.evidence_ids, tuple):
            raise TypeError("evidence_ids must be a tuple of strings")
        cleaned = tuple(item.strip() for item in self.evidence_ids)
        if any(not item for item in cleaned):
            raise ValueError("evidence_ids must not contain empty items")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
