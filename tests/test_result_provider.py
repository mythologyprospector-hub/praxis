"""Tests for the bounded observed-result provider boundary."""

from dataclasses import replace

import pytest

from praxis.result import Result
from praxis.result_provider import ResultOutput, ResultRecorder, record_result
from praxis.result_request import ResultRequest
from praxis.test import Test


def _inputs():
    request = ResultRequest(
        id="result-request",
        problem_id="problem",
        test_id="test",
        intervention_ids=("intervention",),
    )
    test = Test(
        "test",
        "problem",
        "objective",
        ("observation",),
        ("safe",),
        "reversible",
        ("criterion",),
        ("intervention",),
    )
    return request, test


class StubRecorder:
    def record(self, request, test):
        return ResultOutput(
            Result(
                "result",
                test.id,
                "observed",
                ("observation",),
                "test record",
                "known uncertainty",
            )
        )


def test_record_result_returns_observed_result():
    request, test = _inputs()
    output = record_result(request, test, StubRecorder())
    assert output.result.id == "result"
    assert output.result.test_id == test.id


def test_record_result_rejects_wrong_output_type():
    class BadRecorder:
        def record(self, *args):
            return object()

    request, test = _inputs()
    with pytest.raises(TypeError, match="ResultOutput"):
        record_result(request, test, BadRecorder())


def test_record_result_rejects_result_for_different_test():
    class BadRecorder(StubRecorder):
        def record(self, request, test):
            return ResultOutput(replace(super().record(request, test).result, test_id="other"))

    request, test = _inputs()
    with pytest.raises(ValueError, match="different test"):
        record_result(request, test, BadRecorder())


def test_record_result_rejects_request_intervention_missing_from_test():
    request, test = _inputs()
    request = replace(request, intervention_ids=("missing",))
    with pytest.raises(ValueError, match="does not reference"):
        record_result(request, test, StubRecorder())


def test_result_recorder_protocol_is_runtime_checkable():
    assert isinstance(StubRecorder(), ResultRecorder)
