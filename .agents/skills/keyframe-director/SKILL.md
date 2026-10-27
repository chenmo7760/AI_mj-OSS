---
name: keyframe-director
description: Use to plan or register start/end keyframes for AI manga/drama shots, connecting image prompts, reference assets, and storyboard continuity before video prompt generation.
---

# Keyframe Director

Plan or register keyframes. Do not generate final video.

## Inputs

- `storyboard.json`
- image prompts
- `characters.json`
- `assets/references/*`

## Rules

- Every high-risk shot should have `start_frame` and `end_frame`; ordinary low-risk shots may document why text-only is acceptable.
- Read `shot_routes.json` before keyframe planning. Prioritize first/last frames for shots routed to `first-last`; use grid cells as candidate frames for shots routed to `nine-grid`.
- If keyframes are chosen from a grid, use or require `scripts/select_grid_cell.py` so selected `first_frame`, `last_frame`, or `reference` crops are written back to storyboard/tasks/assets metadata.
- Write start/end frame descriptions before generating images. Each description must include composition, visible characters with `visual_hint`, costume, camera, lighting, environment, and key props.
- The start frame is the state just before the shot's motion begins.
- The end frame is the stable state after the motion completes. Avoid motion blur or transitional poses if it will be reused downstream.
- Link adjacent shots with `previous_end_frame` and `next_start_frame`.
- Preserve scene, prop, costume, and locked character references.
- Record missing keyframes explicitly.

## Output

Update storyboard keyframe fields or create keyframe prompt notes.
