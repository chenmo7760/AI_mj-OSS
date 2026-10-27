---
name: project-reviewer
description: Use to review an AI manga project skeleton before production starts, checking directories, core JSON files, style guide, cost file, quality gate policy, and whether the project is ready for source event planning.
---

# Project Reviewer

Review only the project setup. Do not create story content.

## Inputs

- `project.json`
- `style_guide.md`
- `cost.json`
- `freeze_log.md`
- expected project directories

## Checks

- Required directories exist.
- `project.json` has `project_id`, format, target platform, duration, skill source, and quality gate policy.
- `prompt_templates/registry.json` exists when referenced by project config, and every required slot file exists.
- `provider_capabilities/provider_capabilities.json` exists when referenced by project config, and task provider IDs are registered there.
- `global_asset_library` and `asset_resolution_order` are declared if cross-episode reuse is planned.
- `style_guide.md` gives visual and narrative constraints.
- `cost.json` exists even if empty.
- `freeze_log.md` exists.
- No stage is marked frozen without a review file.

## Output

Write `reviews/project_review_vXXX.md` or project-level review notes with:

- `Result`
- `Missing Files`
- `Blocking Findings`
- `Required Fixes`
- `Next Role`
