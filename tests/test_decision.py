from __future__ import annotations

import json

import pytest

from praxis.decision import Decision


def test_decision_records_human_authority_without_becoming_an_execution() -> None:
    decision = Decision(
        id="decision-1",
        problem_id="problem-1",
        decision="Proceed to the bounded test.",
        rationale="The current evidence and safety constraints justify the next step.",
        decided_by="human-decision-1",
        subject_id="test-1",
    )

    assert decision.to_dict() == {
        "id": "decision-1",
        "problem_id": "problem-1",
        "decision": "Proceed to the bounded test.",
        "rationale": "The current evidence and safety constraints justify the next step.",
        "decided_by": "human-decision-1",
        "subject_id": "test-1",
    }


def test_decision_requires_human_identity_and_rationale() -> None:
    with pytest.raises(ValueError, match="decided_by"):
        Decision(
            id="decision-1",
            problem_id="problem-1",
            decision="Proceed.",
            rationale="Reason.",
            decided_by="",
        )

    with pytest.raises(ValueError, match="rationale"):
        Decision(
            id="decision-1",
            problem_id="problem-1",
            decision="Proceed.",
            rationale="",
            decided_by="human-1",
        )


def test_decision_rejects_invalid_optional_subject() -> None:
    with pytest.raises(ValueError, match="subject_id"):
        Decision(
            id="decision-1",
            problem_id="problem-1",
            decision="Proceed.",
            rationale="Reason.",
            decided_by="human-1",
            subject_id=" ",
        )


def test_decision_serialization_is_deterministic() -> None:
    decision = Decision(
        id="decision-1",
        problem_id="problem-1",
        decision="Proceed.",
        rationale="Reason.",
        decided_by="human-1",
    )

    assert decision.to_json() == json.dumps(
        decision.to_dict(), sort_keys=True, separators=(",", ":")
    )
