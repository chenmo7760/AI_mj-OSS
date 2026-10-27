#!/usr/bin/env python3
"""Run a deterministic continuity smoke check over adjacent storyboard shots."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def as_set(value) -> set[str]:
    return {str(v) for v in (value or [])}


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: check_continuity.py <project_dir> [episode_id]")
        return 2
    project_dir = Path(sys.argv[1]).resolve()
    episode_id = sys.argv[2] if len(sys.argv) == 3 else "ep01"
    episode_dir = project_dir / "episodes" / episode_id
    storyboard = load_json(episode_dir / "storyboard.json")

    findings = []
    sorted_shots = sorted(storyboard, key=lambda s: s.get("order", 0))
    for prev, cur in zip(sorted_shots, sorted_shots[1:]):
        prev_id = prev.get("shot_id")
        cur_id = cur.get("shot_id")
        prev_chars = as_set(prev.get("characters") or prev.get("character_ids"))
        cur_chars = as_set(cur.get("characters") or cur.get("character_ids"))
        shared = prev_chars & cur_chars
        prev_costumes = prev.get("costume_overrides") or {}
        cur_costumes = cur.get("costume_overrides") or {}
        for char_id in sorted(shared):
            if prev_costumes.get(char_id) and cur_costumes.get(char_id) and prev_costumes.get(char_id) != cur_costumes.get(char_id):
                findings.append({
                    "severity": "high",
                    "from_shot": prev_id,
                    "to_shot": cur_id,
                    "character_id": char_id,
                    "issue": "costume override changes across adjacent shots"
                })
        if prev.get("continuity_to") and cur.get("continuity_from") and prev.get("continuity_to") != cur.get("shot_id"):
            findings.append({
                "severity": "medium",
                "from_shot": prev_id,
                "to_shot": cur_id,
                "issue": "continuity_to does not point to the next shot id"
            })
        prev_end = (prev.get("keyframes") or {}).get("end_frame") or (prev.get("keyframes") or {}).get("end_frame_prompt")
        cur_start = (cur.get("keyframes") or {}).get("start_frame") or (cur.get("keyframes") or {}).get("start_frame_prompt")
        if shared and not (prev_end and cur_start):
            findings.append({
                "severity": "medium",
                "from_shot": prev_id,
                "to_shot": cur_id,
                "issue": "shared character across shots without adjacent end/start frame anchors"
            })

    report = {
        "schema_version": "0.1.0",
        "episode_id": episode_id,
        "created_at": str(date.today()),
        "result": "Pass" if not findings else "Needs Fix",
        "findings": findings
    }
    out_path = episode_dir / "reports" / "continuity_check.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Continuity {report['result']}: {len(findings)} findings -> {out_path}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
