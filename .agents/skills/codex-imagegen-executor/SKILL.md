---
name: codex-imagegen-executor
description: Execute AI manga/drama image generation through a Codex subagent instead of a manual web provider. Use when a task, provider capability, or production supervisor selects `codex_imagegen_subagent` for character reference sheets, shot stills, first/end keyframes, grids, costume packs, expression packs, or other bitmap image assets that must be generated and then registered in local project metadata.
---

# Codex Imagegen Executor

## Contract

Use a Codex worker subagent for image generation with:

- `model`: a supported model explicitly configured for the current session
- `reasoning_effort`: `xhigh`
- `service_tier`: default unless the user explicitly changes it

This skill is for image assets only. Do not use it for video generation; the current video transition provider is Gemini/Veo manual web.

The public capability profile and fictional task records use `configure_supported_model`
as a configuration placeholder. Stop while that placeholder remains; select a model
available to the current session and record its actual identifier before dispatch.

## Required Inputs

Read the relevant project files before generation:

- `project.json`
- `characters.json`
- `style_guide.md`
- `assets.json`
- `provider_capabilities/provider_capabilities.json`
- `prompt_templates/registry.json`
- target episode `storyboard.json`
- target episode `tasks.json`
- target prompt file from the task
- any locked reference image paths named by the task or character card

Block generation if the target task has a missing prompt, stale prompt, failed prompt review, impossible provider capability, or missing required reference image.

## Workflow

1. Confirm the task provider is `codex_imagegen_subagent`.
2. Confirm the task type is image generation or an image-like asset task: character reference, shot image, keyframe, grid image, costume pack, expression pack, or scene/prop reference.
3. Build a concise image prompt from the approved prompt file and structured task data.
4. Confirm the runtime model is configured, then spawn a Codex worker with that actual model identifier and a supported reasoning effort.
5. Tell the worker to generate the requested bitmap asset, respecting style profile, aspect ratio, locked references, negative rules, and candidate policy.
6. Save or collect generated image files under the project asset path selected by the task.
7. Register every generated candidate in `assets.json` with provider metadata, checksum if available, prompt file, candidate group, candidate index, selected state, and quality notes.
8. Do not auto-select a final candidate unless the task is explicitly marked as smoke-test or single-candidate. Otherwise route to `asset-reviewer`.

## Candidate Policy

Interpret candidate counts per candidate group:

- For an ordinary shot still or non-critical reference: generate 2 candidates.
- For a key character reference sheet, keyframe pair, hero shot, reusable scene/prop reference, costume pack, or expression pack: generate 4 candidates.
- For quick smoke tests only: 1 candidate is acceptable, but record it as an accepted risk.

One shot can have multiple candidate groups, for example first-frame candidates and last-frame candidates. Count each group separately.

## Output Rules

Generated image assets must not be treated as production-ready until metadata exists.

Each registered asset should include:

- `asset_id`
- `type`
- `scope`
- `shot_id` or `character_id` context in `meta`
- `provider`: `codex_imagegen_subagent`
- `model`: the actual identifier used for generation
- `generation_mode`: `codex_subagent_imagegen`
- `prompt_file`
- `candidate_group_id`
- `candidate_index`
- `path`
- `checksum` when available
- `selected`
- `quality_notes`

If generation fails, update the task with `status: failed`, add the failure reason, and route to `character_failure_diagnosis` or `shot_rerun_diagnosis`.
