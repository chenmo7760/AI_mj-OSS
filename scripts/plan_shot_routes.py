#!/usr/bin/env python3
"""Plan lightweight generation routes for storyboard shots."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path


ROUTES = {"text-only", "reference-image", "first-frame", "first-last", "nine-grid"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def provider_by_id(capabilities: dict) -> dict[str, dict]:
    return {p.get("provider_id"): p for p in capabilities.get("providers", [])}


def choose_route(shot: dict, provider: dict | None) -> tuple[str, str, list[str], list[str], str]:
    keyframes = shot.get("keyframes") or {}
    reference_images = shot.get("reference_images") or []
    reference_prompts = shot.get("reference_image_prompts") or []
    characters = shot.get("characters") or []
    action = (shot.get("action") or "") + " " + (shot.get("motion_script") or "")
    has_first = bool(keyframes.get("start_frame") or keyframes.get("start_frame_prompt"))
    has_last = bool(keyframes.get("end_frame") or keyframes.get("end_frame_prompt"))
    has_refs = bool(reference_images)
    has_ref_prompts = bool(reference_prompts)
    complex_motion = any(word in action.lower() for word in ["fight", "run", "turn", "camera", "push", "追", "打", "跑", "转", "推近"])
    multi_character = len(characters) > 1

    provider_modes = set((provider or {}).get("video_modes") or [])
    required: list[str] = []
    missing: list[str] = []

    if has_first and has_last and "first-last" in provider_modes:
        return (
            "first-last",
            "first_last",
            ["start_frame", "end_frame", "video_prompt"],
            [item for item in ["start_frame", "end_frame"] if not keyframes.get(item)],
            "planned start/end frame anchors exist; use interpolation to lock continuity",
        )

    if (complex_motion or multi_character) and has_ref_prompts:
        required = ["grid_prompt", "reference_image_prompts", "asset-reviewer selection"]
        return (
            "nine-grid",
            "nine_grid",
            required,
            [],
            "shot is visually risky and has reference prompts; use grid exploration before final frame/video",
        )

    if has_first and "first-frame" in provider_modes:
        return (
            "first-frame",
            "first_frame",
            ["start_frame", "video_prompt"],
            [] if keyframes.get("start_frame") else ["start_frame asset"],
            "start frame is available or planned; use it as motion anchor",
        )

    if has_refs and "reference-image" in provider_modes:
        return (
            "reference-image",
            "reference_images",
            ["reference_images", "video_prompt"],
            [],
            "reference images exist and provider supports reference image video",
        )

    if "text-only" in provider_modes:
        return (
            "text-only",
            "text_only",
            ["video_prompt"],
            [],
            "low-control fallback; no usable frame or reference asset is present",
        )

    return (
        "reference-image",
        "reference_images",
        ["reference_images", "video_prompt"],
        ["provider capability for chosen route"],
        "provider profile lacks a clean route; supervisor must decide",
    )


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("Usage: plan_shot_routes.py <project_dir> [episode_id]")
        return 2

    project_dir = Path(sys.argv[1]).resolve()
    episode_id = sys.argv[2] if len(sys.argv) == 3 else "ep01"
    episode_dir = project_dir / "episodes" / episode_id
    storyboard_path = episode_dir / "storyboard.json"
    project_path = project_dir / "project.json"
    if not storyboard_path.exists():
        print(f"storyboard.json not found: {storyboard_path}")
        return 2

    project = load_json(project_path)
    provider_file = project.get("provider_capabilities_file") or "provider_capabilities/provider_capabilities.json"
    provider_path = (project_dir.parent.parent / provider_file).resolve() if not Path(provider_file).is_absolute() else Path(provider_file)
    if not provider_path.exists():
        provider_path = (Path.cwd() / provider_file).resolve()
    capabilities = load_json(provider_path)
    providers = provider_by_id(capabilities)

    storyboard = load_json(storyboard_path)
    routes = []
    for shot in storyboard:
        provider_id = (
            ((shot.get("route_plan") or {}).get("provider_id"))
            or ((shot.get("assets") or {}).get("provider"))
            or "manual_web"
        )
        provider = providers.get(provider_id) or providers.get("manual_web") or next(iter(providers.values()), {})
        route, reference_mode, required, missing, rationale = choose_route(shot, provider)
        if route not in ROUTES:
            missing.append("valid route")
        routes.append({
            "shot_id": shot.get("shot_id"),
            "route": route,
            "reference_mode": reference_mode,
            "provider_id": provider.get("provider_id", provider_id),
            "required_inputs": required,
            "missing_inputs": missing,
            "rationale": rationale,
            "review_status": "pending"
        })

    out = {
        "schema_version": "0.1.0",
        "episode_id": episode_id,
        "created_at": str(date.today()),
        "routes": routes
    }
    out_path = episode_dir / "shot_routes.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(routes)} shot routes: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
