"""Bounded assembly for explicit human decisions."""

from __future__ import annotations

from praxis.decision import Decision
from praxis.decision_request import DecisionRequest
from praxis.decision_lineage import validate_decision_lineage


def assemble_decision(request: DecisionRequest, decision: Decision, *, candidate_sets=(), tests=(), results=(), evidence_items=()) -> Decision:
    """Validate a human decision against its explicit decision request."""
    if not isinstance(decision, Decision):
        raise TypeError("decision must be a Decision")
    if decision.id == request.id:
        raise ValueError("decision identity must differ from request identity")
    if decision.problem_id != request.problem_id:
        raise ValueError("decision belongs to a different problem")
    if decision.subject_id != request.subject_id:
        raise ValueError("decision belongs to a different subject")
    validate_decision_lineage(request, candidate_sets=candidate_sets, tests=tests, results=results, evidence_items=evidence_items)
    return decision
