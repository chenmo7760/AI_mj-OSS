Return JSON only:

{
  "character_id": "...",
  "style_profile_id": "...",
  "costume_set_id": "...",
  "prompt": "...",
  "negative_prompt": "...",
  "required_views": ["front_full_body", "three_quarter_full_body", "side_full_body", "back_full_body", "head_closeup", "expression_strip"],
  "candidate_policy": {
    "min_candidates": 2,
    "recommended_candidates": 4,
    "compare_required": true
  },
  "lock_requirements": [
    "selected asset must be registered with checksum",
    "selected asset must be referenced by character.reference_assets",
    "selected asset id must be added to character.locked_asset_ids before formal video generation"
  ]
}
