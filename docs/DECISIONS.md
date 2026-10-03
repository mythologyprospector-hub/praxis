# Praxis Decisions

## Initial decisions

### 2026-10-02 — Human agency is a system constraint

Praxis is a tool for helping humans solve chosen problems, not an authority that chooses human ends.

### 2026-10-02 — Consequential action is separated from proposal

Generating an intervention and authorizing or executing that intervention are separate stages.

### 2026-10-02 — Failure analysis is first-class

Praxis must search for ways an intervention could fail or cause harm rather than optimizing only for apparent success.

### 2026-10-02 — Build the substrate before the machinery

The initial implementation should establish inspectable representations, provenance, tests, and boundaries before adding autonomous or consequential behavior.

### 2026-10-03 — Evidence and hypothesis remain separate

A hypothesis is represented as a proposal with explicit rationale and problem association. It is not an evidence object and does not gain evidentiary status merely by being generated or stored.

### 2026-10-03 — Evaluation remains distinct from evidence

A hypothesis evaluation records an inference, uncertainty, and explicit references to the evidence considered. Recording an inference does not make it evidence, and referencing evidence does not change the epistemic status of the evaluation.

### 2026-10-03 — Intervention remains a proposal

An intervention records a proposed change and intended outcome for a defined problem, with optional links to hypotheses. It does not carry evidentiary status and does not imply that the intended outcome has occurred.

### 2026-10-03 — Failure analysis remains separate from intervention and evidence

A failure mode represents a concrete way a candidate intervention could fail or cause harm. It may reference the intervention it challenges, but it remains an analysis object rather than evidence, an intervention, or an observed result.
