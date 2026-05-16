# Memory System

The CodexPy memory system exists to make engineering context durable. It records the information that AI coding workflows usually lose: prompts, assumptions, decisions, tradeoffs, validation evidence, and the reasons a repository evolved in a particular direction.

## Goals

The memory system should allow Codex and developers to:

- retrieve prior engineering decisions
- understand why implementation choices exist
- avoid contradictory changes
- connect prompts to behavior expectations
- reconstruct feature history
- summarize repository evolution
- preserve architecture intent over time

## Memory Types

CodexPy should track several kinds of memory.

| Memory Type | Purpose |
| --- | --- |
| Prompt records | Preserve original engineering requests and inferred intent. |
| Feature records | Track user-facing or system-facing capabilities over time. |
| Decision records | Capture architecture choices, constraints, and consequences. |
| Implementation rationale | Explain why code was written in a particular way. |
| Tradeoff records | Preserve alternatives considered and why they were rejected. |
| Behavior expectations | Store durable workflow and repository-level guarantees. |
| Validation evidence | Connect behavior claims to test runs, reports, and outcomes. |
| Evolution events | Record repository drift, dependency changes, and architecture movement. |

## Local Storage Model

CodexPy should default to transparent local storage inside the repository.

```text
.codexpy/
  memory/
    prompts/
      2026-05-16-add-authentication.md
    decisions/
      ADR-0001-fastapi-service-layout.md
    features/
      authentication.md
    context/
      repository-summary.md
  indexes/
    memory-index.json
```

Markdown is useful for human-readable memory. JSON or SQLite can support indexing and retrieval. The storage format should make the system useful even without a hosted backend.

## Prompt Record

A prompt record should preserve both the original instruction and CodexPy's interpretation of it.

```yaml
id: prompt-2026-05-16-001
created_at: 2026-05-16T10:30:00Z
source: codex
summary: Add authentication support
status: implemented
related_features:
  - authentication
related_decisions:
  - ADR-0003-session-auth
related_behaviors:
  - behavior-auth-login
```

The markdown body should include:

- original prompt
- inferred requirements
- constraints
- affected modules
- implementation notes
- validation results
- follow-up tasks

## Decision Records

Decision records should capture architectural intent, not just a final choice.

Recommended sections:

- Context
- Decision
- Alternatives considered
- Tradeoffs
- Consequences
- Related prompts
- Related behavior specs
- Superseded decisions

This makes future repository changes less likely to contradict past reasoning.

## Repository Decision Graph

The memory engine should model relationships between prompts, features, decisions, behaviors, files, and validation evidence.

```text
Prompt
  ├─ creates Feature
  ├─ records Decision
  ├─ generates Behavior Spec
  ├─ changes Files
  └─ produces Validation Evidence

Decision
  ├─ constrains Feature
  ├─ affects Files
  └─ is validated by Behavior Spec
```

The graph does not need to start as a complex database. A structured index can provide the first version, with richer graph storage later.

## Retrieval

CodexPy memory retrieval should support practical engineering queries:

- What prior decisions affect this module?
- Which behavior specs protect this feature?
- Why was this dependency introduced?
- What did the user originally ask for?
- Which assumptions might this change violate?
- Which previous regressions are related?

The retrieval API should return compact context suitable for AI prompts and detailed references suitable for developers.

## Memory Lifecycle

```text
capture -> normalize -> link -> retrieve -> validate -> summarize
```

1. Capture the prompt, decision, or behavior event.
2. Normalize it into a structured record.
3. Link it to features, files, decisions, and validations.
4. Retrieve it during future work.
5. Validate new changes against historical expectations.
6. Summarize repository evolution in reports.

## Provider Independence

The memory system should not depend on one AI provider. Codex should be a first-class workflow target, but memory records, retrieval APIs, and report generation should work for local scripts, CI, and other AI-assisted engineering tools.
