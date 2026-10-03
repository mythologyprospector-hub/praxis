"""Bounded assembly for candidate-generation outputs."""
from __future__ import annotations

from collections.abc import Iterable

from praxis.candidate import CandidateSet
from praxis.candidate_request import CandidateRequest
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention


def assemble_candidate_set(
    request: CandidateRequest,
    *,
    hypotheses: Iterable[Hypothesis] = (),
    interventions: Iterable[Intervention] = (),
) -> CandidateSet:
    """Assemble generated candidates under an explicit request."""
    hypotheses = tuple(hypotheses)
    interventions = tuple(interventions)

    if "hypothesis" not in request.requested_types and hypotheses:
        raise ValueError("request does not permit hypothesis candidates")
    if "intervention" not in request.requested_types and interventions:
        raise ValueError("request does not permit intervention candidates")

    for item in hypotheses:
        if not isinstance(item, Hypothesis):
            raise TypeError("hypotheses must contain Hypothesis objects")
        if item.problem_id != request.problem_id:
            raise ValueError("hypothesis belongs to a different problem")
        if not set(item.evidence_ids).issubset(request.evidence_ids):
            raise ValueError("hypothesis references evidence outside the request")

    for item in interventions:
        if not isinstance(item, Intervention):
            raise TypeError("interventions must contain Intervention objects")
        if item.problem_id != request.problem_id:
            raise ValueError("intervention belongs to a different problem")
        if not set(item.hypothesis_ids).issubset({item.id for item in hypotheses}):
            raise ValueError("intervention references hypotheses outside the candidate set")

    hypothesis_ids = {item.id for item in hypotheses}
    intervention_ids = {item.id for item in interventions}
    if hypothesis_ids & intervention_ids:
        raise ValueError("candidate ids must be unique across candidate types")

    if not hypotheses and not interventions:
        raise ValueError("candidate generation produced no candidates")

    return CandidateSet(
        id=f"{request.id}:candidates",
        problem_id=request.problem_id,
        hypothesis_ids=tuple(item.id for item in hypotheses),
        intervention_ids=tuple(item.id for item in interventions),
    )
