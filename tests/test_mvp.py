from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from codexpy.behavior import BehaviorStore
from codexpy.bootstrap import ProjectBootstrapper
from codexpy.cli import main
from codexpy.memory import MemoryStore
from codexpy.models import MemoryEvent
from codexpy.validation import ValidationEngine


class CodexPyMvpTests(unittest.TestCase):
    def test_bootstrap_generates_ai_native_project(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            project = ProjectBootstrapper(Path(raw)).init("demo_service")

            self.assertTrue((project / "app/main.py").exists())
            self.assertTrue((project / "pyproject.toml").exists())
            self.assertTrue((project / "AGENTS.md").exists())
            self.assertTrue((project / "behaviors/service-health.json").exists())
            self.assertTrue((project / ".codexpy/memory.json").exists())
            self.assertTrue(MemoryStore(project).decisions_timeline())

    def test_memory_and_behavior_validation_flow(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            project = ProjectBootstrapper(Path(raw)).init("demo_service")
            store = MemoryStore(project)
            behavior_path = BehaviorStore(project).create_from_text(
                "authentication",
                ["login works", "unauthorized requests fail"],
            )

            store.record(
                event=MemoryEvent(
                    kind="prompt",
                    feature="authentication",
                    summary="Add authentication system",
                    prompt="Create auth with login and unauthorized failures.",
                    affected_files=[str(behavior_path.relative_to(project))],
                )
            )

            result = ValidationEngine(project).validate("authentication")

            self.assertEqual(result["status"], "passed")
            self.assertIsNotNone(store.show_feature("authentication"))

    def test_cli_end_to_end_without_pytest_run(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            with patch("pathlib.Path.cwd", return_value=Path(raw)):
                self.assertEqual(main(["init", "demo_service"]), 0)
            project = Path(raw) / "demo_service"

            self.assertEqual(
                main(
                    [
                        "--repo",
                        str(project),
                        "behavior",
                        "add",
                        "billing",
                        "invoice creation works",
                    ]
                ),
                0,
            )
            self.assertEqual(main(["--repo", str(project), "memory", "list"]), 0)
            self.assertEqual(main(["--repo", str(project), "codex", "context"]), 0)
            self.assertEqual(main(["--repo", str(project), "report"]), 0)
            self.assertTrue((project / ".codexpy/codex-context.md").exists())
            self.assertTrue((project / "reports/engineering-report.md").exists())


if __name__ == "__main__":
    unittest.main()
