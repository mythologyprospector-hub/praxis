from __future__ import annotations
import json
import pytest
from praxis.derivation import Derivation

def test_derivation_records_sources_without_becoming_evidence():
    d=Derivation(id="d-1",artifact_id="analysis-1",source_ids=("attack-1","model-1"),method="bounded review",uncertainty="partial")
    assert d.to_dict()["source_ids"]==("attack-1","model-1")
    assert "evidence" not in d.to_dict()
    assert "decision" not in d.to_dict()

def test_derivation_allows_no_sources_for_originating_artifacts():
    assert Derivation(id="d-1",artifact_id="candidate-1").source_ids==()

def test_derivation_requires_unique_sources():
    with pytest.raises(ValueError):
        Derivation(id="d-1",artifact_id="a-1",source_ids=("x","x"))

def test_derivation_requires_tuple_sources():
    with pytest.raises(TypeError):
        Derivation(id="d-1",artifact_id="a-1",source_ids=["x"]) # type: ignore[arg-type]

def test_derivation_serialization_is_deterministic():
    d=Derivation(id="d-1",artifact_id="a-1",source_ids=("x",))
    assert d.to_json()==json.dumps(d.to_dict(),sort_keys=True,separators=(",",":"))
