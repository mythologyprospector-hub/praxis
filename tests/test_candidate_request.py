from __future__ import annotations

import json

import pytest

from praxis.candidate_request import CandidateRequest


def test_candidate_request_defines_inputs_without_selecting_candidates() -> None:
    request = CandidateRequest(
        id="request-1",
        problem_id="problem-1",
        evidence_ids=("evidence-1",),
        gap_ids=("gap-1",),
        constraints=("must be reversible",),
    )

    data = request.to_dict()

    assert data["problem_id"] == "problem-1"
    assert data["requested_types"] == ("hypothesis", "intervention")
    assert "candidate_ids" not in data
    assert "decision" not in data


def test_candidate_request_requires_supported_candidate_types() -> None:
    with pytest.raises(ValueError):
        CandidateRequest(
            id="request-1",
            problem_id="problem-1",
            requested_types=("unsupported",),
        )


def test_candidate_request_requires_nonempty_requested_types() -> None:
    with pytest.raises(ValueError):
        CandidateRequest(
            id="request-1",
            problem_id="problem-1",
            requested_types=(),
        )


def test_candidate_request_requires_unique_reference_and_constraint_ids() -> None:
    with pytest.raises(ValueError):
        CandidateRequest(
            id="request-1",
            problem_id="problem-1",
            evidence_ids=("evidence-1", "evidence-1"),
        )

    with pytest.raises(ValueError):
        CandidateRequest(
            id="request-1",
            problem_id="problem-1",
            constraints=("same", "same"),
        )


def test_candidate_request_requires_tuple_fields() -> None:
    with pytest.raises(TypeError):
        CandidateRequest(
            id="request-1",
            problem_id="problem-1",
            gap_ids=["gap-1"],  # type: ignore[arg-type]
        )


def test_candidate_request_serialization_is_deterministic() -> None:
    request = CandidateRequest(
        id="request-1",
        problem_id="problem-1",
        evidence_ids=("evidence-1",),
    )

    assert request.to_json() == json.dumps(
        request.to_dict(), sort_keys=True, separators=(",", ":")
    )
