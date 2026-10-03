from __future__ import annotations

import pytest

from praxis.candidate_generation import CandidateGenerationOutput, assemble_candidate_set, generate_candidates
from praxis.context import ReasoningContext
from praxis.evidence import EvidenceItem, EvidenceState
from praxis.gap import EvidenceGap
from praxis.problem import Problem
from praxis.candidate_request import CandidateRequest
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention


def test_assembly_groups_generated_candidates_under_request():
    request = CandidateRequest(id="req-1", problem_id="p-1")
    hypothesis = Hypothesis(
        id="h-1", problem_id="p-1", statement="h", rationale="r"
    )
    intervention = Intervention(
        id="i-1", problem_id="p-1", description="d", intended_outcome="o"
    )

    result = assemble_candidate_set(
        request, hypotheses=(hypothesis,), interventions=(intervention,)
    )

    assert result.id == "req-1:candidates"
    assert result.problem_id == "p-1"
    assert result.hypothesis_ids == ("h-1",)
    assert result.intervention_ids == ("i-1",)


def test_assembly_rejects_candidates_from_another_problem():
    request = CandidateRequest(id="req-1", problem_id="p-1")
    hypothesis = Hypothesis(
        id="h-1", problem_id="p-2", statement="h", rationale="r"
    )

    with pytest.raises(ValueError):
        assemble_candidate_set(request, hypotheses=(hypothesis,))


def test_assembly_respects_requested_types():
    request = CandidateRequest(
        id="req-1", problem_id="p-1", requested_types=("hypothesis",)
    )
    intervention = Intervention(
        id="i-1", problem_id="p-1", description="d", intended_outcome="o"
    )

    with pytest.raises(ValueError):
        assemble_candidate_set(request, interventions=(intervention,))


def test_assembly_rejects_wrong_artifact_types():
    request = CandidateRequest(id="req-1", problem_id="p-1")

    with pytest.raises(TypeError):
        assemble_candidate_set(request, hypotheses=("not-a-hypothesis",))  # type: ignore[arg-type]


def test_assembly_requires_output():
    request = CandidateRequest(id="req-1", problem_id="p-1")

    with pytest.raises(ValueError):
        assemble_candidate_set(request)


def test_assembly_rejects_id_collision_across_candidate_types():
    request = CandidateRequest(id="req-1", problem_id="p-1")
    hypothesis = Hypothesis(
        id="same-id", problem_id="p-1", statement="h", rationale="r"
    )
    intervention = Intervention(
        id="same-id", problem_id="p-1", description="d", intended_outcome="o"
    )

    with pytest.raises(ValueError, match="unique"):
        assemble_candidate_set(
            request, hypotheses=(hypothesis,), interventions=(intervention,)
        )


def test_assembly_rejects_wrong_intervention_type():
    request = CandidateRequest(id="req-1", problem_id="p-1")
    with pytest.raises(TypeError, match="Intervention"):
        assemble_candidate_set(request, interventions=(object(),))  # type: ignore[arg-type]


def test_assembly_rejects_wrong_request_type():
    with pytest.raises(TypeError, match="CandidateRequest"):
        assemble_candidate_set(object())  # type: ignore[arg-type]


class _Generator:
    def generate(self, request, context):
        from praxis.derivation import Derivation
        hypothesis = Hypothesis(id="h-1", problem_id=request.problem_id, statement="h", rationale="r")
        intervention = Intervention(id="i-1", problem_id=request.problem_id, description="d", intended_outcome="o")
        return CandidateGenerationOutput(hypotheses=(hypothesis,), interventions=(intervention,), derivations=(
            Derivation(id="d-h", artifact_id="h-1", source_ids=("g-1",), method="test", uncertainty="u"),
            Derivation(id="d-i", artifact_id="i-1", source_ids=("g-1",), method="test", uncertainty="u"),
        ))


def _context():
    problem = Problem(id="p-1", title="Problem", goal="Learn.")
    evidence = EvidenceState(
        problem_id="p-1",
        items=(EvidenceItem(id="e-1", statement="s", provenance="p", uncertainty="u"),),
    )
    gap = EvidenceGap(
        id="g-1", problem_id="p-1", description="unknown", decision_relevance="relevant"
    )
    return ReasoningContext(problem=problem, evidence=evidence, gaps=(gap,))


def test_generation_uses_explicit_context_and_provider_boundary():
    request = CandidateRequest(
        id="req-1", problem_id="p-1", evidence_ids=("e-1",), gap_ids=("g-1",)
    )
    result = generate_candidates(request, _context(), _Generator())

    assert result.hypothesis_ids == ("h-1",)
    assert result.intervention_ids == ("i-1",)


