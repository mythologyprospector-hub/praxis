from __future__ import annotations

import pytest

from praxis.decision import Decision
from praxis.decision_assembly import assemble_decision
from praxis.decision_request import DecisionRequest


def _request() -> DecisionRequest:
    return DecisionRequest(id="request-1", problem_id="problem-1", subject_id="subject-1")


def _decision() -> Decision:
    return Decision(id="decision-1", problem_id="problem-1", decision="Proceed with bounded test.", rationale="Human choice.", decided_by="human-1")


def test_matching_request_accepts_decision() -> None:
    assert assemble_decision(_request(), _decision()) == _decision()


def test_wrong_problem_rejected() -> None:
    decision = Decision(id="decision-1", problem_id="problem-2", decision="Proceed.", rationale="Choice.", decided_by="human-1")
    with pytest.raises(ValueError, match="problem"):
        assemble_decision(_request(), decision)


def test_request_and_decision_identity_must_differ() -> None:
    decision = Decision(id="request-1", problem_id="problem-1", decision="Proceed.", rationale="Choice.", decided_by="human-1")
    with pytest.raises(ValueError, match="identity"):
        assemble_decision(_request(), decision)


def test_wrong_decision_type_rejected() -> None:
    with pytest.raises(TypeError, match="Decision"):
        assemble_decision(_request(), object())  # type: ignore[arg-type]
