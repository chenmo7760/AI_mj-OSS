#!/usr/bin/env python3
"""Mark downstream files as stale after an upstream artifact changes."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def affected_shots(storyboard: list[dict], source_type: str, source_id: str) -> set[str]:
    if source_type in {"character", "characters"}:
        return {
            s.get("shot_id")
            for s in storyboard
            if source_id in (s.get("characters") or []) or source_id in (s.get("character_ids") or [])
        }
    if source_type in {"source_event", "event"}:
        return {s.get("shot_id") for s in storyboard if source_id in (s.get("source_events") or [])}
    if source_type in {"shot", "storyboard"}:
        return {source_id}
    return set()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    parser.add_argument("source_type")
    parser.add_argument("source_id")
    parser.add_argument("--episode", default="ep01")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    episode_dir = project_dir / "episodes" / args.episode
    storyboard_path = episode_dir / "storyboard.json"
    prompt_index_path = episode_dir / "prompts" / "prompt_index.json"
    tasks_path = episode_dir / "tasks.json"
    assets_path = project_dir / "assets.json"
    grid_path = episode_dir / "grid" / "grid_assignments.json"
    delivery_path = episode_dir / "delivery" / "delivery_manifest.json"
    resolved_assets_path = episode_dir / "resolved_assets.json"
    shot_routes_path = episode_dir / "shot_routes.json"

    storyboard = load_json(storyboard_path)
    prompt_index = load_json(prompt_index_path)
    tasks = load_json(tasks_path)
    assets = load_json(assets_path)
    grid_assignments = load_json(grid_path) if grid_path.exists() else None
    delivery_manifest = load_json(delivery_path) if delivery_path.exists() else None
    resolved_assets = load_json(resolved_assets_path) if resolved_assets_path.exists() else None
    shot_routes = load_json(shot_routes_path) if shot_routes_path.exists() else None
    shots = affected_shots(storyboard, args.source_type, args.source_id)
    reason = f"{args.source_type}:{args.source_id} changed"

    stale_items = []
    for shot in storyboard:
        if shot.get("shot_id") in shots:
            shot["stale"] = True
            shot["stale_reason"] = reason
            stale_items.append({"target_type": "shot", "target_id": shot.get("shot_id"), "target_file": "storyboard.json", "reason": reason, "severity": "high"})

    for prompt in prompt_index:
        if prompt.get("shot_id") in shots:
            prompt["stale"] = True
            prompt["stale_reason"] = reason
            stale_items.append({"target_type": "prompt", "target_id": prompt.get("prompt_id"), "target_file": prompt.get("prompt_file"), "reason": reason, "severity": "high"})

    for task in tasks:
        if task.get("shot_id") in shots:
            task["stale"] = True
            task["stale_reason"] = reason
            stale_items.append({"target_type": "task", "target_id": task.get("task_id"), "target_file": "tasks.json", "reason": reason, "severity": "medium"})

    for asset in assets:
        if asset.get("shot_id") in shots:
            asset["stale"] = True
            asset["stale_reason"] = reason
            stale_items.append({"target_type": "asset", "target_id": asset.get("asset_id"), "target_file": "assets.json", "reason": reason, "severity": "medium"})

    if grid_assignments:
        for grid in grid_assignments.get("grids", []):
            touched = False
            for cell in grid.get("cells", []):
                if cell.get("shot_id") in shots:
                    cell["stale"] = True
                    cell["stale_reason"] = reason
                    touched = True
                    stale_items.append({
                        "target_type": "grid_cell",
                        "target_id": f"{grid.get('grid_id')}:cell{cell.get('cell_index')}",
                        "target_file": "grid/grid_assignments.json",
                        "reason": reason,
                        "severity": "medium"
                    })
            if touched:
                grid["stale"] = True
                grid["stale_reason"] = reason

    if shot_routes:
        for route in shot_routes.get("routes", []):
            if route.get("shot_id") in shots:
                route["stale"] = True
                route["stale_reason"] = reason
                stale_items.append({"target_type": "shot_route", "target_id": route.get("shot_id"), "target_file": "shot_routes.json", "reason": reason, "severity": "medium"})

    if resolved_assets:
        for asset in resolved_assets.get("assets", []):
            if asset.get("shot_id") in shots:
                asset["stale"] = True
                asset["stale_reason"] = reason
                stale_items.append({"target_type": "resolved_asset", "target_id": asset.get("asset_id"), "target_file": "resolved_assets.json", "reason": reason, "severity": "medium"})

    if delivery_manifest:
        delivery_manifest["stale"] = True
        delivery_manifest["stale_reason"] = reason
        stale_items.append({"target_type": "delivery_manifest", "target_id": args.episode, "target_file": "delivery/delivery_manifest.json", "reason": reason, "severity": "medium"})

    for folder_name in ["reviews", "reports"]:
        folder = episode_dir / folder_name
        if folder.exists():
            for path in sorted(folder.glob("*")):
                if path.is_file():
                    stale_items.append({
                        "target_type": folder_name.rstrip("s"),
                        "target_id": path.name,
                        "target_file": f"{folder_name}/{path.name}",
                        "reason": reason,
                        "severity": "low"
                    })

    manifest = {
        "schema_version": "0.1.0",
        "episode_id": args.episode,
        "created_at": str(date.today()),
        "source_change": {"source_type": args.source_type, "source_id": args.source_id},
        "stale_items": stale_items
    }

    if args.dry_run:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0

    write_json(storyboard_path, storyboard)
    write_json(prompt_index_path, prompt_index)
    write_json(tasks_path, tasks)
    write_json(assets_path, assets)
    if grid_assignments:
        write_json(grid_path, grid_assignments)
    if delivery_manifest:
        write_json(delivery_path, delivery_manifest)
    if resolved_assets:
        write_json(resolved_assets_path, resolved_assets)
    if shot_routes:
        write_json(shot_routes_path, shot_routes)
    out_path = episode_dir / "stale_manifest.json"
    write_json(out_path, manifest)
    print(f"Marked {len(stale_items)} stale items: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
