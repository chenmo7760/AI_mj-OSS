# Public example scope

Both `projects/demo-drama` and `projects/office-comedy-test` are fictional fixtures.
Display names and identifiers are demonstration labels. No real employee, customer,
business record, production approval or production result is represented.

Asset lists and spend records are empty. Tasks are pending, prompt reviews are pending,
and the demo review explicitly reports `Blocked`. Generated media, candidate selections,
old provider payloads, production reports and personal research records are excluded.

`python scripts/check_public_examples.py` must pass structural validation and confirm a
nonzero readiness exit caused by pending reviews. It also confirms that the production
gate remains blocked. No network requests or generated-media calls are made.

Before sharing changes, check staged files for local paths, real names, source material,
credentials and business data. Do not commit another person's media without permission.
