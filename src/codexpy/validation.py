from __future__ import annotations

import subprocess
import time
from importlib.util import find_spec
from pathlib import Path

from codexpy.behavior import BehaviorStore
from codexpy.models import MemoryEvent, utc_now
from codexpy.storage import append_jsonl, read_json, write_json


class ValidationEngine:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.behaviors = BehaviorStore(self.root)
        self.state = self.root / ".codexpy"
        self.last_result_file = self.state / "last-validation.json"
        self.regressions_file = self.state / "regressions.json"

    def validate(self, feature: str | None = None) -> dict:
        started = time.monotonic()
        specs = [self.behaviors.get(feature)] if feature else self.behaviors.list()
        specs = [spec for spec in specs if spec]
        behavior_results = [self._validate_spec(spec) for spec in specs]
        pytest_result = self._run_pytest()
        failures = [
            result for result in behavior_results if result["status"] != "passed"
        ]
        if pytest_result["status"] == "failed":
            failures.append(pytest_result)

        result = {
            "timestamp": utc_now(),
            "feature": feature or "all",
            "status": "failed" if failures else "passed",
            "duration_ms": round((time.monotonic() - started) * 1000, 2),
            "behaviors": behavior_results,
            "pytest": pytest_result,
            "failures": failures,
        }
        write_json(self.last_result_file, result)
        append_jsonl(
            self.state / "telemetry.jsonl",
            {
                "timestamp": result["timestamp"],
                "event": "validation",
                "feature": result["feature"],
                "status": result["status"],
                "duration_ms": result["duration_ms"],
                "behavior_count": len(behavior_results),
            },
        )
        if failures:
            regressions = read_json(self.regressions_file, {"items": []})
            regressions.setdefault("items", []).append(result)
            write_json(self.regressions_file, regressions)
        return result

    def _validate_spec(self, spec: dict) -> dict:
        checks = spec.get("checks") or []
        failures: list[str] = []
        for check in checks:
            if check.get("type") == "file_exists":
                target = self.root / check.get("target", "")
                if not target.exists():
                    failures.append(f"Missing expected file: {check.get('target')}")
            elif check.get("type") == "text":
                target = check.get("target", "").strip()
                if not target:
                    failures.append("Empty text expectation")
        return {
            "id": spec.get("id"),
            "feature": spec.get("feature"),
            "status": "failed" if failures else "passed",
            "failures": failures,
            "expected_outcomes": spec.get("expected_outcomes", []),
        }

    def _run_pytest(self) -> dict:
        tests_dir = self.root / "tests"
        if not tests_dir.exists():
            return {"status": "skipped", "reason": "tests directory not found"}
        if find_spec("pytest") is None:
            return {"status": "skipped", "reason": "pytest is not installed"}
        process = subprocess.run(
            ["python", "-m", "pytest"],
            cwd=self.root,
            text=True,
            capture_output=True,
            timeout=120,
            check=False,
        )
        return {
            "status": "passed" if process.returncode == 0 else "failed",
            "returncode": process.returncode,
            "stdout": process.stdout[-4000:],
            "stderr": process.stderr[-4000:],
        }

    def regressions(self) -> list[dict]:
        return read_json(self.regressions_file, {"items": []}).get("items", [])


def validation_memory_event(result: dict) -> MemoryEvent:
    return MemoryEvent(
        kind="validation",
        summary=f"Validation {result['status']} for {result['feature']}",
        validation_result=result["status"],
        metadata={"duration_ms": result["duration_ms"], "failures": result["failures"]},
    )
