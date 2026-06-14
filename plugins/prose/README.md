# prose

One-pass editor for work prose, plus an opt-in register. See the
[marketplace README](../../README.md) for the architecture and install
steps.

## Components

- `skills/prose/` - the editing skill. Three layers in order: structure
  (characters as subjects, actions as verbs, old-to-new flow, stress
  position), concision (prune, plain diction, figurative-verb tics), surface
  (tell-phrases, emphasis adverbs, active voice, earned contrast, rhythm).
  Genre structures live in `skills/prose/references/genre-playbook.md`.
- `skills/laconic/` - the terse register. Opt-in only; it changes voice, so
  it never fires on a generic "edit this".
- `commands/polish.md` - `/prose:polish`, the full pass on a pasted draft.
- `examples/before-after.md` - worked fixtures, one per diagnosis tag.

Enforcement is prompt-side: the skill applies the layers while drafting, and
the shared prose-rules floor keeps the mechanical rules in view. Replies have
no linter.
