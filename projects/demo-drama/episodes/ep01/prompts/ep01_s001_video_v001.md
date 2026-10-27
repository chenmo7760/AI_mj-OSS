# Assembled Prompt: shot_video_first_last

Template Version: 1
Prompt Type: video
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

### motion_rules

# Motion Rules

Use `motion_script` for time-segmented planning, but keep the final model prompt concise. Preserve one primary action or emotional beat per shot. Do not insert spoken dialogue into motion prose unless the provider explicitly asks for dialogue in the prompt.


## Project Override

time segmented motion in storyboard; final prompt concise

### keyframe_rules

# Keyframe Rules

When first and last frames are available, treat them as hard visual anchors. The prompt must interpolate between them and must not contradict character identity, costume, scene, prop placement, or final pose. If only keyframe descriptions exist, mention them as planned anchors and mark the task as awaiting frame assets.


## Project Override

first and last frames are hard anchors when generated

### dialogue_rules

# Dialogue Rules

Use `dialogues` only as voice/subtitle timing context. Do not ask the video model to draw subtitles, captions, or speech text on screen.

### output_format

# Output Format

Return one concise provider-facing prompt and a separate metadata block:

```text
PROMPT: [duration], [aspect ratio], [active style profile], [scene], [character visual anchors], [camera movement], [action progression], [first/last frame interpolation intent], [style cautions].
METADATA: style_profile_id=[style_profile_id]; reference_mode=[mode]; first_frame=[path or pending]; last_frame=[path or pending]; dialogue_context=[yes/no]
HUMAN_WEB_STEPS: upload=[first/last/reference files]; paste_prompt=yes; check_style=[style-specific cautions]; download_naming=[expected output path]
```

### negative_rules

# Negative Rules

Avoid identity drift, changed face, changed hair, changed costume, wrong era, extra characters, duplicated limbs, malformed hands, visible captions, subtitles, logos, watermarks, UI elements, and modern objects unless explicitly required by the storyboard.

## Production Context

