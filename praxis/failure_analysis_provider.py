"""Bounded provider boundary for failure analysis."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from praxis.context import ReasoningContext
from praxis.derivation import Derivation
from praxis.derivation_assembly import assemble_derivation
from praxis.failure import FailureMode
from praxis.failure_analysis import FailureAnalysis
from praxis.failure_analysis_assembly import assemble_failure_analysis
from praxis.failure_request import FailureAnalysisRequest
from praxis.intervention import Intervention


@dataclass(frozen=True)
class FailureAnalysisOutput:
    analysis: FailureAnalysis
    failure_modes: tuple[FailureMode, ...]
    derivations: tuple[Derivation, ...]


@runtime_checkable
class FailureAnalyzer(Protocol):
    def analyze(
        self,
        request: FailureAnalysisRequest,
        context: ReasoningContext,
        interventions: tuple[Intervention, ...],
    ) -> FailureAnalysisOutput:
        ...


def analyze_failures(
    request: FailureAnalysisRequest,
    context: ReasoningContext,
    interventions: tuple[Intervention, ...],
    analyzer: FailureAnalyzer,
) -> FailureAnalysisOutput:
    if not isinstance(request, FailureAnalysisRequest):
        raise TypeError("request must be a FailureAnalysisRequest")
    if not isinstance(context, ReasoningContext):
        raise TypeError("context must be a ReasoningContext")
    if not isinstance(analyzer, FailureAnalyzer):
        raise TypeError("analyzer must implement FailureAnalyzer")
    if not isinstance(interventions, tuple) or any(not isinstance(x, Intervention) for x in interventions):
        raise TypeError("interventions must be a tuple of Intervention objects")
    if context.problem.id != request.problem_id:
        raise ValueError("context belongs to a different problem")
    if {x.id for x in interventions} != set(request.intervention_ids):
        raise ValueError("supplied interventions must exactly match the request")
    if any(x.problem_id != request.problem_id for x in interventions):
        raise ValueError("intervention belongs to a different problem")

    output = analyzer.analyze(request, context, interventions)
    if not isinstance(output, FailureAnalysisOutput):
        raise TypeError("analyzer must return FailureAnalysisOutput")
    assemble_failure_analysis(request, output.analysis, failure_modes=output.failure_modes)

    mode_ids = {x.id for x in output.failure_modes}
    if len(mode_ids) != len(output.failure_modes):
        raise ValueError("failure analysis output must contain unique failure modes")
    if len(output.derivations) != len(output.failure_modes):
        raise ValueError("each generated failure mode must have exactly one derivation")

    lineage_ids = tuple(request.intervention_ids) + tuple(request.gap_ids) + tuple(request.evidence_ids)
    for mode, derivation in zip(output.failure_modes, output.derivations):
        if derivation.artifact_id != mode.id:
            raise ValueError("failure-mode derivation must target its finding")
        assemble_derivation(derivation, lineage_ids)
    if {d.artifact_id for d in output.derivations} != mode_ids:
        raise ValueError("each generated failure mode must have exactly one derivation")
    return output
