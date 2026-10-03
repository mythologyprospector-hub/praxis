"""Explicit gaps keep missing knowledge separate from evidence and inference."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class EvidenceGap:
    """A material unknown or unresolved uncertainty in a defined problem."""

    id: str
    problem_id: str
    description: str
    decision_relevance: str

    def __post_init__(self) -> None:
        for name in ("id", "problem_id", "description", "decision_relevance"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
