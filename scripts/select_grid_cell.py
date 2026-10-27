#!/usr/bin/env python3
"""Select a grid cell and wire the crop into storyboard/tasks/assets metadata."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


def load_json(path: Path, default: Any = None) -> Any:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_grid(assignments: dict, grid_id: str) -> dict:
    for grid in assignments.get("grids", []):
        if grid.get("grid_id") == grid_id:
            return grid
    raise SystemExit(f"grid_id not found: {grid_id}")


def find_cell(grid: dict, cell_index: int) -> dict:
    for cell in grid.get("cells", []):
        if int(cell.get("cell_index")) == cell_index:
            return cell
    raise SystemExit(f"cell_index not found in {grid.get('grid_id')}: {cell_index}")


def upsert_asset(assets: list[dict], asset: dict) -> None:
    for index, existing in enumerate(assets):
        if existing.get("asset_id") == asset.get("asset_id"):
            assets[index] = {**existing, **asset}
            return
    assets.append(asset)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    parser.add_argument("episode_id")
    parser.add_argument("grid_id")
    parser.add_argument("cell_index", type=int)
    parser.add_argument("--notes")
    parser.add_argument("--no-storyboard", action="store_true")
    parser.add_argument("--no-tasks", action="store_true")
    parser.add_argument("--no-assets", action="store_true")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    episode_dir = project_dir / "episodes" / args.episode_id
    assignments_path = episode_dir / "grid" / "grid_assignments.json"
    storyboard_path = episode_dir / "storyboard.json"
    tasks_path = episode_dir / "tasks.json"
    assets_path = project_dir / "assets.json"
    project = load_json(project_dir / "project.json", {})

    assignments = load_json(assignments_path, {})
    grid = find_grid(assignments, args.grid_id)
    selected_cell = find_cell(grid, args.cell_index)
    crop_path = selected_cell.get("crop_path")
    if not crop_path:
        raise SystemExit("Selected cell has no crop_path. Run split_grid_image.py first.")
    shot_id = selected_cell.get("shot_id")
    frame_type = selected_cell.get("frame_type")

    for cell in grid.get("cells", []):
        if cell.get("shot_id") == shot_id and cell.get("frame_type") == frame_type:
            cell["selected"] = int(cell.get("cell_index")) == args.cell_index
    selected_cell["selected"] = True
    if args.notes:
        selected_cell["notes"] = args.notes

    updates = ["grid_assignments"]

    if not args.no_storyboard:
        storyboard = load_json(storyboard_path, [])
        for shot in storyboard:
            if shot.get("shot_id") != shot_id:
                continue
            keyframes = shot.setdefault("keyframes", {})
            if frame_type == "first_frame":
                keyframes["start_frame"] = crop_path
            elif frame_type == "last_frame":
                keyframes["end_frame"] = crop_path
            else:
                refs = shot.setdefault("reference_images", [])
                ref = {"type": "grid_cell", "path": crop_path, "grid_id": args.grid_id, "cell_index": args.cell_index}
                if ref not in refs:
                    refs.append(ref)
            updates.append("storyboard")
            break
        write_json(storyboard_path, storyboard)

    if not args.no_tasks:
        tasks = load_json(tasks_path, [])
        for task in tasks:
            if task.get("shot_id") != shot_id:
                continue
            if task.get("type") != "video_generation":
                continue
            if frame_type == "first_frame":
                task["first_frame_url"] = crop_path
            elif frame_type == "last_frame":
                task["last_frame_url"] = crop_path
            else:
                refs = task.setdefault("reference_images", [])
                if crop_path not in refs:
                    refs.append(crop_path)
            updates.append("tasks")
        write_json(tasks_path, tasks)

    if not args.no_assets:
        assets = load_json(assets_path, [])
        parent_asset = next((asset for asset in assets if asset.get("asset_id") == grid.get("source_asset_id")), {})
        asset_id = f"asset_{shot_id}_{frame_type}_{args.grid_id}_cell{args.cell_index:02d}_v001"
        upsert_asset(assets, {
            "asset_id": asset_id,
            "type": "image",
            "style_profile_id": parent_asset.get("style_profile_id") or project.get("style_profile_id"),
            "variant_id": f"grid_cell_{args.cell_index:02d}",
            "sequence_in_type": args.cell_index,
            "is_active": True,
            "selected_image_id": None,
            "shot_id": shot_id,
            "episode_id": args.episode_id,
            "version": 1,
            "asset_version": 1,
            "path": crop_path,
            "source": "nine_grid_crop",
            "provider": parent_asset.get("provider") or "manual_web",
            "model": parent_asset.get("model") or "to_be_confirmed",
            "generation_mode": parent_asset.get("generation_mode") or "manual_web",
            "reference_mode": "nine_grid",
            "provider_task_id": None,
            "provider_request_id": None,
            "prompt_file": grid.get("prompt_file"),
            "candidate_group_id": args.grid_id,
            "candidate_index": args.cell_index,
            "candidate_rank": 1,
            "duration_sec_actual": None,
            "width": None,
            "height": None,
            "fps": None,
            "checksum": None,
            "last_frame_url": None,
            "meta": {"frame_type": frame_type},
            "scope": "project",
            "parent_asset_id": grid.get("source_asset_id"),
            "inherits_from": [grid.get("source_asset_id")] if grid.get("source_asset_id") else [],
            "grid_cell": {
                "grid_id": args.grid_id,
                "cell_index": args.cell_index,
                "row": selected_cell.get("row"),
                "col": selected_cell.get("col"),
                "frame_type": frame_type,
            },
            "stale": False,
            "stale_reason": None,
            "quality_score": {},
            "selected": True,
            "rejected_reason": None,
            "review_file": None,
            "quality_notes": f"Selected grid cell for {shot_id} {frame_type}.",
            "created_at": str(date.today()),
        })
        updates.append("assets")
        write_json(assets_path, assets)

    write_json(assignments_path, assignments)
    selection = {
        "schema_version": "0.1.0",
        "episode_id": args.episode_id,
        "grid_id": args.grid_id,
        "selected_at": str(date.today()),
        "selected_cell": selected_cell,
        "updated": sorted(set(updates)),
    }
    selection_path = episode_dir / "grid" / f"{args.grid_id}_selection.json"
    write_json(selection_path, selection)
    print(f"Selected cell {args.cell_index} for {shot_id} {frame_type}: {crop_path}")
    print(f"Selection: {selection_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
