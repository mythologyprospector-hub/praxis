# Praxis Working Context

This file is the durable working memory for Praxis.

Its purpose is to let the steward reconstruct the current project state from the repository without relying on conversational context.

## Rules

- GitHub is the source of durable project context.
- Conversation is temporary working space.
- Record decisions, discoveries, unresolved questions, rejected directions, and current hypotheses here when they materially affect future work.
- Do not use this file as a dumping ground.
- Prefer concise, dated entries with links to the durable artifact that contains the detail.
- Never silently rewrite history. Correct or supersede prior entries explicitly.
- Context is evidence about project state, not authority over reality.
- Repository artifacts, tests, and external evidence remain the authoritative sources for their respective claims.

## Current state

**2026-10-03 — Phase 5 observed-result boundary implemented**

The first Phase 5 domain boundary now exists in `praxis/result.py`, with tests in `tests/test_result.py`. `Result` records what was observed during a bounded test, including summary, observations, provenance, uncertainty, and optional deviations. It remains distinct from the Test plan and is not automatically promoted into the evidence state.

Local verification of this latest commit is pending.

**2026-10-03 — Phase 4 bounded-test boundary implemented**

The first Phase 4 domain boundary now exists in `praxis/test.py`, with tests in `tests/test_test.py`. `Test` represents a bounded plan for learning about a candidate intervention: objective, expected observations, safety constraints, reversibility, decision criteria, and optional intervention references. It remains explicitly distinct from an observed result.

Local verification of this latest commit is pending.

**2026-10-03 — Phase 3 failure-mode boundary implemented**

The first Phase 3 domain boundary now exists in `praxis/failure.py`, with tests in `tests/test_failure.py`. `FailureMode` represents a concrete way a candidate intervention could fail or cause harm, with severity and likelihood descriptors and optional intervention references. It remains explicitly distinct from evidence, interventions, and observed results.

Commit: `14c7a9357468f8b8478b7d3c6855d0581766ebb7`.

Local verification of this latest commit is pending.

**2026-10-03 — Phase 2 intervention boundary implemented**

The first Phase 2 domain boundary now exists in `praxis/intervention.py`, with tests in `tests/test_intervention.py`. `Intervention` represents a proposed change and intended outcome for a defined problem, with optional hypothesis references. It remains explicitly distinct from evidence and results.

Local pytest verification reports 23 passing tests on commit `7910b70d08dd4279a37dd5b532b839a2db88e205`.

**2026-10-02 — Phase 1 evaluation boundary implemented**

The Phase 1 substrate includes `HypothesisEvaluation` in `praxis/evaluation.py`, with tests in `tests/test_evaluation.py`. It records an inference, uncertainty, and explicit evidence references while remaining distinct from both `EvidenceItem` and `Hypothesis`.

Local pytest verification reports 19 passing tests on commit `0f7fb075a553cf9f419036f789b4952bf19cb504`.

**2026-10-03 — Phase 1 problem substrate started**

The first executable Praxis domain object now exists in `praxis/problem.py`, with tests in `tests/test_problem.py`. It represents the human-defined problem fields required by the Phase 1 success criterion and provides deterministic JSON serialization.

GitHub Actions has executed the new pytest suite; the test step completed successfully on commit `6a62320ecbf4875d313652ccd0492ce4769eec0b`.

`docs/INTEGRATION.md` establishes the initial boundary with Organs: Praxis owns domain semantics; Organs owns runtime discovery, transport, and shared runtime mechanisms. No Organs dependency is introduced into the Phase 1 domain substrate yet.

**2026-10-02 — Foundation established**

Praxis was created as a public repository.

Initial durable artifacts:

- `CANON.md` — governing principles and human-agency constraints.
- `docs/ARCHITECTURE.md` — initial architectural hypothesis and boundaries.
- `docs/ROADMAP.md` — staged development path.
- `docs/DECISIONS.md` — initial decisions.
- `README.md` — project orientation.

The repository is intentionally being built from the domain substrate outward rather than beginning with runtime machinery.

## Core conception

Praxis is a human-centered solution-discovery engine.

Its intended movement is:

```
defined problem
→ structured problem
→ evidence state
→ candidate interventions
→ failure / harm analysis
→ bounded test
→ human decision
→ observed result
→ learned evidence
```

## System relationship

The current conceptual relationship is:

- Episteme — understand.
- Renaissance — connect.
- Praxis — act through human-directed problem solving.
- Organs — shared runtime infrastructure through explicit contracts.

These are working boundaries. Integration must be justified by an actual workflow and must preserve domain ownership and provenance.

## Open questions

No unresolved architectural question should be silently answered here. Record it when it becomes concrete enough to investigate.

## Active hypotheses

The Phase 1 `Problem` representation is intentionally small and domain-local. Future workflow objects should be added only when the next stage of the roadmap establishes a concrete need.

## Rejected / prohibited directions

See `CANON.md`. In particular, Praxis must not drift toward surveillance, coercive optimization, population control, social-credit machinery, autonomous authority over people, or hidden objectives.

## Steward note

Before undertaking substantial work, read this file and the governing project artifacts. Then inspect the repository itself.

The objective is not to remember everything.

The objective is to remember **only what future work needs**.
