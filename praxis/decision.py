"""Explicit human decisions remain distinct from proposals and execution."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json


@dataclass(frozen=True)
class Decision:
    """A recorded human decision about how to proceed within a problem."""

    id: str
    problem_id: str
    decision: str
    rationale: str
    decided_by: str
    subject_id: str | None = None

    def __post_init__(self) -> None:
        for name in ("id", "problem_id", "decision", "rationale", "decided_by"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if self.subject_id is not None and (
            not isinstance(self.subject_id, str) or not self.subject_id.strip()
        ):
            raise ValueError("subject_id must be a non-empty string when provided")

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        if self.subject_id is None:
            data.pop("subject_id")
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
