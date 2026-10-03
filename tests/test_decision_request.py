from __future__ import annotations
import json
import pytest
from praxis.decision_request import DecisionRequest

def test_request_makes_decision_inputs_explicit():
    request=DecisionRequest(id="r-1",problem_id="p-1",subject_id="s-1",candidate_ids=("c-1",),test_ids=("t-1",),result_ids=("res-1",),evidence_ids=("e-1",))
    data=request.to_dict()
    assert data["subject_id"]=="s-1"
    assert data["candidate_ids"]==("c-1",)
    assert "decision" not in data
    assert "decided_by" not in data

def test_request_requires_core_identity():
    with pytest.raises(ValueError):
        DecisionRequest(id="r-1",problem_id="p-1",subject_id=" ")

def test_request_rejects_duplicate_inputs():
    with pytest.raises(ValueError):
        DecisionRequest(id="r-1",problem_id="p-1",subject_id="s-1",result_ids=("res-1","res-1"))

def test_request_requires_tuple_fields():
    with pytest.raises(TypeError):
        DecisionRequest(id="r-1",problem_id="p-1",subject_id="s-1",candidate_ids=["c-1"]) # type: ignore[arg-type]

def test_request_serialization_is_deterministic():
    request=DecisionRequest(id="r-1",problem_id="p-1",subject_id="s-1")
    assert request.to_json()==json.dumps(request.to_dict(),sort_keys=True,separators=(",",":"))
