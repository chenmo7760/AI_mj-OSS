#!/usr/bin/env python3
"""Assemble a prompt from prompt_templates registry slots and project context."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path, default: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else default


def workspace_root(project_dir: Path) -> Path:
    return project_dir.parents[1]


def find_template(registry: dict, prompt_key: str) -> dict:
    for template in registry.get("templates", []):
        if template.get("prompt_key") == prompt_key:
            return template
    raise SystemExit(f"Unknown prompt_key: {prompt_key}")


def shot_by_id(storyboard: list[dict], shot_id: str | None) -> dict | None:
    if not shot_id:
        return None
    for shot in storyboard:
        if shot.get("shot_id") == shot_id:
            return shot
    return None


def prompt_index_entry(prompt_index: list[dict], prompt_key: str, shot_id: str | None) -> dict | None:
    for entry in prompt_index:
        if entry.get("prompt_key") == prompt_key and (not shot_id or entry.get("shot_id") == shot_id):
            return entry
    return None


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def build_context(project_dir: Path, episode_id: str, shot_id: str | None, prompt_key: str) -> dict:
    episode_dir = project_dir / "episodes" / episode_id
    root = workspace_root(project_dir)
    project = load_json(project_dir / "project.json", {})
    style_profiles_rel = project.get("style_profiles_file") or "style_profiles/style_profiles.json"
    style_profiles_path = Path(style_profiles_rel)
    if not style_profiles_path.is_absolute():
        style_profiles_path = root / style_profiles_path
    storyboard = load_json(episode_dir / "storyboard.json", [])
    prompt_index = load_json(episode_dir / "prompts" / "prompt_index.json", [])
    selected_shot = shot_by_id(storyboard, shot_id)
    characters = load_json(project_dir / "characters.json", [])
    if selected_shot:
        char_ids = set(selected_shot.get("characters") or selected_shot.get("character_ids") or [])
        characters = [c for c in characters if c.get("character_id") in char_ids]
    entry = prompt_index_entry(prompt_index, prompt_key, shot_id)
    return {
        "project": project,
        "style_profiles": load_json(style_profiles_path, {}),
        "source_events": load_json(project_dir / "source_events.json", []),
        "style_guide": read_text(project_dir / "style_guide.md"),
        "episode_script": read_text(episode_dir / "script.md"),
        "characters": characters,
        "shot": selected_shot,
        "storyboard": storyboard if not selected_shot or prompt_key in {"shot_split", "grid_prompt"} else None,
        "prompt_index_entry": entry,
        "slot_overrides": (entry or {}).get("slot_contents", {}),
    }


def assemble(args: argparse.Namespace) -> str:
    project_dir = Path(args.project_dir).resolve()
    root = workspace_root(project_dir)
    project = load_json(project_dir / "project.json", {})
    registry_rel = args.registry or project.get("prompt_template_registry") or "prompt_templates/registry.json"
    registry_path = Path(registry_rel)
    if not registry_path.is_absolute():
        registry_path = root / registry_path
    registry = load_json(registry_path, {})
    template = find_template(registry, args.prompt_key)
    context = build_context(project_dir, args.episode, args.shot_id, args.prompt_key)

    lines = [
        f"# Assembled Prompt: {args.prompt_key}",
        "",
        f"Template Version: {template.get('version')}",
        f"Prompt Type: {template.get('prompt_type')}",
        f"Episode: {args.episode}",
        f"Shot ID: {args.shot_id or ''}",
        "",
        "## Slots",
        "",
    ]
    overrides = context.get("slot_overrides") or {}
    for slot in template.get("slots", []):
        slot_key = slot.get("slot_key")
        slot_path = registry_path.parent / slot.get("file", "")
        content = read_text(slot_path, "")
        if slot_key in overrides:
            content += f"\n\n## Project Override\n\n{overrides[slot_key]}"
        lines.extend([f"### {slot_key}", "", content.strip(), ""])

    lines.extend([
        "## Production Context",
        "",
        "```json",
        compact_json(context),
        "```",
        "",
        "## Final Instruction",
        "",
        "Use the slots and production context above to produce the requested artifact. Preserve frozen facts and return the output format required by the template.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_key")
    parser.add_argument("--project-dir", default="projects/demo-drama")
    parser.add_argument("--episode", default="ep01")
    parser.add_argument("--shot-id")
    parser.add_argument("--registry")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = assemble(args)
    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result, encoding="utf-8")
        print(f"Wrote assembled prompt: {out_path}")
    else:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
