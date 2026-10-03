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
