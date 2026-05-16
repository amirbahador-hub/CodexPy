from __future__ import annotations

from pathlib import Path

from codexpy.behavior import BehaviorStore
from codexpy.memory import MemoryStore
from codexpy.paths import RepoPaths
from codexpy.storage import read_json


class ReportGenerator:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.paths = RepoPaths(self.root)
        self.memory = MemoryStore(self.root)
        self.behaviors = BehaviorStore(self.root)

    def generate(self) -> Path:
        self.paths.ensure_state()
        events = self.memory.list_events()
        decisions = self.memory.decisions_timeline()
        behaviors = self.behaviors.list()
        regressions = read_json(self.paths.state / "regressions.json", {"items": []}).get("items", [])
        telemetry = self._telemetry_summary()
        lines = [
            "# CodexPy Engineering Report",
            "",
            "## Repository Evolution",
            "",
        ]
        if events:
            lines.extend(f"- `{event['timestamp']}` {event['kind']}: {event['summary']}" for event in events)
        else:
            lines.append("- No memory events recorded yet.")
        lines.extend(["", "## Engineering Decisions", ""])
        if decisions:
            lines.extend(
                f"- `{decision['timestamp']}` {decision['decision_summary']}" for decision in decisions
            )
        else:
            lines.append("- No decisions recorded yet.")
        lines.extend(["", "## Behavior Coverage", ""])
        if behaviors:
            for behavior in behaviors:
                lines.append(
                    f"- {behavior.get('feature')}: {len(behavior.get('expected_outcomes', []))} expectations"
                )
        else:
            lines.append("- No behaviors recorded yet.")
        lines.extend(["", "## Regression Analysis", ""])
        if regressions:
            lines.extend(
                f"- `{item['timestamp']}` {item['feature']}: {item['status']}"
                for item in regressions[-10:]
            )
        else:
            lines.append("- No regressions recorded.")
        lines.extend(["", "## Telemetry", ""])
        lines.append(f"- validation runs: {telemetry['validation_runs']}")
        lines.append(f"- repair attempts: {telemetry['repair_attempts']}")
        lines.append(f"- average validation latency ms: {telemetry['average_validation_ms']}")
        lines.append("")
        path = self.paths.reports / "engineering-report.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def _telemetry_summary(self) -> dict:
        if not self.paths.telemetry_file.exists():
            return {"validation_runs": 0, "repair_attempts": 0, "average_validation_ms": 0}
        validation_durations: list[float] = []
        repair_attempts = 0
        for line in self.paths.telemetry_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = read_json_line(line)
            if item.get("event") == "validation":
                validation_durations.append(float(item.get("duration_ms", 0)))
            if item.get("event") == "repair":
                repair_attempts += 1
        average = round(sum(validation_durations) / len(validation_durations), 2) if validation_durations else 0
        return {
            "validation_runs": len(validation_durations),
            "repair_attempts": repair_attempts,
            "average_validation_ms": average,
        }


def read_json_line(line: str) -> dict:
    import json

    return json.loads(line)
