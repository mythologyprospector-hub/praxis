"""Bounded transition for explicitly admitting evidence into state."""

from __future__ import annotations

from praxis.admission import EvidenceAdmission
from praxis.evidence import EvidenceItem, EvidenceState


def admit_evidence(
    state: EvidenceState,
    item: EvidenceItem,
    admission: EvidenceAdmission,
) -> EvidenceState:
    """Return a new evidence state after an explicit admission authorization."""
    if not isinstance(state, EvidenceState):
        raise TypeError("state must be an EvidenceState")
    if not isinstance(item, EvidenceItem):
        raise TypeError("item must be an EvidenceItem")
    if not isinstance(admission, EvidenceAdmission):
        raise TypeError("admission must be an EvidenceAdmission")
    return state.admit(item, admission)
