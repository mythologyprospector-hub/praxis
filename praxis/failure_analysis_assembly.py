"""Bounded assembly for failure and harm analysis."""

from __future__ import annotations

from praxis.failure_analysis import FailureAnalysis
from praxis.failure_request import FailureAnalysisRequest


def assemble_failure_analysis(
    request: FailureAnalysisRequest,
    analysis: FailureAnalysis,
) -> FailureAnalysis:
    """Validate failure-analysis findings against their explicit request."""
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
    return analysis
