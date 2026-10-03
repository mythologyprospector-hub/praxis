from __future__ import annotations

import pytest

from praxis.derivation import Derivation
from praxis.derivation_assembly import assemble_derivation


def _derivation() -> Derivation:
    return Derivation(
        id="derivation-1",
        artifact_id="model-1",
        source_ids=("evidence-1", "hypothesis-1"),
        method="bounded inference",
        uncertainty="moderate",
    )


def test_matching_sources_accept_derivation() -> None:
    derivation = _derivation()
    assert assemble_derivation(derivation, ("evidence-1", "hypothesis-1")) is derivation


def test_extra_supplied_sources_are_allowed() -> None:
    derivation = _derivation()
    assert assemble_derivation(
        derivation, ("evidence-1", "hypothesis-1", "result-1")
    ) is derivation


def test_missing_source_rejected() -> None:
    with pytest.raises(ValueError, match="outside supplied lineage"):
        assemble_derivation(_derivation(), ("evidence-1",))


def test_wrong_derivation_type_rejected() -> None:
    with pytest.raises(TypeError, match="Derivation"):
        assemble_derivation(object(), ())  # type: ignore[arg-type]


def test_invalid_source_identity_rejected() -> None:
    with pytest.raises(ValueError, match="non-empty strings"):
        assemble_derivation(_derivation(), ("evidence-1", ""))


def test_empty_source_list_is_rejected_when_derivation_requires_sources() -> None:
    with pytest.raises(ValueError, match="outside supplied lineage"):
        assemble_derivation(_derivation(), ())
