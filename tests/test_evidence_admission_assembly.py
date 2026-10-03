from __future__ import annotations

import pytest

from praxis.admission import EvidenceAdmission
from praxis.evidence import EvidenceItem
from praxis.evidence_admission_assembly import assemble_evidence_admission
from praxis.evidence_admission_request import EvidenceAdmissionRequest


def _request() -> EvidenceAdmissionRequest:
    return EvidenceAdmissionRequest(id="request-1", problem_id="problem-1", result_id="result-1", evidence_item_id="evidence-1", rationale="Observed result may be admitted.")


def _item(**overrides: object) -> EvidenceItem:
    values: dict[str, object] = {"id":"evidence-1","statement":"Observed outcome.","provenance":"experiment-log","uncertainty":"moderate"}
    values.update(overrides)
    return EvidenceItem(**values)  # type: ignore[arg-type]


def _admission(**overrides: object) -> EvidenceAdmission:
    values: dict[str, object] = {"id":"admission-1","problem_id":"problem-1","evidence_item_id":"evidence-1","authorized_by":"human-1","rationale":"Authorized."}
    values.update(overrides)
    return EvidenceAdmission(**values)  # type: ignore[arg-type]


def test_matching_request_accepts_admission() -> None:
    admission = _admission()
    assert assemble_evidence_admission(_request(), admission, _item()) is admission


def test_wrong_problem_rejected() -> None:
    with pytest.raises(ValueError, match="different problem"):
        assemble_evidence_admission(_request(), _admission(problem_id="problem-2"), _item())


def test_wrong_evidence_item_rejected() -> None:
    with pytest.raises(ValueError, match="different evidence item"):
        assemble_evidence_admission(_request(), _admission(evidence_item_id="evidence-2"), _item())


def test_mismatched_item_rejected() -> None:
    with pytest.raises(ValueError, match="does not match"):
        assemble_evidence_admission(_request(), _admission(), _item(id="evidence-2"))


def test_request_and_admission_identity_must_differ() -> None:
    with pytest.raises(ValueError, match="identity"):
        assemble_evidence_admission(_request(), _admission(id="request-1"), _item())


def test_wrong_admission_type_rejected() -> None:
    with pytest.raises(TypeError, match="EvidenceAdmission"):
        assemble_evidence_admission(_request(), object(), _item())  # type: ignore[arg-type]


def test_wrong_evidence_type_rejected() -> None:
    with pytest.raises(TypeError, match="EvidenceItem"):
        assemble_evidence_admission(_request(), _admission(), object())  # type: ignore[arg-type]
