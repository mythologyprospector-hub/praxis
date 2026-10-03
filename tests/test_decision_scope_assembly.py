from __future__ import annotations

import pytest

from praxis.decision import Decision
from praxis.decision_scope import DecisionScope
from praxis.decision_scope_assembly import assemble_decision_scope
from praxis.intervention import Intervention
from praxis.test import Test


def _decision() -> Decision:
    return Decision(
        id="decision-1",
        problem_id="problem-1",
        decision="Proceed with bounded test.",
        rationale="Human choice.",
        decided_by="human-1",
    )


def _test() -> Test:
    return Test(
        id="test-1",
        problem_id="problem-1",
        objective="Learn whether the intervention meets the test criterion.",
        expected_observations=("Observed outcome.",),
        safety_constraints=("Stop on unsafe result.",),
        reversibility="Reversible.",
        decision_criteria=("Use the observed result.",),
        intervention_ids=("intervention-1",),
    )


def _intervention() -> Intervention:
    return Intervention(
        id="intervention-1",
        problem_id="problem-1",
        description="A bounded proposed change.",
        intended_outcome="Improve the defined outcome.",
    )


def _scope() -> DecisionScope:
    return DecisionScope(
        id="scope-1",
        decision_id="decision-1",
        problem_id="problem-1",
        test_id="test-1",
        intervention_id="intervention-1",
    )


def test_matching_decision_accepts_scope() -> None:
    assert (
        assemble_decision_scope(_scope(), _decision(), _test(), _intervention())
        == _scope()
    )


def test_wrong_decision_rejected() -> None:
    scope = DecisionScope(
        id="scope-1", decision_id="decision-2",
        problem_id="problem-1", test_id="test-1",
    )
    with pytest.raises(ValueError, match="decision"):
        assemble_decision_scope(scope, _decision(), _test())


def test_wrong_problem_rejected() -> None:
    scope = DecisionScope(
        id="scope-1", decision_id="decision-1",
        problem_id="problem-2", test_id="test-1",
    )
    with pytest.raises(ValueError, match="problem"):
        assemble_decision_scope(scope, _decision(), _test())


def test_wrong_test_rejected() -> None:
    scope = DecisionScope(
        id="scope-1", decision_id="decision-1",
        problem_id="problem-1", test_id="test-2",
    )
    with pytest.raises(ValueError, match="test"):
        assemble_decision_scope(scope, _decision(), _test())


def test_wrong_intervention_rejected() -> None:
    scope = DecisionScope(
        id="scope-1", decision_id="decision-1",
        problem_id="problem-1", intervention_id="intervention-2",
    )
    with pytest.raises(ValueError, match="intervention"):
        assemble_decision_scope(scope, _decision(), intervention=_intervention())


def test_intervention_outside_test_rejected() -> None:
    test = Test(
        id="test-1",
        problem_id="problem-1",
        objective="Learn whether the intervention meets the test criterion.",
        expected_observations=("Observed outcome.",),
        safety_constraints=("Stop on unsafe result.",),
        reversibility="Reversible.",
        decision_criteria=("Use the observed result.",),
        intervention_ids=(),
    )
    with pytest.raises(ValueError, match="outside"):
        assemble_decision_scope(
            _scope(), _decision(), test, _intervention()
        )


def test_wrong_scope_type_rejected() -> None:
    with pytest.raises(TypeError, match="DecisionScope"):
        assemble_decision_scope(object(), _decision())  # type: ignore[arg-type]


def test_wrong_decision_type_rejected() -> None:
    with pytest.raises(TypeError, match="Decision"):
        assemble_decision_scope(_scope(), object(), _test())  # type: ignore[arg-type]


def test_missing_test_rejected() -> None:
    with pytest.raises(TypeError, match="Test"):
        assemble_decision_scope(_scope(), _decision())


def test_missing_intervention_rejected() -> None:
    scope = DecisionScope(
        id="scope-1",
        decision_id="decision-1",
        problem_id="problem-1",
        intervention_id="intervention-1",
    )
    with pytest.raises(TypeError, match="Intervention"):
        assemble_decision_scope(scope, _decision())
