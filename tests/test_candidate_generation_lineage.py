from __future__ import annotations

import pytest

from praxis.candidate import CandidateSet
from praxis.candidate_generation import assemble_candidate_set
from praxis.candidate_request import CandidateRequest
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention


def _request() -> CandidateRequest:
    return CandidateRequest(
        id="request-1",
        problem_id="problem-1",
        evidence_ids=("evidence-1",),
        requested_types=("hypothesis", "intervention"),
    )


def _hypothesis() -> Hypothesis:
    return Hypothesis(
        id="hypothesis-1",
        problem_id="problem-1",
        statement="Mechanism.",
        rationale="Rationale.",
        evidence_ids=("evidence-1",),
    )


def _intervention() -> Intervention:
    return Intervention(
        id="intervention-1",
        problem_id="problem-1",
        description="Change.",
        intended_outcome="Outcome.",
        hypothesis_ids=("hypothesis-1",),
    )


def test_matching_candidates_are_assembled() -> None:
    result = assemble_candidate_set(
        _request(), hypotheses=(_hypothesis(),), interventions=(_intervention(),)
    )
    assert isinstance(result, CandidateSet)
    assert result.hypothesis_ids == ("hypothesis-1",)
    assert result.intervention_ids == ("intervention-1",)


def test_hypothesis_cannot_reference_unrequested_evidence() -> None:
    request = CandidateRequest(
        id="request-1",
        problem_id="problem-1",
        evidence_ids=("evidence-1",),
        requested_types=("hypothesis",),
    )
    hypothesis = Hypothesis(
        id="hypothesis-1",
        problem_id="problem-1",
        statement="Mechanism.",
        rationale="Rationale.",
        evidence_ids=("evidence-2",),
    )
    with pytest.raises(ValueError, match="evidence outside"):
        assemble_candidate_set(request, hypotheses=(hypothesis,))


def test_intervention_cannot_reference_absent_hypothesis() -> None:
    with pytest.raises(ValueError, match="hypotheses outside"):
        assemble_candidate_set(_request(), interventions=(_intervention(),))


def test_mismatched_problem_rejected() -> None:
    hypothesis = Hypothesis(
        id="hypothesis-1",
        problem_id="problem-2",
        statement="Mechanism.",
        rationale="Rationale.",
    )
    with pytest.raises(ValueError, match="different problem"):
        assemble_candidate_set(_request(), hypotheses=(hypothesis,))
