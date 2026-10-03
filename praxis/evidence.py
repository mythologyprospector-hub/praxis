"""Evidence representations for a Praxis problem.

Evidence is deliberately narrower than inference or hypothesis. An EvidenceItem
records an externally grounded statement together with enough provenance and
uncertainty information to keep its epistemic status inspectable.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json


@dataclass(frozen=True)
class EvidenceItem:
    """A single evidence-bearing statement with explicit provenance."""

    id: str
    statement: str
    provenance: str
    uncertainty: str

    def __post_init__(self) -> None:
        for name in ("id", "statement", "provenance", "uncertainty"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceState:
    """The current evidence explicitly associated with one Problem."""

    problem_id: str
    items: tuple[EvidenceItem, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.problem_id, str) or not self.problem_id.strip():
            raise ValueError("problem_id must be a non-empty string")
        if not isinstance(self.items, tuple):
            raise TypeError("items must be a tuple of EvidenceItem")
        if any(not isinstance(item, EvidenceItem) for item in self.items):
            raise TypeError("items must contain only EvidenceItem instances")

    def to_dict(self) -> dict[str, object]:
        return {
            "problem_id": self.problem_id,
            "items": [item.to_dict() for item in self.items],
        }

    def to_json(self) -> str:
        """Serialize deterministically for storage and later transport."""
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
