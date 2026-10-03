from __future__ import annotations

import pytest

from praxis.test import Test
from praxis.test_assembly import assemble_test
from praxis.test_request import TestRequest


def _test(**overrides: object) -> Test:
    values: dict[str, object] = {
        "id": "test-1",
        "problem_id": "problem-1",
        "objective": "learn",
        "expected_observations": ("observation",),
        "safety_constraints": ("safe",),
        "reversibility": "yes",
        "decision_criteria": ("criterion",),
        "intervention_ids": ("intervention-1",),
        "hypothesis_ids": ("hypothesis-1",),
        "failure_mode_ids": ("failure-1",),
        "model_ids": ("model-1",),
    }
    values.update(overrides)
    return Test(**values)


def test_assembly_accepts_complete_lineage() -> None:
    request = TestRequest(
        id="request-1",
        problem_id="problem-1",
        intervention_ids=("intervention-1",),
        hypothesis_ids=("hypothesis-1",),
        failure_mode_ids=("failure-1",),
        model_ids=("model-1",),
    )
    assert assemble_test(request, _test()) is not None


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("intervention_ids", ("intervention-1", "intervention-2")),
        ("hypothesis_ids", ("hypothesis-1", "hypothesis-2")),
        ("failure_mode_ids", ("failure-1", "failure-2")),
        ("model_ids", ("model-1", "model-2")),
    ],
)
def test_assembly_rejects_missing_lineage(field: str, expected: tuple[str, ...]) -> None:
    request = TestRequest(
        id="request-1",
        problem_id="problem-1",
        intervention_ids=("intervention-1",),
        hypothesis_ids=("hypothesis-1",),
        failure_mode_ids=("failure-1",),
        model_ids=("model-1",),
    )
    with pytest.raises(ValueError):
        assemble_test(request, _test(**{field: expected}))


def test_assembly_rejects_wrong_problem() -> None:
    request = TestRequest(id="request-1", problem_id="problem-1", intervention_ids=("intervention-1",))
    with pytest.raises(ValueError):
        assemble_test(request, _test(problem_id="problem-2"))


def test_assembly_keeps_request_and_test_distinct() -> None:
    request = TestRequest(id="request-1", problem_id="problem-1", intervention_ids=("intervention-1",))
    with pytest.raises(ValueError):
        assemble_test(request, _test(id="request-1"))