```json
{
  "project": {
    "schema_version": "0.1.0",
    "project_id": "demo-drama",
    "title": "示例漫剧",
    "format": "vertical_short_drama",
    "target_platform": [
      "kuaishou",
      "douyin"
    ],
    "episode_duration_sec": 120,
    "visual_style": "cinematic motion comic, Chinese fantasy, vertical 9:16",
    "style_profiles_file": "style_profiles/style_profiles.json",
    "style_profile_id": "style_motion_comic_v001",
    "allowed_style_profile_ids": [
      "style_motion_comic_v001",
      "style_live_action_light_realism_v001"
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
      "include_final_mp4": true,
      "include_shot_segments": true,
      "include_source_assets": true,
      "include_prompt_package": true,
      "include_subtitles": true
    },
    "quality_gate_policy": {
      "required_before_generation": true,
      "required_before_export": true,
      "max_auto_fix_rounds": 2
    },
    "status": "draft",
    "created_at": "2026-07-07"
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
      "event_id": "event_ch01_001",
      "source": "demo_outline",
      "chapter": "ch01",
      "summary": "Demo Heroine wakes inside a cold abandoned palace chamber during a rainy night and realizes she is no longer in her own era.",
      "characters": [
        "char_heroine"
      ],
      "location": "cold palace chamber",
      "must_keep": true,
      "dramatic_function": "opening hook and displacement",
      "adapted_episode": "ep01",
      "adapted_shots": [
        "ep01_s001"
      ],
      "frozen_version": "source_events_v002",
      "review_file": "episodes/ep01/reviews/ep01_source_event_review_v001.md"
    },
    {
      "event_id": "event_ch01_002",
      "source": "demo_outline",
      "chapter": "ch01",
      "summary": "Footsteps approach outside the broken door, forcing Demo Heroine to hide before she understands the danger.",
      "characters": [
        "char_heroine"
      ],
      "location": "cold palace chamber",
      "must_keep": true,
      "dramatic_function": "external threat",
      "adapted_episode": "ep01",
      "adapted_shots": [
        "ep01_s002"
      ],
      "frozen_version": "source_events_v002",
      "review_file": "episodes/ep01/reviews/ep01_source_event_review_v001.md"
    },
    {
      "event_id": "event_ch01_003",
      "source": "demo_outline",
      "chapter": "ch01",
      "summary": "Demo Heroine hides behind a torn bed curtain, grips a silver hairpin, and watches the door through a narrow gap.",
      "characters": [
        "char_heroine"
      ],
      "location": "cold palace chamber",
      "must_keep": true,
      "dramatic_function": "survival choice",
      "adapted_episode": "ep01",
      "adapted_shots": [
        "ep01_s003"
      ],
      "frozen_version": "source_events_v002",
      "review_file": "episodes/ep01/reviews/ep01_source_event_review_v001.md"
    },
    {
      "event_id": "event_ch01_004",
      "source": "demo_outline",
      "chapter": "ch01",
      "summary": "A tall shadow stops outside the door; Demo Heroine sees a palace token on the floor and understands someone has deliberately trapped her.",
      "characters": [
        "char_heroine"
      ],
      "location": "cold palace chamber",
      "must_keep": true,
      "dramatic_function": "cliffhanger clue",
      "adapted_episode": "ep01",
      "adapted_shots": [
        "ep01_s004"
      ],
      "frozen_version": "source_events_v002",
      "review_file": "episodes/ep01/reviews/ep01_source_event_review_v001.md"
    }
  ],
  "style_guide": "# Style Guide\n\nFormat: vertical 9:16 short drama.\n\nVisual style: cinematic motion comic, Chinese fantasy, rainy night, restrained color, clear faces.\n\nRules:\n\n- Keep character faces consistent.\n- Prefer strong hooks and clear scene goals.\n- Avoid overly decorative shots that hide the character.\n- Keep subtitles readable on mobile.\n",
  "episode_script": "# Episode ep01 Script\n\n## Logline\n\nOn a rainy night, Demo Heroine wakes in a cold palace chamber, hides from approaching footsteps, and discovers a clue proving she was brought there on purpose.\n\n## Beats\n\n1. Demo Heroine wakes on an old wooden bed. Rain taps the broken window. Her silver hairpin is the only familiar object.\n2. Footsteps approach outside the door. She hears a wooden latch shake.\n3. She slips behind a torn bed curtain, gripping the hairpin like a weapon.\n4. A tall shadow pauses outside. A palace token glints on the wet floor, suggesting a deliberate trap.\n\n## Dialogue\n\n- Demo Heroine: \"Where am I?\"\n- Demo Heroine: \"Someone is outside.\"\n- Demo Heroine: \"Stay quiet... breathe.\"\n- Demo Heroine: \"This was not an accident.\"\n",
  "characters": [
    {
      "character_id": "char_heroine",
      "name": "演示角色甲",
      "role": "female_lead",
      "age": 22,
      "visual_hint": "黑发银簪",
      "style_profile_ids": [
        "style_motion_comic_v001",
        "style_live_action_light_realism_v001"
      ],
      "default_style_profile_id": "style_motion_comic_v001",
      "body_type": "slender young woman",
      "height_cm": 165,
      "appearance": "瓜子脸，杏眼，长黑发，以银色发簪固定发髻。身形纤细，穿浅青色古装，衣料轻薄但不华丽。整体轮廓清冷、干净、带古代宫廷气质，适合制作全身参考图和三视图。",
      "personality": "外柔内刚，警觉，善于隐藏情绪，在危险中会先观察再行动。",
      "performance_style": "紧张时会下意识握紧银簪，先微微后退再抬眼观察；情绪表达克制，眼神变化比大幅动作更明显。",
      "active_costume_id": "costume_heroine_palace_v001",
      "costume_sets": [
        {
          "costume_id": "costume_heroine_palace_v001",
          "name": "冷宫浅青古装",
          "description": "浅青色交领古装，窄袖，银色发簪，素色腰带，无现代饰品。",
          "negative_rules": [
            "不要换成现代服装",
            "不要增加华丽皇冠",
            "不要改变银簪"
          ],
          "reference_assets": [],
          "locked": false
        }
      ],
      "relationships": [],
      "voice": {
        "provider": "to_be_selected",
        "voice_id": "to_be_selected",
        "style": "soft but determined",
        "age_range": "young_adult",
        "emotion_range": "quiet fear to restrained resolve"
      },
      "reference_assets": [],
      "locked_asset_ids": [],
      "negative_rules": [
        "不要改变发色",
        "不要换成现代服装",
        "不要变成欧美脸",
        "不要增加额外发饰",
        "不要改变银色发簪"
      ],
      "frozen_version": "characters_v001",
      "review_file": "episodes/ep01/reviews/ep01_character_review_v001.md"
    }
  ],
  "shot": {
    "shot_id": "ep01_s001",
    "episode": "ep01",
    "order": 1,
    "title": "Rain Wake",
    "duration_sec": 5,
    "location": "cold palace chamber",
    "time": "rainy night",
    "atmosphere": "damp, tense, disoriented",
    "scene": "An abandoned palace bedchamber at night, old wooden bed, torn curtain, rain-streaked window, weak candlelight.",
    "scene_title": "Cold Palace Night",
    "scene_description": "A broken but once elegant chamber with wet wood, candle smoke, and rain-blue shadows.",
    "lighting": "dim candlelight with cold blue rain fill",
    "color_palette": "pale cyan, cold blue, candle amber",
    "characters": [
      "char_heroine"
    ],
    "character_ids": [
      "char_heroine"
    ],
    "action": "Demo Heroine jolts awake on an old bed, scans the chamber, and grips the silver hairpin in her hair.",
    "result": "She realizes the place is unfamiliar and becomes alert.",
    "dialogue": "Where am I?",
    "dialogues": [
      {
        "sequence": 1,
        "character_id": "char_heroine",
        "speaker": "Demo Heroine",
        "text": "Where am I?",
        "emotion": "low, confused, frightened",
        "start_ratio": 0.58,
        "end_ratio": 0.82
      }
    ],
    "narration": "She wakes to rain and a room she has never seen before.",
    "camera": "vertical 9:16 medium close-up, slow push-in",
    "shot_type": "medium close-up",
    "angle": "slightly high angle to eye level",
    "movement": "slow push-in",
    "camera_direction": "Push in from bed edge to Demo Heroine's face and silver hairpin.",
    "composition_guide": "Keep her face and silver hairpin upper center; keep lower frame subtitle-safe.",
    "focal_point": "Demo Heroine's startled eyes and silver hairpin",
    "depth_of_field": "shallow depth of field, background candle and rainy window softly blurred",
    "motion_script": "0-3s: Demo Heroine wakes sharply and half-sits on the bed. 3-5s: she scans the chamber and grips the silver hairpin.",
    "video_script": "Rainy cold palace chamber. Demo Heroine wakes on an old bed, tense and confused, then grips a silver hairpin as candlelight flickers.",
    "image_prompt": "Vertical 9:16 cinematic motion comic frame, medium close-up of Demo Heroine waking on an old bed in a cold palace room at rainy night.",
    "video_prompt": "Use first-last keyframe mode when available; preserve black hair, silver hairpin, pale cyan ancient costume, cold palace room, rain, and candlelight.",
    "bgm_prompt": "low tense strings, sparse, rainy night",
    "sound_effect": "rain on wooden window, faint candle crackle, fabric rustle",
    "sound_design": "rain ambience under low room tone; brief fabric rustle when she wakes",
    "music_cue": "subtle tension swell after she grips the hairpin",
    "transition_in": "fade in from black with rain sound already present",
    "transition_out": "cut on her alert stare toward the door",
    "reference_image_prompts": [
      "Demo Heroine character reference sheet, black hair, silver hairpin, pale cyan ancient costume, neutral pose, plain background, no text, no watermark",
      "Cold palace room background, rainy night, old bed, wooden window, candlelight, no people, no text, no watermark"
    ],
    "reference_images": [],
    "costume_overrides": {
      "char_heroine": "costume_heroine_palace_v001"
    },
    "source_events": [
      "event_ch01_001"
    ],
    "scene_asset_ids": [],
    "prop_asset_ids": [],
    "previous_shot_summary": null,
    "next_shot_intent": "Footsteps approach outside the broken door.",
    "continuity_from": null,
    "continuity_to": "ep01_s002",
    "keyframes": {
      "start_frame": "assets/candidates/grid-cells/grid_ep01_story_v001_cell01_first_frame.png",
      "end_frame": "assets/candidates/grid-cells/grid_ep01_story_v001_cell02_last_frame.png",
      "previous_end_frame": null,
      "next_start_frame": null,
      "start_frame_prompt": "Demo Heroine just waking on the old bed, pale cyan ancient costume, black hair with silver hairpin, rainy cold palace room.",
      "end_frame_prompt": "Demo Heroine sitting at the bed edge, gripping the silver hairpin and staring toward the door, candlelight and rain-blue fill."
    },
    "prompt_files": {
      "image": "episodes/ep01/prompts/ep01_s001_image_v001.md",
      "video": "episodes/ep01/prompts/ep01_s001_video_v001.md"
    },
    "prompt_versions": {
      "image": 1,
      "video": 1
    },
    "assets": {
      "image": null,
      "video": "asset_ep01_s001_video_c001_v001",
      "voice": null
    },
    "quality_gate": {
      "status": "pending",
      "review_file": null
    },
    "route_plan": {
      "route": "first-last",
      "reference_mode": "first_last",
      "provider_id": "gemini_video_web_manual",
      "rationale": "Start/end frame anchors are planned for identity and continuity control."
    },
    "stale": false,
    "stale_reason": null,
    "frozen_version": "storyboard_v002",
    "status": "planned"
  },
  "storyboard": null,
  "prompt_index_entry": {
    "prompt_id": "prompt_ep01_s001_video_v001",
    "shot_id": "ep01_s001",
    "prompt_type": "video",
    "prompt_key": "shot_video_first_last",
    "variant": "baseline",
    "language": "mixed_zh_en",
    "style_profile_id": "style_motion_comic_v001",
    "version": 1,
    "prompt_file": "episodes/ep01/prompts/ep01_s001_video_v001.md",
    "previous_prompt_id": null,
    "derived_from": [
      "source_events:event_ch01_001",
      "characters:char_heroine",
      "style_guide:v001",
      "storyboard:ep01_s001",
      "keyframes:ep01_s001_planned"
    ],
    "provider_target": "gemini_video_web_manual",
    "template_ref": "shot_video_first_last",
    "template_version": 1,
    "slot_contents": {
      "generation_mode": "manual_web",
      "reference_mode": "first_last_when_available",
      "duration_sec": 5,
      "aspect_ratio": "9:16",
      "motion_rules": "time segmented motion in storyboard; final prompt concise",
      "keyframe_rules": "first and last frames are hard anchors when generated"
    },
    "polish_history": [],
    "ab_test_group_id": null,
    "stale": false,
    "stale_reason": null,
    "rollback_of": null,
    "change_reason": "baseline prompt",
    "review_status": "pending",
    "review_file": null,
    "frozen": false,
    "created_at": "2026-07-07"
  },
  "slot_overrides": {
    "generation_mode": "manual_web",
    "reference_mode": "first_last_when_available",
    "duration_sec": 5,
    "aspect_ratio": "9:16",
    "motion_rules": "time segmented motion in storyboard; final prompt concise",
    "keyframe_rules": "first and last frames are hard anchors when generated"
  }
}
```

## Final Instruction

Use the slots and production context above to produce the requested artifact. Preserve frozen facts and return the output format required by the template.
