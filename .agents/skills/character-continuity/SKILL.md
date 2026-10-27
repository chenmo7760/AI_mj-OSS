---
name: character-continuity
description: Use to check character, costume, scene, prop, and action continuity across storyboard shots, prompts, keyframes, and selected assets in an AI manga/drama episode.
---

# Character Continuity

Check continuity across nodes. Do not create new story or prompts.

## Inputs

- `characters.json`
- `world_bible.md`
- `storyboard.json`
- prompt files
- `assets.json`

## Checks

- Character IDs are valid.
- Appearance, costume, and props do not drift.
- Scene changes are intentional.
- `continuity_from` and `continuity_to` are coherent.
- Keyframes and selected assets do not contradict locked references.

## Output

Write a continuity issue list with required fixes and affected shots.
