"""Explicit linkage between a bounded test and its governing decision."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json

@dataclass(frozen=True)
class DecisionScope:
    """Records what a human decision governs without executing that decision."""

    id: str
    decision_id: str
    problem_id: str
    test_id: str = ""
    intervention_id: str = ""

    def __post_init__(self) -> None:
        for name in ("id", "decision_id", "problem_id", "test_id", "intervention_id"):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if name not in ("test_id", "intervention_id") and not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
            if name in ("test_id", "intervention_id") and value and not value.strip():
                raise ValueError(f"{name} must be non-empty when provided")
        if not self.test_id and not self.intervention_id:
            raise ValueError("decision scope requires a test or intervention")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
