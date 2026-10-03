from __future__ import annotations
import json
import pytest
from praxis.evidence_admission_request import EvidenceAdmissionRequest

def test_request_separates_admission_request_from_authorization():
    request=EvidenceAdmissionRequest(id="request-1",problem_id="problem-1",result_id="result-1",evidence_item_id="evidence-1",rationale="result may resolve a material gap")
    data=request.to_dict()
    assert data["result_id"]=="result-1"
    assert data["evidence_item_id"]=="evidence-1"
    assert "authorized_by" not in data
    assert "evidence" not in data

def test_request_requires_all_identities_and_rationale():
    with pytest.raises(ValueError):
        EvidenceAdmissionRequest(id="r",problem_id="p",result_id="res",evidence_item_id="e",rationale=" ")

def test_request_serialization_is_deterministic():
    request=EvidenceAdmissionRequest(id="r",problem_id="p",result_id="res",evidence_item_id="e",rationale="why")
    assert request.to_json()==json.dumps(request.to_dict(),sort_keys=True,separators=(",",":"))
