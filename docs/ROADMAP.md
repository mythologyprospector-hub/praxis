# Praxis Roadmap

This is a research/build roadmap, not a promise of implementation.

## Phase 0 — Foundation

- establish canon;
- establish terminology;
- establish provenance requirements;
- establish human-gating requirements;
- establish minimal repository/test structure.

**Status:** foundation established.

## Phase 1 — Problem substrate

Create a minimal, inspectable representation for a defined problem.

**Status:** evidence-state boundary implemented and verified by tests.

The Phase 1 substrate now contains:

- `Problem` — the human-defined problem;
- `EvidenceItem` — an evidence-bearing statement with provenance and uncertainty;
- `EvidenceState` — evidence explicitly associated with a problem.

The remaining Phase 1 work is to establish the distinction between evidence and hypotheses/proposals before moving into candidate generation.

The current `Problem` object preserves:

- goal;
- constraints;
- values;
- non-negotiables;
- stakeholders;
- known risks;
- acceptable tradeoffs;
- unacceptable tradeoffs.

It also has deterministic serialization suitable for later transport or persistence.



## Phase 2 — Candidate generation

Represent hypotheses, mechanisms, and candidate interventions without conflating proposals with evidence.

## Phase 3 — Failure analysis

Represent counterexamples, failure modes, harms, unintended consequences, assumptions, and boundary conditions.

## Phase 4 — Test design

Represent bounded tests with explicit objectives, expected observations, safety constraints, reversibility, and decision criteria.

## Phase 5 — Result capture

Capture actual observations and preserve their provenance.

## Phase 6 — Closed loop

Connect results back into the problem's evidence state and, where appropriate, to Episteme.

## Phase 7 — Cross-domain reasoning

Investigate carefully bounded use of Renaissance outputs.

## Phase 8 — Real-world pilots

Only after the earlier substrate is stable should Praxis be considered for carefully bounded real-world problem-solving workflows.

Every phase requires explicit review before the next consequential capability is added.
