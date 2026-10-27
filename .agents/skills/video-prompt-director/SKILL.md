---
name: video-prompt-director
description: Use to create versioned video generation prompts for AI manga/drama shots from storyboard, character cards, style guide, keyframes, and continuity constraints.
---

# Video Prompt Director

Create `episodes/<episode>/prompts/<shot_id>_video_vXXX.md`.

## Inputs

- `storyboard.json`
- `characters.json`
- `style_guide.md`
- keyframe fields/files
- `prompt_index.json`

## Rules

- Choose `reference_mode`: text-only, reference-images, first-frame, first-last, or multi-ref.
- Read `shot_routes.json` and `provider_capabilities/provider_capabilities.json` before writing the prompt. Do not target a route unsupported by the provider.
- Load `prompt_templates/registry.json` when available and record `template_ref`, `template_version`, and important slot overrides in `prompt_index.json`. Prefer `python scripts/assemble_prompt.py shot_video_first_last --project-dir <project> --episode <episode> --shot-id <shot_id> --out <prompt_file>` for repeatable prompt assembly.
- Reference start/end keyframes when available. If first/last frames exist, the prompt must not contradict them.
- Preserve character identity, `visual_hint`, active costume, props, scene, and continuity links.
- Use `motion_script` for time-segmented action planning and `video_script` for concise model-facing prose.
- Keep dialogue outside the final model prompt unless the provider explicitly supports dialogue. Use `dialogues` for voice/subtitle planning.
- Describe camera motion and action clearly, with duration and vertical aspect ratio.
- Record target provider assumptions, generation mode, reference image list, first/last frame paths, and key provider params in `prompt_index.json` or task metadata.
- If editing an existing prompt, update prompt history and write a prompt diff when the change is significant.
- Keep one prompt file per shot per version.
- Update `prompt_index.json`.
- Do not mark the prompt as passed.

## Output

Versioned video prompt files and updated prompt index.
