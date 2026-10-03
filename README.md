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

Phase 0 is established. Phase 1 now has an inspectable problem/evidence substrate and an explicit evaluation boundary, all covered by tests.

The Phase 1 epistemic boundary distinguishes:

- evidence-bearing statements, with provenance and uncertainty;
- hypotheses, which are proposed explanations or mechanisms;
- evaluations, which record inferences about hypotheses, their uncertainty, and the evidence considered.

The implementation currently has deterministic serialization and a locally verified pytest suite.

## Integration

See [docs/INTEGRATION.md](docs/INTEGRATION.md) for the current Organs boundary. Runtime integration is deliberately downstream of stable domain semantics.

## Principles

See [CANON.md](CANON.md).
