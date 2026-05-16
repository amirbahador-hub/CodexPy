from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from codexpy.behavior import BehaviorStore, infer_behavior_outcomes
from codexpy.bootstrap import ProjectBootstrapper
from codexpy.codex import CodexContext, agents_md
from codexpy.memory import MemoryStore
from codexpy.models import MemoryEvent
from codexpy.paths import RepoPaths, find_repo_root
from codexpy.repair import RepairLoop
from codexpy.reports import ReportGenerator
from codexpy.validation import ValidationEngine, validation_memory_event


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"codexpy: error: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codexpy")
    parser.add_argument("--repo", type=Path, default=None, help="Repository root")
    subparsers = parser.add_subparsers(required=True)

    init = subparsers.add_parser("init", help="Generate an AI-native Python project")
    init.add_argument("name")
    init.add_argument("--template", default="fastapi", choices=["fastapi"])
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)

    memory = subparsers.add_parser("memory", help="Repository memory commands")
    memory_sub = memory.add_subparsers(required=True)
    memory_list = memory_sub.add_parser("list")
    memory_list.set_defaults(func=cmd_memory_list)
    memory_show = memory_sub.add_parser("show")
    memory_show.add_argument("feature")
    memory_show.set_defaults(func=cmd_memory_show)
    memory_record = memory_sub.add_parser("record")
    memory_record.add_argument("summary")
    memory_record.add_argument("--kind", default="note")
    memory_record.add_argument("--feature", default="")
    memory_record.add_argument("--prompt", default="")
    memory_record.add_argument("--decision", default="")
    memory_record.add_argument("--validation", default="not_run")
    memory_record.add_argument("--file", action="append", default=[])
    memory_record.set_defaults(func=cmd_memory_record)

    decisions = subparsers.add_parser("decisions", help="Engineering decision commands")
    decisions_sub = decisions.add_subparsers(required=True)
    timeline = decisions_sub.add_parser("timeline")
    timeline.set_defaults(func=cmd_decisions_timeline)
    decision_record = decisions_sub.add_parser("record")
    decision_record.add_argument("summary")
    decision_record.add_argument("--feature", default="")
    decision_record.add_argument("--prompt", default="")
    decision_record.add_argument("--file", action="append", default=[])
    decision_record.set_defaults(func=cmd_decision_record)

    behavior = subparsers.add_parser("behavior", help="Behavior specification commands")
    behavior_sub = behavior.add_subparsers(required=True)
    behavior_add = behavior_sub.add_parser("add")
    behavior_add.add_argument("feature")
    behavior_add.add_argument("outcomes", nargs="*")
    behavior_add.add_argument("--from-prompt", default="")
    behavior_add.set_defaults(func=cmd_behavior_add)
    behavior_list = behavior_sub.add_parser("list")
    behavior_list.set_defaults(func=cmd_behavior_list)

    prompt = subparsers.add_parser("prompt", help="Prompt tracking commands")
    prompt_sub = prompt.add_subparsers(required=True)
    prompt_record = prompt_sub.add_parser("record")
    prompt_record.add_argument("summary")
    prompt_record.add_argument("--request", required=True)
    prompt_record.add_argument("--output", default="")
    prompt_record.add_argument("--feature", default="")
    prompt_record.add_argument("--file", action="append", default=[])
    prompt_record.add_argument("--validation", default="not_run")
    prompt_record.add_argument("--retry-count", type=int, default=0)
    prompt_record.set_defaults(func=cmd_prompt_record)

    validate = subparsers.add_parser("validate", help="Run behavior and regression validation")
    validate.add_argument("feature", nargs="?")
    validate.set_defaults(func=cmd_validate)

    regressions = subparsers.add_parser("regressions", help="Show stored regression failures")
    regressions.set_defaults(func=cmd_regressions)

    repair = subparsers.add_parser("repair", help="Record a repair-loop attempt")
    repair.add_argument("feature", nargs="?")
    repair.set_defaults(func=cmd_repair)

    codex = subparsers.add_parser("codex", help="Codex workflow integration")
    codex_sub = codex.add_subparsers(required=True)
    context = codex_sub.add_parser("context")
    context.set_defaults(func=cmd_codex_context)
    sync_agents = codex_sub.add_parser("sync-agents")
    sync_agents.set_defaults(func=cmd_sync_agents)

    report = subparsers.add_parser("report", help="Generate engineering reports")
    report.set_defaults(func=cmd_report)
    return parser


