# AI_mj-OSS

A small, file-based workflow prototype for AI-assisted manga and short-drama preparation.
The core tools validate links between story events, character cards, storyboards, prompt
templates, tasks and asset records. They also prepare provider payloads and review gates.

这是脱敏后的公开版。`projects/` 中的人物、对白和事件全部作为虚构演示使用；
不包含真实客户资料、个人工作路径、生成媒体、历史制作报告或私有开发历史。

## Quick start

Python 3.10 or newer is required. The offline checks use only the standard library:

```sh
git clone https://github.com/chenmo7760/AI_mj-OSS.git
cd AI_mj-OSS
python scripts/check_public_examples.py
```

The check validates both fictional projects and verifies that the missing-review gate blocks
generation. A successful offline check does **not** approve the example for production.
Generated check reports stay under ignored `projects/*/episodes/ep01/reports/` paths.

For a single structural check:

```sh
python scripts/validate_all.py projects/demo-drama
python scripts/validate_all.py projects/office-comedy-test
```

## What is included

| Directory | Purpose |
| --- | --- |
| `scripts/` | Local validation, prompt assembly, routing and asset bookkeeping |
| `schemas/` | JSON data contracts |
| `prompt_templates/` | Reusable prompt slots and registry |
| `style_profiles/` | Fictional visual-style examples |
| `provider_capabilities/` | Example capability profiles |
| `.agents/skills/` | Optional workflow role instructions for Codex |
| `projects/` | Two fictional text-and-metadata fixtures |

## External generation and optional tools

No API key, paid service or model request is needed for the quick start. Provider profiles
are examples, not a guarantee of current service availability. Replace the explicit
`configure_supported_model` placeholder with a model available to your own session before
generation; never send that placeholder to a service. Keep keys and local configuration
outside committed files. Image helpers optionally require Pillow; final composition needs
a separately installed FFmpeg. Video generation currently uses a manually managed provider
handoff; automatic submit/poll/download integration is incomplete.

The public fixtures contain no media, selected candidates, real spend or approved production
reviews. Character-reference locking, production quality, external providers, TTS and final
export have not been accepted by this public release's offline checks.

## Documentation

- [Architecture and workflow](docs/architecture.md)
- [Example scope and validation limits](docs/public_examples.md)
- [Provider decisions](docs/production_decisions_needed_v0.1.md)
- [Contribution and data policy](CONTRIBUTING.md)
- [Dependency and source notes](THIRD_PARTY_NOTICES.md)

## License

Original code, templates and fictional examples in this public edition are available under
the [MIT License](LICENSE). External tools and services retain their own licenses and terms.
