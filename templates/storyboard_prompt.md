# Storyboard Planning

Episode:
Target Duration:
Shot Count Target:
Aspect Ratio:
Default Duration Range:

## Required Inputs

- source_events.json
- script.md
- characters.json
- style_guide.md

## Shot Requirements

Each shot must include:

- shot_id
- title
- source_events
- duration_sec
- scene
- location / time / atmosphere
- characters and character_ids
- action
- result
- dialogue plus dialogues array
- camera / shot_type / angle / movement / camera_direction
- composition_guide / focal_point / depth_of_field
- motion_script
- video_script
- sound_design / music_cue / sound_effect
- transition_in / transition_out
- reference_image_prompts
- continuity_from
- continuity_to
- keyframes placeholders

## Motion Script Rules

Write time-segmented action beats, usually 0-3s and 3-6s for a short vertical shot. Keep one primary action per shot. Include visible character behavior, object interaction, and camera movement.

## Video Script Rules

Write the model-facing video prose separately from dialogue. Keep it concise, continuous, and executable. Do not put spoken lines inside the video prose; put them in `dialogues`.

## Continuity Rules

The end frame of shot N must be a stable state that can logically become the start frame of shot N+1. Use character `visual_hint` when naming visible characters.
