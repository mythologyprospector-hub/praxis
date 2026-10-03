from __future__ import annotations

import pytest

from praxis.admission import EvidenceAdmission
from praxis.episteme_handoff import EpistemeEvidenceHandoff, prepare_episteme_handoff
from praxis.evidence import EvidenceItem, EvidenceState


def _admitted():
    item = EvidenceItem(
        id="evidence-1",
        statement="Observed result.",
        provenance="test-log",
        uncertainty="limited",
        source_result_id="result-1",
    )
    admission = EvidenceAdmission(
        id="admission-1",
        problem_id="problem-1",
        evidence_item_id="evidence-1",
        authorized_by="human-1",
        rationale="Admit the observed result.",
    )
    state = EvidenceState(problem_id="problem-1").admit(item, admission)
    return state, item, admission


def test_episteme_handoff_preserves_praxis_identity_and_admission():
    state, item, admission = _admitted()

    handoff = prepare_episteme_handoff(
        state,
        item,
        admission,
        record_kind="RESULT",
        source_id="praxis:test-log",
        captured_at="2026-10-03T16:00:00+00:00",
        source_location="https://example.invalid/test-log",
    )

    assert isinstance(handoff, EpistemeEvidenceHandoff)
    assert handoff.praxis_evidence.id == "evidence-1"
    assert handoff.praxis_evidence.source_result_id == "result-1"
    assert handoff.praxis_admission.id == "admission-1"
    assert handoff.record_kind == "RESULT"
    assert handoff.to_dict()["source_id"] == "praxis:test-log"


def test_episteme_handoff_serialization_is_deterministic():
    state, item, admission = _admitted()
    handoff = prepare_episteme_handoff(
        state,
        item,
        admission,
        record_kind="OBSERVATION",
        source_id="praxis:test-log",
        captured_at="2026-10-03T16:00:00+00:00",
    )

    assert handoff.to_json() == handoff.to_json()
    assert '"praxis_evidence"' in handoff.to_json()


def test_episteme_handoff_requires_prior_admission():
    item = EvidenceItem(
        id="evidence-1",
        statement="Observed result.",
        provenance="test-log",
        uncertainty="limited",
    )
    state = EvidenceState(problem_id="problem-1")
    admission = EvidenceAdmission(
        id="admission-1",
        problem_id="problem-1",
        evidence_item_id="evidence-1",
        authorized_by="human-1",
        rationale="Admit.",
    )

    with pytest.raises(ValueError, match="already be admitted"):
        prepare_episteme_handoff(
            state,
            item,
            admission,
            record_kind="RESULT",
            source_id="praxis:test-log",
            captured_at="2026-10-03T16:00:00+00:00",
        )


def test_episteme_handoff_does_not_infer_record_kind_or_capture_time():
    state, item, admission = _admitted()

    with pytest.raises(TypeError):
        prepare_episteme_handoff(
            state,
            item,
            admission,
            record_kind=None,
            source_id="praxis:test-log",
            captured_at="2026-10-03T16:00:00+00:00",
        )

    with pytest.raises(ValueError, match="captured_at"):
        prepare_episteme_handoff(
            state,
            item,
            admission,
            record_kind="RESULT",
            source_id="praxis:test-log",
            captured_at="",
        )