def repo_root(args: argparse.Namespace) -> Path:
    return find_repo_root(args.repo)


def cmd_init(args: argparse.Namespace) -> int:
    root = ProjectBootstrapper(Path.cwd()).init(args.name, force=args.force)
    print(f"initialized {root}")
    return 0


def cmd_memory_list(args: argparse.Namespace) -> int:
    events = MemoryStore(repo_root(args)).list_events()
    print(json.dumps(events, indent=2))
    return 0


def cmd_memory_show(args: argparse.Namespace) -> int:
    feature = MemoryStore(repo_root(args)).show_feature(args.feature)
    if not feature:
        print(f"feature not found: {args.feature}", file=sys.stderr)
        return 1
    print(json.dumps(feature, indent=2))
    return 0


def cmd_memory_record(args: argparse.Namespace) -> int:
    event = MemoryEvent(
        kind=args.kind,
        summary=args.summary,
        prompt=args.prompt,
        affected_files=args.file,
        decision_summary=args.decision,
        validation_result=args.validation,
        feature=args.feature,
    )
    stored = MemoryStore(repo_root(args)).record(event)
    print(json.dumps(stored, indent=2))
    return 0


def cmd_decisions_timeline(args: argparse.Namespace) -> int:
    print(json.dumps(MemoryStore(repo_root(args)).decisions_timeline(), indent=2))
    return 0


def cmd_decision_record(args: argparse.Namespace) -> int:
    event = MemoryEvent(
        kind="decision",
        summary=args.summary,
        prompt=args.prompt,
        affected_files=args.file,
        decision_summary=args.summary,
        feature=args.feature,
    )
    print(json.dumps(MemoryStore(repo_root(args)).record(event), indent=2))
    return 0


def cmd_behavior_add(args: argparse.Namespace) -> int:
    outcomes = args.outcomes or infer_behavior_outcomes(args.feature, args.from_prompt)
    path = BehaviorStore(repo_root(args)).create_from_text(args.feature, outcomes)
    MemoryStore(repo_root(args)).record(
        MemoryEvent(
            kind="behavior",
            feature=args.feature,
            summary=f"Added behavior spec for {args.feature}",
            prompt=args.from_prompt,
            affected_files=[str(path.relative_to(repo_root(args)))],
            validation_result="not_run",
        )
    )
    print(f"created {path}")
    return 0


def cmd_behavior_list(args: argparse.Namespace) -> int:
    print(json.dumps(BehaviorStore(repo_root(args)).list(), indent=2))
    return 0


def cmd_prompt_record(args: argparse.Namespace) -> int:
    event = MemoryEvent(
        kind="prompt",
        feature=args.feature,
        summary=args.summary,
        prompt=args.request,
        affected_files=args.file,
        validation_result=args.validation,
        metadata={
            "generated_implementation": args.output,
            "retry_count": args.retry_count,
            "repository_context": CodexContext(repo_root(args)).render(),
        },
    )
    print(json.dumps(MemoryStore(repo_root(args)).record(event), indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    result = ValidationEngine(repo_root(args)).validate(args.feature)
    MemoryStore(repo_root(args)).record(validation_memory_event(result))
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "passed" else 1


def cmd_regressions(args: argparse.Namespace) -> int:
    print(json.dumps(ValidationEngine(repo_root(args)).regressions(), indent=2))
    return 0


def cmd_repair(args: argparse.Namespace) -> int:
    attempt = RepairLoop(repo_root(args)).run(args.feature)
    print(json.dumps(attempt, indent=2))
    return 0 if attempt["converged"] else 1


def cmd_codex_context(args: argparse.Namespace) -> int:
    path = CodexContext(repo_root(args)).write()
    print(f"wrote {path}")
    return 0


def cmd_sync_agents(args: argparse.Namespace) -> int:
    root = repo_root(args)
    (root / "AGENTS.md").write_text(agents_md(root.name), encoding="utf-8")
    print(f"wrote {root / 'AGENTS.md'}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    path = ReportGenerator(repo_root(args)).generate()
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
