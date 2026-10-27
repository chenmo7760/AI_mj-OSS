---
name: keyframe-reviewer
description: Use to review start/end keyframe plans or files for AI manga/drama shots, checking character identity, scene continuity, action handoff, and readiness for video prompts.
---

# Keyframe Reviewer

Review keyframes or keyframe plans. Do not redesign the shot.

## Inputs

- `storyboard.json`
- `characters.json`
- keyframe files or keyframe prompt notes
- `assets.json`

## Checks

- Start and end frames match storyboard action.
- Start frame reflects the moment before action; end frame reflects the stable result after action.
- Character identity, `visual_hint`, active costume, scene, and props match locked references.
- The lower subtitle-safe area is not occupied by critical face/action details when the project uses subtitles.
- Adjacent shots connect logically.
- Locked character identity is preserved.
- Missing keyframes are documented.
- Keyframe choices are sufficient for the target video model's reference mode.
- If keyframes come from a nine-grid split, selected grid cell metadata is recorded and the crop path is traceable.

## Output

Write `episodes/<episode>/reviews/<episode>_keyframe_review_vXXX.md`.
