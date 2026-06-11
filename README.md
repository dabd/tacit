# tacit

A Claude Code plugin marketplace for the prose engineers write: Slack
messages, PR descriptions, review comments, design docs, incident updates,
commit messages.

One plugin, **prose**. Three parts:

| Part | What it does | When it runs |
|------|--------------|--------------|
| `prose` skill | One editing pass with three ordered layers: structure (Williams & Bizup), concision, surface de-slop (adapted from Hardik Pandya's stop-slop) | On any draft or edit request; explicitly via /prose:polish |
| `laconic` skill | Terse declarative register, Klinkenborg-inspired | Opt-in, via /prose:laconic or an explicit ask |
| `prose-gate` Stop hook | Lints the final reply for the mechanical floor: unicode dashes, tell-phrases, figurative verbs, emphasis adverbs, telegraphed contrasts. Blocks once per turn so the reply gets revised | Every turn |

## How the layers work together

The `prose` skill applies its layers in a fixed order. Each depends on the
one before:

1. **Structure** (Williams & Bizup) makes each sentence clear: characters as
   subjects, actions as verbs, old information before new, emphasis in the
   stress position. Until the actor is visible, polish is wasted.
2. **Concision** tightens the clear sentence: prune filler, choose the plain
   word over the inflated one, swap figurative-verb tics for plain verbs.
   The guardrail: cut words, never load-bearing reasoning.
3. **Surface** runs last, on finished sentences: tell-phrases, emphasis
   adverbs, contrast templates, rhythm. It strips the patterns that read as
   generated.

The `laconic` register sits outside the pass. It imposes a voice. It runs on
request only, after the three layers. The gate backs all of it: the Stop
hook checks every reply against the mechanical floor and blocks once on a
violation.

## Install

```
/plugin marketplace add dabd/tacit
/plugin install prose@tacit
```

The plugin declares no version. Every commit is one.
`/plugin marketplace update tacit` pulls the latest.

## Use

- Ask for a draft, an edit, or feedback on work prose. The `prose` skill
  fires on its own.
- `/prose:polish` - the command form of the `prose` skill: the full pass on
  a pasted draft or selection.
- `/prose:laconic` - the terse register, on request.
- The gate needs nothing from you. If a reply stops short and revises
  itself, that was the gate.

Tune the gate by editing the pattern lists in
`plugins/prose/hooks/prose-gate.sh`. Keep
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
