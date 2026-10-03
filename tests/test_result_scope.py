from __future__ import annotations
import json
import pytest
from praxis.result_scope import ResultScope

def test_scope_links_result_to_test_without_becoming_evidence():
    scope=ResultScope(id="scope-1",result_id="result-1",problem_id="problem-1",test_id="test-1")
    data=scope.to_dict()
    assert data["result_id"]=="result-1"
    assert data["test_id"]=="test-1"
    assert "evidence" not in data
    assert "decision" not in data

def test_scope_can_record_interventions():
    scope=ResultScope(id="scope-1",result_id="result-1",problem_id="problem-1",test_id="test-1",intervention_ids=("i-1",))
    assert scope.intervention_ids==("i-1",)

def test_scope_requires_core_identities():
    with pytest.raises(ValueError):
        ResultScope(id="scope-1",result_id="result-1",problem_id="problem-1",test_id="")

def test_scope_requires_tuple_interventions():
    with pytest.raises(TypeError):
        ResultScope(id="scope-1",result_id="result-1",problem_id="problem-1",test_id="test-1",intervention_ids=["i-1"]) # type: ignore[arg-type]

def test_scope_rejects_duplicate_interventions():
    with pytest.raises(ValueError):
        ResultScope(id="scope-1",result_id="result-1",problem_id="problem-1",test_id="test-1",intervention_ids=("i-1","i-1"))

def test_scope_serialization_is_deterministic():
    scope=ResultScope(id="scope-1",result_id="result-1",problem_id="problem-1",test_id="test-1")
    assert scope.to_json()==json.dumps(scope.to_dict(),sort_keys=True,separators=(",",":"))
