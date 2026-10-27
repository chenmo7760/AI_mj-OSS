---
name: video-prompt-reviewer
description: Use to review AI manga/drama video prompts for executability, continuity, character consistency, keyframe usage, model risk, and readiness before manual or API video generation.
---

# Video Prompt Reviewer

Review video prompts. Do not rewrite all prompts.

## Inputs

- `storyboard.json`
- `characters.json`
- keyframe records
- `prompts/*video*.md`
- `prompt_index.json`

## Checks

- Prompt matches storyboard action.
- Character `visual_hint`, appearance, costume, scene, and prop rules are preserved.
- Keyframes are referenced when available and the prompt does not contradict first/last frames.
- `reference_mode`, generation mode, duration, aspect ratio, and target provider assumptions are explicit.
- Active `style_profile_id` is explicit in the prompt or metadata. For Gemini/Veo web manual generation, include human web steps, upload files, download naming, and style-specific review cautions.
- Photorealistic video is acceptable for `style_live_action_light_realism_v001`; comic or illustrated video is acceptable for `style_motion_comic_v001`. Any style switch needs a shot-level override.
- Provider capability supports the requested route, reference count, first/last frames, duration, ratio, seed, and negative prompt usage.
- Prompt template slots are present and no required slot was bypassed without rationale.
- `motion_script` and final model prose do not fight each other.
- Dialogue is separated from model-facing motion prose unless the provider requires otherwise.
- Motion is feasible for the target video model.
- Prompt avoids contradictory instructions.
- Known model risks are listed: identity drift, hand/prop errors, camera complexity, subtitle/text leakage, reference overload.

## Output

Write `episodes/<episode>/reviews/<episode>_video_prompt_review_vXXX.md`.
