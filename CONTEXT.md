# Praxis Working Context

This file is the durable working memory for Praxis.

Its purpose is to let the steward reconstruct the current project state from the repository without relying on conversational context.

## Rules

- GitHub is the source of durable project context.
- Conversation is temporary working space.
- Record decisions, discoveries, unresolved questions, rejected directions, and current hypotheses here when they materially affect future work.
- Do not use this file as a dumping ground.
- Prefer concise, dated entries with links to the durable artifact that contains the detail.
- Never silently rewrite history. Correct or supersede prior entries explicitly.
- Context is evidence about project state, not authority over reality.
- Repository artifacts, tests, and external evidence remain the authoritative sources for their respective claims.

## Current state

**2026-10-02 — Foundation established**

Praxis was created as a public repository.

Initial durable artifacts:

- `CANON.md` — governing principles and human-agency constraints.
- `docs/ARCHITECTURE.md` — initial architectural hypothesis and boundaries.
- `docs/ROADMAP.md` — staged development path.
- `docs/DECISIONS.md` — initial decisions.
- `README.md` — project orientation.

The repository is intentionally not yet an implementation-heavy system.

## Core conception

Praxis is a human-centered solution-discovery engine.

Its intended movement is:

```
defined problem
→ structured problem
→ evidence state
→ candidate interventions
→ failure / harm analysis
→ bounded test
→ human decision
→ observed result
→ learned evidence
```

## System relationship

The current conceptual relationship is:

- Episteme — understand.
- Renaissance — connect.
- Praxis — act through human-directed problem solving.
- Organs — shared infrastructure where justified.

These are working boundaries, not permission to assume integrations before their contracts exist.

## Open questions

No unresolved architectural question should be silently answered here. Record it when it becomes concrete enough to investigate.

## Active hypotheses

None yet beyond the initial architecture documented in `docs/ARCHITECTURE.md`.

## Rejected / prohibited directions

See `CANON.md`. In particular, Praxis must not drift toward surveillance, coercive optimization, population control, social-credit machinery, autonomous authority over people, or hidden objectives.

## Steward note

Before undertaking substantial work, read this file and the governing project artifacts. Then inspect the repository itself.

The objective is not to remember everything.

The objective is to remember **only what future work needs**.
