# Replaying and reviewing this benchmark

Run the deterministic code checks from the repository root:

```sh
python3 docs/evaluations/benchmark-2026-10-17/replay_checks.py
```

To rerun task behavior, start a new agent for each selected manifest entry without prior conversation history. Give it that entry's exact user prompt and the frozen skill/reference for skill conditions; for controls, do not provide skill files. Use a new isolated output directory and fresh fixtures, rather than overwriting archived evidence. The task wrappers under runs/ record the exact historical instructions, including old absolute paths; substitute the new sandbox and snapshot paths and record that substitution. Start X02 from stress-fixtures/, whose working.py is the original failing proposal, not the already-restored runs/X02-skill/working.py.

Do not expose checks, condition keys, prior responses or reviewer judgments to task runners. Use the supplied four common and case-specific checks for grading. Start fresh independent grading agents with opaque response IDs. Preserve raw judgments before adjudication. All historical masked packets and exact wrapper text are archived, though their absolute paths refer to the original local execution. Resolve packet filenames in their archive folder for a new run.

This suite is now known to the skill maintainer. A revision tested on its failures is a regression test, not a held-out generalization test. Add and freeze genuinely new short-refinement cases before testing that revision, and report original, revised and held-out results separately.
