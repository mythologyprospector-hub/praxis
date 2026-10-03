"""Bounded assembly for explicit human decisions."""

from __future__ import annotations

from praxis.decision import Decision
from praxis.decision_request import DecisionRequest


def assemble_decision(request: DecisionRequest, decision: Decision) -> Decision:
    """Validate a human decision against its explicit decision request."""
    if not isinstance(decision, Decision):
        raise TypeError("decision must be a Decision")
    if decision.id == request.id:
        raise ValueError("decision identity must differ from request identity")
    if decision.problem_id != request.problem_id:
        raise ValueError("decision belongs to a different problem")
    if decision.subject_id != request.subject_id:
        raise ValueError("decision belongs to a different subject")
    return decision
