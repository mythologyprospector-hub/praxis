import json

import pytest

from praxis.hypothesis import Hypothesis


def test_hypothesis_is_distinct_from_evidence():
    hypothesis = Hypothesis(
        id="h1",
        problem_id="water-001",
        statement="A maintenance schedule may reduce service interruptions.",
        rationale="Repeated failures appear after deferred maintenance.",
    )

    assert hypothesis.to_dict()["statement"].startswith("A maintenance")
    assert "provenance" not in hypothesis.to_dict()


def test_hypothesis_requires_explicit_problem_and_rationale():
    with pytest.raises(ValueError, match="rationale"):
        Hypothesis(
            id="h1",
            problem_id="p1",
            statement="Something may help.",
            rationale="",
        )


def test_hypothesis_serialization_is_deterministic_and_json_compatible():
    hypothesis = Hypothesis("h1", "p1", "A may cause B.", "Observed pattern.")
    encoded = hypothesis.to_json()

    assert encoded == hypothesis.to_json()
    assert json.loads(encoded)["problem_id"] == "p1"
