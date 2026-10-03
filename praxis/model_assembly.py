"""Bounded assembly for model artifacts."""
from __future__ import annotations

from .model import Model
from .model_request import ModelRequest
from .hypothesis import Hypothesis
from .intervention import Intervention


def assemble_model(
    request: ModelRequest,
    model: Model,
    hypothesis: Hypothesis | None = None,
    intervention: Intervention | None = None,
) -> Model:
    """Validate a model against its explicit construction request."""
    if not isinstance(model, Model):
        raise TypeError("model must be a Model")
    if model.id == request.id:
        raise ValueError("model identity must differ from request identity")
    if model.problem_id != request.problem_id:
        raise ValueError("model belongs to a different problem")
    if model.purpose != request.purpose:
        raise ValueError("model purpose does not match request")
    if hypothesis is not None:
        if not isinstance(hypothesis, Hypothesis):
            raise TypeError("hypothesis must be a Hypothesis")
        if hypothesis.id not in request.hypothesis_ids:
            raise ValueError("hypothesis is outside the model request")
        if hypothesis.problem_id != request.problem_id:
            raise ValueError("hypothesis belongs to a different problem")
        if hypothesis.id not in model.input_ids:
            raise ValueError("model does not reference supplied hypothesis")
    if intervention is not None:
        if not isinstance(intervention, Intervention):
            raise TypeError("intervention must be an Intervention")
        if intervention.id not in request.intervention_ids:
            raise ValueError("intervention is outside the model request")
        if intervention.problem_id != request.problem_id:
            raise ValueError("intervention belongs to a different problem")
        if intervention.id not in model.input_ids:
            raise ValueError("model does not reference supplied intervention")
    if request.input_ids and not set(request.input_ids).issubset(model.input_ids):
        raise ValueError("model does not reference all requested inputs")
    if request.hypothesis_ids and not set(request.hypothesis_ids).issubset(model.input_ids):
        raise ValueError("model does not reference all requested hypotheses")
    if request.intervention_ids and not set(request.intervention_ids).issubset(model.input_ids):
        raise ValueError("model does not reference all requested interventions")
    return model
