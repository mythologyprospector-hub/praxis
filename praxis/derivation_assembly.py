"""Bounded assembly for derivation lineage."""

from __future__ import annotations

from praxis.derivation import Derivation


def assemble_derivation(derivation: Derivation, artifact_ids: tuple[str, ...]) -> Derivation:
    """Validate that a derivation's declared sources are part of its supplied lineage."""
    if not isinstance(derivation, Derivation):
        raise TypeError("derivation must be a Derivation")
    supplied = set(artifact_ids)
    if any(not isinstance(value, str) or not value for value in artifact_ids):
        raise ValueError("artifact_ids must contain non-empty strings")
    if not set(derivation.source_ids).issubset(supplied):
        raise ValueError("derivation references sources outside supplied lineage")
    return derivation
