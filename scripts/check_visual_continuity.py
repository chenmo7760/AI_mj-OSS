#!/usr/bin/env python3
"""Compare adjacent shot frame images with lightweight visual metrics."""

from __future__ import annotations

import json
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_path(project_dir: Path, value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    return project_dir / path


def average_rgb(path: Path) -> tuple[float, float, float]:
    with Image.open(path).convert("RGB") as image:
        thumb = image.resize((64, 64))
        return tuple(float(v) for v in ImageStat.Stat(thumb).mean[:3])


def brightness(rgb: tuple[float, float, float]) -> float:
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def dhash(path: Path, size: int = 8) -> int:
    with Image.open(path).convert("L") as image:
        image = image.resize((size + 1, size))
        pixels = list(image.getdata())
    value = 0
    for row in range(size):
        for col in range(size):
            left = pixels[row * (size + 1) + col]
            right = pixels[row * (size + 1) + col + 1]
            value = (value << 1) | int(left > right)
    return value


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: check_visual_continuity.py <project_dir> [episode_id]")
        return 2

    project_dir = Path(sys.argv[1]).resolve()
    episode_id = sys.argv[2] if len(sys.argv) == 3 else "ep01"
    episode_dir = project_dir / "episodes" / episode_id
    storyboard = load_json(episode_dir / "storyboard.json")
    findings = []
    comparisons = []

    sorted_shots = sorted(storyboard, key=lambda s: s.get("order", 0))
    for prev, cur in zip(sorted_shots, sorted_shots[1:]):
        prev_id = prev.get("shot_id")
        cur_id = cur.get("shot_id")
        prev_end = resolve_path(project_dir, (prev.get("keyframes") or {}).get("end_frame"))
        cur_start = resolve_path(project_dir, (cur.get("keyframes") or {}).get("start_frame"))
        if not prev_end or not cur_start:
            findings.append({
                "severity": "medium",
                "from_shot": prev_id,
                "to_shot": cur_id,
                "issue": "missing actual end/start frame file for visual comparison"
            })
            continue
        if not prev_end.exists() or not cur_start.exists():
            findings.append({
                "severity": "high",
                "from_shot": prev_id,
                "to_shot": cur_id,
                "issue": "frame path does not exist",
                "prev_end": str(prev_end),
                "cur_start": str(cur_start)
            })
            continue

        prev_rgb = average_rgb(prev_end)
        cur_rgb = average_rgb(cur_start)
        color_delta = math.sqrt(sum((a - b) ** 2 for a, b in zip(prev_rgb, cur_rgb)))
        brightness_delta = abs(brightness(prev_rgb) - brightness(cur_rgb))
        hash_delta = hamming(dhash(prev_end), dhash(cur_start))
        prev_size = image_size(prev_end)
        cur_size = image_size(cur_start)
        size_mismatch = prev_size != cur_size
        comparison = {
            "from_shot": prev_id,
            "to_shot": cur_id,
            "prev_end": str(prev_end),
            "cur_start": str(cur_start),
            "prev_size": prev_size,
            "cur_size": cur_size,
            "color_delta": round(color_delta, 2),
            "brightness_delta": round(brightness_delta, 2),
            "dhash_hamming": hash_delta,
        }
        comparisons.append(comparison)
        if size_mismatch:
            findings.append({**comparison, "severity": "medium", "issue": "frame size mismatch"})
        if color_delta > 90 or brightness_delta > 55:
            findings.append({**comparison, "severity": "medium", "issue": "large color or brightness jump"})
        if hash_delta > 48:
            findings.append({**comparison, "severity": "low", "issue": "large structural image difference; human review recommended"})

    report = {
        "schema_version": "0.1.0",
        "episode_id": episode_id,
        "created_at": str(date.today()),
        "result": "Pass" if not findings else "Needs Review",
        "comparisons": comparisons,
        "findings": findings,
        "limits": [
            "This is a lightweight visual metric check, not face recognition.",
            "Use it to catch missing files, hard style jumps, and obvious frame discontinuity before human review."
        ]
    }
    out_path = episode_dir / "reports" / "visual_continuity_check.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Visual continuity {report['result']}: {len(findings)} findings -> {out_path}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
