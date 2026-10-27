# Assembled Prompt: grid_prompt

Template Version: 1
Prompt Type: image
Episode: ep01
Shot ID: ep01_s001

## Slots

### role_definition

# Role Definition

You create grid image prompts for fast candidate exploration. The grid will later be split into cell-level first_frame, last_frame, or reference assets.

### layout_rules

# Layout Rules

- State exact rows, columns, and visible panel count.
- Require separate panels with clear boundaries.
- Require consistent art style, lighting, and palette across cells.
- No merged panels, missing panels, text, watermarks, logos, or UI.
- For `first_last` grids, alternate opening and closing beats only when the cell assignment requires it. Do not invent extra shots.
- Include a cell map in the prompt body: `Cell 01 = shot_id + frame_type + visual beat`.
- Keep each cell self-contained so it can be cropped into a usable first frame, last frame, or reference image.


## Project Override

3 x 3 grid, exactly 9 visible panels, crop-safe cell boundaries.

### mode_rules

# Mode Rules

- `first_frame`: each cell explores an opening composition.
- `first_last`: alternate or pair opening and closing beats for the shot.
- `multi_ref`: explore scene angles, prop references, or composition variants.
- Each cell prompt must include shot_id and frame_type.


## Project Override

cells map to first_frame, last_frame, or reference roles from grid_assignments.json.

### output_format

# Output Format

Return valid JSON only:

