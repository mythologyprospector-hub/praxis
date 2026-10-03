from __future__ import annotations

import pytest

from praxis.decision import Decision
from praxis.decision_scope import DecisionScope
from praxis.decision_scope_assembly import assemble_decision_scope


def _decision() -> Decision:
    return Decision(
        id="decision-1",
        problem_id="problem-1",
        decision="Proceed with bounded test.",
        rationale="Human choice.",
        decided_by="human-1",
    )


def _scope() -> DecisionScope:
    return DecisionScope(
        id="scope-1",
        decision_id="decision-1",
        problem_id="problem-1",
        test_id="test-1",
    )


def test_matching_decision_accepts_scope() -> None:
    assert assemble_decision_scope(_scope(), _decision()) == _scope()


def test_wrong_decision_rejected() -> None:
    scope = DecisionScope(
        id="scope-1", decision_id="decision-2",
        problem_id="problem-1", test_id="test-1",
    )
    with pytest.raises(ValueError, match="decision"):
        assemble_decision_scope(scope, _decision())


def test_wrong_problem_rejected() -> None:
    scope = DecisionScope(
        id="scope-1", decision_id="decision-1",
        problem_id="problem-2", test_id="test-1",
    )
    with pytest.raises(ValueError, match="problem"):
        assemble_decision_scope(scope, _decision())


def test_wrong_scope_type_rejected() -> None:
    with pytest.raises(TypeError, match="DecisionScope"):
        assemble_decision_scope(object(), _decision())  # type: ignore[arg-type]


def test_wrong_decision_type_rejected() -> None:
    with pytest.raises(TypeError, match="Decision"):
        assemble_decision_scope(_scope(), object())  # type: ignore[arg-type]
