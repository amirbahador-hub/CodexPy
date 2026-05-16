# Architecture

CodexPy is organized as a layered local-first system. Each layer has a clear responsibility, but the layers are designed to reinforce one another: prompts become memory, memory becomes behavior, behavior becomes validation, and validation becomes durable repository evolution.

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                Codex Workflow Integration Layer              │
├─────────────────────────────────────────────────────────────┤
│                 Repository Context Layer                     │
├─────────────────────────────────────────────────────────────┤
│              Validation & Regression Layer                   │
├─────────────────────────────────────────────────────────────┤
│               Behavior Specification Layer                   │
├─────────────────────────────────────────────────────────────┤
│                  Prompt History System                       │
├─────────────────────────────────────────────────────────────┤
│                    AI Memory Engine                          │
├─────────────────────────────────────────────────────────────┤
│                Repository Convention Layer                   │
├─────────────────────────────────────────────────────────────┤
│                  Project Bootstrap Layer                     │
└─────────────────────────────────────────────────────────────┘
```

## 1. Project Bootstrap Layer

The Project Bootstrap Layer generates Python projects that are ready for long-term AI-assisted engineering. It should provide templates for FastAPI services and future Python project types while installing the baseline engineering system around the application code.

Generated projects should include:

- package layout and import conventions
- FastAPI application structure
- Ruff configuration
- pyright configuration
- pytest setup
- pre-commit hooks
- CI/CD workflows
- Docker files
- observability hooks
- repository memory directories
- behavior specification directories
- Codex-oriented project instructions

The bootstrapper is not just a template renderer. It establishes the repository contract that later memory, validation, and evolution tools depend on.

## 2. Repository Convention Layer

The Repository Convention Layer defines where durable engineering context lives and how it is structured. It gives CodexPy-generated projects predictable places for memory, decisions, behavior specifications, reports, and validation outputs.

Proposed convention:

```text
.codexpy/
  memory/
    prompts/
    decisions/
    features/
    context/
  behavior/
    specs/
    expectations/
    workflows/
  reports/
    timelines/
    architecture/
    validation/
  indexes/
    memory-index.json
    behavior-index.json
```

This layer should remain understandable without a hosted service. A developer should be able to inspect repository memory directly in markdown, JSON, or another transparent structured format.

## 3. AI Memory Engine

The AI Memory Engine stores and retrieves persistent engineering context. It tracks what was requested, why decisions were made, how features evolved, and which assumptions should constrain future work.

The memory engine is responsible for:

- structured prompt history
- architecture decision records
- implementation rationale
- feature evolution timelines
- tradeoff records
- repository decision graphs
- retrieval APIs for AI agents

The goal is to let Codex ask, "Why does this system work this way?" and get a repository-grounded answer.

## 4. Prompt History System

The Prompt History System captures engineering prompts and turns them into durable artifacts. A prompt is not treated as disposable input. It is treated as the beginning of a change record.

Prompt records should capture:

- original prompt
- inferred feature or task
- implementation constraints
- impacted repository areas
- accepted decisions
- generated behavior expectations
- validation results
- follow-up changes

Prompt records connect user intent to code, tests, behavior specs, and future repository queries.

## 5. Behavior Specification Layer

The Behavior Specification Layer converts prompts, feature requests, and implementation instructions into durable expectations.

Examples:

- authentication must continue working
- Kafka retries must preserve ordering
- map rendering must remain under the latency threshold
- billing workflows must reject duplicate invoice creation

Behavior specs should describe repository-level guarantees rather than only low-level unit behavior. They can be backed by pytest, integration tests, smoke tests, contract tests, performance checks, or manual validation notes.

## 6. Validation & Regression Layer

The Validation & Regression Layer runs behavior validation and compares current repository behavior against historical expectations.

It should answer:

- Which previously validated behaviors are affected by this change?
- Which assumptions does this change touch?
- Which behavior specs failed?
- Which regressions are semantic rather than only test failures?
- What evidence supports accepting the change?

This layer should integrate with standard Python tools while adding repository-aware validation semantics on top.

## 7. Repository Context Layer

The Repository Context Layer builds a current understanding of the project. It indexes files, modules, dependencies, public interfaces, behavior specs, prior decisions, and generated reports.

This layer feeds Codex and other AI agents with compact, relevant context. It should reduce repeated repository rediscovery and help avoid contradictory implementations.

## 8. Codex Workflow Integration Layer

The Codex Workflow Integration Layer makes the repository memory system usable inside Codex-style development loops.

It should support workflows such as:

- retrieve relevant decisions before implementation
- record a prompt before code generation
- propose behavior specs from a feature request
- run validations after implementation
- generate a markdown report for a completed change
- update repository memory after validation

Codex integration should not make the rest of the system provider-specific. The memory and behavior APIs should remain reusable.

## Change Flow

```text
┌──────────┐
│ Prompt   │
└────┬─────┘
     │
     v
┌──────────────────┐
│ Prompt Record     │
└────┬─────────────┘
     │
     v
┌──────────────────┐
│ Decision Memory   │
└────┬─────────────┘
     │
     v
┌──────────────────┐
│ Behavior Specs    │
└────┬─────────────┘
     │
     v
┌──────────────────┐
│ Implementation    │
└────┬─────────────┘
     │
     v
┌──────────────────┐
│ Validation         │
└────┬─────────────┘
     │
     v
┌──────────────────┐
│ Evolution Report   │
└──────────────────┘
```

## Component Map

```text
codexpy CLI
  ├─ bootstrap generator
  ├─ memory commands
  ├─ decision commands
  ├─ behavior commands
  ├─ validation commands
  └─ report commands

repository artifacts
  ├─ .codexpy/memory
  ├─ .codexpy/behavior
  ├─ .codexpy/reports
  └─ project source tree

runtime services
  ├─ memory engine
  ├─ context indexer
  ├─ behavior validator
  ├─ regression analyzer
  └─ markdown report generator
```
