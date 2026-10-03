from __future__ import annotations

import json

import pytest

from praxis.gap import EvidenceGap


def test_evidence_gap_represents_missing_knowledge_not_evidence() -> None:
    gap = EvidenceGap(
        id="gap-1",
        problem_id="problem-1",
        description="The effect under the relevant boundary condition is unknown.",
        decision_relevance="The uncertainty could change whether the candidate is tested.",
    )

    data = gap.to_dict()

    assert data["problem_id"] == "problem-1"
    assert "provenance" not in data
    assert "statement" not in data
    assert "evidence_ids" not in data


def test_evidence_gap_requires_core_fields() -> None:
    with pytest.raises(ValueError):
        EvidenceGap(
            id="gap-1",
            problem_id="",
            description="An unknown.",
            decision_relevance="Relevant.",
        )

    with pytest.raises(ValueError):
        EvidenceGap(
            id="gap-1",
            problem_id="problem-1",
            description="",
            decision_relevance="Relevant.",
        )


def test_evidence_gap_serialization_is_deterministic() -> None:
    gap = EvidenceGap(
        id="gap-1",
        problem_id="problem-1",
        description="An unknown.",
        decision_relevance="Relevant.",
    )

    assert gap.to_json() == json.dumps(
        gap.to_dict(), sort_keys=True, separators=(",", ":")
    )
