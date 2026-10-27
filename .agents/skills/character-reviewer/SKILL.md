---
name: character-reviewer
description: Use to review characters.json, world_bible.md, character reference assets, negative rules, scene/prop references, and whether visual identity is stable enough for storyboard and prompt generation.
---

# Character Reviewer

Review character and visual asset constraints. Do not redesign characters.

## Inputs

- `characters.json`
- `world_bible.md`
- `style_guide.md`
- `assets/references/*`
- `script.md`

## Checks

- Each main role has stable `character_id`.
- All named, speaking, visible, or repeatedly referenced characters from the current episode are present or intentionally excluded with rationale.
- `visual_hint` is short, visible, and specific enough to paste after the character name in image/video prompts.
- If the project has `style_profile_id` or `allowed_style_profile_ids`, each main character records compatible `style_profile_ids` and a `default_style_profile_id`.
- `appearance` is stable and reference-sheet friendly; it must not include one-off actions, emotions, camera moves, or plot spoilers.
- `performance_style` captures recurring gesture/acting notes separately from appearance.
- `body_type`, costume anchors, and `costume_sets` are specific enough for generation.
- Negative rules block the most likely identity drift: hair, face, age, costume, era, style, and extra accessories.
- Locked reference assets are recorded.
- Locked reference assets include `style_profile_id`; do not pass a final multi-shot workflow that mixes motion-comic and live-action references without explicit shot overrides.
- Scene and prop references are not mixed with character refs.
- Voice direction exists for speaking roles.
- If references are missing, list whether the project can proceed with text-only prompts or must stop for reference generation.

## Output

Write `episodes/<episode>/reviews/<episode>_character_review_vXXX.md`.

Use `Pass` only when storyboard and prompt agents can rely on the character file without guessing.
