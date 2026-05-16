from __future__ import annotations

from pathlib import Path

from codexpy.models import MemoryEvent, slugify, utc_now
from codexpy.paths import RepoPaths
from codexpy.storage import read_json, write_json


class MemoryStore:
    def __init__(self, root: Path) -> None:
        self.paths = RepoPaths(root)
        self.paths.ensure_state()

    def _load(self) -> dict:
        return read_json(
            self.paths.memory_file,
            {
                "version": 1,
                "created_at": utc_now(),
                "events": [],
                "features": {},
                "decisions": {},
            },
        )

    def _save(self, data: dict) -> None:
        write_json(self.paths.memory_file, data)

    def record(self, event: MemoryEvent) -> dict:
        data = self._load()
        event_data = event.to_dict()
        data.setdefault("events", []).append(event_data)
        if event.feature:
            feature_key = slugify(event.feature)
            feature = data.setdefault("features", {}).setdefault(
                feature_key,
                {
                    "id": feature_key,
                    "name": event.feature,
                    "created_at": event.timestamp,
                    "events": [],
                    "affected_files": [],
                },
            )
            feature["updated_at"] = event.timestamp
            feature.setdefault("events", []).append(event.event_id)
            feature["affected_files"] = sorted(
                set(feature.get("affected_files", [])) | set(event.affected_files)
            )
        if event.kind == "decision":
            decision_key = slugify(event.summary)
            data.setdefault("decisions", {})[decision_key] = {
                "id": decision_key,
                "timestamp": event.timestamp,
                "summary": event.summary,
                "decision_summary": event.decision_summary or event.summary,
                "feature": event.feature,
                "affected_files": event.affected_files,
            }
        self._save(data)
        self._write_sidecar(event)
        return event_data

    def _write_sidecar(self, event: MemoryEvent) -> None:
        slug = slugify(event.summary)
        body = [
            f"# {event.summary}",
            "",
            f"- id: `{event.event_id}`",
            f"- timestamp: `{event.timestamp}`",
            f"- kind: `{event.kind}`",
            f"- feature: `{event.feature or 'none'}`",
            f"- validation: `{event.validation_result}`",
            "",
        ]
        if event.prompt:
            body.extend(["## Prompt", "", event.prompt, ""])
        if event.decision_summary:
            body.extend(["## Decision Summary", "", event.decision_summary, ""])
        if event.rationale:
            body.extend(["## Rationale", "", event.rationale, ""])
        if event.affected_files:
            body.extend(["## Affected Files", ""])
            body.extend(f"- `{path}`" for path in event.affected_files)
            body.append("")

        if event.kind == "prompt":
            directory = self.paths.prompts
        elif event.kind == "decision":
            directory = self.paths.decisions
        else:
            directory = self.paths.state / "events"
            directory.mkdir(parents=True, exist_ok=True)
        (directory / f"{event.timestamp[:10]}-{slug}.md").write_text(
            "\n".join(body), encoding="utf-8"
        )

    def list_events(self, kind: str | None = None) -> list[dict]:
        events = self._load().get("events", [])
        if kind:
            return [event for event in events if event.get("kind") == kind]
        return events

    def show_feature(self, feature: str) -> dict | None:
        data = self._load()
        feature_key = slugify(feature)
        result = data.get("features", {}).get(feature_key)
        if not result:
            return None
        event_ids = set(result.get("events", []))
        result = dict(result)
        result["event_details"] = [
            event for event in data.get("events", []) if event.get("id") in event_ids
        ]
        return result

    def decisions_timeline(self) -> list[dict]:
        return sorted(self._load().get("decisions", {}).values(), key=lambda item: item["timestamp"])
