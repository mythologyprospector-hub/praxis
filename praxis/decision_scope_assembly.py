"""Bounded assembly for scoped decisions."""

from __future__ import annotations

from praxis.decision import Decision
from praxis.decision_scope import DecisionScope
from praxis.intervention import Intervention
from praxis.test import Test


def assemble_decision_scope(
    scope: DecisionScope,
    decision: Decision,
    test: Test | None = None,
    intervention: Intervention | None = None,
) -> DecisionScope:
    """Validate that a DecisionScope actually scopes its decision and target."""
    if not isinstance(scope, DecisionScope):
        raise TypeError("scope must be a DecisionScope")
    if not isinstance(decision, Decision):
        raise TypeError("decision must be a Decision")
    if scope.decision_id != decision.id:
        raise ValueError("scope targets a different decision")
    if decision.problem_id != scope.problem_id:
        raise ValueError("decision belongs to a different problem")
    if scope.test_id:
        if not isinstance(test, Test):
            raise TypeError("test must be a Test when test_id is scoped")
        if test.id != scope.test_id:
            raise ValueError("test belongs to a different decision scope")
        if test.problem_id != scope.problem_id:
            raise ValueError("test belongs to a different problem")
    if scope.intervention_id:
        if not isinstance(intervention, Intervention):
            raise TypeError(
                "intervention must be an Intervention when intervention_id is scoped"
            )
        if intervention.id != scope.intervention_id:
            raise ValueError("intervention belongs to a different decision scope")
        if intervention.problem_id != scope.problem_id:
            raise ValueError("intervention belongs to a different problem")
    if scope.test_id and scope.intervention_id:
        if scope.intervention_id not in test.intervention_ids:
            raise ValueError("intervention is outside the scoped test")
    return scope
