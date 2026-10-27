#!/usr/bin/env python3
"""Aggregate local gate signals for the production supervisor."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


NEGATIVE_MARKERS = ["Needs Fix", "Blocked", "Needs Human Decision"]


def load_json(path: Path, default: Any = None) -> Any:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def review_findings(reviews_dir: Path) -> list[dict]:
    findings = []
    if not reviews_dir.exists():
        return findings
    for path in sorted(reviews_dir.glob("*.md")):
        text = read_text(path)
        for marker in NEGATIVE_MARKERS:
            if marker in text:
                findings.append({"review_file": path.name, "marker": marker, "source": "markdown"})
                break
    for path in sorted(reviews_dir.glob("*.json")):
        data = load_json(path, {})
        if not isinstance(data, dict):
            continue
        result = data.get("result")
        if result in NEGATIVE_MARKERS:
            findings.append({
                "review_file": path.name,
                "marker": result,
                "source": "json",
                "target_type": data.get("target_type"),
                "target_id": data.get("target_id"),
                "required_fixes": data.get("required_fixes", []),
                "blocking_findings": data.get("blocking_findings", []),
            })
        if data.get("stale"):
            findings.append({
                "review_file": path.name,
                "marker": "Blocked",
                "source": "json",
                "target_type": data.get("target_type"),
                "target_id": data.get("target_id"),
                "required_fixes": ["refresh stale review before advancing gate"],
                "blocking_findings": ["structured review is marked stale"],
            })
    return findings


def report_findings(reports_dir: Path) -> list[dict]:
    findings = []
    if not reports_dir.exists():
        return findings
    for path in sorted(reports_dir.glob("*.json")):
        data = load_json(path, {})
        if not isinstance(data, dict):
            continue
        result = str(data.get("result", ""))
        if result and result.lower() not in {"pass", "passed", "ok"}:
            findings.append({"report_file": path.name, "result": result, "findings": data.get("findings", [])})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    parser.add_argument("--episode", default="ep01")
    parser.add_argument("--stage", default="current")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    episode_dir = project_dir / "episodes" / args.episode
    project = load_json(project_dir / "project.json", {})
    tasks = load_json(episode_dir / "tasks.json", [])
    assets = load_json(project_dir / "assets.json", [])
    stale_manifest = load_json(episode_dir / "stale_manifest.json", {})
    review_issues = review_findings(episode_dir / "reviews")
    report_issues = report_findings(episode_dir / "reports")

    task_issues = []
    for task in tasks:
        if task.get("stale"):
            task_issues.append({"task_id": task.get("task_id"), "issue": "stale task"})
        if task.get("status") == "failed":
            task_issues.append({"task_id": task.get("task_id"), "issue": task.get("error") or "failed task"})

    asset_issues = []
    for asset in assets:
        if asset.get("selected") and not asset.get("quality_notes"):
            asset_issues.append({"asset_id": asset.get("asset_id"), "issue": "selected asset missing quality_notes"})
        if asset.get("stale"):
            asset_issues.append({"asset_id": asset.get("asset_id"), "issue": "stale asset"})

    stale_items = stale_manifest.get("stale_items", []) if stale_manifest else []
    blocking = []
    blocking.extend(task_issues)
    blocking.extend(asset_issues)
    blocking.extend({"issue": "stale item", **item} for item in stale_items)
    blocking.extend({"issue": "review marker", **item} for item in review_issues if item.get("marker") in {"Blocked", "Needs Human Decision"})
    blocking.extend({"issue": "report issue", **item} for item in report_issues if item.get("result") == "Blocked")

    needs_fix = []
    needs_fix.extend({"issue": "review marker", **item} for item in review_issues if item.get("marker") == "Needs Fix")
    needs_fix.extend({"issue": "report issue", **item} for item in report_issues if item.get("result") not in {"Pass", "Blocked"})

    if blocking:
        result = "Blocked"
    elif needs_fix:
        result = "Needs Fix"
    else:
        result = "Pass"

    policy = project.get("quality_gate_policy") or {}
    report = {
        "schema_version": "0.1.0",
        "project_id": project.get("project_id"),
        "episode_id": args.episode,
        "created_at": str(date.today()),
        "stage": args.stage,
        "Production Gate Result": result,
        "Blocking Findings": blocking,
        "Required Fixes": needs_fix,
        "Accepted Risks": [],
        "Next Role": "production-supervisor" if result != "Pass" else "next-stage-executor",
        "Max Auto Fix Rounds Remaining": policy.get("max_auto_fix_rounds", 0),
        "summary": {
            "tasks": len(tasks),
            "assets": len(assets),
            "reviews_with_markers": len(review_issues),
            "reports_with_issues": len(report_issues),
            "stale_items": len(stale_items),
        }
    }
    out_path = episode_dir / "reports" / "production_gate_report.json"
    write_json(out_path, report)
    print(f"Production Gate {result}: {out_path}")
    return 1 if result == "Blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
