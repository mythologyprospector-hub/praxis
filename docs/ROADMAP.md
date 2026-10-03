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

**Status:** substrate established and verified by tests.

The Phase 1 substrate contains:

- `Problem` — the human-defined problem;
- `EvidenceItem` — an evidence-bearing statement with provenance and uncertainty;
- `EvidenceState` — evidence explicitly associated with a problem;
- `Hypothesis` — a proposed explanation or mechanism that may reference evidence without becoming evidence;
- `HypothesisEvaluation` — an inference about a hypothesis with explicit uncertainty and evidence references, kept distinct from evidence.

The evidence/hypothesis/evaluation distinctions are represented and tested.

`EvidenceGap` now provides the first explicit boundary for material unknowns that may affect later reasoning or testing. `ReasoningContext` now carries those gaps alongside the matching evidence state, preserving both known evidence and material unknowns at the reasoning input boundary.

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

Represent candidate mechanisms and interventions without conflating proposals with evidence.

**Status:** intervention and candidate-set boundaries established and verified by tests; candidate-generation machinery is not yet implemented.

The current `Intervention` object records:

- the defined problem it belongs to;
- the proposed change;
- the intended outcome;
- optional hypothesis references.

It deliberately does not claim that the intervention works.

`CandidateSet` now provides a minimal grouping boundary for generated hypotheses and/or interventions. It does not rank, select, authorize, or execute candidates.

## Candidate-generation request boundary

**Status:** first bounded candidate-generation request boundary established and tested; candidate-generation machinery is not yet implemented.

The current `CandidateRequest` makes generation inputs explicit: problem identity, evidence and gap references, requested candidate types, and constraints. It deliberately does not generate, rank, select, authorize, or execute candidates.

### Failure-analysis request boundary

**Status:** first bounded failure-analysis request boundary established and tested; failure-analysis machinery is not yet implemented.

`FailureAnalysisRequest` makes the attack inputs explicit: problem identity, intervention references, optional hypothesis/model references, focus areas, and constraints. It deliberately does not create findings, rank candidates, assign risk judgments, authorize action, or execute anything.

### Failure-analysis result boundary

**Status:** first bounded failure-analysis result boundary established and tested; broader failure-analysis machinery is not yet implemented.

`FailureAnalysis` links a request to explicit failure-mode identities and preserves uncertainty. It does not authorize, rank, execute, or convert findings into evidence automatically.

### Derivation boundary

**Status:** first traceability boundary established and tested.

`Derivation` records artifact lineage, source identities, method, and uncertainty without turning lineage into evidence, a decision, or authorization.

## Model boundary

**Status:** first bounded model boundary established and tested; model-execution machinery is not yet implemented.

The current `Model` object records a model's purpose, method, inputs, assumptions, outputs, and uncertainty. It deliberately does not execute a simulation, claim that outputs are true, or make decisions.

## Phase 3 — Failure analysis

Represent counterexamples, failure modes, harms, unintended consequences, assumptions, and boundary conditions.

**Status:** first failure-mode boundary established and tested; broader failure-analysis machinery is not yet implemented.

The current `FailureMode` object records:

- the defined problem it belongs to;
- a concrete description of how a candidate intervention could fail or cause harm;
- severity and likelihood descriptors;
- optional intervention references.

It is deliberately an analysis object rather than evidence or an observed result.

## Phase 4 — Test design

Represent bounded tests with explicit objectives, expected observations, safety constraints, reversibility, and decision criteria.

**Status:** first bounded-test boundary established and tested; test execution machinery is not yet implemented.

The current `Test` object records:

- the defined problem it belongs to;
- the learning objective;
- expected observations;
- safety constraints;
- a reversibility description;
- decision criteria;
- optional intervention references.

It is deliberately a plan for learning rather than an observed result.

## Phase 5 — Result capture

The current `Decision` boundary records a human decision, rationale, decision-maker reference, and optional subject identity. Recording a decision does not execute it.

Capture actual observations and preserve their provenance.

**Status:** first observed-result boundary established and tested; result-to-evidence workflow is not yet implemented.

The current `Result` object records:

- the test it belongs to;
- an observed summary;
- observations;
- provenance;
- uncertainty;
- optional deviations from the test plan.

It is deliberately distinct from the test plan and is not automatically promoted into the evidence state.

## Phase 6 — Closed loop

Connect results back into the problem's evidence state and, where appropriate, to Episteme.

**Status:** explicit Result-to-Evidence admission boundary established and tested; grounded reasoning context now includes both evidence and explicit gaps; broader closed-loop workflow is not yet implemented.

A result-derived EvidenceItem must be created explicitly and retains the source Result identifier, provenance, and uncertainty. A Result is never silently promoted into evidence merely because it exists.

`EvidenceAdmission` is the first human-gating boundary: it records who authorized admission, the rationale, and the exact problem/evidence identities. `EvidenceState.admit(...)` requires that authorization and refuses cross-problem or mismatched-evidence admission.

## Phase 7 — Cross-domain reasoning

Investigate carefully bounded use of Renaissance outputs.

## Phase 8 — Real-world pilots

Only after the earlier substrate is stable should Praxis be considered for carefully bounded real-world problem-solving workflows.

Every phase requires explicit review before the next consequential capability is added.

### Decision-scope boundary

**Status:** first explicit decision-scope boundary established and tested.

`DecisionScope` links a human `Decision` to a defined problem and at least one bounded test or intervention. It does not execute the decision or create autonomous authority.

### Result-scope boundary

**Status:** first explicit result-scope boundary established and tested.

`ResultScope` links an observed `Result` to its bounded test and optional intervention identities. It preserves experimental scope without promoting results to evidence or decisions.

### Test-design request boundary

**Status:** first bounded test-design request boundary established and tested.

`TestRequest` makes intervention and supporting analysis inputs explicit before test design. Test generation and execution machinery remain unimplemented.

### Result-capture request boundary

**Status:** first bounded result-capture request boundary established and tested.

`ResultRequest` makes the test and observation-capture inputs explicit before a `Result` is recorded. It does not promote observations to evidence or make decisions.
