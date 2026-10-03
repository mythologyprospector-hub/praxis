"""Traceable derivation metadata for Praxis analysis artifacts."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
import json

@dataclass(frozen=True)
class Derivation:
    """Records how an analysis artifact was produced without judging its validity."""

    id: str
    artifact_id: str
    source_ids: tuple[str, ...] = field(default_factory=tuple)
    method: str = ""
    uncertainty: str = ""

    def __post_init__(self) -> None:
        for name in ("id", "artifact_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(self.source_ids, tuple):
            raise TypeError("source_ids must be a tuple of strings")
        cleaned = tuple(item.strip() for item in self.source_ids)
        if any(not item for item in cleaned):
            raise ValueError("source_ids must not contain empty items")
        if len(cleaned) != len(set(cleaned)):
            raise ValueError("source_ids must contain unique items")
        for name in ("method", "uncertainty"):
            if not isinstance(getattr(self, name), str):
                raise TypeError(f"{name} must be a string")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
