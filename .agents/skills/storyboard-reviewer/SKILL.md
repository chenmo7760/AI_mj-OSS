---
name: storyboard-reviewer
description: Use to review storyboard.json for structure, timing, source event coverage, character references, camera/action clarity, continuity links, and readiness for prompt generation.
---

# Storyboard Reviewer

Review `storyboard.json`. Do not rewrite the full storyboard.

## Inputs

- `source_events.json`
- `script.md`
- `characters.json`
- `storyboard.json`

## Checks

- Shot order and IDs are stable.
- Total duration matches episode target.
- Each required event is covered.
- Each shot maps to one primary action or emotional beat; overloaded shots are flagged for split.
- Character IDs are valid and visible character names align with `visual_hint`.
- Scene, prop, and costume references are valid or explicitly missing.
- Camera, shot type, angle, movement, composition, focal point, and action are executable.
- `motion_script` is time-segmented and describes visible motion, not dialogue.
- `video_script` is concise model-facing prose and does not duplicate dialogue/subtitle text.
- `dialogues` preserve speaker IDs, sequence, emotion, and optional timing ratios.
- Start/end frame intent is clear enough for keyframe planning.
- `route_plan` or `shot_routes.json` exists before generation and the route matches shot risk, available references, and provider capability.
- Continuity links are complete.
- Shot N end state can logically connect to shot N+1 start state.

## Output

Write `episodes/<episode>/reviews/<episode>_storyboard_review_vXXX.md`.

Use `Needs Fix` when any missing field would force a downstream prompt agent to invent continuity.
