"""Tests for the bounded test-design provider boundary."""

from dataclasses import replace

import pytest

from praxis.derivation import Derivation
from praxis.failure import FailureMode
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention
from praxis.model import Model
from praxis.test import Test
from praxis.test_provider import TestDesignOutput, TestDesigner, design_test
from praxis.test_request import TestRequest


def _inputs():
    request = TestRequest(
        id="test-request",
        problem_id="problem",
        intervention_ids=("intervention",),
        hypothesis_ids=("hypothesis",),
        failure_mode_ids=("failure",),
        model_ids=("model",),
    )
    intervention = Intervention("intervention", "problem", "change", "outcome")
    hypothesis = Hypothesis("hypothesis", "problem", "mechanism", "uncertainty")
    failure = FailureMode("failure", "problem", "failure", "high", "medium", ("intervention",))
    model = Model("model", "problem", "purpose", "method", ("hypothesis", "intervention"))
    return request, intervention, hypothesis, failure, model


class StubDesigner:
    def design(self, request, interventions, hypotheses=(), failure_modes=(), models=()):
        test = Test(
            "test",
            request.problem_id,
            "objective",
            ("observation",),
            ("safe",),
            "reversible",
            ("criterion",),
            tuple(x.id for x in interventions),
            tuple(x.id for x in hypotheses),
            tuple(x.id for x in failure_modes),
            tuple(x.id for x in models),
        )
        derivation = Derivation(
            "test-derivation",
            "test",
            ("intervention", "hypothesis", "failure", "model"),
            "bounded test design",
            "Test is a proposed bounded learning method.",
        )
        return TestDesignOutput(test, derivation)


def test_design_test_returns_test_and_derivation():
    request, intervention, hypothesis, failure, model = _inputs()
    output = design_test(
        request,
        StubDesigner(),
        interventions=(intervention,),
        hypotheses=(hypothesis,),
        failure_modes=(failure,),
        models=(model,),
    )
    assert output.test.id == "test"
    assert output.derivation.artifact_id == "test"


def test_design_test_rejects_wrong_provider_output():
    class BadDesigner:
        def design(self, *args, **kwargs):
            return object()

    request, intervention, hypothesis, failure, model = _inputs()
    with pytest.raises(TypeError, match="TestDesignOutput"):
        design_test(
            request,
            BadDesigner(),
            interventions=(intervention,),
            hypotheses=(hypothesis,),
            failure_modes=(failure,),
            models=(model,),
        )


def test_design_test_requires_complete_derivation_target():
    class BadDesigner(StubDesigner):
        def design(self, *args, **kwargs):
            output = super().design(*args, **kwargs)
            return replace(output, derivation=replace(output.derivation, artifact_id="wrong"))

    request, intervention, hypothesis, failure, model = _inputs()
    with pytest.raises(ValueError, match="must target"):
        design_test(
            request,
            BadDesigner(),
            interventions=(intervention,),
            hypotheses=(hypothesis,),
            failure_modes=(failure,),
            models=(model,),
        )


def test_design_test_rejects_request_artifact_outside_supplied_inputs():
    request, intervention, hypothesis, failure, model = _inputs()
    missing = replace(request, model_ids=("missing-model",))
    with pytest.raises(ValueError, match="model_ids"):
        design_test(
            missing,
            StubDesigner(),
            interventions=(intervention,),
            hypotheses=(hypothesis,),
            failure_modes=(failure,),
            models=(model,),
        )


def test_design_test_rejects_cross_problem_inputs():
    request, intervention, hypothesis, failure, model = _inputs()
    foreign = replace(model, problem_id="other")
    with pytest.raises(ValueError, match="different problem"):
        design_test(
            request,
            StubDesigner(),
            interventions=(intervention,),
            hypotheses=(hypothesis,),
            failure_modes=(failure,),
            models=(foreign,),
        )


def test_test_designer_protocol_is_runtime_checkable():
    assert isinstance(StubDesigner(), TestDesigner)
