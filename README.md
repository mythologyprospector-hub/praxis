# Praxis

A human-centered solution-discovery engine for turning defined problems into testable, safe interventions.

Praxis is intended to help people move from **a problem worth solving** toward **better options for solving it** without turning people into objects of optimization.

## Role in the larger system

- **Episteme** — understand what is known, unknown, uncertain, contradictory, and testable.
- **Renaissance** — discover relationships, structures, and possibilities across domains.
- **Praxis** — work from a defined human problem toward candidate interventions, tests, and evidence.
- **Organs** — provide shared runtime infrastructure through explicit contracts when integration is justified.

Praxis does not replace human judgment. It exists to improve the quality of the options and evidence available to human decision-makers.

## Core loop

```
problem
  ↓
goal + constraints + values
  ↓
known evidence
  ↓
unknowns / uncertainties
  ↓
candidate mechanisms
  ↓
candidate interventions
  ↓
failure / harm / counterexample search
  ↓
models / simulations / calculations where justified
  ↓
smallest informative and safe test
  ↓
human decision
  ↓
real-world result
  ↓
evidence
  ↓
Episteme
```

The loop is intentionally incomplete until evidence returns from the world.

## Current status

Phase 0 is established. Phase 1 has begun with an inspectable `Problem` domain object, deterministic serialization, and CI-verified tests.

The next Phase 1 objective is to establish the evidence-state boundary: what Praxis may treat as known for a problem, how provenance and uncertainty are represented, and how that remains distinct from hypotheses and proposals.

## Integration

See [docs/INTEGRATION.md](docs/INTEGRATION.md) for the current Organs boundary. Runtime integration is deliberately downstream of stable domain semantics.

## Principles

See [CANON.md](CANON.md).
