# Output Format

Return one concise provider-facing prompt and a separate metadata block:

```text
PROMPT: [duration], [aspect ratio], [active style profile], [scene], [character visual anchors], [camera movement], [action progression], [first/last frame interpolation intent], [style cautions].
METADATA: style_profile_id=[style_profile_id]; reference_mode=[mode]; first_frame=[path or pending]; last_frame=[path or pending]; dialogue_context=[yes/no]
HUMAN_WEB_STEPS: upload=[first/last/reference files]; paste_prompt=yes; check_style=[style-specific cautions]; download_naming=[expected output path]
```
