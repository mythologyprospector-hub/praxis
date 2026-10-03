import json

import pytest

from praxis.hypothesis import Hypothesis


def test_hypothesis_can_reference_evidence_without_becoming_evidence():
    hypothesis = Hypothesis(
        id="h1",
        problem_id="water-001",
        statement="A maintenance schedule may reduce service interruptions.",
        rationale="Repeated failures appear after deferred maintenance.",
        evidence_ids=("e1", "e2"),
    )

    data = hypothesis.to_dict()

    assert data["evidence_ids"] == ("e1", "e2")
    assert "provenance" not in data


def test_hypothesis_requires_explicit_problem_and_rationale():
    with pytest.raises(ValueError, match="rationale"):
        Hypothesis(
            id="h1",
            problem_id="p1",
            statement="Something may help.",
            rationale="",
        )


def test_hypothesis_rejects_invalid_evidence_references():
    with pytest.raises(ValueError, match="evidence_ids"):
        Hypothesis(
            id="h1",
            problem_id="p1",
            statement="A may cause B.",
            rationale="Observed pattern.",
            evidence_ids=("e1", ""),
        )

    with pytest.raises(TypeError, match="evidence_ids"):
        Hypothesis(
            id="h1",
            problem_id="p1",
            statement="A may cause B.",
            rationale="Observed pattern.",
            evidence_ids=["e1"],
        )


def test_hypothesis_serialization_is_deterministic_and_json_compatible():
    hypothesis = Hypothesis(
        "h1",
        "p1",
        "A may cause B.",
        "Observed pattern.",
        ("e1",),
    )
    encoded = hypothesis.to_json()

    assert encoded == hypothesis.to_json()
    assert json.loads(encoded)["problem_id"] == "p1"
    assert json.loads(encoded)["evidence_ids"] == ["e1"]
