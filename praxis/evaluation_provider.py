"""Bounded provider boundary for hypothesis evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from praxis.context import ReasoningContext
from praxis.derivation import Derivation
from praxis.derivation_assembly import assemble_derivation
from praxis.evaluation import HypothesisEvaluation
from praxis.evaluation_assembly import assemble_evaluation
from praxis.evaluation_request import EvaluationRequest
from praxis.hypothesis import Hypothesis


@dataclass(frozen=True)
class EvaluationOutput:
    """An evaluated hypothesis plus its explicit derivation trace."""

    evaluation: HypothesisEvaluation
    derivation: Derivation


@runtime_checkable
class HypothesisEvaluator(Protocol):
    """Provider boundary for evaluating a hypothesis without changing evidence."""

    def evaluate(
        self,
        request: EvaluationRequest,
        context: ReasoningContext,
        hypothesis: Hypothesis,
    ) -> EvaluationOutput:
        """Produce one bounded evaluation and its derivation."""


def evaluate_hypothesis(
    request: EvaluationRequest,
    context: ReasoningContext,
    hypothesis: Hypothesis,
    evaluator: HypothesisEvaluator,
) -> EvaluationOutput:
    """Evaluate one hypothesis through an explicit provider boundary."""
    if not isinstance(request, EvaluationRequest):
        raise TypeError("request must be an EvaluationRequest")
    if not isinstance(context, ReasoningContext):
        raise TypeError("context must be a ReasoningContext")
    if not isinstance(hypothesis, Hypothesis):
        raise TypeError("hypothesis must be a Hypothesis")
    if not isinstance(evaluator, HypothesisEvaluator):
        raise TypeError("evaluator must implement HypothesisEvaluator")
    if context.problem.id != request.problem_id:
        raise ValueError("context belongs to a different problem")
    if hypothesis.problem_id != request.problem_id:
        raise ValueError("hypothesis belongs to a different problem")
    if hypothesis.id != request.hypothesis_id:
        raise ValueError("hypothesis does not match request")
    evidence_ids = {item.id for item in context.evidence.items}
    if not set(request.evidence_ids).issubset(evidence_ids):
        raise ValueError("request references evidence outside the reasoning context")
    gap_ids = {gap.id for gap in context.gaps}
    if not set(request.gap_ids).issubset(gap_ids):
        raise ValueError("request references gaps outside the reasoning context")

    output = evaluator.evaluate(request, context, hypothesis)
    if not isinstance(output, EvaluationOutput):
        raise TypeError("evaluator must return EvaluationOutput")

    assemble_evaluation(request, output.evaluation, hypothesis)
    assemble_derivation(
        output.derivation,
        (hypothesis.id,) + tuple(request.evidence_ids) + tuple(request.gap_ids),
    )
    if output.derivation.artifact_id != output.evaluation.id:
        raise ValueError("evaluation derivation must target the evaluation")
    return output
