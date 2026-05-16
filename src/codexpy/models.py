from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    normalized = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    parts = [part for part in normalized.split("-") if part]
    return "-".join(parts) or f"item-{uuid4().hex[:8]}"


@dataclass(frozen=True)
class MemoryEvent:
    kind: str
    summary: str
    prompt: str = ""
    affected_files: list[str] = field(default_factory=list)
    decision_summary: str = ""
    validation_result: str = "not_run"
    feature: str = ""
    rationale: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: f"mem-{uuid4().hex[:12]}")
    timestamp: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.event_id,
            "timestamp": self.timestamp,
            "kind": self.kind,
            "feature": self.feature,
            "summary": self.summary,
            "prompt": self.prompt,
            "affected_files": self.affected_files,
            "decision_summary": self.decision_summary,
            "validation_result": self.validation_result,
            "rationale": self.rationale,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class BehaviorSpec:
    feature: str
    expected_outcomes: list[str]
    regression_expectations: list[str] = field(default_factory=list)
    checks: list[dict[str, str]] = field(default_factory=list)
    behavior_id: str = ""
    status: str = "active"
    created_at: str = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.behavior_id:
            object.__setattr__(self, "behavior_id", slugify(self.feature))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.behavior_id,
            "feature": self.feature,
            "status": self.status,
            "created_at": self.created_at,
            "expected_outcomes": self.expected_outcomes,
            "regression_expectations": self.regression_expectations,
            "checks": self.checks,
        }


def relative_to_repo(repo: Path, paths: list[Path]) -> list[str]:
    output: list[str] = []
    for path in paths:
        try:
            output.append(str(path.resolve().relative_to(repo.resolve())))
        except ValueError:
            output.append(str(path))
    return output
