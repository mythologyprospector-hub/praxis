from praxis.context import ReasoningContext
from praxis.derivation import Derivation
from praxis.evaluation import HypothesisEvaluation
from praxis.evaluation_provider import EvaluationOutput, evaluate_hypothesis


def _context():
    from praxis.evidence import EvidenceItem, EvidenceState
    from praxis.gap import EvidenceGap
    from praxis.problem import Problem

    problem = Problem(id="p-1", title="Problem", goal="Learn.")
    evidence = EvidenceState(
        problem_id="p-1",
        items=(EvidenceItem(id="e-1", statement="s", provenance="p", uncertainty="u"),),
    )
    gap = EvidenceGap(
        id="g-1",
        problem_id="p-1",
        description="unknown",
        decision_relevance="relevant",
    )
    return ReasoningContext(problem=problem, evidence=evidence, gaps=(gap,))


class _Evaluator:
    def evaluate(self, request, context, hypothesis):
        evaluation = HypothesisEvaluation(
            id="ev-1",
            hypothesis_id=hypothesis.id,
            inference="i",
            uncertainty="u",
            evidence_ids=request.evidence_ids,
        )
        return EvaluationOutput(
            evaluation=evaluation,
            derivation=Derivation(
                id="d-1",
                artifact_id="ev-1",
                source_ids=(hypothesis.id, "e-1", "g-1"),
                method="test evaluation",
                uncertainty="u",
            ),
        )


def test_evaluation_uses_explicit_provider_boundary():
    request = __import__("praxis.evaluation_request", fromlist=["EvaluationRequest"]).EvaluationRequest(
        id="req-1",
        problem_id="p-1",
        hypothesis_id="h-1",
        evidence_ids=("e-1",),
        gap_ids=("g-1",),
    )
    hypothesis = __import__("praxis.hypothesis", fromlist=["Hypothesis"]).Hypothesis(
        id="h-1", problem_id="p-1", statement="h", rationale="r"
    )

    result = evaluate_hypothesis(request, _context(), hypothesis, _Evaluator())

    assert result.evaluation.id == "ev-1"
    assert result.evaluation.evidence_ids == ("e-1",)
    assert result.derivation.artifact_id == "ev-1"


def test_evaluation_rejects_output_of_wrong_type():
    class _BadEvaluator:
        def evaluate(self, request, context, hypothesis):
            return object()

    request = __import__("praxis.evaluation_request", fromlist=["EvaluationRequest"]).EvaluationRequest(
        id="req-1", problem_id="p-1", hypothesis_id="h-1", evidence_ids=("e-1",)
    )
    hypothesis = __import__("praxis.hypothesis", fromlist=["Hypothesis"]).Hypothesis(
        id="h-1", problem_id="p-1", statement="h", rationale="r"
    )

    import pytest
    with pytest.raises(TypeError, match="EvaluationOutput"):
        evaluate_hypothesis(request, _context(), hypothesis, _BadEvaluator())


def test_evaluation_requires_derivation_to_target_evaluation():
    class _BadEvaluator:
        def evaluate(self, request, context, hypothesis):
            return EvaluationOutput(
                evaluation=HypothesisEvaluation(
                    id="ev-1", hypothesis_id="h-1",
                    inference="i", uncertainty="u", evidence_ids=("e-1",)
                ),
                derivation=Derivation(
                    id="d-1", artifact_id="h-1", source_ids=("h-1",),
                    method="m", uncertainty="u"
                ),
            )

    request = __import__("praxis.evaluation_request", fromlist=["EvaluationRequest"]).EvaluationRequest(
        id="req-1", problem_id="p-1", hypothesis_id="h-1", evidence_ids=("e-1",)
    )
    hypothesis = __import__("praxis.hypothesis", fromlist=["Hypothesis"]).Hypothesis(
        id="h-1", problem_id="p-1", statement="h", rationale="r"
    )

    import pytest
    with pytest.raises(ValueError, match="must target the evaluation"):
        evaluate_hypothesis(request, _context(), hypothesis, _BadEvaluator())


def test_evaluation_rejects_request_evidence_outside_context():
    request = __import__("praxis.evaluation_request", fromlist=["EvaluationRequest"]).EvaluationRequest(
        id="req-1", problem_id="p-1", hypothesis_id="h-1", evidence_ids=("missing",)
    )
    hypothesis = __import__("praxis.hypothesis", fromlist=["Hypothesis"]).Hypothesis(
        id="h-1", problem_id="p-1", statement="h", rationale="r"
    )

    import pytest
    with pytest.raises(ValueError, match="evidence outside"):
        evaluate_hypothesis(request, _context(), hypothesis, _Evaluator())
