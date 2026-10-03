import json

import pytest

from praxis.evidence import EvidenceItem, EvidenceState


def test_evidence_item_requires_provenance_and_uncertainty():
    with pytest.raises(ValueError, match="provenance"):
        EvidenceItem(
            id="e1",
            statement="Water samples met the measured threshold.",
            provenance="",
            uncertainty="measurement uncertainty remains",
        )

    with pytest.raises(ValueError, match="uncertainty"):
        EvidenceItem(
            id="e1",
            statement="Water samples met the measured threshold.",
            provenance="lab-report-7",
            uncertainty="",
        )


def test_evidence_state_keeps_evidence_distinct_and_traceable():
    item = EvidenceItem(
        id="e1",
        statement="Water samples met the measured threshold.",
        provenance="lab-report-7",
        uncertainty="Sampling covered three locations.",
    )
    state = EvidenceState(problem_id="water-001", items=(item,))

    assert state.to_dict() == {
        "problem_id": "water-001",
        "items": [
            {
                "id": "e1",
                "statement": "Water samples met the measured threshold.",
                "provenance": "lab-report-7",
                "uncertainty": "Sampling covered three locations.",
            }
        ],
    }


def test_evidence_state_serialization_is_deterministic():
    state = EvidenceState(
        problem_id="p1",
        items=(
            EvidenceItem(
                id="e1",
                statement="Observation",
                provenance="source-1",
                uncertainty="limited sample",
            ),
        ),
    )

    assert state.to_json() == state.to_json()
    assert json.loads(state.to_json())["items"][0]["id"] == "e1"


def test_evidence_state_requires_evidence_items():
    with pytest.raises(TypeError, match="EvidenceItem"):
        EvidenceState(problem_id="p1", items=("not evidence",))



def test_result_must_be_explicitly_admitted_as_evidence() -> None:
    from praxis.result import Result

    result = Result(
        id="result-1",
        test_id="test-1",
        summary="Observed change.",
        observations=("The measured value changed.",),
        provenance="measurement-log-1",
        uncertainty="Single test run.",
    )
    evidence = EvidenceItem.from_result(result, "The measured value changed in the test.")

    assert evidence.source_result_id == "result-1"
    assert evidence.provenance == result.provenance
    assert evidence.uncertainty == result.uncertainty


def test_result_is_not_automatically_added_to_evidence_state() -> None:
    from praxis.result import Result

    result = Result(
        id="result-1",
        test_id="test-1",
        summary="Observed change.",
        observations=("The measured value changed.",),
        provenance="measurement-log-1",
        uncertainty="Single test run.",
    )
    state = EvidenceState(problem_id="problem-1")

    assert result.id not in {item.source_result_id for item in state.items}



def test_evidence_state_requires_explicit_admission() -> None:
    from praxis.admission import EvidenceAdmission
    from praxis.result import Result

    result = Result(
        id="result-1",
        test_id="test-1",
        summary="Observed change.",
        observations=("The measured value changed.",),
        provenance="measurement-log-1",
        uncertainty="Single test run.",
    )
    evidence = EvidenceItem.from_result(result, "The measured value changed in the test.")
    state = EvidenceState(problem_id="problem-1")
    admission = EvidenceAdmission(
        id="admission-1",
        problem_id="problem-1",
        evidence_item_id=evidence.id,
        authorized_by="human-decision-1",
        rationale="The result is appropriate for the current evidence state.",
    )

    admitted = state.admit(evidence, admission)

    assert admitted.items == (evidence,)


def test_evidence_admission_cannot_cross_problem_boundary() -> None:
    from praxis.admission import EvidenceAdmission

    evidence = EvidenceItem(
        id="e1",
        statement="Observation",
        provenance="source-1",
        uncertainty="limited sample",
    )
    state = EvidenceState(problem_id="problem-1")
    admission = EvidenceAdmission(
        id="admission-1",
        problem_id="problem-2",
        evidence_item_id="e1",
        authorized_by="human-decision-1",
        rationale="Approved.",
    )

    with pytest.raises(ValueError, match="problem_id"):
        state.admit(evidence, admission)


def test_evidence_admission_must_match_evidence_item() -> None:
    from praxis.admission import EvidenceAdmission

    evidence = EvidenceItem(
        id="e1",
        statement="Observation",
        provenance="source-1",
        uncertainty="limited sample",
    )
    state = EvidenceState(problem_id="problem-1")
    admission = EvidenceAdmission(
        id="admission-1",
        problem_id="problem-1",
        evidence_item_id="other",
        authorized_by="human-decision-1",
        rationale="Approved.",
    )

    with pytest.raises(ValueError, match="evidence_item_id"):
        state.admit(evidence, admission)
