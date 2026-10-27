# Repair Rules

- Return valid JSON only.
- Remove markdown fences and commentary.
- Fix trailing commas, unescaped quotes, missing brackets, and single quotes when the intended structure is clear.
- If a required field is missing, set it to `null` and add the field name to `_repair_notes.missing_fields`.
- If the payload is unrecoverable, return `{ "repair_failed": true, "reason": "..." }`.
