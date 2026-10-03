from praxis.evaluation import HypothesisEvaluation
from praxis.evaluation_request import EvaluationRequest
from praxis.evaluation_assembly import assemble_evaluation
from praxis.hypothesis import Hypothesis
import pytest

def test_assembly_accepts_evaluation_matching_request():
    req=EvaluationRequest(id="req-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=("e-1","e-2"))
    ev=HypothesisEvaluation(id="ev-1",hypothesis_id="h-1",inference="i",uncertainty="u",evidence_ids=("e-1","e-2"))
    assert assemble_evaluation(req,ev) is ev

def test_assembly_rejects_wrong_hypothesis():
    req=EvaluationRequest(id="req-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=("e-1",))
    ev=HypothesisEvaluation(id="ev-1",hypothesis_id="h-2",inference="i",uncertainty="u",evidence_ids=("e-1",))
    with pytest.raises(ValueError): assemble_evaluation(req,ev)

def test_assembly_requires_requested_evidence():
    req=EvaluationRequest(id="req-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=("e-1","e-2"))
    ev=HypothesisEvaluation(id="ev-1",hypothesis_id="h-1",inference="i",uncertainty="u",evidence_ids=("e-1",))
    with pytest.raises(ValueError): assemble_evaluation(req,ev)

def test_assembly_keeps_request_and_evaluation_distinct():
    req=EvaluationRequest(id="req-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=("e-1",))
    ev=HypothesisEvaluation(id="req-1",hypothesis_id="h-1",inference="i",uncertainty="u",evidence_ids=("e-1",))
    with pytest.raises(ValueError): assemble_evaluation(req,ev)


def test_assembly_validates_supplied_hypothesis_lineage():
    req=EvaluationRequest(id="req-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=("e-1",))
    ev=HypothesisEvaluation(id="ev-1",hypothesis_id="h-1",inference="i",uncertainty="u",evidence_ids=("e-1",))
    hypothesis=Hypothesis(id="h-1",problem_id="p-1",statement="h",rationale="r")
    assert assemble_evaluation(req,ev,hypothesis) is ev

def test_assembly_rejects_supplied_hypothesis_from_wrong_problem():
    req=EvaluationRequest(id="req-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=("e-1",))
    ev=HypothesisEvaluation(id="ev-1",hypothesis_id="h-1",inference="i",uncertainty="u",evidence_ids=("e-1",))
    hypothesis=Hypothesis(id="h-1",problem_id="p-2",statement="h",rationale="r")
    with pytest.raises(ValueError, match="different problem"):
        assemble_evaluation(req,ev,hypothesis)


def test_assembly_rejects_evaluation_target_mismatch_with_supplied_hypothesis():
    req=EvaluationRequest(id="req-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=("e-1",))
    ev=HypothesisEvaluation(id="ev-1",hypothesis_id="h-2",inference="i",uncertainty="u",evidence_ids=("e-1",))
    hypothesis=Hypothesis(id="h-1",problem_id="p-1",statement="h",rationale="r")
    with pytest.raises(ValueError, match="different hypothesis"):
        assemble_evaluation(req,ev,hypothesis)

def test_assembly_rejects_evidence_outside_request():
    req=EvaluationRequest(id="req-1",problem_id="p-1",hypothesis_id="h-1",evidence_ids=("e-1",))
    ev=HypothesisEvaluation(id="ev-1",hypothesis_id="h-1",inference="i",uncertainty="u",evidence_ids=("e-1","e-2"))
    with pytest.raises(ValueError, match="outside the request"):
        assemble_evaluation(req,ev)
