"""Failure-analysis findings record identified failure modes without authorizing action."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
import json

@dataclass(frozen=True)
class FailureAnalysis:
    """A bounded record of failure modes identified for an intervention."""

    id: str
    request_id: str
    problem_id: str
    failure_mode_ids: tuple[str, ...] = field(default_factory=tuple)
    uncertainty: str = ""

    def __post_init__(self) -> None:
        for name in ("id", "request_id", "problem_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        for name in ("failure_mode_ids",):
            values = getattr(self, name)
            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be a tuple of strings")
            cleaned = tuple(item.strip() for item in values)
            if any(not item for item in cleaned):
                raise ValueError(f"{name} must not contain empty items")
            if len(cleaned) != len(set(cleaned)):
                raise ValueError(f"{name} must contain unique items")
        if not self.failure_mode_ids:
            raise ValueError("failure analysis requires at least one failure mode")
        if not isinstance(self.uncertainty, str):
            raise TypeError("uncertainty must be a string")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
