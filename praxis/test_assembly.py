"""Bounded assembly for test plans."""
from __future__ import annotations

from praxis.test import Test
from praxis.test_request import TestRequest
from praxis.intervention import Intervention
from praxis.hypothesis import Hypothesis
from praxis.failure import FailureMode
from praxis.model import Model


def assemble_test(
    request: TestRequest,
    test: Test,
    intervention: Intervention | None = None,
    hypothesis: Hypothesis | None = None,
    failure_mode: FailureMode | None = None,
    model: Model | None = None,
) -> Test:
    """Validate a Test against its explicit design request."""
    if not isinstance(request, TestRequest):
        raise TypeError("request must be a TestRequest")
    if not isinstance(test, Test):
        raise TypeError("test must be a Test")
    if test.id == request.id:
        raise ValueError("test identity must differ from request identity")
    if test.problem_id != request.problem_id:
        raise ValueError("test belongs to a different problem")
    artifacts = ((intervention, "intervention_ids", Intervention), (hypothesis, "hypothesis_ids", Hypothesis), (failure_mode, "failure_mode_ids", FailureMode), (model, "model_ids", Model))
    for artifact, field, expected_type in artifacts:
        if artifact is None:
            continue
        if not isinstance(artifact, expected_type):
            raise TypeError(f"{field} artifact has wrong type")
        if artifact.problem_id != request.problem_id:
            raise ValueError(f"{field} artifact belongs to a different problem")
        if artifact.id not in getattr(request, field):
            raise ValueError(f"{field} artifact is outside the request")
        if artifact.id not in getattr(test, field):
            raise ValueError(f"test does not reference supplied {field} artifact")
        if isinstance(artifact, FailureMode) and not set(artifact.intervention_ids).issubset(request.intervention_ids):
            raise ValueError("failure mode references interventions outside the request")
    for name in ("intervention_ids", "hypothesis_ids", "failure_mode_ids", "model_ids"):
        requested = getattr(request, name)
        supplied = getattr(test, name)
        if requested and not set(requested).issubset(supplied):
            raise ValueError(f"test does not reference all requested {name}")
    return test
