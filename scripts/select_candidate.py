#!/usr/bin/env python3
"""Suggest best candidates from assets.json quality_score fields."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


def score(asset: dict) -> float:
    quality = asset.get("quality_score") or {}
    values = [value for value in quality.values() if isinstance(value, (int, float))]
    return sum(values) / len(values) if values else 0.0


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: select_candidate.py <project_dir>")
        return 2

    project_dir = Path(sys.argv[1]).resolve()
    assets_path = project_dir / "assets.json"
    if not assets_path.exists():
        print(f"assets.json not found: {assets_path}")
        return 2

    assets = json.loads(assets_path.read_text(encoding="utf-8"))
    groups = defaultdict(list)
    for asset in assets:
        group_id = asset.get("candidate_group_id")
        if group_id:
            groups[group_id].append(asset)

    suggestions = []
    for group_id, group_assets in sorted(groups.items()):
        ranked = sorted(group_assets, key=score, reverse=True)
        best = ranked[0]
        suggestions.append({
            "candidate_group_id": group_id,
            "shot_id": best.get("shot_id"),
            "selected_asset_id": best.get("asset_id"),
            "score": score(best),
            "selection_reason": "highest average numeric quality_score",
            "rejected_asset_ids": [asset.get("asset_id") for asset in ranked[1:]]
        })

    out_path = project_dir / "assets" / "metadata" / "candidate_selection_suggestions.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(suggestions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(suggestions)} candidate suggestions: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
