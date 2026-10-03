"""Explicit hypotheses keep proposed explanations separate from evidence."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class Hypothesis:
    """A proposed explanation or mechanism, not an evidence claim."""

    id: str
    problem_id: str
    statement: str
    rationale: str

    def __post_init__(self) -> None:
        for name in ("id", "problem_id", "statement", "rationale"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
