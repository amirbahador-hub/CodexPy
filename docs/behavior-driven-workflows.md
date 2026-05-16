# Behavior-Driven Workflows

CodexPy uses behavior-driven workflows to protect repository intent over time. Unit tests remain important, but they are not enough for AI-native development because they often miss workflow assumptions, cross-feature contracts, performance expectations, and architecture constraints.

## Core Idea

A feature request should produce more than code. It should produce durable behavior expectations that future changes must preserve.

```text
feature prompt -> behavior expectations -> implementation -> validation -> regression memory
```

## Behavior Specification

A behavior specification describes a repository-level guarantee.

Examples:

- authentication must continue working
- Kafka retries must preserve ordering
- map rendering must remain under the latency threshold
- CLI project generation must produce a runnable pytest suite
- generated FastAPI services must expose a health endpoint

Behavior specs should be written in a way that both developers and AI agents can understand.

## Suggested Behavior Spec Format

```yaml
id: behavior-auth-login
feature: authentication
status: active
priority: critical
validated_by:
  - tests/integration/test_auth_login.py
  - docs/manual-validation/auth-login.md
expected_behavior:
  - A valid user can log in.
  - An invalid password is rejected.
  - Existing authenticated routes remain protected.
regression_risk:
  - session handling
  - password verification
  - route authorization
```

The markdown body can include scenario details, examples, data setup, assumptions, and validation evidence.

## Prompt-to-Behavior Translation

CodexPy should help translate engineering prompts into behavior expectations.

Prompt:

```text
Add retry handling for Kafka publishing.
```

Generated behavior expectations:

- transient broker failures should be retried
- retries must preserve message ordering for a key
- duplicate sends must be detectable or idempotent
- retry exhaustion must produce observable failure output

The generated specs should be reviewable. AI can propose expectations, but the repository should store accepted expectations.

## Validation Types

CodexPy should support multiple validation strategies:

- unit tests for local logic
- integration tests for service behavior
- workflow tests for user or system flows
- contract tests for external boundaries
- smoke tests for generated projects
- performance checks for latency-sensitive behavior
- static checks for project conventions
- manual validation records when automation is not yet available

The validation layer should map each behavior spec to one or more evidence sources.

## Regression-Safe Vibe Coding

For each new feature, CodexPy should:

1. Retrieve relevant prior decisions and behavior specs.
2. Identify affected features and repository assumptions.
3. Add or update behavior expectations for the new request.
4. Implement the change.
5. Run behavior validation and standard tests.
6. Compare outcomes against previous validation evidence.
7. Record the result in repository memory.

The target is simple: AI-generated features should not silently break old working functionality.

## Behavior Validation Report

A validation report should answer:

- What changed?
- Which behavior specs were relevant?
- Which validations ran?
- Which expectations passed, failed, or were not checked?
- Which regressions were detected?
- What memory records were updated?

Reports should be generated as markdown so they can be committed, reviewed, and used by Codex later.

## Relationship to Tests

CodexPy does not replace pytest, integration tests, or CI. It adds a behavior layer above them.

Tests answer:

```text
Did this assertion pass?
```

Behavior specs answer:

```text
Which repository promise does this assertion protect?
```

That relationship is what makes validation useful as engineering memory.
