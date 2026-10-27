#!/usr/bin/env python3
"""Compose selected shot videos into an episode draft with FFmpeg."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_asset_path(project_dir: Path, asset_path: str | None) -> Path | None:
    if not asset_path:
        return None
    path = Path(asset_path)
    if path.is_absolute():
        return path
    return project_dir / path


def selected_video_by_shot(assets: list[dict]) -> dict[str, dict]:
    selected: dict[str, dict] = {}
    for asset in assets:
        if not asset.get("selected"):
            continue
        if asset.get("type") != "video":
            continue
        shot_id = asset.get("shot_id")
        if shot_id and shot_id not in selected:
            selected[shot_id] = asset
    return selected


def find_optional_file(episode_dir: Path, candidates: list[str]) -> Path | None:
    for rel in candidates:
        path = episode_dir / rel
        if path.exists():
            return path
    return None


def build_plan(project_dir: Path, episode_id: str, output: Path) -> dict:
    episode_dir = project_dir / "episodes" / episode_id
    storyboard = load_json(episode_dir / "storyboard.json")
    assets = load_json(project_dir / "assets.json")
    videos = selected_video_by_shot(assets)

    segments = []
    findings = []
    for shot in sorted(storyboard, key=lambda item: item.get("order", 0)):
        shot_id = shot.get("shot_id")
        asset = videos.get(shot_id)
        if not asset:
            findings.append({"shot_id": shot_id, "issue": "missing selected video asset"})
            continue
        path = resolve_asset_path(project_dir, asset.get("path"))
        if not path or not path.exists():
            findings.append({"shot_id": shot_id, "asset_id": asset.get("asset_id"), "issue": "selected video file not found", "path": asset.get("path")})
            continue
        segments.append({"shot_id": shot_id, "asset_id": asset.get("asset_id"), "path": str(path)})

    subtitles = find_optional_file(episode_dir, ["subtitles.srt", "subtitles/ep01.srt"])
    audio = find_optional_file(episode_dir, ["audio/final_mix.wav", "audio/final_mix.mp3", "voice/final_mix.wav", "voice/final_mix.mp3"])

    return {
        "schema_version": "0.1.0",
        "episode_id": episode_id,
        "created_at": str(date.today()),
        "result": "Blocked" if findings else "Pass",
        "output": str(output),
        "segments": segments,
        "subtitles": str(subtitles) if subtitles else None,
        "audio": str(audio) if audio else None,
        "findings": findings,
    }


def ffmpeg_escape(path: Path) -> str:
    return str(path).replace("\\", "/").replace("'", r"'\''")


def compose(project_dir: Path, episode_id: str, plan: dict, output: Path) -> int:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("ffmpeg not found on PATH")
        return 2

    episode_dir = project_dir / "episodes" / episode_id
    output.parent.mkdir(parents=True, exist_ok=True)
    concat_file = episode_dir / "output" / "concat_list.txt"
    concat_file.parent.mkdir(parents=True, exist_ok=True)

    lines = [f"file '{ffmpeg_escape(Path(segment['path']))}'" for segment in plan["segments"]]
    concat_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    cmd = [ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file)]

    audio = plan.get("audio")
    if audio:
        cmd += ["-i", audio, "-shortest"]

    vf = []
    subtitles = plan.get("subtitles")
    if subtitles:
        subtitle_path = ffmpeg_escape(Path(subtitles))
        vf.append(f"subtitles='{subtitle_path}'")

    if vf:
        cmd += ["-vf", ",".join(vf)]

    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    if audio:
        cmd += ["-c:a", "aac"]
    cmd += [str(output)]

    print("Running:", " ".join(cmd))
    return subprocess.run(cmd, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    parser.add_argument("--episode", default="ep01")
    parser.add_argument("--output", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    episode_dir = project_dir / "episodes" / args.episode
    output = Path(args.output) if args.output else episode_dir / "output" / f"{args.episode}_draft.mp4"
    if not output.is_absolute():
        output = project_dir / output

    plan = build_plan(project_dir, args.episode, output)
    plan_path = episode_dir / "reports" / "export_compose_plan.json"
    write_json(plan_path, plan)
    print(f"Wrote compose plan: {plan_path}")

    if plan["result"] != "Pass":
        print("Compose blocked:")
        for finding in plan["findings"]:
            print(f"- {finding}")
        return 1

    if args.dry_run:
        print("Dry run passed; no FFmpeg command executed.")
        return 0

    return compose(project_dir, args.episode, plan, output)


if __name__ == "__main__":
    raise SystemExit(main())
