from __future__ import annotations

import pytest

from praxis.result import Result
from praxis.result_scope import ResultScope
from praxis.result_scope_assembly import assemble_result_scope
from praxis.test import Test


def _result() -> Result:
    return Result(
        id="result-1", test_id="test-1", summary="Observed.",
        observations=("observation-1",), provenance="experiment", uncertainty="limited", deviations=()
    )


def _test() -> Test:
    return Test(id="test-1", problem_id="problem-1", objective="Learn.", expected_observations=("observation-1",), safety_constraints=("safe",), reversibility="reversible", decision_criteria=("criterion-1",), intervention_ids=("intervention-1",))


def _scope() -> ResultScope:
    return ResultScope(
        id="scope-1", result_id="result-1", problem_id="problem-1",
        test_id="test-1", intervention_ids=("intervention-1",)
    )


def test_matching_result_accepts_scope() -> None:
    assert assemble_result_scope(_scope(), _result(), _test()) == _scope()


def test_wrong_result_rejected() -> None:
    scope = ResultScope(id="scope-1", result_id="result-2", problem_id="problem-1", test_id="test-1", intervention_ids=("intervention-1",))
    with pytest.raises(ValueError, match="result"):
        assemble_result_scope(scope, _result(), _test())


def test_wrong_test_rejected() -> None:
    scope = ResultScope(id="scope-1", result_id="result-1", problem_id="problem-1", test_id="test-2", intervention_ids=("intervention-1",))
    with pytest.raises(ValueError, match="test"):
        assemble_result_scope(scope, _result(), _test())


def test_wrong_scope_type_rejected() -> None:
    with pytest.raises(TypeError, match="ResultScope"):
        assemble_result_scope(object(), _result(), _test())  # type: ignore[arg-type]


def test_wrong_result_type_rejected() -> None:
    with pytest.raises(TypeError, match="Result"):
        assemble_result_scope(_scope(), object(), _test())  # type: ignore[arg-type]



def test_wrong_test_object_rejected() -> None:
    test = Test(id="test-2", problem_id="problem-1", objective="Learn.", expected_observations=("observation-1",), safety_constraints=("safe",), reversibility="reversible", decision_criteria=("criterion-1",), intervention_ids=("intervention-1",))
    with pytest.raises(ValueError, match="test scope"):
        assemble_result_scope(_scope(), _result(), test)


def test_scope_intervention_outside_test_rejected() -> None:
    scope = ResultScope(id="scope-1", result_id="result-1", problem_id="problem-1", test_id="test-1", intervention_ids=("intervention-2",))
    with pytest.raises(ValueError, match="outside the test"):
        assemble_result_scope(scope, _result(), _test())
