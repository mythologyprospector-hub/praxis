import pytest
from praxis.test import Test
from praxis.test_request import TestRequest
from praxis.test_assembly import assemble_test
from praxis.intervention import Intervention
from praxis.hypothesis import Hypothesis
from praxis.failure import FailureMode
from praxis.model import Model

def test_assembly_accepts_test_matching_request():
    req=TestRequest(id="req-1",problem_id="p-1",intervention_ids=("i-1",))
    test=Test(id="t-1",problem_id="p-1",objective="learn",expected_observations=("o",),safety_constraints=("safe",),reversibility="yes",decision_criteria=("c",),intervention_ids=("i-1",))
    assert assemble_test(req,test) is test

def test_assembly_rejects_wrong_problem():
    req=TestRequest(id="req-1",problem_id="p-1",intervention_ids=("i-1",))
    test=Test(id="t-1",problem_id="p-2",objective="learn",expected_observations=("o",),safety_constraints=("safe",),reversibility="yes",decision_criteria=("c",),intervention_ids=("i-1",))
    with pytest.raises(ValueError): assemble_test(req,test)

def test_assembly_requires_requested_interventions():
    req=TestRequest(id="req-1",problem_id="p-1",intervention_ids=("i-1","i-2"))
    test=Test(id="t-1",problem_id="p-1",objective="learn",expected_observations=("o",),safety_constraints=("safe",),reversibility="yes",decision_criteria=("c",),intervention_ids=("i-1",))
    with pytest.raises(ValueError): assemble_test(req,test)

def test_assembly_keeps_request_and_test_distinct():
    req=TestRequest(id="req-1",problem_id="p-1",intervention_ids=("i-1",))
    test=Test(id="req-1",problem_id="p-1",objective="learn",expected_observations=("o",),safety_constraints=("safe",),reversibility="yes",decision_criteria=("c",),intervention_ids=("i-1",))
    with pytest.raises(ValueError): assemble_test(req,test)

def test_assembly_validates_supplied_intervention_lineage():
    req=TestRequest(id="req-1",problem_id="p-1",intervention_ids=("i-1",))
    test=Test(id="t-1",problem_id="p-1",objective="learn",expected_observations=("o",),safety_constraints=("safe",),reversibility="yes",decision_criteria=("c",),intervention_ids=("i-1",))
    intervention=Intervention(id="i-1",problem_id="p-1",description="d",intended_outcome="o")
    assert assemble_test(req,test,intervention=intervention) is test

def test_assembly_rejects_supplied_hypothesis_wrong_problem():
    req=TestRequest(id="req-1",problem_id="p-1",intervention_ids=("i-1",),hypothesis_ids=("h-1",))
    test=Test(id="t-1",problem_id="p-1",objective="learn",expected_observations=("o",),safety_constraints=("safe",),reversibility="yes",decision_criteria=("c",),intervention_ids=("i-1",),hypothesis_ids=("h-1",))
    hypothesis=Hypothesis(id="h-1",problem_id="p-2",statement="h",rationale="r")
    with pytest.raises(ValueError, match="different problem"): assemble_test(req,test,hypothesis=hypothesis)

def test_assembly_validates_supplied_failure_mode_and_model_lineage():
    req=TestRequest(id="req-1",problem_id="p-1",intervention_ids=("i-1",),failure_mode_ids=("f-1",),model_ids=("m-1",))
    test=Test(id="t-1",problem_id="p-1",objective="learn",expected_observations=("o",),safety_constraints=("safe",),reversibility="yes",decision_criteria=("c",),intervention_ids=("i-1",),failure_mode_ids=("f-1",),model_ids=("m-1",))
    failure=FailureMode(id="f-1",problem_id="p-1",description="f",severity="high",likelihood="low",intervention_ids=("i-1",))
    model=Model(id="m-1",problem_id="p-1",purpose="compare",method="calc",input_ids=("i-1",))
    assert assemble_test(req,test,failure_mode=failure,model=model) is test
