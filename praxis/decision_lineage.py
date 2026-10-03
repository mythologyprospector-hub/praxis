"""Bounded lineage validation for human decision requests."""

from __future__ import annotations

from collections.abc import Iterable

from praxis.candidate import CandidateSet
from praxis.decision_request import DecisionRequest
from praxis.evidence import EvidenceItem
from praxis.result import Result
from praxis.test import Test


def validate_decision_lineage(
    request: DecisionRequest,
    *,
    candidate_sets: Iterable[CandidateSet] = (),
    tests: Iterable[Test] = (),
    results: Iterable[Result] = (),
    evidence_items: Iterable[EvidenceItem] = (),
) -> None:
    """Validate that a decision request's referenced artifacts are supplied."""
    supplied_candidates = tuple(candidate_sets)
    supplied_tests = tuple(tests)
    supplied_results = tuple(results)
    supplied_evidence = tuple(evidence_items)

    for candidate_set in supplied_candidates:
        if not isinstance(candidate_set, CandidateSet):
            raise TypeError("candidate_sets must contain CandidateSet objects")
        if candidate_set.problem_id != request.problem_id:
            raise ValueError("candidate set belongs to a different problem")
    for test in supplied_tests:
        if not isinstance(test, Test):
            raise TypeError("tests must contain Test objects")
        if test.problem_id != request.problem_id:
            raise ValueError("test belongs to a different problem")
    supplied_tests_by_id = {item.id: item for item in supplied_tests}
    for result in supplied_results:
        if not isinstance(result, Result):
            raise TypeError("results must contain Result objects")
        if result.test_id not in supplied_tests_by_id:
            raise ValueError("result references a test outside supplied lineage")
    for item in supplied_evidence:
        if not isinstance(item, EvidenceItem):
            raise TypeError("evidence_items must contain EvidenceItem objects")

    if not set(request.candidate_ids).issubset({item.id for item in supplied_candidates}):
        raise ValueError("decision request references candidates outside supplied lineage")
    if not set(request.test_ids).issubset({item.id for item in supplied_tests}):
        raise ValueError("decision request references tests outside supplied lineage")
    if not set(request.result_ids).issubset({item.id for item in supplied_results}):
        raise ValueError("decision request references results outside supplied lineage")
    if not set(request.evidence_ids).issubset({item.id for item in supplied_evidence}):
        raise ValueError("decision request references evidence outside supplied lineage")
    request_test_ids = set(request.test_ids)
    requested_result_ids = set(request.result_ids)
    for result in supplied_results:
        if result.id in requested_result_ids and result.test_id not in request_test_ids:
            raise ValueError("requested result references a test outside the decision request")
    for item in supplied_evidence:
        if item.id in set(request.evidence_ids) and item.source_result_id is not None and item.source_result_id not in requested_result_ids:
            raise ValueError("requested evidence references a result outside the decision request")
