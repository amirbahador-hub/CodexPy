# Project Evolution

CodexPy treats a repository as a system that evolves through prompts, decisions, features, dependencies, behaviors, and validations. The project evolution engine records that movement so future work can understand not only what changed, but why it changed.

## Evolution Events

An evolution event is a durable record of repository movement.

Examples:

- a feature was introduced
- an architecture decision was accepted
- a behavior spec was added
- a validation failed and was fixed
- a dependency was upgraded
- a module boundary changed
- a previous decision was superseded
- repository conventions were updated

These events form an engineering timeline.

## Engineering Timeline

The timeline should connect work across artifacts.

```text
2026-05-16
  prompt: Add authentication support
  decision: Use session-based auth for first release
  behavior: Login, logout, protected routes
  files: app/auth/*, tests/integration/test_auth.py
  validation: passed
```

The timeline should be useful to both humans and AI agents. It should make repository history queryable without digging through commits alone.

## Architecture Evolution Reports

Architecture evolution reports should summarize:

- current architecture
- recent architecture changes
- decisions that shaped the current structure
- deprecated assumptions
- modules with high change frequency
- feature interactions
- dependency movement
- behavior specs affected by architecture changes

These reports help Codex enter a repository with current context instead of relying only on source code scanning.

## Repository Drift

Repository drift occurs when implementation, documentation, decisions, and behavior expectations diverge.

CodexPy should detect and report drift such as:

- code no longer matches documented architecture
- behavior specs no longer have validation evidence
- decisions are contradicted by newer implementation
- dependencies changed without updated rationale
- prompt intent was implemented but not validated
- generated project conventions were manually broken

Drift reports should distinguish between intentional evolution and accidental inconsistency.

## Feature Interactions

Long-lived repositories become risky when new features interact with old assumptions. CodexPy should track relationships such as:

- feature A depends on behavior from feature B
- feature C supersedes part of feature A
- feature D introduces performance constraints on feature B
- feature E changes shared authentication, routing, storage, or messaging logic

This context lets future AI-generated changes identify blast radius before implementation.

## Dependency Evolution

Dependency changes should be treated as engineering events. A dependency record should include:

- package name
- version change
- reason for change
- affected modules
- related decisions
- validation evidence
- rollback notes when relevant

This is especially important for generated projects where framework and tooling upgrades can alter conventions.

## Memory Summaries

CodexPy should generate repository memory summaries for AI workflows.

Useful summaries include:

- current project purpose
- active architecture decisions
- core behavior guarantees
- recent changes
- known risks
- validation status
- recommended context for future Codex sessions

These summaries should be compact enough to feed into an AI coding session and detailed enough to prevent repeated rediscovery.

## Report Generator

The markdown report generator should create:

- engineering timelines
- architecture evolution reports
- behavior validation reports
- memory summaries
- feature history reports
- repository drift reports

Reports should be committed artifacts when they represent durable project history.
