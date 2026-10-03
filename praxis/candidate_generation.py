"""Bounded assembly for candidate-generation outputs."""
from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from praxis.context import ReasoningContext

from praxis.candidate import CandidateSet
from praxis.candidate_request import CandidateRequest
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention


@runtime_checkable
class CandidateGenerator(Protocol):
    """Provider boundary for generating unranked candidate artifacts."""

    def generate(
        self, request: CandidateRequest, context: ReasoningContext
    ) -> tuple[Iterable[Hypothesis], Iterable[Intervention]]:
        """Generate candidate artifacts without ranking, selecting, or executing them."""


def generate_candidates(
    request: CandidateRequest,
    context: ReasoningContext,
    generator: CandidateGenerator,
) -> CandidateSet:
    """Generate and validate candidates through an explicit provider boundary."""
    if not isinstance(request, CandidateRequest):
        raise TypeError("request must be a CandidateRequest")
    if not isinstance(context, ReasoningContext):
        raise TypeError("context must be a ReasoningContext")
    if not isinstance(generator, CandidateGenerator):
        raise TypeError("generator must implement CandidateGenerator")
    if context.problem.id != request.problem_id:
        raise ValueError("context belongs to a different problem")
    if not set(request.evidence_ids).issubset({item.id for item in context.evidence.items}):
        raise ValueError("request references evidence outside the reasoning context")
    if not set(request.gap_ids).issubset({gap.id for gap in context.gaps}):
        raise ValueError("request references gaps outside the reasoning context")
    hypotheses, interventions = generator.generate(request, context)
    return assemble_candidate_set(
        request, hypotheses=hypotheses, interventions=interventions
    )


def assemble_candidate_set(
    request: CandidateRequest,
    *,
    hypotheses: Iterable[Hypothesis] = (),
    interventions: Iterable[Intervention] = (),
) -> CandidateSet:
    """Assemble generated candidates under an explicit request."""
    if not isinstance(request, CandidateRequest):
        raise TypeError("request must be a CandidateRequest")
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
