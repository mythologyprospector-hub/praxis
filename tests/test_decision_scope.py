from __future__ import annotations
import json
import pytest
from praxis.decision_scope import DecisionScope

def test_scope_links_human_decision_to_bounded_subject_without_execution():
    scope=DecisionScope(id="scope-1",decision_id="decision-1",problem_id="problem-1",test_id="test-1")
    assert scope.to_dict()["decision_id"]=="decision-1"
    assert scope.to_dict()["test_id"]=="test-1"
    assert "execute" not in scope.to_dict()

def test_scope_can_target_an_intervention():
    assert DecisionScope(id="scope-1",decision_id="decision-1",problem_id="problem-1",intervention_id="i-1").intervention_id=="i-1"

def test_scope_requires_a_test_or_intervention():
    with pytest.raises(ValueError):
        DecisionScope(id="scope-1",decision_id="decision-1",problem_id="problem-1")

def test_scope_rejects_empty_optional_identity():
    with pytest.raises(ValueError):
        DecisionScope(id="scope-1",decision_id="decision-1",problem_id="problem-1",test_id=" ")

def test_scope_serialization_is_deterministic():
    scope=DecisionScope(id="scope-1",decision_id="decision-1",problem_id="problem-1",test_id="test-1")
    assert scope.to_json()==json.dumps(scope.to_dict(),sort_keys=True,separators=(",",":"))
