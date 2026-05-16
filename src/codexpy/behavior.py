from __future__ import annotations

import re
from pathlib import Path

from codexpy.models import BehaviorSpec, slugify
from codexpy.paths import RepoPaths
from codexpy.storage import read_json, write_json


class BehaviorStore:
    def __init__(self, root: Path) -> None:
        self.paths = RepoPaths(root)
        self.paths.ensure_state()

    def add(self, spec: BehaviorSpec) -> Path:
        data = spec.to_dict()
        path = self.paths.behaviors / f"{spec.behavior_id}.json"
        write_json(path, data)
        hidden_path = self.paths.behaviors_hidden / f"{spec.behavior_id}.json"
        write_json(hidden_path, data)
        return path

    def create_from_text(self, feature: str, outcomes: list[str]) -> Path:
        normalized = [item.strip() for item in outcomes if item.strip()]
        checks = [{"type": "text", "target": outcome} for outcome in normalized]
        spec = BehaviorSpec(
            feature=feature,
            expected_outcomes=normalized,
            regression_expectations=normalized,
            checks=checks,
        )
        return self.add(spec)

    def list(self) -> list[dict]:
        specs: list[dict] = []
        for path in sorted(self.paths.behaviors.glob("*.json")):
            specs.append(read_json(path, {}))
        return specs

    def get(self, feature: str) -> dict | None:
        feature_id = slugify(feature)
        path = self.paths.behaviors / f"{feature_id}.json"
        if path.exists():
            return read_json(path, {})
        for spec in self.list():
            if slugify(spec.get("feature", "")) == feature_id or spec.get("id") == feature_id:
                return spec
        return None


def infer_behavior_outcomes(feature: str, prompt: str) -> list[str]:
    text = prompt.strip()
    candidates = [
        line.strip(" -\t")
        for line in text.splitlines()
        if line.strip().startswith(("-", "*")) and len(line.strip(" -\t")) > 3
    ]
    if candidates:
        return candidates[:8]

    words = re.findall(r"[A-Za-z0-9_'-]+", feature)
    readable_feature = " ".join(words).strip() or "feature"
    return [
        f"{readable_feature} primary workflow continues to work",
        f"{readable_feature} invalid inputs are rejected safely",
        f"{readable_feature} existing validated behavior remains unchanged",
    ]
