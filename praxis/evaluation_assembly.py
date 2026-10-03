"""Bounded assembly for hypothesis evaluations."""
from __future__ import annotations

from collections.abc import Iterable

from .evaluation import HypothesisEvaluation
from .evaluation_request import EvaluationRequest


def assemble_evaluation(
    request: EvaluationRequest,
    evaluation: HypothesisEvaluation,
) -> HypothesisEvaluation:
    """Validate an evaluation against its explicit request boundary."""
    if not isinstance(evaluation, HypothesisEvaluation):
        raise TypeError("evaluation must be a HypothesisEvaluation")
    if evaluation.id.strip() != evaluation.id:
        raise ValueError("evaluation id must not have surrounding whitespace")
    if evaluation.hypothesis_id != request.hypothesis_id:
        raise ValueError("evaluation targets a different hypothesis")
    if evaluation.id == request.id:
        raise ValueError("evaluation identity must differ from request identity")
    if not isinstance(request.evidence_ids, tuple):
        raise TypeError("request evidence_ids must be a tuple")
    missing = set(request.evidence_ids) - set(evaluation.evidence_ids)
    if missing:
        raise ValueError("evaluation does not reference all requested evidence")
    return evaluation
