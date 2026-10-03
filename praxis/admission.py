"""Explicit human authorization for incorporating evidence into EvidenceState."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class EvidenceAdmission:
    """A recorded human authorization to add one EvidenceItem to a problem."""

    id: str
    problem_id: str
    evidence_item_id: str
    authorized_by: str
    rationale: str

    def __post_init__(self) -> None:
        for name in (
            "id",
            "problem_id",
            "evidence_item_id",
            "authorized_by",
            "rationale",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
