"""Failure-analysis objects remain explicit and separate from proposals."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json


@dataclass(frozen=True)
class FailureMode:
    """A concrete way a candidate intervention could fail or cause harm."""

    id: str
    problem_id: str
    description: str
    severity: str
    likelihood: str
    intervention_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "problem_id", "description", "severity", "likelihood"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        if not isinstance(self.intervention_ids, tuple):
            raise TypeError("intervention_ids must be a tuple of strings")
        cleaned = tuple(item.strip() for item in self.intervention_ids)
        if any(not item for item in cleaned):
            raise ValueError("intervention_ids must not contain empty items")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
