---
name: character-designer
description: Use to create or revise characters.json, world_bible.md, and reference asset plans for AI manga/drama characters, scenes, props, voices, and visual constraints.
---

# Character Designer

Design reusable visual and voice constraints. Do not write storyboard or video prompts.

## Inputs

- `script.md`
- `source_events.json`
- `style_guide.md`
- existing `assets/references/*`

## Rules

- Assign stable `character_id` values.
- Extract only characters, scenes, props, and voices that are actually needed for the current episode or reusable world bible.
- Reuse existing IDs and locked references before creating new ones.
- Add `visual_hint`: a short visible identifier that can be reused in prompts, such as hair/eye/costume/silhouette anchors. It must be physical, not personality-based.
- Add `style_profile_ids` and `default_style_profile_id` when the project supports more than one visual style, such as motion-comic and live-action light realism.
- Add `body_type`, optional `height_cm`, `performance_style`, and `costume_sets` for every recurring or speaking character.
- Keep `appearance` neutral and reference-sheet friendly: face, hair, body, clothing, silhouette, color anchors, recurring marks. Do not mix in one-off plot actions.
- Put signature gestures, acting rhythm, and emotional expression into `performance_style`, not `appearance`.
- Separate characters, scenes, props, and world references. Scene references must not become character references.
- Add fixed voice direction and negative rules for speaking roles.
- Mark human-approved reference assets as `locked: true`.
- Record `style_profile_id` on every character reference asset. Do not reuse a motion-comic reference as a live-action reference, or the reverse, unless the reviewer explicitly approves it as a style bridge.
- Do not change frozen script events.

## Output

Update:

- `characters.json`
- `world_bible.md`
- reference asset plan under `assets/references/*`

Each main character entry should include:

- `character_id`
- `name`
- `role`
- `visual_hint`
- `style_profile_ids`
- `default_style_profile_id`
- `body_type`
- `appearance`
- `personality`
- `performance_style`
- `active_costume_id`
- `costume_sets`
- `voice`
- `reference_assets`
- `negative_rules`
