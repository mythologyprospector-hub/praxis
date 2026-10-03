"""Bounded assembly for observed test results."""

from __future__ import annotations

from praxis.result import Result
from praxis.result_request import ResultRequest


def assemble_result(request: ResultRequest, result: Result) -> Result:
    """Validate an observed Result against its explicit capture request."""
    if not isinstance(result, Result):
        raise TypeError("result must be a Result")
    if result.id == request.id:
        raise ValueError("result identity must differ from request identity")
    if result.test_id != request.test_id:
        raise ValueError("result belongs to a different test")
    return result
