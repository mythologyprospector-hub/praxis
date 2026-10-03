from __future__ import annotations

import pytest

from praxis.context import ReasoningContext
from praxis.derivation import Derivation
from praxis.evidence import EvidenceItem, EvidenceState
from praxis.failure import FailureMode
from praxis.failure_analysis import FailureAnalysis
from praxis.failure_analysis_provider import FailureAnalysisOutput, analyze_failures
from praxis.failure_request import FailureAnalysisRequest
from praxis.gap import EvidenceGap
from praxis.hypothesis import Hypothesis
from praxis.intervention import Intervention
from praxis.model import Model
from praxis.problem import Problem


def _context() -> ReasoningContext:
    problem = Problem(id="p-1", title="Problem", goal="Learn.")
    evidence = EvidenceState(
        problem_id="p-1",
        items=(EvidenceItem(id="e-1", statement="s", provenance="p", uncertainty="u"),),
    )
    gap = EvidenceGap(
        id="g-1", problem_id="p-1", description="unknown", decision_relevance="relevant"
    )
    return ReasoningContext(problem=problem, evidence=evidence, gaps=(gap,))


class _Analyzer:
    def analyze(self, request, context, interventions, hypotheses=(), models=()):
        mode = FailureMode(
            id="f-1",
            problem_id="p-1",
            description="The intervention could fail.",
            severity="bounded",
            likelihood="uncertain",
            intervention_ids=("i-1",),
        )
        return FailureAnalysisOutput(
            analysis=FailureAnalysis(
                id="fa-1",
                request_id=request.id,
                problem_id="p-1",
                failure_mode_ids=("f-1",),
                uncertainty="u",
            ),
            failure_modes=(mode,),
            derivations=(
                Derivation(
                    id="d-1",
                    artifact_id="f-1",
                    source_ids=("i-1", "h-1", "m-1", "g-1", "e-1"),
                    method="bounded attack",
                    uncertainty="u",
                ),
            ),
        )


def _inputs():
    intervention = Intervention(
        id="i-1", problem_id="p-1", proposal="change", intended_outcome="learn"
    )
    hypothesis = Hypothesis(
        id="h-1", problem_id="p-1", statement="h", rationale="r"
    )
    model = Model(
        id="m-1", problem_id="p-1", purpose="compare", method="bounded"
    )
    request = FailureAnalysisRequest(
        id="req-1",
        problem_id="p-1",
        intervention_ids=("i-1",),
        hypothesis_ids=("h-1",),
        model_ids=("m-1",),
    )
    return request, intervention, hypothesis, model


def test_failure_analysis_provider_preserves_explicit_lineage():
    request, intervention, hypothesis, model = _inputs()
    result = analyze_failures(
        request,
        _context(),
        (intervention,),
        _Analyzer(),
        hypotheses=(hypothesis,),
        models=(model,),
    )
    assert result.analysis.id == "fa-1"
    assert result.failure_modes[0].id == "f-1"
    assert result.derivations[0].artifact_id == "f-1"


def test_failure_analysis_provider_rejects_missing_requested_hypothesis():
    request, intervention, _, model = _inputs()
    with pytest.raises(ValueError, match="hypotheses"):
        analyze_failures(
            request,
            _context(),
            (intervention,),
            _Analyzer(),
            models=(model,),
        )


def test_failure_analysis_provider_rejects_derivation_outside_grounded_context():
    request, intervention, hypothesis, model = _inputs()

    class BadAnalyzer(_Analyzer):
        def analyze(self, request, context, interventions, hypotheses=(), models=()):
            output = super().analyze(request, context, interventions, hypotheses, models)
            bad = Derivation(
                id="d-1",
                artifact_id="f-1",
                source_ids=("not-supplied",),
                method="bad",
                uncertainty="u",
            )
            return FailureAnalysisOutput(
                analysis=output.analysis,
                failure_modes=output.failure_modes,
                derivations=(bad,),
            )

    with pytest.raises(ValueError, match="outside supplied lineage"):
        analyze_failures(
            request,
            _context(),
            (intervention,),
            BadAnalyzer(),
            hypotheses=(hypothesis,),
            models=(model,),
        )
