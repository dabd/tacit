# tacit

A Claude Code plugin marketplace for the prose a software engineer writes:
Slack messages, PR descriptions, review comments, design docs, incident
updates, commit messages.

The marketplace contains one plugin, **prose**, with three parts:

| Part | What it does | When it runs |
|------|--------------|--------------|
| `prose` skill | One editing pass with three ordered layers: structure (Williams & Bizup), concision, surface de-slop (adapted from Hardik Pandya's stop-slop) | On any draft or edit request |
| `laconic` skill | Terse declarative register, Klinkenborg-inspired | Opt-in, via /prose:laconic or an explicit ask |
| `prose-gate` Stop hook | Lints the final reply for the mechanical floor: unicode dashes, tell-phrases, figurative verbs, emphasis adverbs, telegraphed contrasts. Blocks once per turn so the reply gets revised | Every turn |

## How the layers work together

The `prose` skill applies its three layers in a fixed order, because each
layer depends on the one before:

1. **Structure** (Williams & Bizup) makes each sentence clear: characters as
   subjects, actions as verbs, old information before new, emphasis in the
   stress position. There is no point polishing a sentence that still hides
   who does what.
2. **Concision** tightens the clear sentence: prune filler, choose the plain
   word over the inflated one, swap figurative-verb tics for plain verbs.
   One guardrail: cut words, never load-bearing reasoning.
3. **Surface** runs last, on finished sentences: tell-phrases, emphasis
   adverbs, contrast templates, rhythm. It removes the patterns that make
   prose read as generated.

The `laconic` register sits outside the pass. It imposes a voice, so it runs
only on request, after the three layers. The gate backs the whole thing:
whatever slips through in a reply, the Stop hook checks against the
mechanical floor and blocks once so the reply gets fixed.

## Install

```
/plugin marketplace add dabd/tacit
/plugin install prose@tacit
```

The plugin has no explicit version, so every commit is a new version;
`/plugin marketplace update tacit` pulls the latest.

## Use

- Ask for any draft, edit, or feedback on work prose: the `prose` skill
  handles it without being named.
- `/prose:polish` - the full pass on a pasted draft or selection.
- `/prose:laconic` - the terse register, on request.
- The gate needs nothing from you. If a reply stops short and revises
  itself, that was the gate.

To tune the gate, edit the pattern lists in
`plugins/prose/hooks/prose-gate.sh` and keep
`plugins/prose/hooks/test-prose-gate.sh` green. To turn it off, disable the
plugin (`/plugin disable prose`) or delete the Stop entry in
`plugins/prose/hooks/hooks.json`.

## Credits

- prose and laconic skills by dabd (MIT, see [LICENSE](LICENSE)).
- The structure and concision layers encode the method of Joseph M. Williams
  and Joseph Bizup, *Style: Lessons in Clarity and Grace*. The laconic
  register blends Verlyn Klinkenborg's sentence-first discipline (*Several
  Short Sentences About Writing*) with the plainness of Grant's field
  orders. No text from the books; original wording only.
- The surface layer and the gate adapt the tell inventory of
  [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya
  (MIT), re-tuned for work writing.
