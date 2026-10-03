"""Bounded composition of Praxis reasoning stages.

The coordinator sequences established provider boundaries. It does not reason,
rank, select, authorize, execute, or admit evidence.
"""
from __future__ import annotations

from dataclasses import dataclass

from praxis.candidate_generation import CandidateGenerationResult, CandidateGenerator, generate_candidates
from praxis.candidate_request import CandidateRequest
from praxis.decision import Decision
from praxis.decision_assembly import assemble_decision
from praxis.decision_request import DecisionRequest
from praxis.decision_scope import DecisionScope
from praxis.decision_scope_assembly import assemble_decision_scope
from praxis.evidence import EvidenceItem, EvidenceState
from praxis.admission import EvidenceAdmission
from praxis.evidence_admission_request import EvidenceAdmissionRequest
from praxis.intervention import Intervention
from praxis.result import Result
from praxis.result_evidence_admission import admit_result_as_evidence
from praxis.result_request import ResultRequest
from praxis.result_provider import ResultRecorder, record_result
from praxis.result_scope import ResultScope
from praxis.result_scope_assembly import assemble_result_scope
from praxis.context import ReasoningContext
from praxis.evaluation_provider import EvaluationOutput, HypothesisEvaluator, evaluate_hypothesis
from praxis.evaluation_request import EvaluationRequest
from praxis.failure_analysis_provider import FailureAnalysisOutput, FailureAnalyzer, analyze_failures
from praxis.failure_request import FailureAnalysisRequest
from praxis.model_provider import ModelBuilder, ModelOutput, build_model
from praxis.model_request import ModelRequest
from praxis.test_provider import TestDesignOutput, TestDesigner, design_test
from praxis.test_request import TestRequest


@dataclass(frozen=True)
class WorkflowRequest:
    """Explicit inputs for one bounded pre-decision workflow."""

    id: str
    problem_id: str
    candidate_request: CandidateRequest
    evaluation_requests: tuple[EvaluationRequest, ...] = ()
    failure_request: FailureAnalysisRequest | None = None
    model_request: ModelRequest | None = None
    test_request: TestRequest | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("id must be a non-empty string")
        if not isinstance(self.problem_id, str) or not self.problem_id.strip():
            raise ValueError("problem_id must be a non-empty string")
        if not isinstance(self.candidate_request, CandidateRequest):
            raise TypeError("candidate_request must be a CandidateRequest")
        if self.candidate_request.problem_id != self.problem_id:
            raise ValueError("candidate request belongs to a different problem")
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

    candidates = generate_candidates(request.candidate_request, context, generator)
    hypotheses = {item.id: item for item in candidates.hypotheses}
    interventions = {item.id: item for item in candidates.interventions}

    for evaluation_request in request.evaluation_requests:
        if evaluation_request.hypothesis_id not in hypotheses:
            raise ValueError("evaluation request references a hypothesis outside generated candidates")

    evaluations = tuple(
        evaluate_hypothesis(
            evaluation_request,
            context,
            hypotheses[evaluation_request.hypothesis_id],
            evaluator,
        )
        for evaluation_request in request.evaluation_requests
    )

    failure_analysis = None
    if request.failure_request is not None:
        if failure_analyzer is None:
            raise ValueError("failure_analyzer is required by failure_request")
        if not set(request.failure_request.intervention_ids).issubset(interventions):
            raise ValueError("failure request references interventions outside generated candidates")
        if not set(request.failure_request.hypothesis_ids).issubset(hypotheses):
            raise ValueError("failure request references hypotheses outside generated candidates")
        failure_analysis = analyze_failures(
            request.failure_request,
            context,
            tuple(interventions.values()),
            failure_analyzer,
            hypotheses=tuple(hypotheses.values()),
        )

    model = None
    if request.model_request is not None:
        if model_builder is None:
            raise ValueError("model_builder is required by model_request")
        if not set(request.model_request.hypothesis_ids).issubset(hypotheses):
            raise ValueError("model request references hypotheses outside generated candidates")
        if not set(request.model_request.intervention_ids).issubset(interventions):
            raise ValueError("model request references interventions outside generated candidates")
        model = build_model(
            request.model_request,
            model_builder,
            hypotheses=tuple(hypotheses.values()),
            interventions=tuple(interventions.values()),
        )

    test = None
    if request.test_request is not None:
        if test_designer is None:
            raise ValueError("test_designer is required by test_request")
        if not set(request.test_request.intervention_ids).issubset(interventions):
            raise ValueError("test request references interventions outside generated candidates")
        if not set(request.test_request.hypothesis_ids).issubset(hypotheses):
            raise ValueError("test request references hypotheses outside generated candidates")
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


@dataclass(frozen=True)
class WorkflowCompletion:
    """Validated artifacts produced after the human decision gate."""

    preparation: WorkflowPreparation
    decision_request: DecisionRequest
    decision: Decision
    decision_scope: DecisionScope
    result_request: ResultRequest
    result: Result
    result_scope: ResultScope
    evidence_admission_request: EvidenceAdmissionRequest
    evidence_admission: EvidenceAdmission
    evidence_item: EvidenceItem
    evidence_state: EvidenceState


def complete_workflow(
    preparation: WorkflowPreparation,
    decision_request: DecisionRequest,
    decision: Decision,
    decision_scope: DecisionScope,
    result_request: ResultRequest,
    recorder: ResultRecorder,
    result_scope: ResultScope,
    evidence_admission_request: EvidenceAdmissionRequest,
    evidence_admission: EvidenceAdmission,
    evidence_item: EvidenceItem,
    evidence_state: EvidenceState,
    *,
    decision_intervention: Intervention | None = None,
) -> WorkflowCompletion:
    """Compose post-decision stages without interpreting or authorizing them."""
    if not isinstance(preparation, WorkflowPreparation):
        raise TypeError("preparation must be a WorkflowPreparation")
    if preparation.test is None:
        raise ValueError("workflow preparation must contain a designed test")
    test = preparation.test.test

    assemble_decision(
        decision_request,
        decision,
        candidate_sets=(preparation.candidates.candidate_set,),
        tests=(test,),
    )
    assemble_decision_scope(
        decision_scope,
        decision,
        test,
        decision_intervention,
    )

    result = record_result(result_request, test, recorder).result
    assemble_result_scope(result_scope, result, test)

    final_state = admit_result_as_evidence(
        evidence_state,
        evidence_admission_request,
        evidence_admission,
        result,
        evidence_item,
    )
    return WorkflowCompletion(
        preparation=preparation,
        decision_request=decision_request,
        decision=decision,
        decision_scope=decision_scope,
        result_request=result_request,
        result=result,
        result_scope=result_scope,
        evidence_admission_request=evidence_admission_request,
        evidence_admission=evidence_admission,
        evidence_item=evidence_item,
        evidence_state=final_state,
    )
