---
name: source-event-planner
description: Use to convert an outline, novel excerpt, or spoken story idea into source_events.json for AI manga/drama adaptation, preserving must-keep plot facts and mapping them to planned episodes.
---

# Source Event Planner

Create or update `source_events.json`. This is the upstream fact source for script and storyboard.

## Inputs

- User outline, novel excerpt, or notes
- `project.json`
- `style_guide.md`

## Rules

- Preserve all must-keep plot facts.
- Split events by dramatic beat, not by paragraph length.
- Assign stable `event_id` values such as `event_ch01_001`.
- Include characters, location, dramatic function, and target episode.
- Do not write the full script here.

## Output

Update `source_events.json` with:

- `event_id`
- `source`
- `chapter`
- `summary`
- `characters`
- `location`
- `must_keep`
- `dramatic_function`
- `adapted_episode`
- `adapted_shots`
