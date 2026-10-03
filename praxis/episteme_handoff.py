"""Explicit translation boundary for handing admitted Praxis evidence toward Episteme.

This module deliberately does not import Episteme. It defines a stable, JSON-compatible
handoff packet that preserves Praxis identity and human-admission provenance while
requiring the Episteme-side record semantics to be supplied explicitly by the caller.
"""

from __future__ import annotations

from dataclasses import dataclass
import json

from praxis.admission import EvidenceAdmission
from praxis.evidence import EvidenceItem, EvidenceState


@dataclass(frozen=True)
class EpistemeEvidenceHandoff:
    """A bounded, non-authoritative packet for one admitted Praxis evidence item."""

    schema_version: int
    record_kind: str
    source_id: str
    captured_at: str
    praxis_evidence: EvidenceItem
    praxis_admission: EvidenceAdmission
    source_location: str | None = None

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise ValueError("schema_version must be 1")
        for name in ("record_kind", "source_id", "captured_at"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(self.praxis_evidence, EvidenceItem):
            raise TypeError("praxis_evidence must be an EvidenceItem")
        if not isinstance(self.praxis_admission, EvidenceAdmission):
            raise TypeError("praxis_admission must be an EvidenceAdmission")
        if self.source_location is not None and (
            not isinstance(self.source_location, str) or not self.source_location.strip()
        ):
            raise ValueError("source_location must be a non-empty string when provided")

    def to_dict(self) -> dict[str, object]:
        data: dict[str, object] = {
            "schema_version": self.schema_version,
            "record_kind": self.record_kind,
            "source_id": self.source_id,
            "captured_at": self.captured_at,
            "praxis_evidence": self.praxis_evidence.to_dict(),
            "praxis_admission": self.praxis_admission.to_dict(),
        }
        if self.source_location is not None:
            data["source_location"] = self.source_location
        return data

    def to_json(self) -> str:
        """Serialize deterministically for a transport/import boundary."""
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))


def prepare_episteme_handoff(
    evidence_state: EvidenceState,
    evidence_item: EvidenceItem,
    admission: EvidenceAdmission,
    *,
    record_kind: str,
    source_id: str,
    captured_at: str,
    source_location: str | None = None,
) -> EpistemeEvidenceHandoff:
    """Create a handoff only from evidence already admitted by Praxis.

    Episteme record kind, source identity, and capture time are explicit inputs.
    Nothing here infers epistemic status, generates an Episteme record ID, or
    authorizes evidence admission.
    """
    if not isinstance(evidence_state, EvidenceState):
        raise TypeError("evidence_state must be an EvidenceState")
    if evidence_item not in evidence_state.items:
        raise ValueError("evidence item must already be admitted to evidence state")
    if admission.problem_id != evidence_state.problem_id:
        raise ValueError("admission problem_id does not match evidence state")
    if admission.evidence_item_id != evidence_item.id:
        raise ValueError("admission evidence_item_id does not match evidence item")

    return EpistemeEvidenceHandoff(
        schema_version=1,
        record_kind=record_kind,
        source_id=source_id,
        captured_at=captured_at,
        praxis_evidence=evidence_item,
        praxis_admission=admission,
        source_location=source_location,
    )
