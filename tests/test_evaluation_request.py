from __future__ import annotations
import json
import pytest
from praxis.evaluation_request import EvaluationRequest

def test_request_makes_evaluation_inputs_explicit():
    request=EvaluationRequest(id="r-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=("e-1",),gap_ids=("g-1",))
    data=request.to_dict()
    assert data["hypothesis_id"]=="h-1"
    assert data["evidence_ids"]==("e-1",)
    assert "inference" not in data

def test_request_requires_evidence():
    with pytest.raises(ValueError):
        EvaluationRequest(id="r-1",problem_id="p-1",hypothesis_id="h-1")

def test_request_rejects_duplicate_inputs():
    with pytest.raises(ValueError):
        EvaluationRequest(id="r-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=("e-1","e-1"))

def test_request_requires_tuple_fields():
    with pytest.raises(TypeError):
        EvaluationRequest(id="r-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=["e-1"]) # type: ignore[arg-type]

def test_request_serialization_is_deterministic():
    request=EvaluationRequest(id="r-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=("e-1",))
    assert request.to_json()==json.dumps(request.to_dict(),sort_keys=True,separators=(",",":"))
