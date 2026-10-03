"""Evidence representations for a Praxis problem.

Evidence is deliberately narrower than inference or hypothesis. An EvidenceItem
records an externally grounded statement together with enough provenance and
uncertainty information to keep its epistemic status inspectable.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from praxis.result import Result


@dataclass(frozen=True)
class EvidenceItem:
    """A single evidence-bearing statement with explicit provenance."""

    id: str
    statement: str
    provenance: str
    uncertainty: str
    source_result_id: str | None = None

    def __post_init__(self) -> None:
        for name in ("id", "statement", "provenance", "uncertainty"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if self.source_result_id is not None and (
            not isinstance(self.source_result_id, str) or not self.source_result_id.strip()
        ):
            raise ValueError("source_result_id must be a non-empty string when provided")

    @classmethod
    def from_result(cls, result: "Result", statement: str) -> "EvidenceItem":
        """Explicitly admit an observed Result as an evidence-bearing statement."""
        if not isinstance(result.id, str) or not result.id.strip():
            raise ValueError("result must have a non-empty id")
        return cls(
            id=f"evidence:{result.id}",
            statement=statement,
            provenance=result.provenance,
            uncertainty=result.uncertainty,
            source_result_id=result.id,
        )

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        if self.source_result_id is None:
            data.pop("source_result_id")
        return data


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
