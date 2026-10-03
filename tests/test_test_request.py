from __future__ import annotations
import json
import pytest
from praxis.test_request import TestRequest

def test_request_makes_test_design_inputs_explicit():
    request=TestRequest(id="request-1",problem_id="problem-1",intervention_ids=("i-1",),failure_mode_ids=("f-1",),model_ids=("m-1",))
    data=request.to_dict()
    assert data["intervention_ids"]==("i-1",)
    assert data["failure_mode_ids"]==("f-1",)
    assert "decision" not in data
    assert "execute" not in data

def test_request_requires_an_intervention():
    with pytest.raises(ValueError):
        TestRequest(id="request-1",problem_id="problem-1")

def test_request_rejects_duplicate_inputs():
    with pytest.raises(ValueError):
        TestRequest(id="request-1",problem_id="problem-1",intervention_ids=("i-1","i-1"))

def test_request_requires_tuple_fields():
    with pytest.raises(TypeError):
        TestRequest(id="request-1",problem_id="problem-1",intervention_ids=["i-1"]) # type: ignore[arg-type]

def test_request_serialization_is_deterministic():
    request=TestRequest(id="request-1",problem_id="problem-1",intervention_ids=("i-1",))
    assert request.to_json()==json.dumps(request.to_dict(),sort_keys=True,separators=(",",":"))
