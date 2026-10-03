"""Bounded assembly for scoped test results."""

from __future__ import annotations

from praxis.result import Result
from praxis.result_scope import ResultScope
from praxis.test import Test


def assemble_result_scope(scope: ResultScope, result: Result, test: Test) -> ResultScope:
    """Validate that a ResultScope actually scopes its result and test lineage."""
    if not isinstance(scope, ResultScope):
        raise TypeError("scope must be a ResultScope")
    if not isinstance(result, Result):
        raise TypeError("result must be a Result")
    if not isinstance(test, Test):
        raise TypeError("test must be a Test")
    if scope.result_id != result.id:
        raise ValueError("scope targets a different result")
    if result.test_id != scope.test_id:
        raise ValueError("result belongs to a different test")
    if test.id != scope.test_id:
        raise ValueError("test belongs to a different test scope")
    if test.problem_id != scope.problem_id:
        raise ValueError("test belongs to a different problem")
    if not set(scope.intervention_ids).issubset(test.intervention_ids):
        raise ValueError("scope references interventions outside the test")
    return scope
