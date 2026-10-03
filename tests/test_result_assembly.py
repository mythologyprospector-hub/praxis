from __future__ import annotations

import pytest

from praxis.result import Result
from praxis.result_assembly import assemble_result
from praxis.result_request import ResultRequest
from praxis.test import Test


def _request() -> ResultRequest:
    return ResultRequest(
        id="request-1",
        problem_id="problem-1",
        test_id="test-1",
        expected_observation_ids=("obs-1",),
        intervention_ids=("i-1",),
    )


def _result(**overrides: object) -> Result:
    values: dict[str, object] = {
        "id": "result-1",
        "test_id": "test-1",
        "summary": "Observed outcome",
        "observations": ("obs-1",),
        "provenance": "experiment-log",
        "uncertainty": "moderate",
    }
    values.update(overrides)
    return Result(**values)  # type: ignore[arg-type]


def test_matching_request_accepts_result() -> None:
    result = _result()
    assert assemble_result(_request(), result) is result


def test_wrong_test_rejected() -> None:
    with pytest.raises(ValueError, match="different test"):
        assemble_result(_request(), _result(test_id="test-2"))


def test_request_and_result_identity_must_differ() -> None:
    with pytest.raises(ValueError, match="identity"):
        assemble_result(_request(), _result(id="request-1"))


def test_wrong_artifact_type_rejected() -> None:
    with pytest.raises(TypeError, match="Result"):
        assemble_result(_request(), object())  # type: ignore[arg-type]

def _test() -> Test:
    return Test(id="test-1", problem_id="problem-1", objective="Learn", expected_observations=("obs-1",), safety_constraints=("safe",), reversibility="reversible", decision_criteria=("criterion",), intervention_ids=("i-1",))

def test_assembly_validates_test_lineage():
    result = _result()
    assert assemble_result(_request(), result, _test()) is result

def test_assembly_rejects_test_from_wrong_problem():
    test = Test(id="test-1", problem_id="problem-2", objective="Learn", expected_observations=("obs-1",), safety_constraints=("safe",), reversibility="reversible", decision_criteria=("criterion",), intervention_ids=("i-1",))
    with pytest.raises(ValueError, match="different problem"):
        assemble_result(_request(), _result(), test)

def test_assembly_rejects_missing_requested_intervention():
    test = Test(id="test-1", problem_id="problem-1", objective="Learn", expected_observations=("obs-1",), safety_constraints=("safe",), reversibility="reversible", decision_criteria=("criterion",), intervention_ids=("i-2",))
    with pytest.raises(ValueError, match="requested interventions"):
        assemble_result(_request(), _result(), test)
