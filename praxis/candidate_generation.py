"""Bounded assembly for candidate-generation outputs."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from praxis.context import ReasoningContext
from praxis.derivation import Derivation
from praxis.derivation_assembly import assemble_derivation

from praxis.candidate import CandidateSet
from praxis.candidate_request import CandidateRequest
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention


@runtime_checkable
@dataclass(frozen=True)
class CandidateGenerationOutput:
    """Generated candidates plus explicit derivations for each artifact."""

    hypotheses: tuple[Hypothesis, ...] = ()
    interventions: tuple[Intervention, ...] = ()
    derivations: tuple[Derivation, ...] = ()


@runtime_checkable
class CandidateGenerator(Protocol):
    """Provider boundary for generating unranked candidate artifacts."""

    def generate(
        self, request: CandidateRequest, context: ReasoningContext
    ) -> CandidateGenerationOutput:
        """Generate candidates and their explicit derivation traces."""


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
    output = generator.generate(request, context)
    if not isinstance(output, CandidateGenerationOutput):
        raise TypeError("generator must return CandidateGenerationOutput")
    candidate_ids = {item.id for item in output.hypotheses} | {item.id for item in output.interventions}
    for derivation in output.derivations:
        if derivation.artifact_id not in candidate_ids:
            raise ValueError("derivation targets an artifact outside generated candidates")
        assemble_derivation(
            derivation,
            tuple(candidate_ids) + tuple(request.gap_ids) + tuple(request.evidence_ids),
        )
    return assemble_candidate_set(
        request, hypotheses=output.hypotheses, interventions=output.interventions
    )



class GapDirectedCandidateGenerator:
    """Generate conservative candidates directly from explicit evidence gaps."""

    def generate(
        self, request: CandidateRequest, context: ReasoningContext
    ) -> CandidateGenerationOutput:
        gaps = tuple(gap for gap in context.gaps if gap.id in request.gap_ids)
        if not gaps:
            raise ValueError(
                "GapDirectedCandidateGenerator requires at least one requested evidence gap"
            )

        hypotheses = []
        interventions = []
        derivations = []

        for gap in gaps:
            hypothesis_id = f"{request.id}:hypothesis:{gap.id}"
            if "hypothesis" in request.requested_types:
                hypotheses.append(
                    Hypothesis(
                        id=hypothesis_id,
                        problem_id=request.problem_id,
                        statement=(
                            f"Resolving the evidence gap '{gap.description}' may "
                            f"change which options are justified for the goal "
                            f"'{context.problem.goal}'."
                        ),
                        rationale=(
                            f"Generated from gap '{gap.id}', whose decision relevance "
                            f"is '{gap.decision_relevance}'. This is a proposal, "
                            "not evidence."
                        ),
                    )
                )

            if "intervention" in request.requested_types:
                interventions.append(
                    Intervention(
                        id=f"{request.id}:intervention:{gap.id}",
                        problem_id=request.problem_id,
                        description=(
                            f"Conduct a bounded investigation of evidence gap "
                            f"'{gap.description}' that can distinguish materially "
                            "different explanations or next steps."
                        ),
                        intended_outcome=(
                            "Reduce the uncertainty represented by the gap with "
                            "newly grounded information, subject to the request "
                            "constraints."
                        ),
                        hypothesis_ids=(
                            (hypothesis_id,)
                            if "hypothesis" in request.requested_types
                            else ()
                        ),
                    )
                )

        return tuple(hypotheses), tuple(interventions)


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
