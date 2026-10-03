"""Bounded assembly for scoped test results."""

from __future__ import annotations

from praxis.result import Result
from praxis.result_scope import ResultScope


def assemble_result_scope(scope: ResultScope, result: Result) -> ResultScope:
    """Validate that a ResultScope actually scopes its referenced result."""
    if not isinstance(scope, ResultScope):
        raise TypeError("scope must be a ResultScope")
    if not isinstance(result, Result):
        raise TypeError("result must be a Result")
    if scope.result_id != result.id:
        raise ValueError("scope targets a different result")
    if result.test_id != scope.test_id:
        raise ValueError("result belongs to a different test")
    return scope
