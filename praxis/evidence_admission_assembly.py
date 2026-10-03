"""Bounded assembly for explicit evidence admission."""

from __future__ import annotations

from praxis.admission import EvidenceAdmission
from praxis.evidence import EvidenceItem
from praxis.evidence_admission_request import EvidenceAdmissionRequest
from praxis.result import Result


def assemble_evidence_admission(
    request: EvidenceAdmissionRequest,
    admission: EvidenceAdmission,
    evidence_item: EvidenceItem,
    result: Result | None = None,
) -> EvidenceAdmission:
    """Validate an explicit authorization against its admission request and item."""
    if not isinstance(request, EvidenceAdmissionRequest):
        raise TypeError("request must be an EvidenceAdmissionRequest")
    if not isinstance(admission, EvidenceAdmission):
        raise TypeError("admission must be an EvidenceAdmission")
    if not isinstance(evidence_item, EvidenceItem):
        raise TypeError("evidence_item must be an EvidenceItem")
    if admission.id == request.id:
        raise ValueError("admission identity must differ from request identity")
    if admission.problem_id != request.problem_id:
        raise ValueError("admission belongs to a different problem")
    if admission.evidence_item_id != request.evidence_item_id:
        raise ValueError("admission targets a different evidence item")
    if evidence_item.id != request.evidence_item_id:
        raise ValueError("evidence item does not match request")
    if result is not None:
        if not isinstance(result, Result):
            raise TypeError("result must be a Result")
        if result.id != request.result_id:
            raise ValueError("result does not match request")
        if evidence_item.source_result_id != result.id:
            raise ValueError("evidence item does not reference the supplied result")
    return admission
