import pytest
from praxis.model import Model
from praxis.model_request import ModelRequest
from praxis.model_assembly import assemble_model
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention

def test_assembly_accepts_model_matching_request():
    req=ModelRequest(id="req-1",problem_id="p-1",purpose="compare",input_ids=("x-1",),hypothesis_ids=("h-1",))
    model=Model(id="m-1",problem_id="p-1",purpose="compare",method="calc",input_ids=("x-1","h-1"))
    assert assemble_model(req,model) is model

def test_assembly_rejects_wrong_problem():
    req=ModelRequest(id="req-1",problem_id="p-1",purpose="compare")
    model=Model(id="m-1",problem_id="p-2",purpose="compare",method="calc")
    with pytest.raises(ValueError): assemble_model(req,model)

def test_assembly_rejects_wrong_purpose():
    req=ModelRequest(id="req-1",problem_id="p-1",purpose="compare")
    model=Model(id="m-1",problem_id="p-1",purpose="forecast",method="calc")
    with pytest.raises(ValueError): assemble_model(req,model)

def test_assembly_requires_requested_inputs():
    req=ModelRequest(id="req-1",problem_id="p-1",purpose="compare",input_ids=("x-1","x-2"))
    model=Model(id="m-1",problem_id="p-1",purpose="compare",method="calc",input_ids=("x-1",))
    with pytest.raises(ValueError): assemble_model(req,model)

def test_assembly_keeps_request_and_model_distinct():
    req=ModelRequest(id="req-1",problem_id="p-1",purpose="compare")
    model=Model(id="req-1",problem_id="p-1",purpose="compare",method="calc")
    with pytest.raises(ValueError): assemble_model(req,model)


def test_assembly_validates_supplied_hypothesis_lineage():
    req=ModelRequest(id="req-1",problem_id="p-1",purpose="compare",hypothesis_ids=("h-1",))
    model=Model(id="m-1",problem_id="p-1",purpose="compare",method="calc",input_ids=("h-1",))
    hypothesis=Hypothesis(id="h-1",problem_id="p-1",statement="h",rationale="r")
    assert assemble_model(req,model,hypothesis=hypothesis) is model

def test_assembly_rejects_supplied_hypothesis_from_wrong_problem():
    req=ModelRequest(id="req-1",problem_id="p-1",purpose="compare",hypothesis_ids=("h-1",))
    model=Model(id="m-1",problem_id="p-1",purpose="compare",method="calc",input_ids=("h-1",))
    hypothesis=Hypothesis(id="h-1",problem_id="p-2",statement="h",rationale="r")
    with pytest.raises(ValueError, match="different problem"):
        assemble_model(req,model,hypothesis=hypothesis)

def test_assembly_validates_supplied_intervention_lineage():
    req=ModelRequest(id="req-1",problem_id="p-1",purpose="compare",intervention_ids=("i-1",))
    model=Model(id="m-1",problem_id="p-1",purpose="compare",method="calc",input_ids=("i-1",))
    intervention=Intervention(id="i-1",problem_id="p-1",description="d",intended_outcome="o")
    assert assemble_model(req,model,intervention=intervention) is model
