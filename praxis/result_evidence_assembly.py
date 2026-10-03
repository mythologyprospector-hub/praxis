"""Bounded assembly for result-derived evidence items."""

from __future__ import annotations

from praxis.evidence import EvidenceItem
from praxis.result import Result


def assemble_result_evidence(result: Result, evidence_item: EvidenceItem) -> EvidenceItem:
    """Validate that an evidence item explicitly derives from the supplied result."""
    if not isinstance(result, Result):
        raise TypeError("result must be a Result")
    if not isinstance(evidence_item, EvidenceItem):
        raise TypeError("evidence_item must be an EvidenceItem")
    if evidence_item.source_result_id != result.id:
        raise ValueError("evidence item does not reference the supplied result")
    return evidence_item
