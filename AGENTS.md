# Working on Taste × Elegance

- Read `SKILL.md` and `references/calibration.md` before changing the rubric. They
  preserve the user-supplied canonical skill. Keep the two axes independent.
- Gates come first. Never claim research, verification, or deployment without evidence.
- The site is static Python, HTML, CSS, and JavaScript. Keep it free of runtime
  dependencies, external fonts, analytics, and backend services.
- Content is in `site/site.json` and `site/template.html`; canonical anchors and
  questions are read directly from the skill and reference at build time.
- Keep the MIT notice in `site/theme/LICENSE`. Do not imply institutional affiliation.
- Examples and map positions are illustrative. Do not present them as measured data.
- Use plain words, visible labels, keyboard controls, and reduced-motion support.
- Run `python3 scripts/build.py`, `python3 scripts/check.py`, and
  `node --check site/site.js`. Inspect desktop and phone layouts after UI changes.
- Do not add a remote, push, publish, deploy, or contact anyone unless asked.
