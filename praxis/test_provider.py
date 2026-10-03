"""Bounded provider boundary for test design."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from praxis.derivation import Derivation
from praxis.derivation_assembly import assemble_derivation
from praxis.failure import FailureMode
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention
from praxis.model import Model
from praxis.test import Test
from praxis.test_assembly import assemble_test
from praxis.test_request import TestRequest


@dataclass(frozen=True)
class TestDesignOutput:
    test: Test
    derivation: Derivation


@runtime_checkable
class TestDesigner(Protocol):
    def design(
        self,
        request: TestRequest,
        interventions: tuple[Intervention, ...],
        hypotheses: tuple[Hypothesis, ...] = (),
        failure_modes: tuple[FailureMode, ...] = (),
        models: tuple[Model, ...] = (),
    ) -> TestDesignOutput:
        ...


def design_test(
    request: TestRequest,
    designer: TestDesigner,
    *,
    interventions: tuple[Intervention, ...],
    hypotheses: tuple[Hypothesis, ...] = (),
    failure_modes: tuple[FailureMode, ...] = (),
    models: tuple[Model, ...] = (),
) -> TestDesignOutput:
    if not isinstance(request, TestRequest):
        raise TypeError("request must be a TestRequest")
    if not isinstance(designer, TestDesigner):
        raise TypeError("designer must implement TestDesigner")

    inputs = (
        (interventions, Intervention, "interventions"),
        (hypotheses, Hypothesis, "hypotheses"),
        (failure_modes, FailureMode, "failure_modes"),
        (models, Model, "models"),
    )
    for values, expected_type, name in inputs:
        if not isinstance(values, tuple) or any(not isinstance(x, expected_type) for x in values):
            raise TypeError(f"{name} must be a tuple of {expected_type.__name__} objects")

    requested = {
        "intervention_ids": interventions,
        "hypothesis_ids": hypotheses,
        "failure_mode_ids": failure_modes,
        "model_ids": models,
    }
    for field, values in requested.items():
        ids = {x.id for x in values}
        if not set(getattr(request, field)).issubset(ids):
            raise ValueError(f"request references {field} outside supplied inputs")
        if any(x.problem_id != request.problem_id for x in values):
            raise ValueError(f"{field} contains an artifact from a different problem")

    output = designer.design(request, interventions, hypotheses, failure_modes, models)
    if not isinstance(output, TestDesignOutput):
        raise TypeError("designer must return TestDesignOutput")

    assemble_test(request, output.test)
    if output.derivation.artifact_id != output.test.id:
        raise ValueError("test derivation must target the test")

    lineage_ids = (
        tuple(request.intervention_ids)
        + tuple(request.hypothesis_ids)
        + tuple(request.failure_mode_ids)
        + tuple(request.model_ids)
    )
    assemble_derivation(output.derivation, lineage_ids)
    return output
