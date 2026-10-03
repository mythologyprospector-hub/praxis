from __future__ import annotations

import pytest

from praxis.candidate_generation import assemble_candidate_set
from praxis.candidate_request import CandidateRequest
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention


def test_assembly_groups_generated_candidates_under_request():
    request = CandidateRequest(id="req-1", problem_id="p-1")
    hypothesis = Hypothesis(
        id="h-1", problem_id="p-1", statement="h", rationale="r"
    )
    intervention = Intervention(
        id="i-1", problem_id="p-1", description="d", intended_outcome="o"
    )

    result = assemble_candidate_set(
        request, hypotheses=(hypothesis,), interventions=(intervention,)
    )

    assert result.id == "req-1:candidates"
    assert result.problem_id == "p-1"
    assert result.hypothesis_ids == ("h-1",)
    assert result.intervention_ids == ("i-1",)


def test_assembly_rejects_candidates_from_another_problem():
    request = CandidateRequest(id="req-1", problem_id="p-1")
    hypothesis = Hypothesis(
        id="h-1", problem_id="p-2", statement="h", rationale="r"
    )

    with pytest.raises(ValueError):
        assemble_candidate_set(request, hypotheses=(hypothesis,))


def test_assembly_respects_requested_types():
    request = CandidateRequest(
        id="req-1", problem_id="p-1", requested_types=("hypothesis",)
    )
    intervention = Intervention(
        id="i-1", problem_id="p-1", description="d", intended_outcome="o"
    )

    with pytest.raises(ValueError):
        assemble_candidate_set(request, interventions=(intervention,))


def test_assembly_rejects_wrong_artifact_types():
    request = CandidateRequest(id="req-1", problem_id="p-1")

    with pytest.raises(TypeError):
        assemble_candidate_set(request, hypotheses=("not-a-hypothesis",))  # type: ignore[arg-type]


def test_assembly_requires_output():
    request = CandidateRequest(id="req-1", problem_id="p-1")

    with pytest.raises(ValueError):
        assemble_candidate_set(request)


def test_assembly_rejects_id_collision_across_candidate_types():
    request = CandidateRequest(id="req-1", problem_id="p-1")
    hypothesis = Hypothesis(
        id="same-id", problem_id="p-1", statement="h", rationale="r"
    )
    intervention = Intervention(
        id="same-id", problem_id="p-1", description="d", intended_outcome="o"
    )

    with pytest.raises(ValueError, match="unique"):
        assemble_candidate_set(
            request, hypotheses=(hypothesis,), interventions=(intervention,)
        )


def test_assembly_rejects_wrong_intervention_type():
    request = CandidateRequest(id="req-1", problem_id="p-1")
    with pytest.raises(TypeError, match="Intervention"):
        assemble_candidate_set(request, interventions=(object(),))  # type: ignore[arg-type]


def test_assembly_rejects_wrong_request_type():
    with pytest.raises(TypeError, match="CandidateRequest"):
        assemble_candidate_set(object())  # type: ignore[arg-type]
