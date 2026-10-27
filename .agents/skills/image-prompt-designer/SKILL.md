---
name: image-prompt-designer
description: Use to create versioned image generation prompts for AI manga/drama shots from storyboard, character cards, style guide, and reference assets.
---

# Image Prompt Designer

Create `episodes/<episode>/prompts/<shot_id>_image_vXXX.md`.

## Inputs

- `storyboard.json`
- `characters.json`
- `style_guide.md`
- `assets/references/*`

## Rules

- Choose the prompt type first: character reference, scene reference, shot frame, or grid candidate prompt.
- Load `prompt_templates/registry.json` when available and assemble prompts from the matching `prompt_key` slots before writing freeform prose. Prefer `python scripts/assemble_prompt.py <prompt_key> --project-dir <project> --episode <episode> --shot-id <shot_id> --out <prompt_file>` for repeatable assembly.
- Include fixed character `visual_hint`, appearance, active costume, locked references, and negative rules.
- For scene reference prompts, describe the environment only. Do not include people, figures, dialogue, or action.
- For shot frame prompts, include shot type, camera angle, composition, visible characters, single action or stable pose, environment, lighting, and style.
- For grid prompts, state the exact rows, columns, and panel count. Require separate panels and consistent style.
- When using nine-grid, create or update `episodes/<episode>/grid/grid_assignments.json`; after image generation, run or require `scripts/split_grid_image.py`, then `scripts/select_grid_cell.py` for selected cells.
- Include scene and prop references when present, with file IDs or paths when available.
- Use vertical 9:16 composition unless project says otherwise.
- Add `no text`, `no watermark`, and project-specific identity drift negatives unless the target provider forbids negative wording.
- Keep one prompt file per shot per version.
- Update `prompt_index.json`.

## Output

Versioned image prompt files and prompt index entries.
