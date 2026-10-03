from __future__ import annotations

import pytest

from praxis.failure_analysis import FailureAnalysis
from praxis.failure_analysis_assembly import assemble_failure_analysis
from praxis.failure_request import FailureAnalysisRequest


def _request() -> FailureAnalysisRequest:
    return FailureAnalysisRequest(
        id="request-1",
        problem_id="problem-1",
        intervention_ids=("intervention-1",),
    )


def _analysis() -> FailureAnalysis:
    return FailureAnalysis(
        id="analysis-1",
        request_id="request-1",
        problem_id="problem-1",
        failure_mode_ids=("failure-1",),
        uncertainty="bounded uncertainty",
    )


def test_matching_request_accepts_analysis() -> None:
    assert assemble_failure_analysis(_request(), _analysis()) == _analysis()


def test_wrong_request_rejected() -> None:
    analysis = FailureAnalysis(
        id="analysis-1", request_id="request-2", problem_id="problem-1",
        failure_mode_ids=("failure-1",), uncertainty="bounded uncertainty"
    )
    with pytest.raises(ValueError, match="request"):
        assemble_failure_analysis(_request(), analysis)


def test_wrong_problem_rejected() -> None:
    analysis = FailureAnalysis(
        id="analysis-1", request_id="request-1", problem_id="problem-2",
        failure_mode_ids=("failure-1",), uncertainty="bounded uncertainty"
    )
    with pytest.raises(ValueError, match="problem"):
        assemble_failure_analysis(_request(), analysis)


def test_empty_findings_rejected() -> None:
    with pytest.raises(ValueError, match="failure mode"):
        FailureAnalysis(
            id="analysis-1", request_id="request-1", problem_id="problem-1",
            failure_mode_ids=(), uncertainty="bounded uncertainty"
        )


def test_identity_must_differ() -> None:
    analysis = FailureAnalysis(
        id="request-1", request_id="request-1", problem_id="problem-1",
        failure_mode_ids=("failure-1",), uncertainty="bounded uncertainty"
    )
    with pytest.raises(ValueError, match="identity"):
        assemble_failure_analysis(_request(), analysis)


def test_wrong_type_rejected() -> None:
    with pytest.raises(TypeError, match="FailureAnalysis"):
        assemble_failure_analysis(_request(), object())  # type: ignore[arg-type]
