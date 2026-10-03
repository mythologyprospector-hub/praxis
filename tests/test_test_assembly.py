import pytest
from praxis.test import Test
from praxis.test_request import TestRequest
from praxis.test_assembly import assemble_test

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
