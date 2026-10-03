from __future__ import annotations
import json
import pytest
from praxis.result_request import ResultRequest

def test_request_links_observation_capture_to_test():
    request=ResultRequest(id="request-1",problem_id="problem-1",test_id="test-1",expected_observation_ids=("obs-1",),intervention_ids=("i-1",))
    data=request.to_dict()
    assert data["test_id"]=="test-1"
    assert data["expected_observation_ids"]==("obs-1",)
    assert "evidence" not in data
    assert "decision" not in data

def test_request_requires_core_identities():
    with pytest.raises(ValueError):
        ResultRequest(id="request-1",problem_id="problem-1",test_id="")

def test_request_rejects_duplicate_inputs():
    with pytest.raises(ValueError):
        ResultRequest(id="request-1",problem_id="problem-1",test_id="test-1",intervention_ids=("i-1","i-1"))

def test_request_requires_tuple_fields():
    with pytest.raises(TypeError):
        ResultRequest(id="request-1",problem_id="problem-1",test_id="test-1",constraints=["c-1"]) # type: ignore[arg-type]

def test_request_serialization_is_deterministic():
    request=ResultRequest(id="request-1",problem_id="problem-1",test_id="test-1")
    assert request.to_json()==json.dumps(request.to_dict(),sort_keys=True,separators=(",",":"))
