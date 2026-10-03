"""Explicit request boundary for admitting a result-derived evidence item."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json

@dataclass(frozen=True)
class EvidenceAdmissionRequest:
    """A bounded request to seek human authorization for evidence admission."""

    id: str
    problem_id: str
    result_id: str
    evidence_item_id: str
    rationale: str

    def __post_init__(self) -> None:
        for name in ("id", "problem_id", "result_id", "evidence_item_id", "rationale"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
