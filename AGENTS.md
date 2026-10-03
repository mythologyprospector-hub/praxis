# AGENTS.md

## Purpose

This repository is the durable project memory for Praxis. Work must be reconstructible from GitHub without relying on an earlier conversation.

## Division of labor

- **Human** — final human gate. Provides approval for consequential direction and decisions.
- **Foreman / driver** — determines architecture, sequencing, scope, and the next engineering objective from repository truth and available evidence.
- **Codex / implementation agent** — performs the established implementation work, runs tests, reports failures, and records durable project changes in Git.
- **Git / GitHub** — durable memory, project record, implementation history, and evidence of what was actually tested.
- **CI / GitHub Actions** — repeatable inspection and test evidence.

The implementation agent must not silently become the architectural authority. If implementation reveals that the established direction is inadequate, stop at the boundary, record the finding, and surface it for the driver.

## Operating rule

**Do not depend on conversational context. Read the repository.**

Before substantial work:
1. Read CONTEXT.md.
2. Read CANON.md.
3. Read the relevant architecture/roadmap/decision artifacts.
4. Inspect the actual repository state and existing tests.
5. Determine the next task from repository evidence.
6. Implement only the established task.
7. Run the relevant tests and report their actual result.
8. Record durable decisions, discoveries, contradictions, rejected approaches, or implementation state when they materially affect future work.

The repository is authoritative for project history and recorded decisions. Conversation is temporary working space.

## Context discipline

Do not turn this file or CONTEXT.md into a transcript.

Record only information that a future steward/agent needs in order to reconstruct why the current repository state exists. Prefer concise dated entries and links to concrete artifacts, commits, tests, or external evidence.

Never present speculation as established fact. Never silently erase historical decisions; supersede them with an explicit record when necessary.

## Change discipline

- Inspect before editing.
- Prefer small, coherent commits.
- Do not invent APIs, dependencies, integrations, or architecture merely to make implementation convenient.
- Do not add autonomous consequential behavior.
- Preserve Praxis's human-agency constraint.
- Keep proposals, evidence, tests, results, and human decisions distinct.
- Do not use another project as an architectural template merely because code can be copied from it.
- Do not claim tests passed unless they actually passed.
- Keep CI configuration minimal until the repository has demonstrated a need for more machinery.

## Test discipline

Pytest is the initial Python test runner.

When tests exist, CI must execute them through Python's module interface:

    python -m pytest -q

When no tests exist yet, CI must say so explicitly rather than manufacturing coverage or treating an empty suite as successful test evidence.

Every implementation change should add or update tests when behavior is introduced.

## Durable handoff

At the end of a material task, leave the repository in a state that another agent can pick up cold:
- implementation is committed;
- tests and their actual result are known;
- important discoveries or decisions are recorded in the appropriate repository artifact;
- unresolved questions remain explicit;
- no essential context exists only in chat.

## Scope boundary

Praxis helps humans reason from defined problems toward candidate interventions, failure analysis, bounded tests, observed results, and improved evidence.

It does not choose human ends, exercise autonomous authority over people, perform population optimization or surveillance, or take consequential action merely because an action is technically possible.