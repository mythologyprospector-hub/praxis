"""Observed test results remain distinct from test plans and evidence."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json


@dataclass(frozen=True)
class Result:
    """What was observed when a bounded test was performed."""

    id: str
    test_id: str
    summary: str
    observations: tuple[str, ...]
    provenance: str
    uncertainty: str
    deviations: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for name in ("id", "test_id", "summary", "provenance", "uncertainty"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

        for name in ("observations", "deviations"):
            value = getattr(self, name)
            if not isinstance(value, tuple):
                raise TypeError(f"{name} must be a tuple of strings")
            cleaned = tuple(item.strip() for item in value)
            if any(not item for item in cleaned):
                raise ValueError(f"{name} must not contain empty items")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
