"""Immutable reasoning context assembled from a defined problem and grounded inputs."""

from __future__ import annotations

from dataclasses import dataclass
import json

from praxis.evidence import EvidenceState
from praxis.gap import EvidenceGap
from praxis.problem import Problem


@dataclass(frozen=True)
class ReasoningContext:
    """The grounded inputs available to a Praxis reasoning step."""

    problem: Problem
    evidence: EvidenceState
    gaps: tuple[EvidenceGap, ...] = ()

    def __post_init__(self) -> None:
        if self.evidence.problem_id != self.problem.id:
            raise ValueError("evidence state problem_id does not match problem")
        for gap in self.gaps:
            if gap.problem_id != self.problem.id:
                raise ValueError("evidence gap problem_id does not match problem")

    def to_dict(self) -> dict[str, object]:
        return {
            "problem": self.problem.to_dict(),
            "evidence": self.evidence.to_dict(),
            "gaps": [gap.to_dict() for gap in self.gaps],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))