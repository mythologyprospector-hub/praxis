"""Bounded provider boundary for model construction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from praxis.derivation import Derivation
from praxis.derivation_assembly import assemble_derivation
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention
from praxis.model import Model
from praxis.model_assembly import assemble_model
from praxis.model_request import ModelRequest


@dataclass(frozen=True)
class ModelOutput:
    model: Model
    derivation: Derivation


@runtime_checkable
class ModelBuilder(Protocol):
    def build(
        self,
        request: ModelRequest,
        hypotheses: tuple[Hypothesis, ...] = (),
        interventions: tuple[Intervention, ...] = (),
    ) -> ModelOutput:
        ...


def build_model(
    request: ModelRequest,
    builder: ModelBuilder,
    *,
    hypotheses: tuple[Hypothesis, ...] = (),
    interventions: tuple[Intervention, ...] = (),
) -> ModelOutput:
    if not isinstance(request, ModelRequest):
        raise TypeError("request must be a ModelRequest")
    if not isinstance(builder, ModelBuilder):
        raise TypeError("builder must implement ModelBuilder")
    if not isinstance(hypotheses, tuple) or any(not isinstance(x, Hypothesis) for x in hypotheses):
        raise TypeError("hypotheses must be a tuple of Hypothesis objects")
    if not isinstance(interventions, tuple) or any(not isinstance(x, Intervention) for x in interventions):
        raise TypeError("interventions must be a tuple of Intervention objects")
    if not set(request.hypothesis_ids).issubset({x.id for x in hypotheses}):
        raise ValueError("request references hypotheses outside supplied inputs")
    if not set(request.intervention_ids).issubset({x.id for x in interventions}):
        raise ValueError("request references interventions outside supplied inputs")
    if any(x.problem_id != request.problem_id for x in hypotheses):
        raise ValueError("hypothesis belongs to a different problem")
    if any(x.problem_id != request.problem_id for x in interventions):
        raise ValueError("intervention belongs to a different problem")

    output = builder.build(request, hypotheses, interventions)
    if not isinstance(output, ModelOutput):
        raise TypeError("builder must return ModelOutput")
    assemble_model(request, output.model)
    if output.derivation.artifact_id != output.model.id:
        raise ValueError("model derivation must target the model")
    assemble_derivation(
        output.derivation,
        tuple(request.input_ids) + tuple(request.hypothesis_ids) + tuple(request.intervention_ids),
    )
    return output
