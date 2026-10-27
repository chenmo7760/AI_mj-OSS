---
name: export-compositor
description: Use to plan or run FFmpeg composition for AI manga/drama episodes, combining selected video assets, voice assets, subtitles, and music into draft or final MP4 outputs.
---

# Export Compositor

Prepare composition. Do not choose creative replacements.

## Inputs

- `storyboard.json`
- `assets.json`
- `subtitles.srt`
- voice/music assets

## Rules

- Use selected assets only unless the human approves otherwise.
- Preserve shot order.
- Emit reproducible FFmpeg commands or use `scripts/compose_ffmpeg.py`.
- Before final export, create or inspect `episodes/<episode>/delivery/delivery_manifest.json` so prompt package, selected assets, subtitles, shot segments, and source metadata are preserved.
- Write draft output as `output/<episode>_draft_vXXX.mp4`.

## Output

- concat list or command notes
- draft/final output path
- task status updates
