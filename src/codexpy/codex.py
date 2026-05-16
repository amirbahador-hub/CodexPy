from __future__ import annotations

from pathlib import Path

from codexpy.behavior import BehaviorStore
from codexpy.memory import MemoryStore
from codexpy.paths import RepoPaths


class CodexContext:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.paths = RepoPaths(self.root)
        self.memory = MemoryStore(self.root)
        self.behaviors = BehaviorStore(self.root)

    def render(self) -> str:
        events = self.memory.list_events()[-12:]
        decisions = self.memory.decisions_timeline()[-8:]
        behaviors = self.behaviors.list()
        lines = [
            "# CodexPy Repository Context",
            "",
            "Use this context before making AI-assisted changes. Preserve active behavior specs and record new decisions when implementation intent changes.",
            "",
            "## Recent Memory",
        ]
        if events:
            lines.extend(
                f"- `{event['timestamp']}` {event['kind']}: {event['summary']}"
                for event in events
            )
        else:
            lines.append("- No memory events recorded yet.")
        lines.extend(["", "## Active Decisions"])
        if decisions:
            lines.extend(
                f"- `{decision['timestamp']}` {decision['decision_summary']}"
                for decision in decisions
            )
        else:
            lines.append("- No decisions recorded yet.")
        lines.extend(["", "## Behavior Specs"])
        if behaviors:
            for behavior in behaviors:
                lines.append(f"- {behavior.get('feature')} (`{behavior.get('id')}`)")
        else:
            lines.append("- No behavior specs recorded yet.")
        lines.extend(
            [
                "",
                "## Workflow Policy",
                "- Load memory before implementation.",
                "- Add behavior specs for new features.",
                "- Run `codexpy validate` after changes.",
                "- Record decisions when architecture or tradeoffs change.",
                "- Update AGENTS.md when repository rules evolve.",
                "",
            ]
        )
        return "\n".join(lines)

    def write(self) -> Path:
        self.paths.ensure_state()
        rendered = self.render()
        self.paths.context_file.write_text(rendered, encoding="utf-8")
        return self.paths.context_file


def agents_md(project_name: str = "CodexPy generated project") -> str:
    return f"""# AGENTS.md

## Project

{project_name} is managed with CodexPy. Treat repository memory, behavior specs, and validation reports as durable engineering context.

## Architecture Rules

- Keep application code in `app/`.
- Keep tests in `tests/`.
- Keep behavior specifications in `behaviors/`.
- Record architecture decisions in `.decisions/`.
- Record prompt history in `.prompts/`.
- Keep telemetry helpers in `telemetry/`.

## Coding Conventions

- Use typed Python.
- Run Ruff, pyright, and pytest before considering work complete.
- Prefer small cohesive modules over broad utility files.
- Keep generated behavior expectations human readable and AI readable.

## Workflow Constraints

- Load repository memory before implementing features.
- Preserve existing behavior specs unless a decision explicitly supersedes them.
- Add or update behavior specs for new feature work.
- Record decisions when architecture, dependencies, or tradeoffs change.

## Validation Policy

- Run `codexpy validate` after AI-assisted changes.
- Treat failed behavior validation as a regression until explained by a recorded decision.
- Use `codexpy report` to summarize repository evolution before releases.
"""
