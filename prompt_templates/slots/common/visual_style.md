# Visual Style

Keep the project art direction consistent across shots. Reuse style anchors from `style_guide.md`, avoid sudden palette changes, and keep character silhouettes recognizable in vertical 9:16 composition.

Use the active `style_profile_id` from `project.json` or the shot override when present. Judge style match against the referenced entry in `style_profiles/style_profiles.json`, not against a hard-coded default.

- For `style_motion_comic_v001`, preserve a colorful motion-comic / illustrated drama look and reject unapproved photorealistic live-action drift.
- For `style_live_action_light_realism_v001`, preserve cinematic actor-like realism and reject unapproved comic/anime drift or celebrity likeness.
- If a shot intentionally changes style, the shot must declare its own `style_profile_id` and the reviewer must approve the override.
