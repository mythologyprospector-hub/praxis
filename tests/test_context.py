from __future__ import annotations

import json

import pytest

from praxis.context import ReasoningContext
from praxis.evidence import EvidenceItem, EvidenceState
from praxis.gap import EvidenceGap
from praxis.problem import Problem


def test_reasoning_context_joins_matching_grounded_inputs() -> None:
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
    gap = EvidenceGap(
        id="g1",
        problem_id="p1",
        description="A material unknown.",
        decision_relevance="It could change the next test.",
    )

    context = ReasoningContext(problem=problem, evidence=evidence, gaps=(gap,))

    assert context.to_dict() == {
        "problem": problem.to_dict(),
        "evidence": evidence.to_dict(),
        "gaps": [gap.to_dict()],
    }
    assert context.to_json() == json.dumps(
        context.to_dict(), sort_keys=True, separators=(",", ":")
    )


def test_reasoning_context_allows_no_gaps() -> None:
    problem = Problem(id="p1", title="Problem", goal="Learn.")
    evidence = EvidenceState(problem_id="p1")

    context = ReasoningContext(problem=problem, evidence=evidence)

    assert context.gaps == ()
    assert context.to_dict()["gaps"] == []


def test_reasoning_context_rejects_evidence_for_another_problem() -> None:
    problem = Problem(id="p1", title="Problem", goal="Learn.")
    evidence = EvidenceState(problem_id="p2")

    with pytest.raises(ValueError, match="problem_id"):
        ReasoningContext(problem=problem, evidence=evidence)


def test_reasoning_context_rejects_gap_for_another_problem() -> None:
    problem = Problem(id="p1", title="Problem", goal="Learn.")
    evidence = EvidenceState(problem_id="p1")
    gap = EvidenceGap(
        id="g1",
        problem_id="p2",
        description="A material unknown.",
        decision_relevance="It could change the next test.",
    )

    with pytest.raises(ValueError, match="problem_id"):
        ReasoningContext(problem=problem, evidence=evidence, gaps=(gap,))

def test_reasoning_context_requires_typed_unique_gaps() -> None:
    problem = Problem(id="p1", title="Problem", goal="Learn.")
    evidence = EvidenceState(problem_id="p1")
    gap = EvidenceGap(
        id="g1",
        problem_id="p1",
        description="A material unknown.",
        decision_relevance="Relevant.",
    )

    with pytest.raises(TypeError, match="tuple"):
        ReasoningContext(problem=problem, evidence=evidence, gaps=[gap])

    with pytest.raises(TypeError, match="EvidenceGap"):
        ReasoningContext(problem=problem, evidence=evidence, gaps=("not a gap",))

    with pytest.raises(ValueError, match="unique"):
        ReasoningContext(problem=problem, evidence=evidence, gaps=(gap, gap))
