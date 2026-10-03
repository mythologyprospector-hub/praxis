from __future__ import annotations
import json
import pytest
from praxis.failure_analysis import FailureAnalysis

def test_analysis_links_request_and_failure_modes_without_becoming_a_decision():
    analysis=FailureAnalysis(id="analysis-1",request_id="attack-1",problem_id="problem-1",failure_mode_ids=("failure-1",),uncertainty="limited evidence")
    data=analysis.to_dict()
    assert data["request_id"]=="attack-1"
    assert data["failure_mode_ids"]==("failure-1",)
    assert "decision" not in data
    assert "authorized_by" not in data

def test_analysis_requires_a_failure_mode():
    with pytest.raises(ValueError):
        FailureAnalysis(id="analysis-1",request_id="attack-1",problem_id="problem-1")

def test_analysis_requires_unique_failure_modes():
    with pytest.raises(ValueError):
        FailureAnalysis(id="analysis-1",request_id="attack-1",problem_id="problem-1",failure_mode_ids=("f-1","f-1"))

def test_analysis_requires_tuple_failure_modes():
    with pytest.raises(TypeError):
        FailureAnalysis(id="analysis-1",request_id="attack-1",problem_id="problem-1",failure_mode_ids=["f-1"]) # type: ignore[arg-type]

def test_analysis_serialization_is_deterministic():
    analysis=FailureAnalysis(id="analysis-1",request_id="attack-1",problem_id="problem-1",failure_mode_ids=("f-1",))
    assert analysis.to_json()==json.dumps(analysis.to_dict(),sort_keys=True,separators=(",",":"))
