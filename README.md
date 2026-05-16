# CodexPy

CodexPy is an AI-native Python engineering framework for building stable, long-lived AI-assisted projects.

It combines Python project bootstrapping, repository conventions, persistent AI memory, behavior-driven validation, engineering decision tracking, regression protection, and Codex workflow integration to enable safer vibe coding, maintainable AI-generated systems, and long-term repository evolution.

CodexPy is not another Python template, AI wrapper, prompt tool, or code generator. It is engineering infrastructure for teams and solo developers who want AI-assisted repositories to retain intent, preserve behavior, and evolve without losing their history.

## Why CodexPy Exists

AI coding workflows often fail because prompts disappear, architectural intent is lost, behavior assumptions are undocumented, regressions accumulate, AI forgets prior decisions, and repository evolution becomes unstable.

CodexPy changes the workflow from:

```text
prompt -> code
```

to:

```text
prompt -> decision memory -> behavior specification -> implementation -> validation -> persistent evolution
```

That shift makes repository context durable. New AI-generated changes can be checked against prior decisions, validated behavior, and historical feature expectations before they become silent regressions.

## What CodexPy Provides

CodexPy is designed around five core capabilities:

- AI-native Python project bootstrap: generate maintainable Python projects with FastAPI support, Ruff, pyright, pytest, pre-commit, CI/CD, Docker, observability hooks, and conventions optimized for Codex-style development.
- Persistent engineering memory: track prompts, feature requests, architecture decisions, implementation rationale, tradeoffs, and repository evolution history.
- Behavior-driven validation: turn feature intent into durable behavior specifications that validate workflows, repository expectations, and user-facing guarantees beyond unit tests.
- Regression-safe vibe coding: compare new changes against historical behavior, prior assumptions, and validated expectations before accepting AI-generated implementation work.
- Repository evolution engine: record how architecture, dependencies, features, prompts, and decisions change over time, then generate timelines and memory summaries.

## Architecture

CodexPy is organized into layered systems:

1. Project Bootstrap Layer
2. Repository Convention Layer
3. AI Memory Engine
4. Prompt History System
5. Behavior Specification Layer
6. Validation & Regression Layer
7. Repository Context Layer
8. Codex Workflow Integration Layer

See [docs/architecture.md](docs/architecture.md) for the full architecture and diagrams.

## MVP CLI

The MVP ships a local-first CLI:

```bash
codexpy init my-service --template fastapi
codexpy prompt record auth-feature --request "Add authentication"
codexpy decisions record "Use token auth"
codexpy behavior add
codexpy validate
codexpy report
```

Current commands:

```bash
codexpy init my_project
codexpy memory list
codexpy memory show authentication
codexpy memory record "Implemented auth" --feature authentication
codexpy decisions timeline
codexpy decisions record "Use token auth" --feature authentication
codexpy behavior add authentication "login works" "unauthorized requests fail"
codexpy prompt record auth-feature --request "Add authentication" --feature authentication
codexpy validate
codexpy validate authentication
codexpy regressions
codexpy repair
codexpy codex context
codexpy codex sync-agents
codexpy report
```

Every generated project includes enough structure for Codex to understand the repository, retrieve engineering memory, preserve behavior, and explain why implementation choices exist.

## Documentation

- [Architecture](docs/architecture.md)
- [Memory System](docs/memory-system.md)
- [Behavior-Driven Workflows](docs/behavior-driven-workflows.md)
- [Project Evolution](docs/project-evolution.md)
- [Roadmap](docs/roadmap.md)

## Implementation Scope

CodexPy is implemented primarily in Python with modular local-first components:

- Python CLI
- project bootstrap generator
- Codex integration
- repository memory engine
- prompt tracking system
- behavior validation framework
- regression engine
- markdown report generator

Provider lock-in should be avoided. Repository memory APIs should be reusable outside any single AI tool, while still giving Codex-style workflows first-class support.

## Development

```bash
PYTHONPATH=src python -m codexpy.cli --help
PYTHONPATH=src python -m unittest discover -s tests
```

## Design Philosophy

CodexPy should feel like long-term memory and stability infrastructure for AI-native Python engineering.

The project focuses on repository evolution, engineering memory, behavior preservation, AI-native workflows, regression safety, long-term maintainability, and persistent engineering intelligence.

## Long-Term Vision

CodexPy should evolve toward persistent AI engineering memory, repository cognition systems, behavior-aware AI development, autonomous regression prevention, long-lived AI-native software systems, and reusable engineering memory infrastructure.
