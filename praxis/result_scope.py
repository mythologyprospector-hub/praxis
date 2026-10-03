"""Explicit result linkage preserves what was actually tested and observed."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
import json

@dataclass(frozen=True)
class ResultScope:
    """Links an observed Result to its bounded test and optional intervention."""

    id: str
    result_id: str
    problem_id: str
    test_id: str
    intervention_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "result_id", "problem_id", "test_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(self.intervention_ids, tuple):
            raise TypeError("intervention_ids must be a tuple of strings")
        cleaned = tuple(item.strip() for item in self.intervention_ids)
        if any(not item for item in cleaned):
            raise ValueError("intervention_ids must not contain empty items")
        if len(cleaned) != len(set(cleaned)):
            raise ValueError("intervention_ids must contain unique items")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
