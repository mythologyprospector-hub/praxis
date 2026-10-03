from __future__ import annotations

import json

import pytest

from praxis.test import Test


def test_test_is_a_plan_not_a_result() -> None:
    test = Test(
        id="test-1",
        problem_id="problem-1",
        objective="Determine whether the intervention changes the target outcome.",
        expected_observations=("The target outcome changes measurably.",),
        safety_constraints=("Stop if the defined harm threshold is crossed.",),
        reversibility="The intervention can be withdrawn without lasting effects.",
        decision_criteria=("Proceed only if the target change occurs without the defined harm.",),
        intervention_ids=("int-1",),
    )
    data = test.to_dict()
    assert data["problem_id"] == "problem-1"
    assert data["intervention_ids"] == ("int-1",)
    assert "result" not in data
    assert "observed_at" not in data


def test_test_requires_core_fields() -> None:
    with pytest.raises(ValueError):
        Test(
            id="test-1",
            problem_id="",
            objective="Determine something.",
            expected_observations=(),
            safety_constraints=(),
            reversibility="Reversible.",
            decision_criteria=(),
        )
    with pytest.raises(ValueError):
        Test(
            id="test-1",
            problem_id="problem-1",
            objective="",
            expected_observations=(),
            safety_constraints=(),
            reversibility="Reversible.",
            decision_criteria=(),
        )


def test_test_rejects_non_tuple_collections() -> None:
    with pytest.raises(TypeError):
        Test(
            id="test-1",
            problem_id="problem-1",
            objective="Determine something.",
            expected_observations=["Something happens."],  # type: ignore[arg-type]
            safety_constraints=(),
            reversibility="Reversible.",
            decision_criteria=(),
        )


def test_test_serialization_is_deterministic() -> None:
    test = Test(
        id="test-1",
        problem_id="problem-1",
        objective="Determine something.",
        expected_observations=("A.", "B."),
        safety_constraints=("C.",),
        reversibility="Reversible.",
        decision_criteria=("D.",),
        intervention_ids=("int-1",),
    )
    assert test.to_json() == json.dumps(test.to_dict(), sort_keys=True, separators=(",", ":"))
