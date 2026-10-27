---
name: asset-reviewer
description: Use to review AI manga/drama generated assets, candidate pools, naming, metadata, selected/rejected rationale, and whether image/video/voice assets can enter downstream production.
---

# Asset Reviewer

Review asset registration and candidate selection. Do not delete candidates.

## Inputs

- `assets.json`
- `storyboard.json`
- `tasks.json`
- files under `assets/*`

## Checks

- Asset paths exist or missing files are listed.
- Every shot asset has `shot_id`.
- Candidate groups have rank, selected flag, active flag, variant ID, and rejected reasons.
- Compare 2-4 candidates side by side in writing when available; do not accept the first candidate just because it exists.
- For nine-grid assets, verify `grid/grid_assignments.json` maps selected cells to `first_frame`, `last_frame`, or `reference` with row/column/crop metadata. Check that `scripts/split_grid_image.py` produced a split manifest and `scripts/select_grid_cell.py` produced a selection manifest when grid cells are used downstream.
- Verify asset inheritance scope (`global`, `project`, `episode`, `shot`) and whether lower-scope assets override higher-scope assets intentionally.
- Provider, model, generation mode, reference mode, provider task/request IDs, prompt file, seed, duration, resolution, and first/last frame inputs are recorded when available.
- `last_frame_url` or generated end-frame metadata is preserved if the provider returns it.
- Duration, width, height, fps, checksum are present when available.
- Selected assets match storyboard and prompts.
- Selected assets match the active `style_profile_id`. Do not reject photorealism merely because it is not motion-comic when the project is `style_live_action_light_realism_v001`.
- If an asset style differs from the project default, require a shot-level `style_profile_id` override and review rationale before it can be selected.
- Selected assets must not break locked character identity, costume, scene, prop, or continuity links.
- If no candidate is good enough, require rerun with targeted changes rather than forcing a bad selection.
- If an upstream artifact is stale, do not pass selected assets unless the stale risk is explicitly accepted.
- Use `docs/reviewer_casebook_v0.1.md` when available to calibrate common failure types such as style drift, weak comedy readability, missing character anchors, and candidate-pool shortcuts.

## Output

Write `episodes/<episode>/reviews/<episode>_asset_review_vXXX.md`.
