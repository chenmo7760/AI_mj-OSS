#!/usr/bin/env python3
"""Lightweight validator for the Codex-first AI manga project skeleton."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_PROJECT_FILES = [
    "project.json",
    "source_events.json",
    "characters.json",
    "assets.json",
    "style_guide.md",
    "cost.json",
    "freeze_log.md",
]

REQUIRED_EPISODE_FILES = [
    "script.md",
    "storyboard.json",
    "tasks.json",
    "prompts/prompt_index.json",
    "quality_gate.md",
]

OPTIONAL_EPISODE_JSON = [
    "shot_routes.json",
    "stale_manifest.json",
    "grid/grid_assignments.json",
    "delivery/delivery_manifest.json",
    "resolved_assets.json",
    "reports/continuity_check.json",
]


def load_json(path: Path):
    try:
      return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
      raise ValueError(f"{path} is not valid JSON: {exc}") from exc


def require_file(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing file: {path}")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_all.py <project_dir>")
        return 2

    project_dir = Path(sys.argv[1]).resolve()
    errors: list[str] = []

    if not project_dir.exists():
        print(f"Project dir not found: {project_dir}")
        return 2

    for rel in REQUIRED_PROJECT_FILES:
        require_file(project_dir / rel, errors)

    episode_dir = project_dir / "episodes" / "ep01"
    for rel in REQUIRED_EPISODE_FILES:
        require_file(episode_dir / rel, errors)

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    project = load_json(project_dir / "project.json")
    events = load_json(project_dir / "source_events.json")
    characters = load_json(project_dir / "characters.json")
    assets = load_json(project_dir / "assets.json")
    storyboard = load_json(episode_dir / "storyboard.json")
    tasks = load_json(episode_dir / "tasks.json")
    prompt_index = load_json(episode_dir / "prompts" / "prompt_index.json")
    cost = load_json(project_dir / "cost.json")

    if not project.get("project_id"):
        errors.append("project.json missing project_id")

    workspace_dir = project_dir.parents[1]
    style_profile_ids: set[str] = set()
    style_profiles_rel = project.get("style_profiles_file")
    if style_profiles_rel:
        style_profiles_path = workspace_dir / style_profiles_rel
        if not style_profiles_path.exists():
            errors.append(f"style_profiles_file not found: {style_profiles_rel}")
        else:
            style_profiles = load_json(style_profiles_path)
            style_profile_ids = {style.get("style_profile_id") for style in style_profiles.get("styles", [])}
            if not style_profile_ids:
                errors.append("style_profiles_file has no styles")
            if len(style_profile_ids) != len(style_profiles.get("styles", [])):
                errors.append("style_profiles_file has duplicate or missing style_profile_id values")

    project_style = project.get("style_profile_id")
    if style_profile_ids and project_style and project_style not in style_profile_ids:
        errors.append(f"project references missing style_profile_id: {project_style}")
    for style_id in project.get("allowed_style_profile_ids", []):
        if style_profile_ids and style_id not in style_profile_ids:
            errors.append(f"project allowed_style_profile_ids references missing style_profile_id: {style_id}")

    prompt_registry_rel = project.get("prompt_template_registry")
    if prompt_registry_rel:
        prompt_registry_path = workspace_dir / prompt_registry_rel
        if not prompt_registry_path.exists():
            errors.append(f"prompt_template_registry not found: {prompt_registry_rel}")
        else:
            prompt_registry = load_json(prompt_registry_path)
            for template in prompt_registry.get("templates", []):
                for slot in template.get("slots", []):
                    slot_file = prompt_registry_path.parent / slot.get("file", "")
                    if not slot_file.exists():
                        errors.append(f"prompt template slot not found: {slot_file}")

    provider_capabilities_rel = project.get("provider_capabilities_file")
    if provider_capabilities_rel:
        provider_path = workspace_dir / provider_capabilities_rel
        if not provider_path.exists():
            errors.append(f"provider_capabilities_file not found: {provider_capabilities_rel}")
        else:
            providers = load_json(provider_path).get("providers", [])
            provider_ids = {provider.get("provider_id") for provider in providers}
            if not provider_ids:
                errors.append("provider_capabilities_file has no providers")
    else:
        provider_ids = set()

    event_ids = {event.get("event_id") for event in events}
    character_ids = {character.get("character_id") for character in characters}
    shot_ids = {shot.get("shot_id") for shot in storyboard}

    for character in characters:
        character_id = character.get("character_id", "<unknown>")
        default_style = character.get("default_style_profile_id")
        if style_profile_ids and default_style and default_style not in style_profile_ids:
            errors.append(f"{character_id} references missing default_style_profile_id: {default_style}")
        for style_id in character.get("style_profile_ids", []):
            if style_profile_ids and style_id not in style_profile_ids:
                errors.append(f"{character_id} references missing style_profile_id: {style_id}")
        for ref in character.get("reference_assets", []):
            style_id = ref.get("style_profile_id")
            if style_profile_ids and style_id and style_id not in style_profile_ids:
                errors.append(f"{character_id} reference asset references missing style_profile_id: {style_id}")

    for shot in storyboard:
        shot_id = shot.get("shot_id", "<unknown>")
        for event_id in shot.get("source_events", []):
            if event_id not in event_ids:
                errors.append(f"{shot_id} references missing event_id: {event_id}")
        for character_id in shot.get("characters", []):
            if character_id not in character_ids:
                errors.append(f"{shot_id} references missing character_id: {character_id}")
        style_id = shot.get("style_profile_id")
        if style_profile_ids and style_id and style_id not in style_profile_ids:
            errors.append(f"{shot_id} references missing style_profile_id: {style_id}")

    for prompt in prompt_index:
        prompt_file = prompt.get("prompt_file")
        shot_id = prompt.get("shot_id")
        if shot_id not in shot_ids:
            errors.append(f"prompt references missing shot_id: {shot_id}")
        if prompt_file and not (project_dir / prompt_file).exists():
            errors.append(f"prompt_file not found: {prompt_file}")
        template_ref = prompt.get("template_ref")
        if prompt_registry_rel and template_ref:
            # Template existence is checked lightly by prompt_key, because slot overrides may be project-local.
            prompt_registry = load_json(workspace_dir / prompt_registry_rel)
            template_keys = {template.get("prompt_key") for template in prompt_registry.get("templates", [])}
            if template_ref not in template_keys:
                errors.append(f"prompt references missing template_ref: {template_ref}")

    for task in tasks:
        prompt_file = task.get("prompt_file")
        shot_id = task.get("shot_id")
        if shot_id and shot_id not in shot_ids:
            errors.append(f"task references missing shot_id: {shot_id}")
        if prompt_file and not (project_dir / prompt_file).exists():
            errors.append(f"task prompt_file not found: {prompt_file}")
        provider = task.get("provider")
        if provider_ids and provider and provider not in provider_ids:
            errors.append(f"task references provider not in capabilities: {provider}")
        style_id = task.get("style_profile_id")
        if style_profile_ids and style_id and style_id not in style_profile_ids:
            errors.append(f"task references missing style_profile_id: {style_id}")

    for asset in assets:
        shot_id = asset.get("shot_id")
        if shot_id and shot_id not in shot_ids:
            errors.append(f"asset references missing shot_id: {shot_id}")
        if asset.get("selected") and not asset.get("quality_notes"):
            errors.append(f"selected asset missing quality_notes: {asset.get('asset_id')}")
        style_id = asset.get("style_profile_id")
        if style_profile_ids and style_id and style_id not in style_profile_ids:
            errors.append(f"asset references missing style_profile_id: {style_id}")

    for rel in OPTIONAL_EPISODE_JSON:
        path = episode_dir / rel
        if path.exists():
            data = load_json(path)
            if rel == "shot_routes.json":
                for route in data.get("routes", []):
                    if route.get("shot_id") not in shot_ids:
                        errors.append(f"shot_routes references missing shot_id: {route.get('shot_id')}")
            if rel == "grid/grid_assignments.json":
                for grid in data.get("grids", []):
                    for cell in grid.get("cells", []):
                        if cell.get("shot_id") not in shot_ids:
                            errors.append(f"grid cell references missing shot_id: {cell.get('shot_id')}")

    if not isinstance(cost, list):
        errors.append("cost.json must be an array")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"Validation passed: {project_dir}")
    print(f"- events: {len(events)}")
    print(f"- characters: {len(characters)}")
    print(f"- shots: {len(storyboard)}")
    print(f"- prompts: {len(prompt_index)}")
    print(f"- tasks: {len(tasks)}")
    print(f"- assets: {len(assets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
