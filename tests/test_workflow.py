from __future__ import annotations

import pytest

from praxis.candidate_generation import CandidateGenerationOutput
from praxis.candidate_request import CandidateRequest
from praxis.context import ReasoningContext
from praxis.derivation import Derivation
from praxis.evaluation import HypothesisEvaluation
from praxis.evaluation_provider import EvaluationOutput
from praxis.evaluation_request import EvaluationRequest
from praxis.evidence import EvidenceItem, EvidenceState
from praxis.gap import EvidenceGap
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention
from praxis.problem import Problem
from praxis.workflow import WorkflowRequest, prepare_workflow


def _context() -> ReasoningContext:
    problem = Problem(id="p-1", title="Problem", goal="Learn.")
    evidence = EvidenceState(
        problem_id="p-1",
        items=(EvidenceItem(id="e-1", statement="s", provenance="p", uncertainty="u"),),
    )
    gap = EvidenceGap(
        id="g-1", problem_id="p-1", description="unknown", decision_relevance="relevant"
    )
    return ReasoningContext(problem=problem, evidence=evidence, gaps=(gap,))


class _Generator:
    def generate(self, request, context):
        hypothesis = Hypothesis(
            id="h-1", problem_id=request.problem_id, statement="h", rationale="r"
        )
        intervention = Intervention(
            id="i-1", problem_id=request.problem_id, description="d", intended_outcome="o",
            hypothesis_ids=("h-1",)
        )
        return CandidateGenerationOutput(
            hypotheses=(hypothesis,),
            interventions=(intervention,),
            derivations=(
                Derivation(id="d-h", artifact_id="h-1", source_ids=("g-1",), method="m", uncertainty="u"),
                Derivation(id="d-i", artifact_id="i-1", source_ids=("g-1", "h-1"), method="m", uncertainty="u"),
            ),
        )


class _Evaluator:
    def evaluate(self, request, context, hypothesis):
        evaluation = HypothesisEvaluation(
            id="eval-1", hypothesis_id=hypothesis.id, inference="inference",
            uncertainty="u", evidence_ids=("e-1",)
        )
        return EvaluationOutput(
            evaluation=evaluation,
            derivation=Derivation(
                id="d-e", artifact_id="eval-1",
                source_ids=("h-1", "e-1"), method="m", uncertainty="u"
            ),
        )


def test_prepare_workflow_composes_candidate_and_evaluation_stages():
    request = WorkflowRequest(
        id="wf-1",
        problem_id="p-1",
        candidate_request=CandidateRequest(
            id="c-1", problem_id="p-1", gap_ids=("g-1",)
        ),
        evaluation_requests=(
            EvaluationRequest(
                id="e-req-1", problem_id="p-1",
                hypothesis_id="h-1", evidence_ids=("e-1",), gap_ids=("g-1",)
            ),
        ),
    )

    result = prepare_workflow(request, _context(), _Generator(), _Evaluator())

    assert result.candidates.hypothesis_ids == ("h-1",)
    assert result.candidates.hypotheses[0].id == "h-1"
    assert result.candidates.interventions[0].id == "i-1"
    assert result.evaluations[0].evaluation.hypothesis_id == "h-1"


def test_prepare_workflow_rejects_evaluation_outside_generated_candidates():
    request = WorkflowRequest(
        id="wf-1",
        problem_id="p-1",
        candidate_request=CandidateRequest(
            id="c-1", problem_id="p-1", gap_ids=("g-1",),
            requested_types=("hypothesis", "intervention")
        ),
        evaluation_requests=(
            EvaluationRequest(
                id="e-req-1", problem_id="p-1",
                hypothesis_id="missing", evidence_ids=("e-1",)
            ),
        ),
    )

    with pytest.raises(ValueError, match="outside generated candidates"):
        prepare_workflow(request, _context(), _Generator(), _Evaluator())


def test_workflow_request_rejects_cross_problem_stage():
    with pytest.raises(ValueError, match="different problem"):
        WorkflowRequest(
            id="wf-1",
            problem_id="p-1",
            candidate_request=CandidateRequest(id="c-1", problem_id="p-2"),
        )
