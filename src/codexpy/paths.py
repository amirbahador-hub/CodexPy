from __future__ import annotations

from pathlib import Path


class RepoPaths:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.state = self.root / ".codexpy"
        self.memory_file = self.state / "memory.json"
        self.telemetry_file = self.state / "telemetry.jsonl"
        self.repairs_file = self.state / "repairs.json"
        self.context_file = self.state / "codex-context.md"
        self.prompts = self.root / ".prompts"
        self.decisions = self.root / ".decisions"
        self.behaviors_hidden = self.root / ".behaviors"
        self.behaviors = self.root / "behaviors"
        self.reports = self.root / "reports"
        self.architecture = self.root / "architecture"
        self.telemetry = self.root / "telemetry"

    def ensure_state(self) -> None:
        for directory in [
            self.state,
            self.prompts,
            self.decisions,
            self.behaviors_hidden,
            self.behaviors,
            self.reports,
            self.architecture,
            self.telemetry,
        ]:
            directory.mkdir(parents=True, exist_ok=True)


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for path in [current, *current.parents]:
        if (path / ".codexpy").exists() or (path / ".git").exists() or (path / "pyproject.toml").exists():
            return path
    return current
