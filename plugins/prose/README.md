# prose

One-pass editor for work prose, plus an opt-in register and a deterministic
gate. See the [marketplace README](../../README.md) for the architecture and
install steps.

## Components

- `skills/prose/` - the editing skill. Three layers in order: structure
  (characters as subjects, actions as verbs, old-to-new flow, stress
  position), concision (prune, plain diction, figurative-verb tics), surface
  (tell-phrases, emphasis adverbs, active voice, earned contrast, rhythm).
  Genre structures live in `skills/prose/references/genre-playbook.md`.
- `skills/laconic/` - the terse register. Opt-in only; it changes voice, so
  it never fires on a generic "edit this".
- `commands/polish.md` - `/prose:polish`, the full pass on a pasted draft.
- `hooks/prose-gate.sh` - Stop hook. Lints the final reply for the
  mechanical floor and blocks once per turn with the violation list, so the
  reply gets revised. Fail-open: any internal error allows the stop.
- `examples/before-after.md` - worked fixtures, one per diagnosis tag.

## The gate's contract

- Gates only the last assistant message; code fences, inline code, and URLs
  are exempt. Blockquotes are gated: a draft presented as a quote is still
  the model's prose. Verbatim third-party quotes belong in code fences.
- Blocks at most once per turn (`stop_hook_active` guard), so it cannot
  loop.
- Checks only mechanical patterns: unicode dashes, tell-phrases, figurative
  verbs (delve, leverage, tap into, deep dive, foster), emphasis adverbs,
  telegraphed contrasts, sycophant openers. Judgment rules stay in the
  skill.
- Tune it by editing the pattern lists in `prose-gate.sh`; every change
  should keep `test-prose-gate.sh` green.
