"""Bounded assembly for hypothesis evaluations."""
from __future__ import annotations

from .evaluation import HypothesisEvaluation
from .evaluation_request import EvaluationRequest
from .hypothesis import Hypothesis


def assemble_evaluation(
    request: EvaluationRequest,
    evaluation: HypothesisEvaluation,
    hypothesis: Hypothesis | None = None,
) -> HypothesisEvaluation:
    """Validate an evaluation against its explicit request boundary."""
    if not isinstance(request, EvaluationRequest):
        raise TypeError("request must be an EvaluationRequest")
    if not isinstance(evaluation, HypothesisEvaluation):
        raise TypeError("evaluation must be a HypothesisEvaluation")
    if evaluation.id.strip() != evaluation.id:
        raise ValueError("evaluation id must not have surrounding whitespace")
    if hypothesis is not None:
        if not isinstance(hypothesis, Hypothesis):
            raise TypeError("hypothesis must be a Hypothesis")
        if hypothesis.id != request.hypothesis_id:
            raise ValueError("hypothesis does not match request")
        if hypothesis.problem_id != request.problem_id:
            raise ValueError("hypothesis belongs to a different problem")
        if evaluation.hypothesis_id != hypothesis.id:
            raise ValueError("evaluation targets a different hypothesis")
    elif evaluation.hypothesis_id != request.hypothesis_id:
        raise ValueError("evaluation targets a different hypothesis")
    if evaluation.id == request.id:
        raise ValueError("evaluation identity must differ from request identity")
    if not isinstance(request.evidence_ids, tuple):
        raise TypeError("request evidence_ids must be a tuple")
    requested_evidence = set(request.evidence_ids)
    evaluation_evidence = set(evaluation.evidence_ids)
    missing = requested_evidence - evaluation_evidence
    if missing:
        raise ValueError("evaluation does not reference all requested evidence")
    if not evaluation_evidence.issubset(requested_evidence):
        raise ValueError("evaluation references evidence outside the request")
    return evaluation
