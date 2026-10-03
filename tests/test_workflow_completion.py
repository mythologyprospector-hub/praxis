from __future__ import annotations

import pytest

from praxis.admission import EvidenceAdmission
from praxis.candidate import CandidateSet
from praxis.candidate_generation import CandidateGenerationResult
from praxis.candidate_request import CandidateRequest
from praxis.decision import Decision
from praxis.decision_request import DecisionRequest
from praxis.decision_scope import DecisionScope
from praxis.evidence import EvidenceItem, EvidenceState
from praxis.evidence_admission_request import EvidenceAdmissionRequest
from praxis.intervention import Intervention
from praxis.result import Result
from praxis.result_provider import ResultOutput
from praxis.result_request import ResultRequest
from praxis.result_scope import ResultScope
from praxis.test import Test
from praxis.test_provider import TestDesignOutput
from praxis.workflow import WorkflowPreparation, WorkflowRequest, complete_workflow


class Recorder:
    def record(self, request, test):
        return ResultOutput(
            Result(
                id="result-1",
                test_id=test.id,
                summary="Observed.",
                observations=("observed",),
                provenance="test-log",
                uncertainty="limited",
            )
        )


def _preparation() -> WorkflowPreparation:
    intervention = Intervention(
        id="intervention-1",
        problem_id="problem-1",
        description="bounded change",
        intended_outcome="learn",
    )
    test = Test(
        id="test-1",
        problem_id="problem-1",
        objective="Learn.",
        expected_observations=("observed",),
        safety_constraints=("stop if unsafe",),
        reversibility="reversible",
        decision_criteria=("use observation",),
        intervention_ids=("intervention-1",),
    )
    return WorkflowPreparation(
        request=WorkflowRequest(
            id="workflow-1",
            problem_id="problem-1",
            candidate_request=CandidateRequest(
                id="candidate-request-1",
                problem_id="problem-1",
                gap_ids=(),
                requested_types=("intervention",),
            ),
        ),
        candidates=CandidateGenerationResult(
            candidate_set=CandidateSet(
                id="candidates-1",
                problem_id="problem-1",
                intervention_ids=("intervention-1",),
            ),
            interventions=(intervention,),
        ),
        test=TestDesignOutput(test=test, derivation=object()),
    )


def test_complete_workflow_crosses_both_human_gates():
    preparation = _preparation()
    result = complete_workflow(
        preparation,
        DecisionRequest(
            id="decision-request-1",
            problem_id="problem-1",
            subject_id="test-1",
            candidate_ids=("candidates-1",),
            test_ids=("test-1",),
        ),
        Decision(
            id="decision-1",
            problem_id="problem-1",
            decision="Proceed with bounded test.",
            rationale="Human choice.",
            decided_by="human-1",
            subject_id="test-1",
        ),
        DecisionScope(
            id="decision-scope-1",
            decision_id="decision-1",
            problem_id="problem-1",
            test_id="test-1",
            intervention_id="intervention-1",
        ),
        ResultRequest(
            id="result-request-1",
            problem_id="problem-1",
            test_id="test-1",
            intervention_ids=("intervention-1",),
        ),
        Recorder(),
        ResultScope(
            id="result-scope-1",
            result_id="result-1",
            problem_id="problem-1",
            test_id="test-1",
            intervention_ids=("intervention-1",),
        ),
        EvidenceAdmissionRequest(
            id="evidence-request-1",
            problem_id="problem-1",
            result_id="result-1",
            evidence_item_id="evidence-1",
            rationale="Human review requested.",
        ),
        EvidenceAdmission(
            id="admission-1",
            problem_id="problem-1",
            evidence_item_id="evidence-1",
            authorized_by="human-2",
            rationale="Admit the observed result.",
        ),
        EvidenceItem(
            id="evidence-1",
            statement="Observed.",
            provenance="test-log",
            uncertainty="limited",
            source_result_id="result-1",
        ),
        EvidenceState(problem_id="problem-1"),
        decision_intervention=preparation.candidates.interventions[0],
    )

    assert result.decision.id == "decision-1"
    assert result.result.id == "result-1"
    assert result.evidence_state.items == (result.evidence_item,)


def test_complete_workflow_requires_predecision_test():
    preparation = _preparation()
    preparation = WorkflowPreparation(
        request=preparation.request,
        candidates=preparation.candidates,
    )

    with pytest.raises(ValueError, match="designed test"):
        complete_workflow(
            preparation,
            DecisionRequest(
                id="decision-request-1",
                problem_id="problem-1",
                subject_id="test-1",
            ),
            Decision(
                id="decision-1",
                problem_id="problem-1",
                decision="Proceed.",
                rationale="Human choice.",
                decided_by="human-1",
                subject_id="test-1",
            ),
            DecisionScope(
                id="decision-scope-1",
                decision_id="decision-1",
                problem_id="problem-1",
                test_id="test-1",
            ),
            ResultRequest(
                id="result-request-1",
                problem_id="problem-1",
                test_id="test-1",
            ),
            Recorder(),
            ResultScope(
                id="result-scope-1",
                result_id="result-1",
                problem_id="problem-1",
                test_id="test-1",
            ),
            EvidenceAdmissionRequest(
                id="evidence-request-1",
                problem_id="problem-1",
                result_id="result-1",
                evidence_item_id="evidence-1",
                rationale="Review.",
            ),
            EvidenceAdmission(
                id="admission-1",
                problem_id="problem-1",
                evidence_item_id="evidence-1",
                authorized_by="human-2",
                rationale="Admit.",
            ),
            EvidenceItem(
                id="evidence-1",
                statement="Observed.",
                provenance="test-log",
                uncertainty="limited",
                source_result_id="result-1",
            ),
            EvidenceState(problem_id="problem-1"),
        )


def test_complete_workflow_rejects_cross_problem_downstream_artifacts():
    preparation = _preparation()

    with pytest.raises(ValueError, match="different workflow problem"):
        complete_workflow(
            preparation,
            DecisionRequest(
                id="decision-request-1",
                problem_id="problem-2",
                subject_id="test-1",
            ),
            Decision(
                id="decision-1",
                problem_id="problem-2",
                decision="Proceed.",
                rationale="Human choice.",
                decided_by="human-1",
                subject_id="test-1",
            ),
            DecisionScope(
                id="decision-scope-1",
                decision_id="decision-1",
                problem_id="problem-2",
                test_id="test-1",
            ),
            ResultRequest(
                id="result-request-1",
                problem_id="problem-2",
                test_id="test-1",
            ),
            Recorder(),
            ResultScope(
                id="result-scope-1",
                result_id="result-1",
                problem_id="problem-2",
                test_id="test-1",
            ),
            EvidenceAdmissionRequest(
                id="evidence-request-1",
                problem_id="problem-2",
                result_id="result-1",
                evidence_item_id="evidence-1",
                rationale="Review.",
            ),
            EvidenceAdmission(
                id="admission-1",
                problem_id="problem-2",
                evidence_item_id="evidence-1",
                authorized_by="human-2",
                rationale="Admit.",
            ),
            EvidenceItem(
                id="evidence-1",
                statement="Observed.",
                provenance="test-log",
                uncertainty="limited",
                source_result_id="result-1",
            ),
            EvidenceState(problem_id="problem-2"),
            decision_intervention=preparation.candidates.interventions[0],
        )
