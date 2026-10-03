# Praxis Architecture

## Status

Initial architectural hypothesis.

This document deliberately describes boundaries and invariants before implementation details.

## Primary transformation

Praxis is concerned with the transformation:

```
defined problem
    →
structured problem
    →
evidence state
    →
candidate interventions
    →
tested candidates
    →
observed results
```

Each transition should preserve provenance and uncertainty.

## Boundary objects

The first durable objects are:

### Problem

What someone is trying to solve.

A problem is not complete merely because it has a title. It should carry the goal, constraints, values, non-negotiables, stakeholders, risks, and tradeoffs that materially define the problem.

### ReasoningContext

An immutable snapshot pairing a defined `Problem` with matching grounded inputs: `EvidenceState` and zero or more uniquely identified `EvidenceGap` objects. It is an input boundary for reasoning machinery, not an inference or decision. It refuses cross-problem inputs and malformed or duplicate gap identities.

### EvidenceItem

A single evidence-bearing statement. It must retain provenance and an explicit description of uncertainty. A result-derived EvidenceItem records its source Result so the admission path remains inspectable.

### EvidenceState

What is currently known for the problem, represented as explicit EvidenceItems with unique identities. Adding an item requires a matching `EvidenceAdmission`, which records the authorization, rationale, problem, and evidence identity.

### EvidenceGap

A material unknown or unresolved uncertainty relevant to the problem. It is not evidence, an inference, or a hypothesis; it records what is missing and why that missing knowledge could matter to a decision.

### Hypothesis

A proposed explanation or mechanism that could affect the problem. It is explicitly separate from EvidenceItem and does not become evidence merely by being represented.

### HypothesisEvaluation

An assessment of a hypothesis against explicitly referenced evidence. It records an inference and its uncertainty without becoming an EvidenceItem itself. Its evidence references identify inputs to the assessment; they do not transfer evidentiary status to the inference.

### Intervention

A proposed change intended to alter an outcome for a defined problem. It may identify the hypotheses it is intended to act upon, but remains a proposal rather than evidence or a result.

### CandidateRequest

A bounded request for generating candidate hypotheses and/or interventions. It records the problem, explicit evidence and gap references, requested candidate types, and generation constraints. It is a request boundary only: it does not generate, rank, select, authorize, or execute candidates.

### CandidateSet

A bounded collection of candidate hypotheses and/or interventions considered together for a defined problem. It provides grouping without ranking, selecting, authorizing, or executing a candidate. Candidate identity within each collection is unique, and at least one candidate is required.

### FailureAnalysisRequest

A bounded request to examine candidate interventions for failure modes and harm. It records the problem, explicit intervention references, optional hypothesis and model references, focus areas, and constraints. It is a request boundary only: it does not create findings, assign severity or likelihood, rank interventions, authorize action, or execute anything.

### FailureAnalysis

A bounded record linking a `FailureAnalysisRequest` to identified `FailureMode` objects. It preserves uncertainty and remains an analysis artifact: it is not evidence, a decision, authorization, ranking, or execution instruction.

### Derivation

A bounded trace record describing how an artifact was produced from explicit source identities, method, and uncertainty. It records lineage without asserting evidentiary validity or authorizing a decision.

### Model

A bounded calculation or simulation used to explore a defined problem. It records purpose, method, inputs, assumptions, outputs, and uncertainty. A Model is an analysis artifact, not evidence, a decision, or an executed intervention.

### FailureMode

A concrete way a candidate intervention could fail or cause harm. It is an analysis object, not evidence, an intervention, or an observed result. A FailureMode may reference the intervention(s) it challenges while keeping the proposed change distinct from the analysis of how it could go wrong.

### Test

A bounded method for learning about a candidate intervention. A Test defines an objective, expected observations, safety constraints, reversibility, and decision criteria. It is a plan for learning, not an observed result.

### Result

What was observed when a bounded test was performed. A Result records the observed summary, observations, provenance, uncertainty, and any declared deviations from the test plan. It is distinct from the Test plan and from the evidence state until deliberately incorporated through a later workflow.

### Decision

A recorded human decision about whether and how to proceed within a defined problem. It records the decision, rationale, human decision reference, and optional subject identity. It does not execute the decision. Evidence admission remains a specialized epistemic gate recorded separately from the evidence itself.

## Proposed pipeline

1. **Frame** — establish the problem and its governing constraints.
2. **Ground** — gather and distinguish relevant evidence.
3. **Expose gaps** — identify unknowns and uncertainties that could change the decision.
4. **Generate** — produce candidate mechanisms and interventions.
5. **Evaluate** — assess hypotheses against explicit evidence while preserving the distinction between evidence and inference.
6. **Attack** — search for failure modes, counterexamples, harms, and unintended consequences, representing concrete failure paths separately from the interventions they challenge.
7. **Model** — use calculations, simulations, or other models when they can discriminate among candidates.
8. **Design test** — define the smallest informative and sufficiently safe test.
9. **Gate** — present the result and implications for human decision.
10. **Observe** — record what actually happened.
11. **Learn** — preserve the result as evidence and make it available to the knowledge loop.

## Important non-goals

The initial architecture does not assume that Praxis should:

- autonomously execute consequential actions;
- monitor populations;
- optimize society;
- make decisions on behalf of people;
- become a general-purpose agent;
- replace Episteme's epistemic substrate;
- replace Renaissance's cross-domain discovery role.

Those questions require explicit future decisions rather than accidental architectural drift.

## Integration

Integration with Episteme, Renaissance, or Organs should be introduced through explicit contracts.

No integration is justified merely because it is technically possible.

### DecisionScope

An explicit linkage between a recorded human `Decision` and the bounded test or intervention it governs. It clarifies decision scope without executing the decision or granting authority to the linkage itself.

### ResultScope

An explicit linkage between an observed `Result`, its bounded `Test`, and any interventions under test. It clarifies what was actually tested without turning the result into evidence or a decision.

### TestRequest

A bounded request to design a `Test` for explicit candidate interventions. It can carry hypotheses, failure modes, models, and constraints as inputs, but does not design, authorize, or execute the test.

### ResultRequest

A bounded request to capture observations from a completed `Test`. It identifies the test and optional expected observations/interventions but does not create evidence, make a decision, or execute anything.

### EvidenceAdmissionRequest

A bounded request to seek human authorization for admitting a result-derived `EvidenceItem`. It identifies the problem, source `Result`, proposed evidence identity, and rationale. It does not itself authorize admission.

### EvaluationRequest

A bounded request to evaluate a specific `Hypothesis` against explicit evidence, with optional gaps and constraints. It is a request boundary only; it does not itself produce an inference or change evidence.

### ModelRequest

A bounded request to construct a `Model` for a defined purpose. It makes relevant inputs, hypotheses, interventions, and constraints explicit without itself producing model outputs or decisions.

### DecisionRequest

A bounded request to formulate a decision for human consideration. It makes the decision subject and supporting candidates, tests, results, evidence, and constraints explicit. It does not itself decide, authorize, or execute anything.
