from __future__ import annotations

import json

import pytest

from praxis.failure import FailureMode


def test_failure_mode_is_analysis_not_evidence() -> None:
    failure = FailureMode(
        id="failure-1",
        problem_id="problem-1",
        description="The intervention could produce an unintended outcome.",
        severity="high",
        likelihood="possible",
        intervention_ids=("int-1",),
    )
    data = failure.to_dict()
    assert data["problem_id"] == "problem-1"
    assert data["intervention_ids"] == ("int-1",)
    assert "provenance" not in data
    assert "uncertainty" not in data


def test_failure_mode_requires_core_fields() -> None:
    with pytest.raises(ValueError):
        FailureMode(id="failure-1", problem_id="", description="A failure.", severity="high", likelihood="possible")
    with pytest.raises(ValueError):
        FailureMode(id="failure-1", problem_id="problem-1", description="", severity="high", likelihood="possible")


def test_failure_mode_rejects_invalid_intervention_references() -> None:
    with pytest.raises(TypeError):
        FailureMode(id="failure-1", problem_id="problem-1", description="A failure.", severity="high", likelihood="possible", intervention_ids=["int-1"])  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        FailureMode(id="failure-1", problem_id="problem-1", description="A failure.", severity="high", likelihood="possible", intervention_ids=(" ",))


def test_failure_mode_serialization_is_deterministic() -> None:
    failure = FailureMode(id="failure-1", problem_id="problem-1", description="A failure.", severity="high", likelihood="possible", intervention_ids=("int-1", "int-2"))
    assert failure.to_json() == json.dumps(failure.to_dict(), sort_keys=True, separators=(",", ":"))
