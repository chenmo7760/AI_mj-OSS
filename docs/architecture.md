# Architecture

The workflow stores durable data in ordinary project files:

`source_events.json -> characters.json -> storyboard.json -> prompt_index.json -> tasks.json -> assets.json`

`scripts/validate_all.py` checks required files and selected cross-file references. It is a
lightweight structural validator, not a complete JSON Schema or media-quality validator.
`scripts/assemble_prompt.py` combines a template's slots with project context.
`scripts/provider_adapter.py` prepares payloads and registers user-supplied results;
it does not implement a complete provider SDK lifecycle.
`scripts/check_generation_readiness.py` blocks missing prompts, reviews and selected inputs.
`scripts/generate_gate_report.py` aggregates review, stale-item and task findings.

Use the normal review roles before generation and before export. An empty or structurally
valid asset list does not establish that any image, video or final production exists.
