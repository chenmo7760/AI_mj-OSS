#!/usr/bin/env python3
"""Build provider payloads and register external generation results."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import date
from pathlib import Path
from typing import Any

from assemble_prompt import assemble as assemble_prompt


def load_json(path: Path, default: Any = None) -> Any:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relpath(path: Path, base: Path) -> str:
    return path.resolve().relative_to(base.resolve()).as_posix()


def find_task(tasks: list[dict], task_id: str) -> dict:
    for task in tasks:
        if task.get("task_id") == task_id:
            return task
    raise SystemExit(f"task_id not found: {task_id}")


def find_shot(storyboard: list[dict], shot_id: str | None) -> dict | None:
    for shot in storyboard:
        if shot.get("shot_id") == shot_id:
            return shot
    return None


def media_role_inputs(task: dict) -> list[dict]:
    media = []
    if task.get("first_frame_url"):
        media.append({"role": "first_frame", "path": task.get("first_frame_url")})
    if task.get("last_frame_url"):
        media.append({"role": "last_frame", "path": task.get("last_frame_url")})
    for ref in task.get("reference_images") or []:
        media.append({"role": "reference_image", "path": ref})
    return media


def workspace_root(project_dir: Path) -> Path:
    return project_dir.parents[1]


def provider_capabilities(project_dir: Path, project: dict) -> dict[str, dict]:
    provider_file = project.get("provider_capabilities_file")
    if not provider_file:
        return {}
    path = Path(provider_file)
    if not path.is_absolute():
        path = workspace_root(project_dir) / path
    capabilities = load_json(path, {})
    return {p.get("provider_id"): p for p in capabilities.get("providers", [])}


def provider_template_for_task(provider_profile: dict | None, task_type: str | None) -> str | None:
    if not provider_profile or not task_type:
        return None
    templates = provider_profile.get("payload_templates") or {}
    return templates.get(task_type)


def provider_instructions(project_dir: Path, episode_id: str, shot_id: str | None, template_key: str | None) -> str | None:
    if not template_key:
        return None
    args = argparse.Namespace(
        prompt_key=template_key,
        project_dir=str(project_dir),
        episode=episode_id,
        shot_id=shot_id,
        registry=None,
        out=None,
    )
    return assemble_prompt(args)


def build_payload(project_dir: Path, episode_id: str, task_id: str) -> Path:
    episode_dir = project_dir / "episodes" / episode_id
    project = load_json(project_dir / "project.json", {})
    tasks = load_json(episode_dir / "tasks.json", [])
    storyboard = load_json(episode_dir / "storyboard.json", [])
    prompt_index = load_json(episode_dir / "prompts" / "prompt_index.json", [])
    task = find_task(tasks, task_id)
    shot = find_shot(storyboard, task.get("shot_id"))
    style_profile_id = task.get("style_profile_id") or (shot or {}).get("style_profile_id") or project.get("style_profile_id")
    prompt_file = task.get("prompt_file")
    prompt_text = (project_dir / prompt_file).read_text(encoding="utf-8") if prompt_file and (project_dir / prompt_file).exists() else ""
    prompt_meta = next((p for p in prompt_index if p.get("prompt_file") == prompt_file), {})
    providers = provider_capabilities(project_dir, project)
    provider_profile = providers.get(task.get("provider"))
    provider_template = provider_template_for_task(provider_profile, task.get("type"))
    payload = {
        "schema_version": "0.1.0",
        "created_at": str(date.today()),
        "provider": task.get("provider"),
        "model": task.get("model"),
        "task_id": task_id,
        "task_type": task.get("type"),
        "shot_id": task.get("shot_id"),
        "style_profile_id": style_profile_id,
        "prompt": prompt_text,
        "prompt_file": prompt_file,
        "prompt_id": prompt_meta.get("prompt_id"),
        "provider_template": provider_template,
        "provider_instructions": provider_instructions(project_dir, episode_id, task.get("shot_id"), provider_template),
        "reference_mode": task.get("reference_mode"),
        "media_inputs": media_role_inputs(task),
        "parameters": task.get("provider_params") or {},
        "metadata": {
            "episode_id": episode_id,
            "style_profile_id": style_profile_id,
            "source_events": (shot or {}).get("source_events", []),
            "characters": (shot or {}).get("characters", []),
            "expected_output": task.get("expected_output"),
        },
    }
    out_path = episode_dir / "provider_payloads" / f"{task_id}_payload.json"
    write_json(out_path, payload)
    print(f"Wrote provider payload: {out_path}")
    return out_path


def file_checksum(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def image_size(path: Path) -> tuple[int | None, int | None]:
    try:
        from PIL import Image

        with Image.open(path) as image:
            return image.size
    except Exception:
        return None, None


def resolve_result_path(project_dir: Path, result_path: str, copy_to: str | None) -> tuple[str, Path | None]:
    src = Path(result_path)
    if copy_to:
        if not src.exists():
            raise SystemExit(f"result path not found: {src}")
        dest = project_dir / copy_to
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        return relpath(dest, project_dir), dest
    if src.is_absolute():
        if src.exists() and project_dir.resolve() in src.resolve().parents:
            return relpath(src, project_dir), src
        return src.as_posix(), src if src.exists() else None
    path = project_dir / src
    return src.as_posix(), path if path.exists() else None


def register_result(args: argparse.Namespace) -> None:
    project_dir = Path(args.project_dir).resolve()
    episode_dir = project_dir / "episodes" / args.episode
    tasks_path = episode_dir / "tasks.json"
    assets_path = project_dir / "assets.json"
    storyboard_path = episode_dir / "storyboard.json"
    tasks = load_json(tasks_path, [])
    assets = load_json(assets_path, [])
    storyboard = load_json(storyboard_path, [])
    task = find_task(tasks, args.task_id)
    shot_id = task.get("shot_id")
    project = load_json(project_dir / "project.json", {})
    shot = find_shot(storyboard, shot_id)
    style_profile_id = task.get("style_profile_id") or (shot or {}).get("style_profile_id") or project.get("style_profile_id")
    group_id = args.candidate_group_id or f"cand_{shot_id}_{task.get('type')}_v{task.get('version', 1):03d}"
    candidate_index = args.candidate_index or (1 + sum(1 for asset in assets if asset.get("candidate_group_id") == group_id))
    media_type = "image" if task.get("type") == "image_generation" else "video" if task.get("type") == "video_generation" else "audio"
    stored_path, local_path = resolve_result_path(project_dir, args.result_path, args.copy_to)
    width, height = image_size(local_path) if media_type == "image" and local_path else (None, None)
    checksum = file_checksum(local_path) if local_path else None
    asset_id = args.asset_id or f"asset_{shot_id}_{media_type}_c{candidate_index:03d}_v{task.get('version', 1):03d}"

    if args.selected:
        for asset in assets:
            if asset.get("candidate_group_id") == group_id:
                asset["selected"] = False
                asset["is_active"] = False

    asset = {
        "asset_id": asset_id,
        "type": media_type,
        "style_profile_id": style_profile_id,
        "variant_id": f"c{candidate_index:03d}",
        "sequence_in_type": candidate_index - 1,
        "is_active": bool(args.selected),
        "selected_image_id": None,
        "shot_id": shot_id,
        "episode_id": args.episode,
        "version": int(task.get("version") or 1),
        "asset_version": int(task.get("version") or 1),
        "path": stored_path,
        "source": args.source or "provider_adapter",
        "provider": task.get("provider"),
        "model": task.get("model"),
        "generation_mode": task.get("generation_mode"),
        "reference_mode": task.get("reference_mode"),
        "provider_task_id": args.provider_task_id,
        "provider_request_id": args.provider_request_id,
        "prompt_file": task.get("prompt_file"),
        "candidate_group_id": group_id,
        "candidate_index": candidate_index,
        "candidate_rank": candidate_index,
        "duration_sec_actual": args.duration_sec,
        "width": width,
        "height": height,
        "fps": args.fps,
        "checksum": checksum,
        "last_frame_url": args.last_frame_url,
        "meta": {"registered_by": "provider_adapter.py"},
        "scope": "project",
        "parent_asset_id": None,
        "inherits_from": [],
        "grid_cell": {},
        "stale": False,
        "stale_reason": None,
        "quality_score": {},
        "selected": bool(args.selected),
        "rejected_reason": None,
        "review_file": None,
        "quality_notes": args.quality_notes,
        "created_at": str(date.today()),
    }
    assets.append(asset)
    task["status"] = "done"
    task["provider_task_id"] = args.provider_task_id
    task["provider_request_id"] = args.provider_request_id
    task["quality_gate_status"] = "pending_asset_review"
    task["expected_output"] = stored_path

    if args.selected:
        for shot in storyboard:
            if shot.get("shot_id") == shot_id:
                shot.setdefault("assets", {})[media_type] = asset_id
                break

    write_json(assets_path, assets)
    write_json(tasks_path, tasks)
    write_json(storyboard_path, storyboard)
    print(f"Registered asset: {asset_id}")


def fail_task(args: argparse.Namespace) -> None:
    project_dir = Path(args.project_dir).resolve()
    tasks_path = project_dir / "episodes" / args.episode / "tasks.json"
    tasks = load_json(tasks_path, [])
    task = find_task(tasks, args.task_id)
    task["status"] = "failed"
    task["retry_count"] = int(task.get("retry_count") or 0) + 1
    task["error"] = args.error
    if args.blocked_by:
        task["blocked_by"] = args.blocked_by
    write_json(tasks_path, tasks)
    print(f"Marked failed: {args.task_id} retry_count={task['retry_count']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    payload = sub.add_parser("build-payload")
    payload.add_argument("project_dir")
    payload.add_argument("--episode", default="ep01")
    payload.add_argument("--task-id", required=True)

    reg = sub.add_parser("register-result")
    reg.add_argument("project_dir")
    reg.add_argument("--episode", default="ep01")
    reg.add_argument("--task-id", required=True)
    reg.add_argument("--result-path", required=True)
    reg.add_argument("--copy-to")
    reg.add_argument("--asset-id")
    reg.add_argument("--candidate-group-id")
    reg.add_argument("--candidate-index", type=int)
    reg.add_argument("--selected", action="store_true")
    reg.add_argument("--source")
    reg.add_argument("--provider-task-id")
    reg.add_argument("--provider-request-id")
    reg.add_argument("--duration-sec", type=float)
    reg.add_argument("--fps", type=float)
    reg.add_argument("--last-frame-url")
    reg.add_argument("--quality-notes")

    fail = sub.add_parser("fail-task")
    fail.add_argument("project_dir")
    fail.add_argument("--episode", default="ep01")
    fail.add_argument("--task-id", required=True)
    fail.add_argument("--error", required=True)
    fail.add_argument("--blocked-by")

    args = parser.parse_args()
    if args.command == "build-payload":
        build_payload(Path(args.project_dir).resolve(), args.episode, args.task_id)
    elif args.command == "register-result":
        register_result(args)
    elif args.command == "fail-task":
        fail_task(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
