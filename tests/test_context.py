from __future__ import annotations

import json

import pytest

from praxis.context import ReasoningContext
from praxis.evidence import EvidenceItem, EvidenceState
from praxis.problem import Problem


def test_reasoning_context_joins_matching_problem_and_evidence() -> None:
    problem = Problem(id="p1", title="Problem", goal="Learn.")
    evidence = EvidenceState(
        problem_id="p1",
        items=(
            EvidenceItem(
                id="e1",
                statement="Observation",
                provenance="source-1",
                uncertainty="limited sample",
            ),
        ),
    )

    context = ReasoningContext(problem=problem, evidence=evidence)

    assert context.to_dict() == {"problem": problem.to_dict(), "evidence": evidence.to_dict()}
    assert json.loads(context.to_json()) == context.to_dict()


def test_reasoning_context_rejects_evidence_for_another_problem() -> None:
    problem = Problem(id="p1", title="Problem", goal="Learn.")
    evidence = EvidenceState(problem_id="p2")

    with pytest.raises(ValueError, match="problem_id"):
        ReasoningContext(problem=problem, evidence=evidence)
