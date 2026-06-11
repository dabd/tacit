# dabd-writing-tools

A Claude Code plugin marketplace for the prose a software engineer writes:
Slack messages, PR descriptions, review comments, design docs, incident
updates, commit messages.

It ships one plugin, **prose**, with three parts:

| Part | What it does | When it runs |
|------|--------------|--------------|
| `prose` skill | One editing pass with three ordered layers: structure (Williams & Bizup), concision, surface de-slop (adapted from Hardik Pandya's stop-slop) | Auto-triggers on any draft/edit request |
| `laconic` skill | Terse declarative register, Klinkenborg-inspired | Opt-in only, via /prose:laconic or an explicit ask |
| `prose-gate` Stop hook | Deterministic lint of the final reply: unicode dashes, tell-phrases, figurative verbs, emphasis adverbs, telegraphed contrasts. Blocks once per turn so the reply gets revised | Every turn, automatically |

## Why one plugin instead of a pipeline

An earlier design split this into three plugins (clarity-and-grace, laconic,
stop-slop) composed by an EDITING-PROTOCOL.md. That failed structurally: the
passes triple-owned rules (adverbs, hedges, fragments) at different
severities, two of them auto-triggered on the same requests in undefined
order, and the document that resolved their conflicts never entered the
model's context at runtime. Skills only work if the text the model loads is
self-sufficient. So the layers and their tie-breakers now live inside one
skill, the register stays a separate opt-in skill, and the only part that
must never be forgotten (the mechanical floor) is enforced by a hook instead
of by memory. This repo supersedes `EDITING-PROTOCOL.md` and the
`dabd/clarity-and-grace` repo.

## Install

```
/plugin marketplace add dabd/dabd-writing-tools
/plugin install prose@dabd-writing-tools
```

The plugin omits an explicit version, so every commit is a new version;
`/plugin marketplace update dabd-writing-tools` pulls the latest.

Migrating from the old marketplace (same name, old source):

```
/plugin uninstall clarity-and-grace@dabd-writing-tools
/plugin marketplace remove dabd-writing-tools
/plugin marketplace add dabd/dabd-writing-tools
/plugin install prose@dabd-writing-tools
```

## Use

- Ask for any draft, edit, or feedback on work prose: the `prose` skill
  triggers on its own.
- `/prose:polish` - run the full pass explicitly on a pasted draft or
  selection.
- `/prose:laconic` - apply the terse register, deliberately.
- The gate needs nothing from you. If a reply stops short and revises
  itself, that was the gate.

To tune the gate, edit the pattern lists in
`plugins/prose/hooks/prose-gate.sh` and run its test suite
(`plugins/prose/hooks/test-prose-gate.sh`). To turn it off, disable the
plugin (`/plugin disable prose`) or delete the Stop entry in
`plugins/prose/hooks/hooks.json`.

## Credits

- prose and laconic skills by dabd (MIT, see [LICENSE](LICENSE)).
- Structure and concision layers encode the method of Joseph M. Williams and
  Joseph Bizup, *Style: Lessons in Clarity and Grace*. The laconic register
  is inspired by Verlyn Klinkenborg, *Several Short Sentences About
  Writing*. No text from either book; original wording only.
- The surface layer and gate adapt the tell inventory of
  [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya
  (MIT), re-tuned for work writing.
