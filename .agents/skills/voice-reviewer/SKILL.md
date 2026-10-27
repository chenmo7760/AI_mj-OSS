---
name: voice-reviewer
description: Use to review AI manga/drama voice scripts, subtitle timing, speaker assignment, emotion notes, voice consistency, and readiness before audio generation or final composition.
---

# Voice Reviewer

Review voice and subtitle files. Do not rewrite all dialogue.

## Inputs

- `script.md`
- `storyboard.json`
- `characters.json`
- `voice_script.md`
- `subtitles.srt`

## Checks

- Speakers match character IDs.
- Subtitle order matches storyboard.
- Emotion notes match scene intent.
- Lines are readable for short vertical video.
- Voice assignments match character age, personality, role importance, and continuity from prior episodes.
- Dialogue timing does not exceed shot duration or collide with essential visual beats.
- Subtitle text is not mistakenly embedded in image/video prompts as visible on-screen text.
- Missing audio tasks are listed.

## Output

Write `episodes/<episode>/reviews/<episode>_voice_review_vXXX.md`.
