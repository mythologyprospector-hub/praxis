from __future__ import annotations

import pytest

from praxis.admission import EvidenceAdmission
from praxis.evidence import EvidenceItem, EvidenceState
from praxis.evidence_admission_request import EvidenceAdmissionRequest
from praxis.result import Result
from praxis.result_evidence_admission import admit_result_as_evidence


def _state() -> EvidenceState:
    return EvidenceState(problem_id="problem-1")


def _request(**overrides: object) -> EvidenceAdmissionRequest:
    values: dict[str, object] = {
        "id": "request-1",
        "problem_id": "problem-1",
        "result_id": "result-1",
        "evidence_item_id": "evidence-1",
        "rationale": "Observed result may be admitted.",
    }
    values.update(overrides)
    return EvidenceAdmissionRequest(**values)  # type: ignore[arg-type]


def _admission(**overrides: object) -> EvidenceAdmission:
    values: dict[str, object] = {
        "id": "admission-1",
        "problem_id": "problem-1",
        "evidence_item_id": "evidence-1",
        "authorized_by": "human-1",
        "rationale": "Authorized.",
    }
    values.update(overrides)
    return EvidenceAdmission(**values)  # type: ignore[arg-type]


def _result(**overrides: object) -> Result:
    values: dict[str, object] = {
        "id": "result-1",
        "test_id": "test-1",
        "summary": "Observed outcome.",
        "observations": ("outcome",),
        "provenance": "experiment-log",
        "uncertainty": "moderate",
    }
    values.update(overrides)
    return Result(**values)  # type: ignore[arg-type]


def _item(**overrides: object) -> EvidenceItem:
    values: dict[str, object] = {
        "id": "evidence-1",
        "statement": "Observed outcome.",
        "provenance": "experiment-log",
        "uncertainty": "moderate",
        "source_result_id": "result-1",
    }
    values.update(overrides)
    return EvidenceItem(**values)  # type: ignore[arg-type]


def test_matching_lineage_admits_result_as_evidence() -> None:
    result = admit_result_as_evidence(_state(), _request(), _admission(), _result(), _item())
    assert result.problem_id == "problem-1"
    assert result.items == (_item(),)


def test_wrong_result_rejected() -> None:
    with pytest.raises(ValueError, match="supplied result"):
        admit_result_as_evidence(
            _state(),
            _request(),
            _admission(),
            _result(id="result-2"),
            _item(),
        )


def test_wrong_request_result_rejected() -> None:
    with pytest.raises(ValueError, match="does not match"):
        admit_result_as_evidence(
            _state(),
            _request(result_id="result-2"),
            _admission(),
            _result(),
            _item(),
        )


def test_wrong_state_problem_rejected() -> None:
    with pytest.raises(ValueError, match="problem_id"):
        admit_result_as_evidence(
            EvidenceState(problem_id="problem-2"),
            _request(),
            _admission(),
            _result(),
            _item(),
        )


def test_wrong_evidence_identity_rejected() -> None:
    with pytest.raises(ValueError, match="does not reference"):
        admit_result_as_evidence(
            _state(),
            _request(),
            _admission(),
            _result(),
            _item(source_result_id="result-2"),
        )
