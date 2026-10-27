# Assembled Prompt: shot_image

Template Version: 1
Prompt Type: image
Episode: ep01
Shot ID: ep01_s001

## Slots

### role_definition

# Role Definition

You are a production prompt specialist for a vertical AI manga/drama workflow. Preserve approved story facts, locked character identity, scene continuity, and provider constraints. Do not invent missing plot facts when a structured field is available.

### source_grounding

# Source Grounding

Use these inputs in priority order:

1. Frozen source events and approved script.
2. Approved character cards, `visual_hint`, active costume, locked reference assets, and negative rules.
3. Approved storyboard fields: action, result, camera, motion_script, video_script, dialogues, scene, props, and continuity links.
4. Style guide and provider capability profile.

If inputs conflict, surface the conflict for review instead of silently choosing.

### visual_style

# Visual Style

Keep the project art direction consistent across shots. Reuse style anchors from `style_guide.md`, avoid sudden palette changes, and keep character silhouettes recognizable in vertical 9:16 composition.

Use the active `style_profile_id` from `project.json` or the shot override when present. Judge style match against the referenced entry in `style_profiles/style_profiles.json`, not against a hard-coded default.

- For `style_motion_comic_v001`, preserve a colorful motion-comic / illustrated drama look and reject unapproved photorealistic live-action drift.
- For `style_live_action_light_realism_v001`, preserve cinematic actor-like realism and reject unapproved comic/anime drift or celebrity likeness.
- If a shot intentionally changes style, the shot must declare its own `style_profile_id` and the reviewer must approve the override.

### composition_rules

# Composition Rules

For shot images, describe a single stable frame. Include shot type, camera angle, focal subject, visible characters with `visual_hint`, active costume, key props, scene, lighting, color palette, and subtitle-safe lower frame when subtitles are planned.

For scene references, exclude people and action. For character references, use a neutral pose and plain background.


## Project Override

doorway-to-meeting diagonal, bright office sitcom energy

### output_format

# Output Format

Return one prompt block:

```text
[aspect ratio], [medium/style], [shot type and camera angle]. [visible characters with visual_hint and costume]. [single action or stable pose]. [scene, props, lighting, color]. [style anchors]. no text, no watermark.
```

### negative_rules

# Negative Rules

Avoid identity drift, changed face, changed hair, changed costume, wrong era, extra characters, duplicated limbs, malformed hands, visible captions, subtitles, logos, watermarks, UI elements, and modern objects unless explicitly required by the storyboard.

## Production Context

