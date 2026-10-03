from __future__ import annotations

import json

import pytest

from praxis.evaluation import HypothesisEvaluation


def test_evaluation_references_hypothesis_and_evidence_without_becoming_evidence() -> None:
    evaluation = HypothesisEvaluation(
        id="eval-1",
        hypothesis_id="hyp-1",
        inference="The proposed mechanism remains plausible.",
        uncertainty="The available evidence does not establish causation.",
        evidence_ids=("evidence-1",),
    )

    data = evaluation.to_dict()

    assert data["hypothesis_id"] == "hyp-1"
    assert data["evidence_ids"] == ("evidence-1",)
    assert "provenance" not in data
    assert "statement" not in data


def test_evaluation_requires_hypothesis_id_and_inference() -> None:
    with pytest.raises(ValueError):
        HypothesisEvaluation(
            id="eval-1",
            hypothesis_id="",
            inference="An inference.",
            uncertainty="Uncertain.",
        )

    with pytest.raises(ValueError):
        HypothesisEvaluation(
            id="eval-1",
            hypothesis_id="hyp-1",
            inference="",
            uncertainty="Uncertain.",
        )


def test_evaluation_rejects_invalid_evidence_references() -> None:
    with pytest.raises(TypeError):
        HypothesisEvaluation(
            id="eval-1",
            hypothesis_id="hyp-1",
            inference="An inference.",
            uncertainty="Uncertain.",
            evidence_ids=["evidence-1"],  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError):
        HypothesisEvaluation(
            id="eval-1",
            hypothesis_id="hyp-1",
            inference="An inference.",
            uncertainty="Uncertain.",
            evidence_ids=(" ",),
        )


def test_evaluation_serialization_is_deterministic() -> None:
    evaluation = HypothesisEvaluation(
        id="eval-1",
        hypothesis_id="hyp-1",
        inference="An inference.",
        uncertainty="Uncertain.",
        evidence_ids=("evidence-1", "evidence-2"),
    )

    assert evaluation.to_json() == json.dumps(
        evaluation.to_dict(), sort_keys=True, separators=(",", ":")
    )
