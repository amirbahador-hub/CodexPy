# Roadmap

This roadmap describes how CodexPy can grow from documentation and initial scaffolding into a full AI-native engineering memory system.

## Phase 0: Project Definition

Status: in progress

- Define project identity and goals.
- Document architecture layers.
- Document memory model.
- Document behavior-driven workflows.
- Document repository evolution model.
- Establish implementation roadmap.

## Phase 1: Python CLI Foundation

Build the base command-line interface.

- Create Python package structure.
- Add CLI entry point.
- Add configuration loading.
- Add local repository detection.
- Add markdown and JSON artifact helpers.
- Add basic report output.

Candidate commands:

```bash
codexpy init
codexpy memory
codexpy decision
codexpy behavior
codexpy validate
codexpy report
```

## Phase 2: Project Bootstrap Generator

Generate AI-native Python projects.

- FastAPI template
- Ruff configuration
- pyright configuration
- pytest setup
- pre-commit setup
- CI/CD workflow
- Dockerfile and compose support
- observability starter hooks
- `.codexpy/` repository memory layout
- Codex-oriented project instructions

The generated project should be immediately runnable and validation-ready.

## Phase 3: Repository Memory Engine

Implement persistent engineering memory.

- Prompt records
- Feature records
- Architecture decision records
- Implementation rationale records
- Tradeoff records
- Memory index
- Retrieval API
- Markdown storage
- JSON index storage

The first version should favor transparent local files over infrastructure complexity.

## Phase 4: Prompt Tracking System

Turn prompts into durable repository artifacts.

- Capture original prompt text.
- Infer task and feature metadata.
- Link prompts to decisions and files.
- Link prompts to behavior specs.
- Record validation outcomes.
- Generate prompt history summaries.

This phase establishes the foundation for repository-aware AI sessions.

## Phase 5: Behavior Validation Framework

Introduce behavior specifications and validation mapping.

- Behavior spec schema
- Behavior spec authoring commands
- Prompt-to-behavior draft generation
- Validation evidence records
- pytest integration
- workflow validation reports
- manual validation records

This phase moves CodexPy beyond templates into behavior preservation.

## Phase 6: Regression Engine

Add regression-safe vibe coding workflows.

- Retrieve relevant prior behavior specs before implementation.
- Detect affected features and assumptions.
- Compare new validation results against previous evidence.
- Flag unvalidated behavior changes.
- Generate regression reports.
- Support CI usage.

The goal is to prevent AI-generated changes from silently breaking old working functionality.

## Phase 7: Repository Evolution Engine

Track long-term repository change.

- Engineering timeline
- Architecture evolution reports
- Dependency evolution records
- Feature interaction map
- Repository drift detection
- Memory summary generation
- Codex session context generation

This phase makes CodexPy a repository evolution framework rather than only a validation tool.

## Phase 8: Advanced Capabilities

Explore richer AI-native engineering workflows.

- Prompt-to-behavior translation
- AI repository memory retrieval
- semantic repository diffing
- architecture drift analysis
- feature conflict detection
- autonomous regression prevention
- provider-neutral agent integration

Advanced capabilities should remain grounded in transparent local repository artifacts.

## Non-Goals

CodexPy should not become:

- a generic prompt manager
- a hosted-only AI platform
- a provider-specific wrapper
- a hidden code generation service
- a template collection without memory and validation semantics

Every feature should support the central purpose: long-term memory and stability infrastructure for AI-native Python engineering.
