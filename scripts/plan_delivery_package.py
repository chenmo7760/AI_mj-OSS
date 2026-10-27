#!/usr/bin/env python3
"""Create a delivery manifest for downstream editing and archive."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: plan_delivery_package.py <project_dir> [episode_id]")
        return 2
    project_dir = Path(sys.argv[1]).resolve()
    episode_id = sys.argv[2] if len(sys.argv) == 3 else "ep01"
    episode_dir = project_dir / "episodes" / episode_id
    storyboard = load_json(episode_dir / "storyboard.json")
    prompt_index = load_json(episode_dir / "prompts" / "prompt_index.json")
    assets = load_json(project_dir / "assets.json")
    selected_assets = [a for a in assets if a.get("selected")]
    files = [
        {"role": "storyboard", "path": f"episodes/{episode_id}/storyboard.json", "required": True},
        {"role": "prompt_index", "path": f"episodes/{episode_id}/prompts/prompt_index.json", "required": True},
        {"role": "subtitles", "path": f"episodes/{episode_id}/subtitles.srt", "required": False},
        {"role": "quality_gate", "path": f"episodes/{episode_id}/quality_gate.md", "required": True},
    ]
    for prompt in prompt_index:
        files.append({"role": f"prompt_{prompt.get('prompt_type')}", "path": prompt.get("prompt_file"), "required": True})
    for asset in selected_assets:
        files.append({"role": f"selected_{asset.get('type')}", "path": asset.get("path"), "required": False, "asset_id": asset.get("asset_id")})
    for shot in storyboard:
        files.append({"role": "shot_segment_placeholder", "path": f"output/segments/{shot.get('shot_id')}.mp4", "required": False, "shot_id": shot.get("shot_id")})

    manifest = {
        "schema_version": "0.1.0",
        "episode_id": episode_id,
        "created_at": str(date.today()),
        "packages": [
            {
                "package_id": f"{episode_id}_editor_handoff_v001",
                "format": "folder_or_zip",
                "files": files,
                "notes": "Includes prompt package, source metadata, selected assets, subtitles, and shot segment placeholders for NLE handoff."
            }
        ]
    }
    out_path = episode_dir / "delivery" / "delivery_manifest.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote delivery manifest: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
