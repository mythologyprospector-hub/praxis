"""Bounded assembly for observed test results."""

from __future__ import annotations

from praxis.result import Result
from praxis.result_request import ResultRequest
from praxis.test import Test


def assemble_result(request: ResultRequest, result: Result, test: Test | None = None) -> Result:
    """Validate an observed Result against its explicit capture request."""
    if not isinstance(request, ResultRequest):
        raise TypeError("request must be a ResultRequest")
    if not isinstance(result, Result):
        raise TypeError("result must be a Result")
    if result.id == request.id:
        raise ValueError("result identity must differ from request identity")
    if result.test_id != request.test_id:
        raise ValueError("result belongs to a different test")
    if test is not None:
        if not isinstance(test, Test):
            raise TypeError("test must be a Test")
        if test.id != request.test_id:
            raise ValueError("test does not match result request")
        if test.problem_id != request.problem_id:
            raise ValueError("test belongs to a different problem")
        if request.intervention_ids and not set(request.intervention_ids).issubset(test.intervention_ids):
            raise ValueError("test does not reference all requested interventions")
    return result
