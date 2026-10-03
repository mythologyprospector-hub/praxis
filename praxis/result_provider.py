"""Bounded provider boundary for observed result capture."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from praxis.result import Result
from praxis.result_assembly import assemble_result
from praxis.result_request import ResultRequest
from praxis.test import Test


@dataclass(frozen=True)
class ResultOutput:
    result: Result


@runtime_checkable
class ResultRecorder(Protocol):
    def record(self, request: ResultRequest, test: Test) -> ResultOutput:
        ...


def record_result(
    request: ResultRequest,
    test: Test,
    recorder: ResultRecorder,
) -> ResultOutput:
    if not isinstance(request, ResultRequest):
        raise TypeError("request must be a ResultRequest")
    if not isinstance(test, Test):
        raise TypeError("test must be a Test")
    if not isinstance(recorder, ResultRecorder):
        raise TypeError("recorder must implement ResultRecorder")
    if test.id != request.test_id:
        raise ValueError("test does not match result request")
    if test.problem_id != request.problem_id:
        raise ValueError("test belongs to a different problem")
    if request.intervention_ids and not set(request.intervention_ids).issubset(test.intervention_ids):
        raise ValueError("test does not reference all requested interventions")
    output = recorder.record(request, test)
    if not isinstance(output, ResultOutput):
        raise TypeError("recorder must return ResultOutput")
    assemble_result(request, output.result, test)
    return output
