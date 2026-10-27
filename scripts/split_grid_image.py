#!/usr/bin/env python3
"""Split a generated grid image into traceable cell crops."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

from PIL import Image


def load_json(path: Path, default: Any = None) -> Any:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relpath(path: Path, base: Path) -> str:
    return path.resolve().relative_to(base.resolve()).as_posix()


def resolve_project_path(project_dir: Path, path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return (project_dir / path).resolve()


def find_grid(assignments: dict, grid_id: str) -> dict:
    for grid in assignments.get("grids", []):
        if grid.get("grid_id") == grid_id:
            return grid
    raise SystemExit(f"grid_id not found: {grid_id}")


def source_image_path(project_dir: Path, grid: dict, explicit_image: str | None) -> Path:
    if explicit_image:
        return resolve_project_path(project_dir, explicit_image)
    source_asset_id = grid.get("source_asset_id")
    if not source_asset_id:
        raise SystemExit("Grid has no source_asset_id; pass --image.")
    for asset in load_json(project_dir / "assets.json", []):
        if asset.get("asset_id") == source_asset_id:
            asset_path = asset.get("path")
            if not asset_path:
                raise SystemExit(f"Source asset has no path: {source_asset_id}")
            return resolve_project_path(project_dir, asset_path)
    raise SystemExit(f"source_asset_id not found in assets.json: {source_asset_id}")


def cell_bounds(width: int, height: int, rows: int, cols: int, row_zero: int, col_zero: int) -> tuple[int, int, int, int]:
    left = round(col_zero * width / cols)
    right = round((col_zero + 1) * width / cols)
    top = round(row_zero * height / rows)
    bottom = round((row_zero + 1) * height / rows)
    return left, top, right, bottom


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    parser.add_argument("episode_id")
    parser.add_argument("grid_id")
    parser.add_argument("--image", help="Source grid image path. Relative paths resolve from project_dir.")
    parser.add_argument("--out-dir", default="assets/candidates/grid-cells")
    parser.add_argument("--no-update", action="store_true", help="Do not update grid_assignments.json.")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    episode_dir = project_dir / "episodes" / args.episode_id
    assignments_path = episode_dir / "grid" / "grid_assignments.json"
    assignments = load_json(assignments_path, {})
    grid = find_grid(assignments, args.grid_id)
    rows = int(grid.get("rows") or 0)
    cols = int(grid.get("cols") or 0)
    if rows <= 0 or cols <= 0:
        raise SystemExit("Grid rows and cols must be positive.")

    image_path = source_image_path(project_dir, grid, args.image)
    if not image_path.exists():
        raise SystemExit(f"Source grid image not found: {image_path}")

    out_dir = resolve_project_path(project_dir, args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    crops = []
    with Image.open(image_path) as image:
        width, height = image.size
        for cell in grid.get("cells", []):
            index = int(cell.get("cell_index"))
            if index < 1 or index > rows * cols:
                raise SystemExit(f"cell_index out of range for {args.grid_id}: {index}")
            row_zero = int(cell.get("row") or 1) - 1
            col_zero = int(cell.get("col") or 1) - 1
            if row_zero < 0 or row_zero >= rows or col_zero < 0 or col_zero >= cols:
                row_zero = (index - 1) // cols
                col_zero = (index - 1) % cols
                cell["row"] = row_zero + 1
                cell["col"] = col_zero + 1
            left, top, right, bottom = cell_bounds(width, height, rows, cols, row_zero, col_zero)
            frame_type = (cell.get("frame_type") or "reference").replace("/", "_")
            out_name = f"{args.grid_id}_cell{index:02d}_{frame_type}.png"
            out_path = out_dir / out_name
            image.crop((left, top, right, bottom)).save(out_path)
            crop_rel = relpath(out_path, project_dir)
            cell["crop_path"] = crop_rel
            crops.append({
                "cell_index": index,
                "row": row_zero + 1,
                "col": col_zero + 1,
                "shot_id": cell.get("shot_id"),
                "frame_type": cell.get("frame_type"),
                "crop_path": crop_rel,
                "bounds": {"left": left, "top": top, "right": right, "bottom": bottom},
            })

    manifest = {
        "schema_version": "0.1.0",
        "episode_id": args.episode_id,
        "grid_id": args.grid_id,
        "source_image": relpath(image_path, project_dir),
        "created_at": str(date.today()),
        "rows": rows,
        "cols": cols,
        "crops": crops,
    }
    manifest_path = episode_dir / "grid" / f"{args.grid_id}_split_manifest.json"
    write_json(manifest_path, manifest)
    if not args.no_update:
        write_json(assignments_path, assignments)

    print(f"Split {len(crops)} cells from {image_path}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
