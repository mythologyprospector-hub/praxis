"""Bounded composition of Praxis reasoning stages.

The coordinator sequences established provider boundaries. It does not reason,
rank, select, authorize, execute, or admit evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from praxis.candidate_generation import CandidateGenerationResult, CandidateGenerator, generate_candidates
from praxis.context import ReasoningContext
from praxis.evaluation import HypothesisEvaluation
from praxis.evaluation_provider import HypothesisEvaluator, EvaluationOutput, evaluate_hypothesis
from praxis.evaluation_request import EvaluationRequest
from praxis.failure_analysis import FailureAnalysis
from praxis.failure_analysis_provider import FailureAnalysisOutput, FailureAnalyzer, analyze_failures
from praxis.failure_request import FailureAnalysisRequest
from praxis.hypothesis import Hypothesis
from praxis.model import Model
from praxis.model_provider import ModelBuilder, ModelOutput, build_model
from praxis.model_request import ModelRequest
from praxis.problem import Problem
from praxis.test import Test
from praxis.test_provider import TestDesignOutput, TestDesigner, design_test
from praxis.test_request import TestRequest


@dataclass(frozen=True)
class WorkflowRequest:
    """Explicit inputs for one bounded pre-decision workflow."""

    id: str
    problem_id: str
    candidate_request: object
    evaluation_requests: tuple[EvaluationRequest, ...] = ()
    failure_request: FailureAnalysisRequest | None = None
    model_request: ModelRequest | None = None
    test_request: TestRequest | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("id must be a non-empty string")
        if not isinstance(self.problem_id, str) or not self.problem_id.strip():
            raise ValueError("problem_id must be a non-empty string")
        if not isinstance(self.evaluation_requests, tuple):
            raise TypeError("evaluation_requests must be a tuple")
        if any(not isinstance(item, EvaluationRequest) for item in self.evaluation_requests):
            raise TypeError("evaluation_requests must contain EvaluationRequest objects")
        for item in self.evaluation_requests:
            if item.problem_id != self.problem_id:
                raise ValueError("evaluation request belongs to a different problem")
        for name, item in (
            ("failure_request", self.failure_request),
            ("model_request", self.model_request),
            ("test_request", self.test_request),
        ):
            if item is not None and item.problem_id != self.problem_id:
                raise ValueError(f"{name} belongs to a different problem")


@dataclass(frozen=True)
class WorkflowPreparation:
    """Validated artifacts produced before the human decision gate."""

    request: WorkflowRequest
    candidates: CandidateGenerationResult
    evaluations: tuple[EvaluationOutput, ...] = ()
    failure_analysis: FailureAnalysisOutput | None = None
    model: ModelOutput | None = None
    test: TestDesignOutput | None = None


def prepare_workflow(
    request: WorkflowRequest,
    context: ReasoningContext,
    generator: CandidateGenerator,
    evaluator: HypothesisEvaluator,
    *,
    failure_analyzer: FailureAnalyzer | None = None,
    model_builder: ModelBuilder | None = None,
    test_designer: TestDesigner | None = None,
) -> WorkflowPreparation:
    """Compose bounded stages through the explicit pre-decision boundary."""
    if not isinstance(request, WorkflowRequest):
        raise TypeError("request must be a WorkflowRequest")
    if not isinstance(context, ReasoningContext):
        raise TypeError("context must be a ReasoningContext")
    if context.problem.id != request.problem_id:
        raise ValueError("context belongs to a different problem")
    if request.candidate_request.problem_id != request.problem_id:
        raise ValueError("candidate request belongs to a different problem")

    candidates = generate_candidates(request.candidate_request, context, generator)
    hypotheses = _by_id(candidates, Hypothesis, candidates.candidate_set.hypothesis_ids)
    interventions = _by_id(candidates, __import__("praxis.intervention", fromlist=["Intervention"]).Intervention, candidates.candidate_set.intervention_ids)

    evaluations = tuple(
        evaluate_hypothesis(
            evaluation_request,
            context,
            hypotheses[evaluation_request.hypothesis_id],
            evaluator,
        )
        for evaluation_request in request.evaluation_requests
    )

    if request.failure_request is None:
        failure_analysis = None
    else:
        if failure_analyzer is None:
            raise ValueError("failure_analyzer is required by failure_request")
        failure_analysis = analyze_failures(
            request.failure_request,
            context,
            tuple(interventions.values()),
            failure_analyzer,
            hypotheses=tuple(hypotheses.values()),
            models=(),
        )

    if request.model_request is None:
        model = None
    else:
        if model_builder is None:
            raise ValueError("model_builder is required by model_request")
        model = build_model(
            request.model_request,
            model_builder,
            hypotheses=tuple(hypotheses.values()),
            interventions=tuple(interventions.values()),
        )

    if request.test_request is None:
        test = None
    else:
        if test_designer is None:
            raise ValueError("test_designer is required by test_request")
        failure_modes = () if failure_analysis is None else failure_analysis.failure_modes
        models = () if model is None else (model.model,)
        test = design_test(
            request.test_request,
            test_designer,
            interventions=tuple(interventions.values()),
            hypotheses=tuple(hypotheses.values()),
            failure_modes=failure_modes,
            models=models,
        )

    return WorkflowPreparation(
        request=request,
        candidates=candidates,
        evaluations=evaluations,
        failure_analysis=failure_analysis,
        model=model,
        test=test,
    )


def _by_id(source: CandidateGenerationResult, expected_type: type, ids: tuple[str, ...]) -> dict[str, object]:
    items = []
    if expected_type is Hypothesis:
        items = [item for item_id in ids for item in source._hypotheses if item.id == item_id] if hasattr(source, "_hypotheses") else []
    if not items:
        raise ValueError("candidate result does not expose requested candidate objects")
    return {item.id: item for item in items}
