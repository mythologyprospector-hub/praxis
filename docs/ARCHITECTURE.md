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

### EvidenceItem

A single evidence-bearing statement. It must retain provenance and an explicit description of uncertainty.

### EvidenceState

What is currently known for the problem, represented as explicit EvidenceItems.

### Hypothesis

A proposed explanation or mechanism that could affect the problem. It is explicitly separate from EvidenceItem and does not become evidence merely by being represented.

### HypothesisEvaluation

An assessment of a hypothesis against explicitly referenced evidence. It records an inference and its uncertainty without becoming an EvidenceItem itself. Its evidence references identify inputs to the assessment; they do not transfer evidentiary status to the inference.

### Intervention

A proposed change intended to alter an outcome for a defined problem. It may identify the hypotheses it is intended to act upon, but remains a proposal rather than evidence or a result.

### FailureMode

A concrete way a candidate intervention could fail or cause harm. It is an analysis object, not evidence, an intervention, or an observed result. A FailureMode may reference the intervention(s) it challenges while keeping the proposed change distinct from the analysis of how it could go wrong.

### Test

A bounded method for learning whether a candidate intervention behaves as expected.

### Result

What happened when a test was actually performed.

### Decision

A human decision about whether and how to proceed.

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
