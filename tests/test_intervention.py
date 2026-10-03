from __future__ import annotations

import json

import pytest

from praxis.intervention import Intervention


def test_intervention_is_a_proposal_not_evidence() -> None:
    intervention = Intervention(
        id="int-1",
        problem_id="problem-1",
        description="Change the relevant process.",
        intended_outcome="Improve the target outcome.",
        hypothesis_ids=("hyp-1",),
    )

    data = intervention.to_dict()

    assert data["problem_id"] == "problem-1"
    assert data["hypothesis_ids"] == ("hyp-1",)
    assert "provenance" not in data
    assert "uncertainty" not in data


def test_intervention_requires_problem_description_and_outcome() -> None:
    with pytest.raises(ValueError):
        Intervention(
            id="int-1",
            problem_id="",
            description="A proposal.",
            intended_outcome="An outcome.",
        )

    with pytest.raises(ValueError):
        Intervention(
            id="int-1",
            problem_id="problem-1",
            description="",
            intended_outcome="An outcome.",
        )

    with pytest.raises(ValueError):
        Intervention(
            id="int-1",
            problem_id="problem-1",
            description="A proposal.",
            intended_outcome="",
        )


def test_intervention_rejects_invalid_hypothesis_references() -> None:
    with pytest.raises(TypeError):
        Intervention(
            id="int-1",
            problem_id="problem-1",
            description="A proposal.",
            intended_outcome="An outcome.",
            hypothesis_ids=["hyp-1"],  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError):
        Intervention(
            id="int-1",
            problem_id="problem-1",
            description="A proposal.",
            intended_outcome="An outcome.",
            hypothesis_ids=(" ",),
        )


def test_intervention_serialization_is_deterministic() -> None:
    intervention = Intervention(
        id="int-1",
        problem_id="problem-1",
        description="A proposal.",
        intended_outcome="An outcome.",
        hypothesis_ids=("hyp-1", "hyp-2"),
    )

    assert intervention.to_json() == json.dumps(
        intervention.to_dict(), sort_keys=True, separators=(",", ":")
    )
