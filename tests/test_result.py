from __future__ import annotations

import json

import pytest

from praxis.result import Result


def test_result_is_observation_not_a_test_plan() -> None:
    result = Result(
        id="result-1",
        test_id="test-1",
        summary="The target outcome changed.",
        observations=("Measured outcome increased.",),
        provenance="measurement-log-1",
        uncertainty="Single test run.",
    )
    data = result.to_dict()
    assert data["test_id"] == "test-1"
    assert data["observations"] == ("Measured outcome increased.",)
    assert data["provenance"] == "measurement-log-1"
    assert "objective" not in data
    assert "decision_criteria" not in data


def test_result_requires_core_fields() -> None:
    with pytest.raises(ValueError):
        Result(
            id="result-1",
            test_id="",
            summary="Observed something.",
            observations=(),
            provenance="log-1",
            uncertainty="limited.",
        )
    with pytest.raises(ValueError):
        Result(
            id="result-1",
            test_id="test-1",
            summary="",
            observations=(),
            provenance="log-1",
            uncertainty="limited.",
        )


def test_result_requires_provenance_and_uncertainty() -> None:
    with pytest.raises(ValueError):
        Result(
            id="result-1",
            test_id="test-1",
            summary="Observed something.",
            observations=(),
            provenance="",
            uncertainty="limited.",
        )
    with pytest.raises(ValueError):
        Result(
            id="result-1",
            test_id="test-1",
            summary="Observed something.",
            observations=(),
            provenance="log-1",
            uncertainty="",
        )


def test_result_rejects_non_tuple_observations() -> None:
    with pytest.raises(TypeError):
        Result(
            id="result-1",
            test_id="test-1",
            summary="Observed something.",
            observations=["something happened"],  # type: ignore[arg-type]
            provenance="log-1",
            uncertainty="limited.",
        )


def test_result_serialization_is_deterministic() -> None:
    result = Result(
        id="result-1",
        test_id="test-1",
        summary="Observed something.",
        observations=("A.", "B."),
        provenance="log-1",
        uncertainty="limited.",
        deviations=("The test ran one day late.",),
    )
    assert result.to_json() == json.dumps(result.to_dict(), sort_keys=True, separators=(",", ":"))
