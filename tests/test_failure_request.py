from __future__ import annotations
import json
import pytest
from praxis.failure_request import FailureAnalysisRequest

def test_request_defines_inputs_without_becoming_a_finding():
    request = FailureAnalysisRequest(id="attack-1", problem_id="problem-1", intervention_ids=("intervention-1",), hypothesis_ids=("hyp-1",), model_ids=("model-1",), focus_areas=("boundary conditions",), constraints=("preserve reversibility",))
    data = request.to_dict()
    assert data["problem_id"] == "problem-1"
    assert data["intervention_ids"] == ("intervention-1",)
    assert "severity" not in data and "likelihood" not in data and "decision" not in data

def test_request_requires_an_intervention():
    with pytest.raises(ValueError):
        FailureAnalysisRequest(id="attack-1", problem_id="problem-1")

def test_request_requires_unique_inputs():
    with pytest.raises(ValueError):
        FailureAnalysisRequest(id="attack-1", problem_id="problem-1", intervention_ids=("i-1", "i-1"))
    with pytest.raises(ValueError):
        FailureAnalysisRequest(id="attack-1", problem_id="problem-1", intervention_ids=("i-1",), focus_areas=("same", "same"))

def test_request_requires_tuple_fields():
    with pytest.raises(TypeError):
        FailureAnalysisRequest(id="attack-1", problem_id="problem-1", intervention_ids=["i-1"])  # type: ignore[arg-type]

def test_request_serialization_is_deterministic():
    request = FailureAnalysisRequest(id="attack-1", problem_id="problem-1", intervention_ids=("i-1",))
    assert request.to_json() == json.dumps(request.to_dict(), sort_keys=True, separators=(",", ":"))
