"""Bounded assembly for candidate-generation outputs."""
from __future__ import annotations

from collections.abc import Iterable

from .candidate import CandidateSet
from .candidate_request import CandidateRequest
from .hypothesis import Hypothesis
from .intervention import Intervention


def assemble_candidate_set(
    request: CandidateRequest,
    *,
    hypotheses: Iterable[Hypothesis] = (),
    interventions: Iterable[Intervention] = (),
) -> CandidateSet:
    """Assemble generated candidates under an explicit request.

    This function does not generate, rank, select, authorize, or execute candidates.
    Generation may be supplied by a future reasoning engine; this boundary only
    validates and groups its proposed artifacts.
    """
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

    for item in interventions:
        if not isinstance(item, Intervention):
            raise TypeError("interventions must contain Intervention objects")
        if item.problem_id != request.problem_id:
            raise ValueError("intervention belongs to a different problem")

    if not hypotheses and not interventions:
        raise ValueError("candidate generation produced no candidates")

    return CandidateSet(
        id=f"{request.id}:candidates",
        problem_id=request.problem_id,
        hypothesis_ids=tuple(item.id for item in hypotheses),
        intervention_ids=tuple(item.id for item in interventions),
    )
