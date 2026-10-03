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

**Status:** intervention, candidate-set, and bounded candidate-generation machinery are established and verified by tests.

The current `Intervention` object records:

- the defined problem it belongs to;
- the proposed change;
- the intended outcome;
- optional hypothesis references.

It deliberately does not claim that the intervention works.

`CandidateSet` now provides a minimal grouping boundary for generated hypotheses and/or interventions. It does not rank, select, authorize, or execute candidates.

## Candidate-generation request boundary

**Status:** first bounded candidate-generation provider boundary established and tested; candidate generation preserves explicit derivation lineage.

The current `CandidateRequest` makes generation inputs explicit: problem identity, evidence and gap references, requested candidate types, and constraints. It deliberately does not generate, rank, select, authorize, or execute candidates.

### Hypothesis evaluation provider boundary

**Status:** first bounded hypothesis-evaluation provider boundary established and tested.

`evaluate_hypothesis(...)` validates the evaluation request, grounded reasoning context, matching hypothesis, provider output, evaluation lineage, and explicit derivation trace. It does not modify evidence or make decisions.

### Failure-analysis request boundary

**Status:** first bounded failure-analysis request and provider boundaries established and tested; provider execution remains an external reasoning capability.

`FailureAnalysisRequest` makes the attack inputs explicit: problem identity, intervention references, optional hypothesis/model references, focus areas, and constraints. It deliberately does not create findings, rank candidates, assign risk judgments, authorize action, or execute anything.

### Failure-analysis result boundary

**Status:** bounded failure-analysis result, assembly, and provider boundaries are established and tested; the provider remains an external reasoning capability.

`FailureAnalysis` links a request to explicit failure-mode identities and preserves uncertainty. Its assembly boundary now validates the supplied `FailureMode` objects, their problem identity, and their intervention references against the originating request. It does not authorize, rank, execute, or convert findings into evidence automatically.

### Derivation boundary

**Status:** first traceability boundary established and tested.

`Derivation` records artifact lineage, source identities, method, and uncertainty without turning lineage into evidence, a decision, or authorization.

## Model boundary

**Status:** bounded model boundary, assembly, and provider boundary are established and tested; model execution remains an external capability.

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

**Status:** bounded test boundary, assembly, and provider boundary are established and tested; test execution remains an external capability.

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

**Status:** observed-result boundary, assembly, and bounded result-capture provider are established and tested; result-to-evidence admission is explicit and human-gated.

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

**Status:** explicit Result-to-Evidence admission boundary is established and tested; grounded reasoning context includes evidence and explicit gaps; the remaining gap is composition of the bounded stages into a reusable workflow.

A result-derived EvidenceItem must be created explicitly and retains the source Result identifier, provenance, and uncertainty. A Result is never silently promoted into evidence merely because it exists.

`Result → EvidenceItem` derivation is now an explicit, tested boundary: a result-derived evidence item must carry the exact source Result identifier. `EvidenceAdmission` is the human-gating boundary: it records who authorized admission, the rationale, and the exact problem/evidence identities. `EvidenceState.admit(...)` requires that authorization and refuses cross-problem or mismatched-evidence admission. `admit_result_as_evidence(...)` now composes these boundaries into one explicit closed-loop transition without granting the transition any autonomous authorization.

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

### Evidence-admission request boundary

**Status:** first explicit request boundary established and tested.

`EvidenceAdmissionRequest` separates asking for admission of result-derived evidence from the actual human authorization recorded by `EvidenceAdmission`. A request never silently authorizes admission.

### Evaluation request boundary

**Status:** first bounded evaluation request boundary established and tested.

`EvaluationRequest` makes the hypothesis, evidence, gaps, and constraints entering evaluation explicit. Evaluation machinery remains distinct from the evidence state and from the resulting `HypothesisEvaluation`.

### Model request boundary

**Status:** first bounded model-request boundary established and tested.

`ModelRequest` makes the purpose and supporting inputs to model construction explicit. Model construction/execution machinery remains unimplemented, and model outputs do not become evidence automatically.

### Decision request boundary

**Status:** first bounded decision-request boundary established and tested.

`DecisionRequest` separates a request for decision formulation from the resulting human `Decision`. The request may carry candidate, test, result, evidence, and constraint references, but it has no decision or execution authority.

### Result-to-evidence assembly

**Status:** first bounded result-to-evidence assembly implemented and tested.

`assemble_result_evidence(...)` validates that an `EvidenceItem` explicitly references the supplied `Result`, preserving provenance lineage before human admission.

### Candidate assembly machinery

**Status:** first bounded candidate-stage assembly implemented and tested.

Candidate artifacts can now be validated and grouped under an explicit `CandidateRequest`. Actual candidate-generation reasoning remains a separate future capability.

### Decision-request lineage assembly

**Status:** first bounded decision-request artifact lineage validation implemented and tested.

`validate_decision_lineage(...)` verifies that the candidate sets, tests, results, and evidence explicitly referenced by a `DecisionRequest` are supplied and belong to the request's problem where applicable. It does not make, rank, authorize, or execute the decision.


### Bounded workflow composition

**Status:** the bounded pre-decision and post-decision stages are now composed and CI-verified.

The reusable workflow coordinator sequences the established provider boundaries through the two explicit human gates:

`Frame → Ground → Expose gaps → Generate → Evaluate → Attack → Model → Design test → Human Decision → Observe → ResultScope → Human Evidence Admission → EvidenceState`

The composition validates stage lineage and delegates result capture and evidence admission to supplied/existing boundaries. It does not interpret the human decision, execute interventions, rank or select candidates, or grant evidence authority implicitly. Runtime integration and autonomous consequential behavior remain out of scope.
