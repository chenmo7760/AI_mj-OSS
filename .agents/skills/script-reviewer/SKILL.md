---
name: script-reviewer
description: Use to review script.md against source_events.json, pacing, hook strength, continuity, character consistency, and readiness before character design or storyboard work.
---

# Script Reviewer

Review `script.md`. Do not rewrite the episode.

## Inputs

- `source_events.json`
- `episodes/<episode>/script.md`
- `style_guide.md`
- `project.json`

## Checks

- Must-keep events are represented.
- Each major beat has event references.
- Pacing matches target duration.
- Dialogue and narration are usable for short drama.
- The ending hook is clear.
- New character candidates are explicit.

## Output

Write `episodes/<episode>/reviews/<episode>_script_review_vXXX.md` with result and required fixes.
