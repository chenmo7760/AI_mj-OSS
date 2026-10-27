#!/usr/bin/env python3
"""Block generation tasks that are missing required upstream artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


PASS_STATUSES = {"pass", "passed", "approved", "ready"}


def load_json(path: Path, default: Any = None) -> Any:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def provider_map(project_dir: Path, project: dict) -> dict[str, dict]:
    provider_file = project.get("provider_capabilities_file")
    if not provider_file:
        return {}
    path = Path(provider_file)
    if not path.is_absolute():
        path = project_dir.parents[1] / path
    capabilities = load_json(path, {})
    return {p.get("provider_id"): p for p in capabilities.get("providers", [])}


def prompt_by_file(prompt_index: list[dict]) -> dict[str, dict]:
    return {entry.get("prompt_file"): entry for entry in prompt_index if entry.get("prompt_file")}


def route_by_shot(episode_dir: Path) -> dict[str, dict]:
    data = load_json(episode_dir / "shot_routes.json", {})
    return {route.get("shot_id"): route for route in data.get("routes", [])}


def provider_supports(provider: dict | None, task_type: str, mode: str | None) -> bool:
    if not provider or not mode:
        return True
    modes_key = "image_modes" if task_type == "image_generation" else "video_modes"
    modes = set(provider.get(modes_key) or [])
    normalized = mode.replace("_", "-")
    return normalized in modes or mode in modes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    parser.add_argument("--episode", default="ep01")
    parser.add_argument("--task-type", default="image_generation")
    parser.add_argument("--require-prompt-review", action="store_true")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    episode_dir = project_dir / "episodes" / args.episode
    project = load_json(project_dir / "project.json", {})
    storyboard = load_json(episode_dir / "storyboard.json", [])
    tasks = load_json(episode_dir / "tasks.json", [])
    prompt_index = load_json(episode_dir / "prompts" / "prompt_index.json", [])
    shots = {shot.get("shot_id"): shot for shot in storyboard}
    prompts = prompt_by_file(prompt_index)
    providers = provider_map(project_dir, project)
    routes = route_by_shot(episode_dir)

    findings = []
    checked = 0
    for task in tasks:
        if task.get("type") != args.task_type:
            continue
        checked += 1
        task_id = task.get("task_id")
        shot_id = task.get("shot_id")
        prompt_file = task.get("prompt_file")
        if task.get("stale"):
            findings.append({"severity": "high", "task_id": task_id, "issue": "task is stale"})
        if shot_id not in shots:
            findings.append({"severity": "high", "task_id": task_id, "issue": f"missing shot: {shot_id}"})
        if prompt_file and not (project_dir / prompt_file).exists():
            findings.append({"severity": "high", "task_id": task_id, "issue": f"prompt file missing: {prompt_file}"})
        prompt = prompts.get(prompt_file)
        if not prompt:
            findings.append({"severity": "high", "task_id": task_id, "issue": "prompt_index entry missing"})
        elif prompt.get("stale"):
            findings.append({"severity": "high", "task_id": task_id, "issue": "prompt is stale"})
        elif args.require_prompt_review and str(prompt.get("review_status", "")).lower() not in PASS_STATUSES:
            findings.append({"severity": "high", "task_id": task_id, "issue": "prompt reviewer has not passed"})
        provider = task.get("provider")
        provider_profile = providers.get(provider)
        if providers and provider and provider not in providers:
            findings.append({"severity": "medium", "task_id": task_id, "issue": f"provider not registered: {provider}"})
        route = routes.get(shot_id)
        if route:
            missing_inputs = route.get("missing_inputs") or []
            if missing_inputs:
                findings.append({"severity": "high", "task_id": task_id, "issue": f"route has missing inputs: {missing_inputs}"})
            route_mode = route.get("route")
            if not provider_supports(provider_profile, args.task_type, route_mode):
                findings.append({"severity": "high", "task_id": task_id, "issue": f"provider does not support route: {route_mode}"})
        if args.task_type == "video_generation":
            reference_mode = (task.get("reference_mode") or "").replace("-", "_")
            route_name = ((route or {}).get("route") or "").replace("-", "_")
            if ("first_last" in reference_mode or "first_last" in route_name) and (not task.get("first_frame_url") or not task.get("last_frame_url")):
                findings.append({"severity": "high", "task_id": task_id, "issue": "first-last video task missing first or last frame"})

    report = {
        "schema_version": "0.1.0",
        "episode_id": args.episode,
        "task_type": args.task_type,
        "created_at": str(date.today()),
        "result": "Pass" if not findings else "Blocked",
        "checked_tasks": checked,
        "findings": findings,
    }
    out_path = episode_dir / "reports" / f"generation_readiness_{args.task_type}.json"
    write_json(out_path, report)
    print(f"Generation readiness {report['result']}: {checked} tasks, {len(findings)} findings -> {out_path}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
