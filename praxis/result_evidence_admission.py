"""Bounded closed-loop transition from an observed result to admitted evidence.

This module composes existing lineage and human-gating boundaries. It does not
generate evidence, authorize admission, or execute consequential action.
"""

from __future__ import annotations

from praxis.evidence import EvidenceItem, EvidenceState
from praxis.evidence_admission import admit_evidence
from praxis.evidence_admission_assembly import assemble_evidence_admission
from praxis.evidence_admission_request import EvidenceAdmissionRequest
from praxis.admission import EvidenceAdmission
from praxis.result import Result
from praxis.result_evidence_assembly import assemble_result_evidence


def admit_result_as_evidence(
    state: EvidenceState,
    request: EvidenceAdmissionRequest,
    admission: EvidenceAdmission,
    result: Result,
    evidence_item: EvidenceItem,
) -> EvidenceState:
    """Admit one result-derived evidence item after explicit human authorization."""
    item = assemble_result_evidence(result, evidence_item)
    assemble_evidence_admission(request, admission, item, result)
    return admit_evidence(state, item, admission)
