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

## Why one plugin instead of a pipeline

An earlier design split this into three plugins (clarity-and-grace, laconic,
stop-slop) composed by an EDITING-PROTOCOL.md. That failed structurally: the
passes owned the same rules (adverbs, hedges, fragments) at three different
severities, two of them triggered on the same requests in undefined order,
and the document that resolved their conflicts never entered the model's
context at runtime. A skill only works if the text the model loads is
self-sufficient. So the layers and their tie-breakers live inside one skill,
the register stays a separate opt-in skill, and the part that must never be
forgotten (the mechanical floor) is enforced by a hook instead of by memory.
This repo supersedes EDITING-PROTOCOL.md and the dabd/clarity-and-grace
repo.

## Install

```
/plugin marketplace add dabd/tacit
/plugin install prose@tacit
```

The plugin has no explicit version, so every commit is a new version;
`/plugin marketplace update tacit` pulls the latest.

Migrating from this marketplace's earlier names (dabd-writing-tools, or the
single-repo dabd/clarity-and-grace):

```
/plugin uninstall prose@dabd-writing-tools
/plugin marketplace remove dabd-writing-tools
/plugin marketplace add dabd/tacit
/plugin install prose@tacit
```

If the old install was `clarity-and-grace@dabd-writing-tools`, uninstall
that name instead.

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
