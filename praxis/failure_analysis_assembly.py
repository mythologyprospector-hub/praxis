"""Bounded assembly for failure and harm analysis."""

from __future__ import annotations

from collections.abc import Iterable

from praxis.failure import FailureMode
from praxis.failure_analysis import FailureAnalysis
from praxis.failure_request import FailureAnalysisRequest


def assemble_failure_analysis(
    request: FailureAnalysisRequest,
    analysis: FailureAnalysis,
    *,
    failure_modes: Iterable[FailureMode] = (),
) -> FailureAnalysis:
    """Validate failure-analysis findings against their explicit request and modes."""
    if not isinstance(analysis, FailureAnalysis):
        raise TypeError("analysis must be a FailureAnalysis")
    if analysis.id == request.id:
        raise ValueError("analysis identity must differ from request identity")
    if analysis.request_id != request.id:
        raise ValueError("analysis belongs to a different request")
    if analysis.problem_id != request.problem_id:
        raise ValueError("analysis belongs to a different problem")
    if not analysis.failure_mode_ids:
        raise ValueError("analysis must contain at least one failure mode")

    supplied = tuple(failure_modes)
    supplied_by_id = {}
    for mode in supplied:
        if not isinstance(mode, FailureMode):
            raise TypeError("failure_modes must contain FailureMode objects")
        if mode.problem_id != request.problem_id:
            raise ValueError("failure mode belongs to a different problem")
        if not set(mode.intervention_ids).issubset(request.intervention_ids):
            raise ValueError("failure mode references interventions outside the request")
        supplied_by_id[mode.id] = mode

    if not set(analysis.failure_mode_ids).issubset(supplied_by_id):
        raise ValueError("analysis references failure modes outside supplied findings")

    return analysis
