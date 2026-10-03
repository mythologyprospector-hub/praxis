from __future__ import annotations

import json

import pytest

from praxis.model import Model


def test_model_is_analysis_not_evidence_or_decision() -> None:
    model = Model(
        id="model-1",
        problem_id="problem-1",
        purpose="Compare plausible intervention outcomes.",
        method="Bounded simulation.",
        input_ids=("evidence-1", "hyp-1"),
        assumptions=("The measured relationship remains stable.",),
        outputs=("Estimated outcome range.",),
        uncertainty="Sensitive to the stated assumption.",
    )

    data = model.to_dict()

    assert data["problem_id"] == "problem-1"
    assert data["input_ids"] == ("evidence-1", "hyp-1")
    assert "decision" not in data
    assert "provenance" not in data


def test_model_requires_identity_purpose_and_method() -> None:
    with pytest.raises(ValueError):
        Model(id="model-1", problem_id="problem-1", purpose="", method="A method.")

    with pytest.raises(ValueError):
        Model(id="model-1", problem_id="problem-1", purpose="A purpose.", method="")


def test_model_requires_tuple_inputs_assumptions_and_outputs() -> None:
    with pytest.raises(TypeError):
        Model(
            id="model-1",
            problem_id="problem-1",
            purpose="A purpose.",
            method="A method.",
            input_ids=["evidence-1"],  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError):
        Model(
            id="model-1",
            problem_id="problem-1",
            purpose="A purpose.",
            method="A method.",
            assumptions=(" ",),
        )


def test_model_serialization_is_deterministic() -> None:
    model = Model(
        id="model-1",
        problem_id="problem-1",
        purpose="A purpose.",
        method="A method.",
        uncertainty="Known limitations.",
    )

    assert model.to_json() == json.dumps(
        model.to_dict(), sort_keys=True, separators=(",", ":")
    )
