from __future__ import annotations

import pytest

from praxis.candidate import CandidateSet
from praxis.decision import Decision
from praxis.decision_assembly import assemble_decision
from praxis.decision_request import DecisionRequest
from praxis.evidence import EvidenceItem
from praxis.result import Result
from praxis.test import Test


def _request() -> DecisionRequest:
    return DecisionRequest(
        id="request-1",
        problem_id="problem-1",
        subject_id="subject-1",
        candidate_ids=("candidates-1",),
        test_ids=("test-1",),
        result_ids=("result-1",),
        evidence_ids=("evidence-1",),
    )


def _decision() -> Decision:
    return Decision(
        id="decision-1",
        problem_id="problem-1",
        decision="Proceed with bounded test.",
        rationale="Human choice.",
        decided_by="human-1",
        subject_id="subject-1",
    )


def _candidate() -> CandidateSet:
    return CandidateSet(id="candidates-1", problem_id="problem-1", hypothesis_ids=("h-1",))


def _test() -> Test:
    return Test(
        id="test-1", problem_id="problem-1", objective="Learn.",
        expected_observations=("Observed.",), safety_constraints=("Stop.",),
        reversibility="Reversible.", decision_criteria=("Use result.",),
    )


def _result() -> Result:
    return Result(
        id="result-1", test_id="test-1", summary="Observed.",
        observations=("Observed.",), provenance="test-run", uncertainty="Low.",
    )


def _evidence() -> EvidenceItem:
    return EvidenceItem(
        id="evidence-1", statement="Observed.", provenance="test-run", uncertainty="Low.",
    )


def test_matching_request_accepts_decision_and_lineage() -> None:
    assert assemble_decision(
        _request(), _decision(),
        candidate_sets=(_candidate(),), tests=(_test(),),
        results=(_result(),), evidence_items=(_evidence(),),
    ) == _decision()


def test_missing_candidate_lineage_rejected() -> None:
    with pytest.raises(ValueError, match="candidates"):
        assemble_decision(_request(), _decision())


def test_missing_test_lineage_rejected() -> None:
    with pytest.raises(ValueError, match="tests"):
        assemble_decision(
            _request(), _decision(), candidate_sets=(_candidate(),)
        )


def test_missing_result_lineage_rejected() -> None:
    with pytest.raises(ValueError, match="results"):
        assemble_decision(
            _request(), _decision(), candidate_sets=(_candidate(),),
            tests=(_test(),)
        )


def test_missing_evidence_lineage_rejected() -> None:
    with pytest.raises(ValueError, match="evidence"):
        assemble_decision(
            _request(), _decision(), candidate_sets=(_candidate(),),
            tests=(_test(),), results=(_result(),)
        )


def test_wrong_problem_candidate_rejected() -> None:
    candidate = CandidateSet(id="candidates-1", problem_id="problem-2", hypothesis_ids=("h-1",))
    with pytest.raises(ValueError, match="candidate set"):
        assemble_decision(
            _request(), _decision(), candidate_sets=(candidate,),
            tests=(_test(),), results=(_result(),), evidence_items=(_evidence(),)
        )


def test_wrong_problem_test_rejected() -> None:
    test = Test(
        id="test-1", problem_id="problem-2", objective="Learn.",
        expected_observations=("Observed.",), safety_constraints=("Stop.",),
        reversibility="Reversible.", decision_criteria=("Use result.",),
    )
    with pytest.raises(ValueError, match="test"):
        assemble_decision(
            _request(), _decision(), candidate_sets=(_candidate(),),
            tests=(test,), results=(_result(),), evidence_items=(_evidence(),)
        )


def test_wrong_result_type_rejected() -> None:
    with pytest.raises(TypeError, match="Result"):
        assemble_decision(
            _request(), _decision(), candidate_sets=(_candidate(),),
            tests=(_test(),), results=(object(),), evidence_items=(_evidence(),)
        )


def test_wrong_evidence_type_rejected() -> None:
    with pytest.raises(TypeError, match="EvidenceItem"):
        assemble_decision(
            _request(), _decision(), candidate_sets=(_candidate(),),
            tests=(_test(),), results=(_result(),), evidence_items=(object(),)
        )


def test_wrong_problem_and_subject_still_rejected() -> None:
    decision = Decision(
        id="decision-1", problem_id="problem-2", decision="Proceed.",
        rationale="Choice.", decided_by="human-1", subject_id="subject-2",
    )
    with pytest.raises(ValueError, match="problem"):
        assemble_decision(_request(), decision)


def test_request_and_decision_identity_must_differ() -> None:
    decision = Decision(
        id="request-1", problem_id="problem-1", decision="Proceed.",
        rationale="Choice.", decided_by="human-1", subject_id="subject-1",
    )
    with pytest.raises(ValueError, match="identity"):
        assemble_decision(_request(), decision)


def test_wrong_decision_type_rejected() -> None:
    with pytest.raises(TypeError, match="Decision"):
        assemble_decision(_request(), object())  # type: ignore[arg-type]
