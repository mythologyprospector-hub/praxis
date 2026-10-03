"""Bounded assembly for model artifacts."""
from __future__ import annotations

from .model import Model
from .model_request import ModelRequest


def assemble_model(request: ModelRequest, model: Model) -> Model:
    """Validate a model against its explicit construction request."""
    if not isinstance(model, Model):
        raise TypeError("model must be a Model")
    if model.id == request.id:
        raise ValueError("model identity must differ from request identity")
    if model.problem_id != request.problem_id:
        raise ValueError("model belongs to a different problem")
    if model.purpose != request.purpose:
        raise ValueError("model purpose does not match request")
    if request.input_ids and not set(request.input_ids).issubset(model.input_ids):
        raise ValueError("model does not reference all requested inputs")
    if request.hypothesis_ids and not set(request.hypothesis_ids).issubset(model.input_ids):
        raise ValueError("model does not reference all requested hypotheses")
    if request.intervention_ids and not set(request.intervention_ids).issubset(model.input_ids):
        raise ValueError("model does not reference all requested interventions")
    return model
