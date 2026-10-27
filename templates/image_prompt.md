# Image Prompt

Prompt ID:
Shot ID:
Version:
Provider Target:
Prompt Key:
Variant:
Language:

## Source

- Source events:
- Storyboard:
- Characters:
- References:
- Style guide:

## Prompt

### Character Reference Prompt

Use for character sheets or locked references:

`[name], [visual_hint], [age/body_type], [face and hair], [costume], [neutral pose/expression], [plain background], [project art style], no text, no watermark.`

### Scene Reference Prompt

Use for pure background references:

`[location], [time], [lighting], [atmosphere], [key props/architecture], cinematic background, no characters, no people, no text, no watermark.`

### Shot Image Prompt

Use for the actual shot frame:

`[shot_type], [camera angle], [composition], [visible characters with visual_hint and costume], [single action or stable pose], [scene], [lighting/color], [project style], vertical 9:16, no text, no watermark.`

### Grid Prompt

Use for multi-candidate grids:

`Create a [rows]x[cols] grid with exactly [N] separate panels, consistent style, no merged panels, no missing panels. Each panel shows one distinct candidate for [frame_type].`

## Negative / Avoid

- Do not change locked character identity.
- Do not ignore negative rules.
- Do not mix scene-only prompts with people or character action.
- Do not add subtitles, captions, logos, UI, or watermarks.

## Metadata

Review Status: pending
Frozen: false
