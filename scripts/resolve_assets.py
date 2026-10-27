#!/usr/bin/env python3
"""Resolve global/project/episode/shot asset inheritance into one view."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load_json_if_exists(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def asset_key(asset: dict) -> str:
    return asset.get("asset_id") or f"{asset.get('type')}:{asset.get('path')}"


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: resolve_assets.py <project_dir> [episode_id]")
        return 2
    project_dir = Path(sys.argv[1]).resolve()
    episode_id = sys.argv[2] if len(sys.argv) == 3 else "ep01"
    project = load_json_if_exists(project_dir / "project.json", {})
    global_file = project.get("global_asset_library") or "global_assets.json"
    global_path = project_dir / global_file
    episode_dir = project_dir / "episodes" / episode_id

    layers = [
        ("global", load_json_if_exists(global_path, [])),
        ("project", load_json_if_exists(project_dir / "assets.json", [])),
        ("episode", load_json_if_exists(episode_dir / "assets.json", [])),
    ]
    resolved: dict[str, dict] = {}
    provenance: dict[str, list[str]] = {}
    for scope, assets in layers:
        for asset in assets:
            key = asset_key(asset)
            item = dict(asset)
            item.setdefault("scope", scope)
            if key in resolved:
                item.setdefault("inherits_from", []).append(resolved[key].get("asset_id", key))
            resolved[key] = item
            provenance.setdefault(key, []).append(scope)

    out = {
        "schema_version": "0.1.0",
        "episode_id": episode_id,
        "resolution_order": [scope for scope, _ in layers],
        "assets": list(resolved.values()),
        "provenance": provenance
    }
    out_path = episode_dir / "resolved_assets.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Resolved {len(resolved)} assets: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
