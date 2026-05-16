from __future__ import annotations

from pathlib import Path

from codexpy.models import utc_now
from codexpy.storage import append_jsonl, read_json, write_json
from codexpy.validation import ValidationEngine


class RepairLoop:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.state = self.root / ".codexpy"
        self.repairs_file = self.state / "repairs.json"

    def run(self, feature: str | None = None) -> dict:
        result = ValidationEngine(self.root).validate(feature)
        attempt = {
            "timestamp": utc_now(),
            "feature": feature or "all",
            "validation_status": result["status"],
            "failure_summary": self._summarize_failures(result),
            "next_instruction": self._next_instruction(result),
            "converged": result["status"] == "passed",
        }
        data = read_json(self.repairs_file, {"attempts": []})
        data.setdefault("attempts", []).append(attempt)
        write_json(self.repairs_file, data)
        append_jsonl(
            self.state / "telemetry.jsonl",
            {
                "timestamp": attempt["timestamp"],
                "event": "repair",
                "feature": attempt["feature"],
                "converged": attempt["converged"],
            },
        )
        return attempt

    def _summarize_failures(self, result: dict) -> list[str]:
        summaries: list[str] = []
        for failure in result.get("failures", []):
            if "feature" in failure:
                summaries.append(f"{failure.get('feature')}: {failure.get('failures')}")
            elif failure.get("status") == "failed":
                summaries.append("pytest failed")
        return summaries

    def _next_instruction(self, result: dict) -> str:
        if result["status"] == "passed":
            return "Validation passed. Record any final decisions and generate a report."
        return (
            "Inject these validation failures into the next Codex implementation attempt, "
            "repair the behavior regression, then rerun `codexpy validate`."
        )
