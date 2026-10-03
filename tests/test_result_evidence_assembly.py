from __future__ import annotations

import pytest

from praxis.evidence import EvidenceItem
from praxis.result import Result
from praxis.result_evidence_assembly import assemble_result_evidence


def _result() -> Result:
    return Result(
        id="result-1",
        test_id="test-1",
        summary="Observed.",
        observations=("observation-1",),
        provenance="experiment-log",
        uncertainty="moderate",
    )


def _item(**overrides: object) -> EvidenceItem:
    values: dict[str, object] = {
        "id": "evidence:result-1",
        "statement": "Observed outcome.",
        "provenance": "experiment-log",
        "uncertainty": "moderate",
        "source_result_id": "result-1",
    }
    values.update(overrides)
    return EvidenceItem(**values)


def test_matching_result_accepts_evidence() -> None:
    item = _item()
    assert assemble_result_evidence(_result(), item) is item


def test_wrong_result_rejected() -> None:
    other = Result(
        id="result-2",
        test_id="test-1",
        summary="Other.",
        observations=("observation-2",),
        provenance="experiment-log",
        uncertainty="moderate",
    )
    with pytest.raises(ValueError, match="does not reference"):
        assemble_result_evidence(other, _item())


def test_missing_source_reference_rejected() -> None:
    with pytest.raises(ValueError, match="does not reference"):
        assemble_result_evidence(_result(), _item(source_result_id=None))


def test_wrong_result_type_rejected() -> None:
    with pytest.raises(TypeError, match="Result"):
        assemble_result_evidence(object(), _item())


def test_wrong_evidence_type_rejected() -> None:
    with pytest.raises(TypeError, match="EvidenceItem"):
        assemble_result_evidence(_result(), object())