```json
{
  "project": {
    "schema_version": "0.1.0",
    "project_id": "office-comedy-test",
    "title": "Office Comedy Image Test",
    "format": "vertical_short_comedy",
    "target_platform": [
      "douyin",
      "kuaishou"
    ],
    "episode_duration_sec": 24,
    "visual_style": "cinematic live-action light realism, modern Chinese office comedy, vertical 9:16",
    "style_profiles_file": "style_profiles/style_profiles.json",
    "style_profile_id": "style_live_action_light_realism_v001",
    "allowed_style_profile_ids": [
      "style_live_action_light_realism_v001",
      "style_motion_comic_v001"
    ],
    "skill_source": ".agents/skills",
    "prompt_template_registry": "prompt_templates/registry.json",
    "provider_capabilities_file": "provider_capabilities/provider_capabilities.json",
    "global_asset_library": "global_assets.json",
    "asset_resolution_order": [
      "global",
      "project",
      "episode",
      "shot"
    ],
    "delivery_policy": {
      "include_final_mp4": false,
      "include_shot_segments": false,
      "include_source_assets": true,
      "include_prompt_package": true,
      "include_subtitles": false
    },
    "quality_gate_policy": {
      "required_before_generation": true,
      "required_before_export": true,
      "max_auto_fix_rounds": 2
    },
    "status": "image_test",
    "created_at": "2026-07-08"
  },
  "style_profiles": {
    "schema_version": "0.1.0",
    "styles": [
      {
        "style_profile_id": "style_motion_comic_v001",
        "style_family": "motion_comic",
        "display_name": "Color Motion-Comic Vertical Drama",
        "intended_use": "Illustrated or comic-like AI drama where stable silhouettes, readable expressions, and stylized acting are more important than live-action realism.",
        "positive_rules": [
          "colorful motion-comic vertical drama",
          "clear character silhouettes and stable facial anchors",
          "cinematic lighting with illustrated or painterly finish",
          "expressive but believable acting",
          "consistent costume, hair, accessories, and scene palette"
        ],
        "negative_rules": [
          "photorealistic live-action look unless explicitly approved",
          "anime exaggeration that changes the intended age or identity",
          "washed-out flat illustration",
          "style switching between shots",
          "visible captions, watermarks, logos, or UI text"
        ],
        "reference_policy": {
          "character_reference_required_for_recurring_characters": true,
          "recommended_views": [
            "front_full_body",
            "three_quarter",
            "side",
            "back",
            "head_closeup",
            "expression_sheet"
          ],
          "separate_reference_per_style": true
        },
        "review_rubric": {
          "identity": "Face, hair, silhouette, costume, and signature accessories remain recognizable as the locked character.",
          "style_match": "The result reads as motion-comic instead of live-action photography.",
          "story_readability": "The shot communicates the intended beat in vertical 9:16.",
          "continuity": "Lighting, palette, costume, and scene remain compatible with adjacent shots."
        },
        "manual_generation_notes": {
          "codex_imagegen": "Ask for a colorful motion-comic still, clear line/painterly finish, stable character anchors, and no photorealistic live-action look.",
          "gemini_video_web": "Paste the video prompt with the motion-comic style line intact; upload locked character or first/last frames when available; reject outputs that become live-action photos unless the shot has an approved override."
        }
      },
      {
        "style_profile_id": "style_live_action_light_realism_v001",
        "style_family": "live_action_light_realism",
        "display_name": "Live-Action Light Realism Vertical Drama",
        "intended_use": "Actor-like vertical short-drama visuals with natural faces, practical lighting, and realistic locations while still avoiding celebrity likeness or uncontrolled identity drift.",
        "positive_rules": [
          "cinematic live-action vertical short drama",
          "natural actor-like faces without celebrity likeness",
          "realistic lighting, lens, wardrobe, and workplace or period-drama production design",
          "subtle but readable acting",
          "consistent hairstyle, costume, age, and body type"
        ],
        "negative_rules": [
          "comic or anime rendering unless explicitly approved",
          "celebrity likeness or recognizable real person",
          "age drift, face drift, hairstyle drift, or costume drift",
          "overly glossy stock-photo look",
          "visible captions, watermarks, logos, or UI text"
        ],
        "reference_policy": {
          "character_reference_required_for_recurring_characters": true,
          "recommended_views": [
            "front_full_body",
            "three_quarter",
            "side",
            "back",
            "head_closeup",
            "expression_sheet"
          ],
          "separate_reference_per_style": true
        },
        "review_rubric": {
          "identity": "The character feels like the same actor-like person across shots without copying a real celebrity.",
          "style_match": "The result reads as light live-action realism instead of comic/anime illustration.",
          "story_readability": "The action and emotion are readable in vertical 9:16.",
          "continuity": "Costume, setting, lens feel, lighting, and age remain stable across adjacent shots."
        },
        "manual_generation_notes": {
          "codex_imagegen": "Ask for cinematic live-action light realism, natural actor-like faces, realistic office or drama lighting, and no celebrity likeness.",
          "gemini_video_web": "Use the live-action style line; upload first/last frames and references when available; reject outputs with celebrity likeness, face drift, or sudden comic/anime rendering."
        }
      }
    ]
  },
  "source_events": [
    {
      "event_id": "event_office_001",
      "source": "user_theme",
      "chapter": "ep01",
      "summary": "Demo Worker rushes into the office with coffee and discovers the whole team waiting for a serious meeting.",
      "characters": [
        "char_demo_worker",
        "char_demo_manager"
      ],
      "location": "modern open office",
      "must_keep": true,
      "dramatic_function": "setup",
      "adapted_episode": "ep01",
      "adapted_shots": [
        "ep01_s001"
      ],
      "frozen_version": "source_events_v001",
      "review_file": "episodes/ep01/reviews/ep01_source_event_review_v001.md"
    },
    {
      "event_id": "event_office_002",
      "source": "user_theme",
      "chapter": "ep01",
      "summary": "A tiny office robot vacuum bumps Demo Worker's chair at the worst possible moment, sending his sticky-note-covered weekly report into the air.",
      "characters": [
        "char_demo_worker",
        "char_demo_manager"
      ],
      "location": "meeting area inside modern office",
      "must_keep": true,
      "dramatic_function": "comic accident",
      "adapted_episode": "ep01",
      "adapted_shots": [
        "ep01_s002"
      ],
      "frozen_version": "source_events_v001",
      "review_file": "episodes/ep01/reviews/ep01_source_event_review_v001.md"
    },
    {
      "event_id": "event_office_003",
      "source": "user_theme",
      "chapter": "ep01",
      "summary": "Demo Manager catches one sticky note on his face while Demo Worker freezes, turning the serious meeting into silent chaos.",
      "characters": [
        "char_demo_worker",
        "char_demo_manager"
      ],
      "location": "meeting area inside modern office",
      "must_keep": true,
      "dramatic_function": "visual punchline",
      "adapted_episode": "ep01",
      "adapted_shots": [
        "ep01_s003"
      ],
      "frozen_version": "source_events_v001",
      "review_file": "episodes/ep01/reviews/ep01_source_event_review_v001.md"
    }
  ],
  "style_guide": "# Style Guide\n\n## Format\n\n- Vertical 9:16 live-action light realism style.\n- Bright modern Chinese office comedy.\n- Visual tone: clean, realistic, expressive, workplace sitcom energy.\n- Avoid celebrity likeness. Characters should feel like fictional actor-like people, not recognizable real people.\n\n## Comedy Rules\n\n- The joke should be understandable from the image alone.\n- Use exaggerated facial expressions and body language, but keep anatomy believable.\n- Avoid on-image text whenever possible; props can imply the joke.\n- Keep office setting recognizable: desks, monitors, sticky notes, coffee cups, meeting-room glass, fluorescent ceiling lights.\n\n## Character Consistency\n\n- Demo Worker: young operations employee, short black hair, round glasses, white shirt, loosened blue tie, anxious but earnest.\n- Demo Manager: middle-aged department manager, neat side-part hair, navy suit, red lanyard, serious face that accidentally makes situations funnier.\n\n## Negative Rules\n\nNo watermark, no subtitles, no UI text, no fake letters, no distorted hands, no extra main characters, no celebrity likeness, no brand logos.\n",
  "episode_script": "# Episode ep01 Script\n\nEpisode target: 3-shot image-stage comedy test.\n\n## Beat 1: The Serious Meeting\n\nEvent: `event_office_001`\n\nAction: Demo Worker rushes into the open office holding coffee, then realizes Demo Manager and the team are already waiting in a serious meeting pose.\n\nDialogue: Demo Worker whispers, \"I am only... three minutes professionally late.\"\n\n## Beat 2: The Tiny Disaster\n\nEvent: `event_office_002`\n\nAction: Demo Worker sits down too quickly. A small robot vacuum bumps his chair. Sticky notes fly up from his weekly report like confetti.\n\nDialogue: Demo Manager says, \"Explain this report.\"\n\n## Beat 3: Silent Punchline\n\nEvent: `event_office_003`\n\nAction: One sticky note lands perfectly on Demo Manager's face. Demo Worker freezes with coffee in hand while everyone else tries not to laugh.\n\nDialogue: Demo Worker whispers, \"The report has... reached leadership.\"\n\nEnding hook: Demo Manager slowly lifts the sticky note, still deadpan.\n",
  "characters": [
    {
      "character_id": "char_demo_worker",
      "name": "Demo Worker",
      "role": "office_employee",
      "age": 27,
      "appearance": "short black hair, round glasses, slim build, expressive anxious face",
      "visual_hint": "short black hair, round glasses, white shirt, loosened blue tie, office ID badge",
      "style_profile_ids": [
        "style_live_action_light_realism_v001",
        "style_motion_comic_v001"
      ],
      "default_style_profile_id": "style_live_action_light_realism_v001",
      "body_type": "slim young office worker",
      "height_cm": 174,
      "performance_style": "nervous office-comedy physical acting; quick eye shifts, tense shoulders, awkward freezes, and good-natured panic.",
      "active_costume_id": "costume_demo_worker_v001",
      "costume_sets": [
        {
          "costume_id": "costume_demo_worker_v001",
          "name": "modern office outfit",
          "description": "white office shirt, loosened blue tie, dark trousers, ID badge, sleeves slightly rolled",
          "negative_rules": [
            "no hoodie",
            "no luxury suit",
            "do not remove glasses",
            "do not remove blue tie"
          ],
          "reference_assets": [],
          "locked": false
        }
      ],
      "personality": "earnest, nervous, tries too hard, physically awkward in funny situations",
      "negative_rules": [
        "no beard",
        "no hoodie",
        "no luxury suit",
        "do not remove glasses"
      ],
      "reference_assets": [],
      "locked_asset_ids": [],
      "voice": {
        "style": "fast, nervous, good-natured"
      },
      "frozen_version": "characters_v001",
      "review_file": "episodes/ep01/reviews/ep01_character_review_v001.md"
    },
    {
      "character_id": "char_demo_manager",
      "name": "Demo Manager",
      "role": "department_manager",
      "age": 45,
      "appearance": "neat side-part black hair, square face, serious eyebrows, average build",
      "visual_hint": "middle-aged manager, navy suit, red lanyard, serious face, neat side-part hair",
      "style_profile_ids": [
        "style_live_action_light_realism_v001",
        "style_motion_comic_v001"
      ],
      "default_style_profile_id": "style_live_action_light_realism_v001",
      "body_type": "average-build middle-aged manager",
      "height_cm": 176,
      "performance_style": "deadpan comedy acting; minimal facial movement, precise posture, slow surprised blinks, and restrained authority.",
      "active_costume_id": "costume_demo_manager_v001",
      "costume_sets": [
        {
          "costume_id": "costume_demo_manager_v001",
          "name": "manager business suit",
          "description": "navy business suit, white shirt, red lanyard, black leather shoes",
          "negative_rules": [
            "no smiling villain look",
            "no celebrity likeness",
            "do not change lanyard color",
            "do not make suit black"
          ],
          "reference_assets": [],
          "locked": false
        }
      ],
      "personality": "stern, precise, unintentionally funny when surprised",
      "negative_rules": [
        "no smiling villain look",
        "no celebrity likeness",
        "do not change lanyard color"
      ],
      "reference_assets": [],
      "locked_asset_ids": [],
      "voice": {
        "style": "low, serious, deadpan"
      },
      "frozen_version": "characters_v001",
      "review_file": "episodes/ep01/reviews/ep01_character_review_v001.md"
    }
  ],
  "shot": {
    "shot_id": "ep01_s001",
    "episode": "ep01",
    "order": 1,
    "title": "Late But Confident",
    "duration_sec": 4,
    "location": "modern open office",
    "time": "weekday morning",
    "atmosphere": "bright, tense, awkwardly formal",
    "scene": "A bright modern open office with glass meeting room, desks, monitors, coffee cups, sticky notes, and a serious meeting already waiting.",
    "scene_title": "Morning Meeting Area",
    "scene_description": "Demo Worker rushes in with coffee and realizes the meeting has already started.",
    "lighting": "soft daylight mixed with clean office ceiling lights",
    "color_palette": "white, office blue, sticky-note yellow, coffee brown",
    "characters": [
      "char_demo_worker",
      "char_demo_manager"
    ],
    "character_ids": [
      "char_demo_worker",
      "char_demo_manager"
    ],
    "action": "Demo Worker freezes mid-step with coffee in hand while Demo Manager looks at him from the meeting table.",
    "result": "The serious meeting energy makes Demo Worker's lateness visually funny.",
    "dialogue": "I am only... three minutes professionally late.",
    "dialogues": [
      {
        "sequence": 1,
        "character_id": "char_demo_worker",
        "speaker": "Demo Worker",
        "text": "I am only... three minutes professionally late.",
        "emotion": "nervous whisper",
        "start_ratio": 0.45,
        "end_ratio": 0.85
      }
    ],
    "narration": "Demo Worker enters like he still has a chance.",
    "camera": "vertical 9:16 medium wide office comedy frame",
    "shot_type": "medium wide",
    "angle": "slightly low angle from office doorway",
    "movement": "static image prompt only",
    "camera_direction": "Frame Demo Worker foreground left, meeting table and Demo Manager background right.",
    "composition_guide": "Use diagonal tension between late employee and serious manager; leave bottom third clean.",
    "focal_point": "Demo Worker's frozen expression and coffee cup",
    "depth_of_field": "moderate depth, readable office background",
    "motion_script": "Static image: Demo Worker frozen mid-step; Demo Manager staring from meeting table.",
    "video_script": "Not used in image-stage test.",
    "image_prompt": "Vertical 9:16 cinematic live-action light realism office comedy frame, Demo Worker frozen mid-step with coffee, Demo Manager serious at meeting table.",
    "video_prompt": null,
    "bgm_prompt": null,
    "sound_effect": null,
    "sound_design": null,
    "music_cue": null,
    "transition_in": null,
    "transition_out": null,
    "reference_image_prompts": [
      "Modern Chinese open office, glass meeting room, desks, monitors, sticky notes, coffee cups, bright daylight, no people, no text",
      "Demo Worker office comedy character, short black hair, round glasses, white shirt, loosened blue tie, anxious expression"
    ],
    "reference_images": [],
    "costume_overrides": {
      "char_demo_worker": "costume_demo_worker_v001",
      "char_demo_manager": "costume_demo_manager_v001"
    },
    "source_events": [
      "event_office_001"
    ],
    "scene_asset_ids": [],
    "prop_asset_ids": [],
    "previous_shot_summary": null,
    "next_shot_intent": "Robot vacuum causes sticky-note disaster.",
    "continuity_from": null,
    "continuity_to": "ep01_s002",
    "keyframes": {
      "start_frame": null,
      "end_frame": null,
      "start_frame_prompt": "Demo Worker enters modern office holding coffee, Demo Manager watches from meeting table.",
      "end_frame_prompt": null
    },
    "prompt_files": {
      "image": "episodes/ep01/prompts/ep01_s001_image_v001.md"
    },
    "prompt_versions": {
      "image": 1
    },
    "assets": {
      "image": null,
      "video": null,
      "voice": null
    },
    "quality_gate": {
      "status": "pending",
      "review_file": null
    },
    "route_plan": {
      "route": "text-only",
      "reference_mode": "text_only",
      "provider_id": "codex_imagegen_subagent",
      "rationale": "Image-stage still frame test; no video route needed yet."
    },
    "stale": false,
    "stale_reason": null,
    "frozen_version": "storyboard_v001",
    "status": "planned"
  },
  "storyboard": null,
  "prompt_index_entry": {
    "prompt_id": "prompt_ep01_s001_image_v001",
    "shot_id": "ep01_s001",
    "prompt_type": "image",
    "prompt_key": "shot_image",
    "variant": "baseline",
    "language": "mixed_zh_en",
    "style_profile_id": "style_live_action_light_realism_v001",
    "version": 1,
    "prompt_file": "episodes/ep01/prompts/ep01_s001_image_v001.md",
    "previous_prompt_id": null,
    "derived_from": [
      "source_events:event_office_001",
      "characters:char_demo_worker",
      "characters:char_demo_manager",
      "style_guide:v001",
      "storyboard:ep01_s001"
    ],
    "provider_target": "codex_imagegen_subagent",
    "template_ref": "shot_image",
    "template_version": 1,
    "slot_contents": {
      "character_visual_hint": "Demo Worker: round glasses, white shirt, blue tie; Demo Manager: navy suit, red lanyard",
      "reference_mode": "text_only_first_test",
      "composition_rules": "doorway-to-meeting diagonal, bright office sitcom energy"
    },
    "polish_history": [],
    "ab_test_group_id": null,
    "stale": false,
    "stale_reason": null,
    "rollback_of": null,
    "change_reason": "office comedy image-stage baseline",
    "review_status": "pass",
    "review_file": "episodes/ep01/reviews/ep01_image_prompt_review_v001.md",
    "frozen": false,
    "created_at": "2026-07-08"
  },
  "slot_overrides": {
    "character_visual_hint": "Demo Worker: round glasses, white shirt, blue tie; Demo Manager: navy suit, red lanyard",
    "reference_mode": "text_only_first_test",
    "composition_rules": "doorway-to-meeting diagonal, bright office sitcom energy"
  }
}
```

## Final Instruction

Use the slots and production context above to produce the requested artifact. Preserve frozen facts and return the output format required by the template.
