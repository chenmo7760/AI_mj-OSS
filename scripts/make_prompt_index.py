#!/usr/bin/env python3
"""Create a lightweight prompt_index.json from versioned prompt files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


PROMPT_RE = re.compile(r"(?P<shot>ep\d+_s\d+)_(?P<kind>image|video)_v(?P<version>\d+)\.md$")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: make_prompt_index.py <episode_dir>")
        return 2

    episode_dir = Path(sys.argv[1]).resolve()
    project_dir = episode_dir.parents[1]
    prompt_dir = episode_dir / "prompts"
    index_path = prompt_dir / "prompt_index.json"

    if not prompt_dir.exists():
        print(f"Prompt dir not found: {prompt_dir}")
        return 2

    entries = []
    for path in sorted(prompt_dir.glob("*.md")):
        match = PROMPT_RE.match(path.name)
        if not match:
            continue
        shot_id = match.group("shot")
        kind = match.group("kind")
        version = int(match.group("version"))
        rel = path.relative_to(project_dir).as_posix()
        entries.append({
            "prompt_id": f"prompt_{shot_id}_{kind}_v{version:03d}",
            "shot_id": shot_id,
            "prompt_type": kind,
            "version": version,
            "prompt_file": rel,
            "derived_from": [],
            "provider_target": None,
            "review_status": "pending",
            "review_file": None,
            "frozen": False,
            "created_at": "2026-07-07"
        })

    index_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} prompt entries: {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
