"""Bounded assembly for scoped decisions."""

from __future__ import annotations

from praxis.decision import Decision
from praxis.decision_scope import DecisionScope


def assemble_decision_scope(
    scope: DecisionScope,
    decision: Decision,
) -> DecisionScope:
    """Validate that a DecisionScope actually scopes its referenced decision."""
    if not isinstance(scope, DecisionScope):
        raise TypeError("scope must be a DecisionScope")
    if not isinstance(decision, Decision):
        raise TypeError("decision must be a Decision")
    if scope.decision_id != decision.id:
        raise ValueError("scope targets a different decision")
    if decision.problem_id != scope.problem_id:
        raise ValueError("decision belongs to a different problem")
    return scope
