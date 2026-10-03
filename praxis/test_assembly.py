"""Bounded assembly for test plans."""
from __future__ import annotations

from praxis.test import Test
from praxis.test_request import TestRequest


def assemble_test(request: TestRequest, test: Test) -> Test:
    """Validate a Test against its explicit design request."""
    if not isinstance(test, Test):
        raise TypeError("test must be a Test")
    if test.id == request.id:
        raise ValueError("test identity must differ from request identity")
    if test.problem_id != request.problem_id:
        raise ValueError("test belongs to a different problem")
    for name in ("intervention_ids", "hypothesis_ids", "failure_mode_ids", "model_ids"):
        requested = getattr(request, name)
        supplied = getattr(test, name)
        if requested and not set(requested).issubset(supplied):
            raise ValueError(f"test does not reference all requested {name}")
    return test
