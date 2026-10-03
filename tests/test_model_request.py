from __future__ import annotations
import json
import pytest
from praxis.model_request import ModelRequest

def test_request_makes_model_inputs_explicit():
    request=ModelRequest(id="r-1",problem_id="p-1",purpose="compare candidates",input_ids=("e-1",),hypothesis_ids=("h-1",),intervention_ids=("i-1",))
    data=request.to_dict()
    assert data["purpose"]=="compare candidates"
    assert data["input_ids"]==("e-1",)
    assert "output" not in data
    assert "decision" not in data

def test_request_requires_core_identity_and_purpose():
    with pytest.raises(ValueError):
        ModelRequest(id="r-1",problem_id="p-1",purpose=" ")

def test_request_rejects_duplicate_inputs():
    with pytest.raises(ValueError):
        ModelRequest(id="r-1",problem_id="p-1",purpose="x",input_ids=("e-1","e-1"))

def test_request_requires_tuple_fields():
    with pytest.raises(TypeError):
        ModelRequest(id="r-1",problem_id="p-1",purpose="x",input_ids=["e-1"]) # type: ignore[arg-type]

def test_request_serialization_is_deterministic():
    request=ModelRequest(id="r-1",problem_id="p-1",purpose="x")
    assert request.to_json()==json.dumps(request.to_dict(),sort_keys=True,separators=(",",":"))
