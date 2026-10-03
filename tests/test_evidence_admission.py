from __future__ import annotations

import pytest

from praxis.admission import EvidenceAdmission
from praxis.evidence import EvidenceItem, EvidenceState
from praxis.evidence_admission import admit_evidence


def _item() -> EvidenceItem:
    return EvidenceItem(id="evidence-1", statement="Observed outcome.", provenance="experiment-log", uncertainty="moderate")


def _admission() -> EvidenceAdmission:
    return EvidenceAdmission(id="admission-1", problem_id="problem-1", evidence_item_id="evidence-1", authorized_by="human-1", rationale="Authorized.")


def test_admission_returns_new_state_with_item() -> None:
    state = EvidenceState(problem_id="problem-1")
    result = admit_evidence(state, _item(), _admission())
    assert result is not state
    assert result.items == (_item(),)


def test_mismatched_problem_rejected() -> None:
    state = EvidenceState(problem_id="problem-2")
    with pytest.raises(ValueError, match="problem_id"):
        admit_evidence(state, _item(), _admission())


def test_mismatched_evidence_rejected() -> None:
    state = EvidenceState(problem_id="problem-1")
    item = EvidenceItem(id="evidence-2", statement="Other.", provenance="log", uncertainty="high")
    with pytest.raises(ValueError, match="evidence_item_id"):
        admit_evidence(state, item, _admission())


def test_wrong_state_type_rejected() -> None:
    with pytest.raises(TypeError, match="EvidenceState"):
        admit_evidence(object(), _item(), _admission())  # type: ignore[arg-type]


def test_wrong_item_type_rejected() -> None:
    with pytest.raises(TypeError, match="EvidenceItem"):
        admit_evidence(EvidenceState(problem_id="problem-1"), object(), _admission())  # type: ignore[arg-type]


def test_wrong_admission_type_rejected() -> None:
    with pytest.raises(TypeError, match="EvidenceAdmission"):
        admit_evidence(EvidenceState(problem_id="problem-1"), _item(), object())  # type: ignore[arg-type]


def test_duplicate_admission_preserves_state() -> None:
    state = EvidenceState(problem_id="problem-1", items=(_item(),))
    result = admit_evidence(state, _item(), _admission())
    assert result is state