def test_generation_requires_derivation_output():
    request = CandidateRequest(id="req-1", problem_id="p-1")
    class _BadGenerator:
        def generate(self, request, context):
            return ((), ())
    with pytest.raises(TypeError, match="CandidateGenerationOutput"):
        generate_candidates(request, _context(), _BadGenerator())


def test_generation_rejects_derivation_for_unknown_artifact():
    request = CandidateRequest(id="req-1", problem_id="p-1", gap_ids=("g-1",))
    from praxis.derivation import Derivation
    class _BadGenerator:
        def generate(self, request, context):
            return CandidateGenerationOutput(
                hypotheses=(Hypothesis(id="h-1", problem_id="p-1", statement="h", rationale="r"),),
                derivations=(Derivation(id="d-1", artifact_id="missing", source_ids=("g-1",), method="m", uncertainty="u"),),
            )
    with pytest.raises(ValueError, match="outside generated"):
        generate_candidates(request, _context(), _BadGenerator())


def test_generation_rejects_derivation_source_outside_lineage():
    request = CandidateRequest(id="req-1", problem_id="p-1", gap_ids=("g-1",))
    from praxis.derivation import Derivation
    class _BadGenerator:
        def generate(self, request, context):
            return CandidateGenerationOutput(
                hypotheses=(Hypothesis(id="h-1", problem_id="p-1", statement="h", rationale="r"),),
                derivations=(Derivation(id="d-1", artifact_id="h-1", source_ids=("missing",), method="m", uncertainty="u"),),
            )
    with pytest.raises(ValueError, match="outside supplied"):
        generate_candidates(request, _context(), _BadGenerator())


def test_generation_rejects_context_for_another_problem():
    request = CandidateRequest(id="req-1", problem_id="p-2")

    with pytest.raises(ValueError, match="different problem"):
        generate_candidates(request, _context(), _Generator())


def test_generation_rejects_evidence_outside_context():
    request = CandidateRequest(id="req-1", problem_id="p-1", evidence_ids=("missing",))

    with pytest.raises(ValueError, match="evidence outside"):
        generate_candidates(request, _context(), _Generator())


def test_generation_rejects_gaps_outside_context():
    request = CandidateRequest(id="req-1", problem_id="p-1", gap_ids=("missing",))

    with pytest.raises(ValueError, match="gaps outside"):
        generate_candidates(request, _context(), _Generator())


def test_generation_rejects_non_provider():
    request = CandidateRequest(id="req-1", problem_id="p-1")

    with pytest.raises(TypeError, match="CandidateGenerator"):
        generate_candidates(request, _context(), object())


def test_gap_directed_generator_creates_unranked_gap_candidates():
    from praxis.candidate_generation import GapDirectedCandidateGenerator

    request = CandidateRequest(
        id="req-1",
        problem_id="p-1",
        evidence_ids=("e-1",),
        gap_ids=("g-1",),
    )
    output = GapDirectedCandidateGenerator().generate(request, _context())
    hypotheses = output.hypotheses
    interventions = output.interventions

    assert len(hypotheses) == 1
    assert len(interventions) == 1
    assert len(output.derivations) == 2
    assert hypotheses[0].evidence_ids == ()
    assert interventions[0].hypothesis_ids == (hypotheses[0].id,)
    assert "not evidence" in hypotheses[0].rationale


def test_gap_directed_generator_respects_requested_candidate_types():
    from praxis.candidate_generation import GapDirectedCandidateGenerator

    request = CandidateRequest(
        id="req-1",
        problem_id="p-1",
        gap_ids=("g-1",),
        requested_types=("intervention",),
    )
    output = GapDirectedCandidateGenerator().generate(request, _context())
    hypotheses = output.hypotheses
    interventions = output.interventions

    assert hypotheses == ()
    assert len(interventions) == 1
    assert interventions[0].hypothesis_ids == ()


def test_gap_directed_generator_requires_requested_gap():
    from praxis.candidate_generation import GapDirectedCandidateGenerator

    request = CandidateRequest(id="req-1", problem_id="p-1")

    with pytest.raises(ValueError, match="at least one"):
        GapDirectedCandidateGenerator().generate(request, _context())


def test_gap_directed_generator_integrates_with_candidate_assembly():
    from praxis.candidate_generation import GapDirectedCandidateGenerator

    request = CandidateRequest(
        id="req-1",
        problem_id="p-1",
        gap_ids=("g-1",),
    )
    result = generate_candidates(
        request, _context(), GapDirectedCandidateGenerator()
    )

    assert result.hypothesis_ids == ("req-1:hypothesis:g-1",)
    assert result.intervention_ids == ("req-1:intervention:g-1",)
