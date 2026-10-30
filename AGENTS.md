# Working on Taste × Elegance

- Read `skills/improve-taste-and-elegance/SKILL.md` and its `references/calibration.md`
  before changing the rubric. They
  descend from the user-supplied canonical skill; record any change in CHANGELOG.md. Keep the two axes independent.
- Gates come first. Never claim research, verification, or deployment without evidence.
- The site is static Python, HTML, CSS, and JavaScript. Keep it free of runtime
  dependencies, external fonts, analytics, and backend services.
- The Amplifier bundle is `bundle.md`, `behaviors/`, `modes/`, and `recipes/`. Keep the
  mode body short (it is injected every turn) and the method in the skill, not copied
  into the mode or recipes. Validate recipes with the `recipes` tool after edits.
- Keep only one file named `SKILL.md` in the repository; snapshots use another name.
- Content is in `site/site.json` and `site/template.html`; canonical anchors and
  questions are read directly from the skill and reference at build time.
- Keep the MIT notice in `site/theme/LICENSE`. Do not imply institutional affiliation.
- Examples and map positions are illustrative. Do not present them as measured data.
- Use plain words, visible labels, keyboard controls, and reduced-motion support.
- Run `python3 scripts/build.py`, `python3 scripts/check.py`, and
  `node --check site/site.js`. Inspect desktop and phone layouts after UI changes.
- Do not add a remote, push, publish, deploy, or contact anyone unless asked.

## Market research upkeep

Local-only market research lives in `.research/market/` (gitignored; never commit it).

At session start, check `.research/market/last_updated`:
- If the file is missing, seed it from this repository's README and capability source/provenance links, using cited primary sources and local retrieval dates.
- If it is older than 30 days, or before any positioning, launch or naming work, refresh it with cited primary sources (URL + retrieved date).
- Keep it local. Never commit it and never copy private research into public docs.
- Log every change in `.research/market/CHANGELOG.md`.

## Capability identity

Public capability identity: `amplifier-capability-taste-elegance`. Preserve the existing portable method folder, native interfaces and legacy installation routes across the approved repository rename.
