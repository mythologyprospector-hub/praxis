# Context Protocol

## Purpose

Praxis uses the repository as durable external memory for project reasoning.

This allows the active conversational context to remain small while preserving the information needed to continue work accurately.

## What belongs in durable context

Record information that changes what should happen next:

- architectural decisions;
- governing constraints;
- important discoveries;
- verified contradictions;
- unresolved questions;
- rejected approaches and why they were rejected;
- experiment results;
- implementation state that cannot be reconstructed cheaply from the repository;
- relationships to external systems;
- provenance pointers.

## What does not belong here

Do not store:

- conversational filler;
- repeated explanations;
- transient thoughts with no project consequence;
- information already obvious from source code or tests;
- speculative claims presented as facts;
- personal information unrelated to the project.

## Entry discipline

Every material entry should answer:

1. What happened?
2. Why does it matter?
3. What artifact or evidence supports it?
4. What remains unresolved?

Use dates.

Prefer links or repository paths over copied material.

## Reconstruction rule

A fresh steward should be able to:

1. read `CONTEXT.md`;
2. read the governing canon;
3. inspect the current repository;
4. inspect referenced evidence;
5. understand why the current work exists;
6. continue without needing the previous conversation.

If that is not possible, the context substrate is insufficient.

## Context is not canon

Working context may contain hypotheses and unresolved questions.

The canon contains governing constraints.

Neither substitutes for evidence.

## Context hygiene

When an entry becomes obsolete:

- mark it superseded;
- preserve the historical reason where useful;
- point to the replacement artifact.

Do not silently erase decisions merely to make the current state look cleaner.
