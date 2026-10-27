# AI_mj Codex Instructions

Project scope is the current repository root.

This repository is a Codex-first AI manga/drama production system. Keep durable workflows in `.agents/skills`, data contracts in `schemas`, executable local checks in `scripts`, and production decisions in `docs`.

## Always-Apply Rules

- Follow higher-priority system, developer, and tool instructions first.
- Do not skip reviewer gates. A `Needs Fix`, `Blocked`, or `Needs Human Decision` result must be fixed or explicitly accepted by the user before downstream production.
- Do not treat external media generation as complete until results are registered in `assets.json` with path, provider, model, prompt, selection status, and quality notes.
- Keep `docs/open_source/_repos/` as local reference cache only. Do not copy large open-source modules, long prompt prose, or license-sensitive code into this repo without an explicit decision.
- Keep generated images, videos, audio, and delivery packages out of git unless the user explicitly asks to track a specific artifact.
- Prefer `scripts/run_project_checks.ps1` for local validation/readiness/gate checks.
- Use `provider_capabilities/provider_capabilities.json` before planning generation work.
- Record aesthetic, budget, provider, commercial, and platform-route decisions in `docs/production_decisions_needed_v0.1.md` or a project review file.

## Default Verification

Run the offline public-example checks:

```powershell
python scripts/check_public_examples.py
```

The supplied fixtures are fictional and intentionally blocked for external media generation.
Do not remove their review gates to make a demo look production-ready. Configure an available
runtime model and complete reviews before requesting generated media. The placeholder
`configure_supported_model` is not a callable model ID.
