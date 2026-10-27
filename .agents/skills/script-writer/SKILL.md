---
name: script-writer
description: Use to write or revise a short vertical AI manga/drama episode script from source_events.json, style guide, and project constraints, producing script.md with narration, dialogue, actions, and event references.
---

# Script Writer

Write `episodes/<episode>/script.md`.

## Inputs

- `source_events.json`
- `project.json`
- `style_guide.md`
- existing `characters.json` if present

## Rules

- Keep each scene traceable to one or more `event_id` values.
- Write for vertical short drama pacing.
- Mark narration, dialogue, action, and hook.
- Extract character candidates but do not finalize visual design.
- Do not write storyboard or prompts.

## Output

`script.md` must include:

- episode target
- scene/beat sections
- event references
- narration
- dialogue
- action notes
- ending hook
