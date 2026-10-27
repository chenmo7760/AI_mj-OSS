---
name: storyboard-director
description: Use to convert an approved episode script into storyboard.json for AI manga/drama production, creating shot IDs, timing, camera, action, event links, continuity links, and keyframe placeholders.
---

# Storyboard Director

Create or revise `episodes/<episode>/storyboard.json`.

## Inputs

- `script.md`
- `source_events.json`
- `characters.json`
- `world_bible.md`
- `style_guide.md`

## Rules

- Use stable shot IDs: `ep01_s001`.
- Bind each shot to `source_events`.
- Keep each shot focused on one primary action or emotional beat. Split shots that require multiple unrelated actions.
- Include duration, title, location/time/atmosphere, scene, characters, `character_ids`, action, result, camera, narration/dialogue.
- Add `shot_type`, `angle`, `movement`, `camera_direction`, `composition_guide`, `focal_point`, and `depth_of_field`.
- Add `motion_script` as time-segmented action beats, usually `0-3s` and `3-6s` for short vertical video.
- Add `video_script` as concise model-facing prose. Do not put dialogue text or timestamps inside it.
- Put spoken lines into `dialogues` with `sequence`, `character_id`, `text`, emotion, and optional start/end ratios.
- Add `sound_design`, `music_cue`, `sound_effect`, `transition_in`, and `transition_out` when useful.
- Add `reference_image_prompts`, `reference_images`, and `costume_overrides` when the shot needs scene, prop, or costume control.
- Add an initial `route_plan` when obvious, but let `scripts/plan_shot_routes.py` produce the authoritative route before generation.
- Set `continuity_from` and `continuity_to`.
- Add keyframe placeholders. The intended end state of shot N must be usable as the start context for shot N+1.
- Use character `visual_hint` in human-readable shot notes when a visible character is named.
- Do not write final prompts here.

## Output

Valid `storyboard.json` shot objects.
