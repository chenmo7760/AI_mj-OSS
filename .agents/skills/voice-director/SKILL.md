---
name: voice-director
description: Use to create AI manga/drama voice scripts, TTS task lists, subtitle timing drafts, speaker assignments, and emotion notes from script and storyboard.
---

# Voice Director

Create voice and subtitle planning files.

## Inputs

- `script.md`
- `storyboard.json`
- `characters.json`

## Rules

- Preserve speaker names and character IDs.
- Match voice candidates by gender/presentation, age, personality, role importance, emotional range, and genre tone.
- Keep subtitle lines short enough for vertical video.
- Add emotion and pacing notes.
- Keep spoken text separate from video model prompts.
- Use storyboard `dialogues` sequence and timing ratios when present.
- Create TTS task entries with provider/model/mode placeholders when audio generation is planned.
- Do not synthesize audio unless explicitly asked.

## Output

- `voice_script.md`
- `subtitles.srt`
- optional TTS task entries in `tasks.json`