```json
{
  "grid_prompt": "",
  "cell_prompts": [
    {
      "cell_index": 1,
      "shot_id": "",
      "frame_type": "first_frame",
      "prompt": ""
    }
  ],
  "rows": 3,
  "cols": 3,
  "mode": "first_last",
  "negative_prompt": "",
  "review_notes": []
}
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
  "storyboard": [
    {
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
    {
      "shot_id": "ep01_s002",
      "episode": "ep01",
      "order": 2,
      "title": "Footsteps",
      "duration_sec": 4,
      "location": "cold palace chamber door",
      "time": "rainy night",
      "atmosphere": "threatening, quiet, claustrophobic",
      "scene": "The broken wooden door and wet stone floor of the cold palace chamber, with rain shadows crossing the wall.",
      "scene_title": "Door in the Rain",
      "scene_description": "A narrow view from inside the chamber toward the door, old latch trembling under an unseen touch.",
      "lighting": "low candle spill with cold blue moon-rain shadow",
      "color_palette": "cold blue, muted teal, old brown wood",
      "characters": [
        "char_heroine"
      ],
      "character_ids": [
        "char_heroine"
      ],
      "action": "Demo Heroine turns toward the door as footsteps stop outside and the latch trembles.",
      "result": "She understands someone is approaching and must hide.",
      "dialogue": "Someone is outside.",
      "dialogues": [
        {
          "sequence": 1,
          "character_id": "char_heroine",
          "speaker": "Demo Heroine",
          "text": "Someone is outside.",
          "emotion": "whispered, alarmed",
          "start_ratio": 0.35,
          "end_ratio": 0.68
        }
      ],
      "narration": "The room answers her with footsteps.",
      "camera": "vertical 9:16 over-shoulder shot from Demo Heroine toward the door",
      "shot_type": "over-shoulder",
      "angle": "low interior angle",
      "movement": "small handheld drift toward the shaking latch",
      "camera_direction": "Frame Demo Heroine's shoulder and hairpin in foreground, door latch in focal point.",
      "composition_guide": "Foreground silhouette left, door latch upper right, lower center clear for subtitles.",
      "focal_point": "the trembling wooden latch",
      "depth_of_field": "foreground soft, latch sharp",
      "motion_script": "0-2s: Demo Heroine freezes and turns toward the door. 2-4s: the latch trembles once as footsteps stop.",
      "video_script": "Over Demo Heroine's shoulder, the broken door latch trembles. She whispers that someone is outside while rain shadows move across the wall.",
      "image_prompt": "Vertical 9:16 cinematic motion comic over-shoulder shot, Demo Heroine foreground, broken palace door and trembling latch in cold rainy candlelight.",
      "video_prompt": "Preserve Demo Heroine's black hair, silver hairpin, pale cyan costume, same cold palace room; emphasize latch movement and tense stillness.",
      "bgm_prompt": "thin sustained strings, quiet pulse",
      "sound_effect": "footsteps outside, wood latch rattle, rain",
      "sound_design": "footsteps cut through rain; latch rattle is sharp and close",
      "music_cue": "brief low hit when latch moves",
      "transition_in": "cut from Demo Heroine's alert stare",
      "transition_out": "cut as she moves toward the curtain",
      "reference_image_prompts": [
        "Broken ancient palace door interior, wet wooden latch, rain shadow, candlelight, no people, no text",
        "Demo Heroine over-shoulder silhouette, black hair, silver hairpin, pale cyan ancient costume, same cold palace room"
      ],
      "reference_images": [],
      "costume_overrides": {
        "char_heroine": "costume_heroine_palace_v001"
      },
      "source_events": [
        "event_ch01_002"
      ],
      "scene_asset_ids": [],
      "prop_asset_ids": [],
      "previous_shot_summary": "Demo Heroine woke on the bed and gripped her silver hairpin.",
      "next_shot_intent": "Demo Heroine hides behind the torn curtain.",
      "continuity_from": "ep01_s001",
      "continuity_to": "ep01_s003",
      "keyframes": {
        "start_frame": null,
        "end_frame": "assets/candidates/grid-cells/grid_ep01_story_v001_cell04_last_frame.png",
        "previous_end_frame": null,
        "next_start_frame": null,
        "start_frame_prompt": "Demo Heroine at bed edge, turning sharply toward the broken door, silver hairpin visible, same chamber.",
        "end_frame_prompt": "Door latch trembling in focus, Demo Heroine's pale cyan shoulder blurred in foreground, rainy candlelit chamber."
      },
      "prompt_files": {
        "image": "episodes/ep01/prompts/ep01_s002_image_v001.md",
        "video": "episodes/ep01/prompts/ep01_s002_video_v001.md"
      },
      "prompt_versions": {
        "image": 1,
        "video": 1
      },
      "assets": {
        "image": null,
        "video": "asset_ep01_s002_video_c001_v001",
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
        "rationale": "Short controlled motion benefits from start/end door-latch anchors."
      },
      "stale": false,
      "stale_reason": null,
      "frozen_version": "storyboard_v002",
      "status": "planned"
    },
    {
      "shot_id": "ep01_s003",
      "episode": "ep01",
      "order": 3,
      "title": "Curtain Hide",
      "duration_sec": 5,
      "location": "cold palace bed curtain",
      "time": "rainy night",
      "atmosphere": "urgent, stealthy, close",
      "scene": "A torn gauze bed curtain inside the cold palace chamber, with candlelight catching dust and rain mist.",
      "scene_title": "Behind the Curtain",
      "scene_description": "Demo Heroine hides in the narrow space behind the torn curtain, using the old bed as cover.",
      "lighting": "candle rim light through gauze, blue rain fill",
      "color_palette": "pale cyan, smoky gray, amber",
      "characters": [
        "char_heroine"
      ],
      "character_ids": [
        "char_heroine"
      ],
      "action": "Demo Heroine slips behind the torn curtain, holds her breath, and raises the silver hairpin as a last defense.",
      "result": "She is hidden but ready to react.",
      "dialogue": "Stay quiet... breathe.",
      "dialogues": [
        {
          "sequence": 1,
          "character_id": "char_heroine",
          "speaker": "Demo Heroine",
          "text": "Stay quiet... breathe.",
          "emotion": "barely audible, controlled fear",
          "start_ratio": 0.55,
          "end_ratio": 0.86
        }
      ],
      "narration": "Instinct moves before memory returns.",
      "camera": "vertical 9:16 tight close-up through torn gauze curtain",
      "shot_type": "tight close-up",
      "angle": "eye level through curtain gap",
      "movement": "slow lateral slide following her into hiding",
      "camera_direction": "Track with Demo Heroine from bed edge into curtain cover, ending on her eyes and hairpin.",
      "composition_guide": "Curtain texture frames her eyes; hairpin visible near lower third but not covering subtitles.",
      "focal_point": "Demo Heroine's eyes through gauze and the raised silver hairpin",
      "depth_of_field": "gauze foreground soft, eyes sharp",
      "motion_script": "0-2s: Demo Heroine slips behind the curtain. 2-5s: she raises the hairpin and steadies her breath.",
      "video_script": "Demo Heroine hides behind the torn gauze curtain, silver hairpin in hand, eyes fixed toward the door as rain and candlelight flicker.",
      "image_prompt": "Vertical 9:16 cinematic close-up through torn curtain, Demo Heroine hiding with silver hairpin, cold palace candlelight and rain-blue shadows.",
      "video_prompt": "Preserve character identity, costume and room; motion is subtle hiding, breathing, eye movement, and candle flicker.",
      "bgm_prompt": "muted heartbeat percussion under rain",
      "sound_effect": "fabric brush, controlled breathing, rain",
      "sound_design": "close breathing and cloth movement under distant footsteps",
      "music_cue": "heartbeat pulse begins under silence",
      "transition_in": "cut as she reaches the curtain",
      "transition_out": "cut on her eyes toward the door shadow",
      "reference_image_prompts": [
        "Torn gauze bed curtain in cold palace chamber, candle rim light, no people, no text",
        "Demo Heroine hiding close-up, black hair, silver hairpin, pale cyan ancient costume, tense eyes"
      ],
      "reference_images": [],
      "costume_overrides": {
        "char_heroine": "costume_heroine_palace_v001"
      },
      "source_events": [
        "event_ch01_003"
      ],
      "scene_asset_ids": [],
      "prop_asset_ids": [],
      "previous_shot_summary": "The door latch trembled and footsteps stopped outside.",
      "next_shot_intent": "A shadow appears outside and a palace token becomes visible.",
      "continuity_from": "ep01_s002",
      "continuity_to": "ep01_s004",
      "keyframes": {
        "start_frame": null,
        "end_frame": null,
        "previous_end_frame": null,
        "next_start_frame": null,
        "start_frame_prompt": "Demo Heroine moving behind the torn curtain, pale cyan sleeve and black hair visible, same cold palace room.",
        "end_frame_prompt": "Demo Heroine hidden behind gauze, eyes sharp, silver hairpin raised near her chest, candle and rain shadows behind."
      },
      "prompt_files": {
        "image": "episodes/ep01/prompts/ep01_s003_image_v001.md",
        "video": "episodes/ep01/prompts/ep01_s003_video_v001.md"
      },
      "prompt_versions": {
        "image": 1,
        "video": 1
      },
      "assets": {
        "image": null,
        "video": "asset_ep01_s003_video_c001_v001",
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
        "rationale": "Close-up identity and prop continuity need anchored start/end frames."
      },
      "stale": false,
      "stale_reason": null,
      "frozen_version": "storyboard_v002",
      "status": "planned"
    },
    {
      "shot_id": "ep01_s004",
      "episode": "ep01",
      "order": 4,
      "title": "Token Shadow",
      "duration_sec": 5,
      "location": "cold palace door",
      "time": "rainy night",
      "atmosphere": "mysterious, threatening, revelatory",
      "scene": "The doorway of the cold palace chamber with a tall shadow outside and a palace token glinting on the wet floor.",
      "scene_title": "The Trap",
      "scene_description": "A final chamber view that connects the unseen intruder, the door, and the token clue.",
      "lighting": "backlit blue rain silhouette with tiny candle reflection on token",
      "color_palette": "deep blue, wet black wood, small gold highlight",
      "characters": [
        "char_heroine"
      ],
      "character_ids": [
        "char_heroine"
      ],
      "action": "From hiding, Demo Heroine sees a tall shadow stop outside the door and notices a palace token on the floor.",
      "result": "She concludes the situation was arranged deliberately.",
      "dialogue": "This was not an accident.",
      "dialogues": [
        {
          "sequence": 1,
          "character_id": "char_heroine",
          "speaker": "Demo Heroine",
          "text": "This was not an accident.",
          "emotion": "whispered, realizing",
          "start_ratio": 0.6,
          "end_ratio": 0.9
        }
      ],
      "narration": "A token on the floor turns fear into a question.",
      "camera": "vertical 9:16 rack focus from Demo Heroine's hidden eye to palace token and door shadow",
      "shot_type": "rack focus close-up",
      "angle": "low from behind curtain",
      "movement": "slow rack focus and slight push toward token",
      "camera_direction": "Begin on Demo Heroine's eye behind curtain, rack focus to token on wet floor and tall door shadow.",
      "composition_guide": "Token in lower right highlight, door shadow upper center, lower left subtitle-safe.",
      "focal_point": "palace token catching candlelight",
      "depth_of_field": "rack focus from eye to token",
      "motion_script": "0-2s: Demo Heroine watches from behind curtain. 2-5s: focus shifts to the palace token as a tall shadow stops outside.",
      "video_script": "From Demo Heroine's hiding place, a tall shadow pauses beyond the broken door. The camera racks focus to a wet palace token on the floor as she realizes this was arranged.",
      "image_prompt": "Vertical 9:16 cinematic motion comic frame, low view from behind curtain, palace token on wet floor, tall shadow outside broken door.",
      "video_prompt": "Use first-last mode; preserve same room, rain, candlelight, Demo Heroine hidden, silver hairpin, and token clue.",
      "bgm_prompt": "low mystery swell with unresolved ending",
      "sound_effect": "rain, distant thunder, faint metal token scrape",
      "sound_design": "rain muffles the unseen intruder; token glint is emphasized with a tiny metallic scrape",
      "music_cue": "unresolved swell at the final realization",
      "transition_in": "cut from Demo Heroine's hidden eyes",
      "transition_out": "hard cut to black for cliffhanger",
      "reference_image_prompts": [
        "Ancient palace token on wet stone floor, candle highlight, no text, no watermark",
        "Tall shadow outside broken palace door, blue rain backlight, no face visible"
      ],
      "reference_images": [
        {
          "type": "grid_cell",
          "path": "assets/candidates/grid-cells/grid_ep01_story_v001_cell09_reference.png",
          "grid_id": "grid_ep01_story_v001",
          "cell_index": 9
        }
      ],
      "costume_overrides": {
        "char_heroine": "costume_heroine_palace_v001"
      },
      "source_events": [
        "event_ch01_004"
      ],
      "scene_asset_ids": [],
      "prop_asset_ids": [],
      "previous_shot_summary": "Demo Heroine hid behind the curtain with the silver hairpin ready.",
      "next_shot_intent": "Episode ends on the clue and unseen threat.",
      "continuity_from": "ep01_s003",
      "continuity_to": null,
      "keyframes": {
        "start_frame": null,
        "end_frame": "assets/candidates/grid-cells/grid_ep01_story_v001_cell08_last_frame.png",
        "previous_end_frame": null,
        "next_start_frame": null,
        "start_frame_prompt": "Demo Heroine's hidden eye visible behind torn curtain, same black hair, silver hairpin, pale cyan costume, rainy cold palace.",
        "end_frame_prompt": "Wet palace token in candle highlight on floor, tall shadow outside broken door, Demo Heroine hidden off frame."
      },
      "prompt_files": {
        "image": "episodes/ep01/prompts/ep01_s004_image_v001.md",
        "video": "episodes/ep01/prompts/ep01_s004_video_v001.md"
      },
      "prompt_versions": {
        "image": 1,
        "video": 1
      },
      "assets": {
        "image": null,
        "video": "asset_ep01_s004_video_c001_v001",
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
        "rationale": "The rack-focus clue shot needs a stable start/end target."
      },
      "stale": false,
      "stale_reason": null,
      "frozen_version": "storyboard_v002",
      "status": "planned"
    }
  ],
  "prompt_index_entry": {
    "prompt_id": "prompt_ep01_grid_story_v001",
    "shot_id": "ep01_s001",
    "prompt_type": "image_grid",
    "prompt_key": "grid_prompt",
    "variant": "story_grid",
    "language": "mixed_zh_en",
    "style_profile_id": "style_motion_comic_v001",
    "version": 1,
    "prompt_file": "episodes/ep01/prompts/ep01_grid_story_v001.md",
    "previous_prompt_id": null,
    "derived_from": [
      "storyboard:ep01",
      "characters:char_heroine",
      "style_guide:v001"
    ],
    "provider_target": "codex_imagegen_subagent",
    "template_ref": "grid_prompt",
    "template_version": 1,
    "slot_contents": {
      "rows": 3,
      "cols": 3,
      "mode": "first_last",
      "layout_rules": "3 x 3 grid, exactly 9 visible panels, crop-safe cell boundaries.",
      "mode_rules": "cells map to first_frame, last_frame, or reference roles from grid_assignments.json."
    },
    "polish_history": [],
    "ab_test_group_id": null,
    "stale": false,
    "stale_reason": null,
    "rollback_of": null,
    "change_reason": "multi-shot grid prompt for pipeline validation",
    "review_status": "pending",
    "review_file": null,
    "frozen": false,
    "created_at": "2026-07-07"
  },
  "slot_overrides": {
    "rows": 3,
    "cols": 3,
    "mode": "first_last",
    "layout_rules": "3 x 3 grid, exactly 9 visible panels, crop-safe cell boundaries.",
    "mode_rules": "cells map to first_frame, last_frame, or reference roles from grid_assignments.json."
  }
}
```

## Final Instruction

Use the slots and production context above to produce the requested artifact. Preserve frozen facts and return the output format required by the template.
