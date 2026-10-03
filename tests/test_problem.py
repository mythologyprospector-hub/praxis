import json

import pytest

from praxis.problem import Problem


def test_problem_preserves_all_problem_definition_fields():
    problem = Problem(
        id="water-001",
        title="Improve local water reliability",
        goal="Increase reliable access to safe water.",
        constraints=("limited budget", "existing infrastructure"),
        values=("reliability", "affordability"),
        non_negotiables=("do not reduce safety",),
        stakeholders=("residents", "operators"),
        known_risks=("service disruption",),
        acceptable_tradeoffs=("slower rollout",),
        unacceptable_tradeoffs=("unsafe water",),
    )

    data = problem.to_dict()

    assert data["goal"] == "Increase reliable access to safe water."
    assert data["constraints"] == ("limited budget", "existing infrastructure")
    assert data["non_negotiables"] == ("do not reduce safety",)
    assert data["unacceptable_tradeoffs"] == ("unsafe water",)


def test_problem_serialization_is_deterministic_and_json_compatible():
    problem = Problem(
        id="p1",
        title="Example",
        goal="Learn",
        constraints=("a", "b"),
    )

    first = problem.to_json()
    second = problem.to_json()

    assert first == second
    assert json.loads(first)["constraints"] == ["a", "b"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", ""),
        ("title", " "),
        ("goal", ""),
    ],
)
def test_problem_requires_core_fields(field, value):
    values = {"id": "p1", "title": "Example", "goal": "Learn"}
    values[field] = value

    with pytest.raises(ValueError):
        Problem(**values)


def test_problem_rejects_empty_items():
    with pytest.raises(ValueError, match="constraints"):
        Problem(id="p1", title="Example", goal="Learn", constraints=("ok", ""))


def test_problem_requires_explicit_tuple_collections():
    with pytest.raises(TypeError, match="constraints"):
        Problem(id="p1", title="Example", goal="Learn", constraints=["not", "a", "tuple"])
