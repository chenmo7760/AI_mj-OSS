Classify each failure:

- identity_drift: face, age, silhouette, body type, hair, or accessories changed
- costume_drift: active costume set not followed
- style_drift: style profile mismatch
- sheet_failure: missing required views or inconsistent views
- provider_artifact: watermark, malformed anatomy, duplicated limbs, text artifacts, unsafe crop
- prompt_gap: missing `visual_hint`, negative rule, costume anchor, or style instruction
- reference_gap: no locked asset, wrong reference, or cross-style reference contamination

Prefer a minimal upstream fix. Do not recommend rerunning blindly when a schema field or locked reference is missing.
