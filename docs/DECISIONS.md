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

### 2026-10-03 — Tests remain plans, not results

A Test defines a bounded way to learn about a candidate intervention, including its objective, expected observations, safety constraints, reversibility, and decision criteria. It does not claim that the test occurred or that its expected observations were observed.

### 2026-10-03 — Results remain distinct from evidence until incorporated

A Result records what was observed during a bounded test, including provenance and uncertainty. It is distinct from the Test plan and is not automatically treated as part of the problem's evidence state. A later closed-loop workflow must explicitly determine when and how results become evidence.

### 2026-10-03 — Result-to-evidence promotion is explicit and traceable

A Result must not silently become evidence. The first closed-loop boundary uses explicit EvidenceItem.from_result(...) admission and retains the source Result identifier, provenance, and uncertainty. Broader workflow and decision criteria remain future work.

### 2026-10-03 — Evidence-state admission requires a recorded authorization

Adding evidence to an EvidenceState is an epistemic state change, so it must not be an implicit side effect of creating an EvidenceItem. The first gate is an EvidenceAdmission record containing the problem, evidence identity, authorizing human reference, and rationale. EvidenceState.admit(...) requires a matching admission and does not itself invent or infer authorization.

### 2026-10-03 — Reasoning consumes an explicit grounded context

Reasoning machinery should receive an immutable context pairing the defined Problem with its matching EvidenceState. The context is an input boundary only: it does not infer, rank, decide, or mutate evidence. A context cannot combine evidence belonging to another problem.

### 2026-10-03 — Missing knowledge is a first-class reasoning input

Praxis should represent material unknowns explicitly rather than forcing absence of evidence into evidence, inference, or hypothesis objects. `EvidenceGap` records the unknown and why it could matter to a decision; it does not assert what the answer is.


### 2026-10-03 — Grounded reasoning context includes explicit gaps

A reasoning input should preserve both what is currently supported by evidence and what remains materially unknown. `ReasoningContext` therefore carries matching `EvidenceState` plus zero or more `EvidenceGap` objects, rejecting cross-problem gaps just as it rejects cross-problem evidence.