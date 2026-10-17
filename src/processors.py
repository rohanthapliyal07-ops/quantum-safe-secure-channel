"""Platform profile loading retained under the repository's original module name."""
from __future__ import annotations
import json
from pathlib import Path


def load_platforms(config_dir: str | Path = "processors") -> dict[str, dict]:
    base = Path(config_dir)
    profiles = {}
    for letter in ("A", "B"):
        path = base / f"processor_{letter}.json"
        profiles[letter] = json.loads(path.read_text(encoding="utf-8"))
    return profiles
