from __future__ import annotations

import json

import pytest

from praxis.candidate import CandidateSet


def test_candidate_set_groups_proposals_without_becoming_a_decision() -> None:
    candidates = CandidateSet(
        id="set-1",
        problem_id="problem-1",
        hypothesis_ids=("hyp-1", "hyp-2"),
        intervention_ids=("int-1",),
    )

    data = candidates.to_dict()

    assert data["problem_id"] == "problem-1"
    assert data["hypothesis_ids"] == ("hyp-1", "hyp-2")
    assert data["intervention_ids"] == ("int-1",)
    assert "decision" not in data
    assert "rationale" not in data


def test_candidate_set_requires_at_least_one_candidate() -> None:
    with pytest.raises(ValueError):
        CandidateSet(id="set-1", problem_id="problem-1")


def test_candidate_set_requires_valid_ids() -> None:
    with pytest.raises(TypeError):
        CandidateSet(
            id="set-1",
            problem_id="problem-1",
            intervention_ids=["int-1"],  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError):
        CandidateSet(
            id="set-1",
            problem_id="problem-1",
            hypothesis_ids=("hyp-1", " "),
        )

    with pytest.raises(ValueError):
        CandidateSet(
            id="set-1",
            problem_id="problem-1",
            intervention_ids=("int-1", "int-1"),
        )


def test_candidate_set_requires_problem_identity() -> None:
    with pytest.raises(ValueError):
        CandidateSet(id="set-1", problem_id=" ", hypothesis_ids=("hyp-1",))


def test_candidate_set_serialization_is_deterministic() -> None:
    candidates = CandidateSet(
        id="set-1",
        problem_id="problem-1",
        hypothesis_ids=("hyp-1",),
    )

    assert candidates.to_json() == json.dumps(
        candidates.to_dict(), sort_keys=True, separators=(",", ":")
    )
