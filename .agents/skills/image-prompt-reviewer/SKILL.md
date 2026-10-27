---
name: image-prompt-reviewer
description: Use to review AI manga/drama image prompts for character consistency, scene/prop references, visual style, negative rules, and readiness before keyframe generation.
---

# Image Prompt Reviewer

Review image prompt files. Do not rewrite all prompts.

## Inputs

- `storyboard.json`
- `characters.json`
- `style_guide.md`
- `prompts/*image*.md`
- `prompt_index.json`

## Checks

- Prompt references valid shot ID.
- Prompt type is clear: character reference, scene reference, shot frame, or grid candidate.
- `template_ref`, `template_version`, and slot contents are present in `prompt_index.json` when the project uses prompt templates.
- Fixed character `visual_hint`, appearance, costume, and locked references are included for visible characters.
- Scene-only prompts contain no characters or action.
- Shot prompts include composition, camera angle, focal subject, environment, lighting, and style.
- Prompt style matches the active `style_profile_id` from `project.json` or the shot override. Photorealism is acceptable for `style_live_action_light_realism_v001`; motion-comic rendering is acceptable for `style_motion_comic_v001`.
- If the prompt style differs from the project default, the shot must declare a `style_profile_id` override and the review must record the reason.
- Grid prompts specify exact panel count and prevent merged/missing panels.
- Grid cell assignments record `cell_index`, `row`, `col`, `shot_id`, `frame_type`, `crop_path`, and selection state when a grid is split.
- Negative rules are present and include identity drift, text, watermark, extra characters, and wrong era/style where relevant.
- Scene/prop references match storyboard.
- Style guide is represented.
- Use `docs/reviewer_casebook_v0.1.md` when available to identify known prompt risks such as photorealistic drift when motion-comic style is required, or comic/anime drift when live-action light realism is required.

## Output

Write `episodes/<episode>/reviews/<episode>_image_prompt_review_vXXX.md`.
