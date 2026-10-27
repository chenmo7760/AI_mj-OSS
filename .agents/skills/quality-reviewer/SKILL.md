---
name: quality-reviewer
description: Use for final or cross-stage AI manga/drama quality review, checking storyboard-to-output match, asset completeness, character consistency, continuity, subtitles, audio, rerun needs, and accepted risks.
---

# Quality Reviewer

Run cross-stage quality review. Do not replace node reviewers.

## Inputs

- `source_events.json`
- `script.md`
- `storyboard.json`
- `prompt_index.json`
- `assets.json`
- output files
- prior reviews

## Checks

- Selected assets cover required shots.
- Run or inspect `scripts/check_continuity.py` output before final pass.
- Run or inspect `scripts/check_visual_continuity.py` when adjacent start/end frame images exist.
- Use `scripts/generate_gate_report.py` as structured gate input for production-supervisor.
- Check `stale_manifest.json` and block final pass when high-severity stale items remain.
- Check `shot_routes.json` for unresolved missing inputs.
- Check selected assets against `resolved_assets.json` when asset inheritance is used.
- Character, costume, scene, and prop continuity are acceptable.
- Video duration and order match storyboard.
- Subtitles and voice are complete.
- Rerun shots are identified with reasons.
- Risks are recorded rather than hidden.
- Use `docs/reviewer_casebook_v0.1.md` when available to separate pipeline pass from final quality pass.

## Output

Write `episodes/<episode>/reviews/<episode>_quality_review_vXXX.md` and rerun task suggestions.
