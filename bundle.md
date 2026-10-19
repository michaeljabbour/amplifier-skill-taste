---
bundle:
  name: taste-elegance
  version: 0.2.0
  description: >-
    Helps a person develop their own taste and elegance: the
    improve-taste-and-elegance skill, a /taste working mode, and two staged,
    human-gated recipes.

# Thin root: a lean host plus this bundle's behavior. Most users should add only
# the behavior to their existing host (see README).
includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main#subdirectory=bundles/anchors/bundle.md
  - bundle: taste-elegance:behaviors/taste-elegance
---

@anchors:context/system.md
