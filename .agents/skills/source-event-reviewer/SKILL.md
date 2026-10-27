---
name: source-event-reviewer
description: Use to review source_events.json for coverage, event granularity, continuity, must-keep facts, and readiness before script writing in an AI manga/drama pipeline.
---

# Source Event Reviewer

Review `source_events.json`. Do not rewrite the story.

## Inputs

- User outline or source notes
- `source_events.json`
- `project.json`
- `style_guide.md`

## Checks

- Must-keep facts are preserved.
- Events are neither too broad nor too tiny.
- Characters and locations are named consistently.
- Every event has a dramatic function.
- Episode mapping is plausible.

## Output

Write `episodes/<episode>/reviews/<episode>_source_event_review_vXXX.md` with:

- `Result`
- `Blocking Findings`
- `Required Fixes`
- `Accepted Risks`
- `Next Role`
