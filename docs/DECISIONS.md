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

### 2026-10-03 — Grounded boundary identities must be unique

Evidence and gap collections are state-bearing inputs, so duplicate identities would make provenance and references ambiguous. `EvidenceState` rejects duplicate EvidenceItem IDs, and `ReasoningContext` rejects malformed or duplicate EvidenceGap identities.

### 2026-10-03 — Human decisions are explicit domain records

Praxis now represents a human decision as a distinct `Decision` object. It records what was decided, why, the human decision reference, and optionally the subject of the decision. Recording a decision does not execute it; consequential action remains a separate boundary.
\n### 2026-10-03 — Candidate generation remains non-authoritative\n\n`CandidateSet` groups candidate hypotheses and interventions for a defined problem without ranking, selecting, authorizing, or executing them. Candidate generation must remain distinct from human decision and consequential action.\n\n### 2026-10-03 — Models remain bounded analysis artifacts\n\n`Model` records a calculation or simulation's purpose, method, inputs, assumptions, outputs, and uncertainty. It does not become evidence merely because it produces an output, and it does not authorize or execute an intervention.\n
### 2026-10-03 — Candidate generation receives an explicit request boundary

`CandidateRequest` records the defined problem, explicit evidence and gap references, requested candidate types, and generation constraints. It is not itself a candidate and carries no ranking, selection, authorization, or execution semantics. Candidate-generation machinery must consume an explicit request rather than relying on hidden inputs.

### 2026-10-03 — Failure analysis receives an explicit request boundary

`FailureAnalysisRequest` makes the interventions and supporting context to be attacked explicit. The request carries no failure finding, severity judgment, ranking, authorization, or execution semantics; those remain separate capabilities.

### 2026-10-03 — Failure-analysis findings remain bounded analysis artifacts

`FailureAnalysis` records the relationship between a failure-analysis request and identified failure modes while preserving uncertainty. Findings remain distinct from evidence, decisions, authorization, and execution.

### 2026-10-03 — Artifact derivation is explicit

`Derivation` records how an artifact was produced from explicit source identities while preserving method and uncertainty. Lineage is not silently promoted to evidence or authority.

### 2026-10-03 — Decision scope is explicit

`DecisionScope` makes the subject of a human decision explicit by linking it to a bounded test or intervention. The linkage records scope; it does not execute or authorize beyond the recorded human decision.

### 2026-10-03 — Result scope is explicit

`ResultScope` makes the relationship between an observed result, its bounded test, and interventions explicit. Scope does not confer evidentiary or decision authority.

### 2026-10-03 — Test design receives an explicit request boundary

`TestRequest` makes the inputs to bounded test design explicit. It remains a request only and does not design, authorize, or execute a test.

### 2026-10-03 — Result capture receives an explicit request boundary

`ResultRequest` separates the request to capture observations from the resulting `Result`. It does not confer evidentiary or decision authority.

### 2026-10-03 — Evidence admission has an explicit request boundary

`EvidenceAdmissionRequest` separates a request for human authorization from the authorization record itself. This preserves the human gate and prevents a request from becoming authority by implication.

### 2026-10-03 — Evaluation receives an explicit request boundary

`EvaluationRequest` separates a request to assess a hypothesis from the resulting inference. Evidence remains input rather than becoming inference by reference.
