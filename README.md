# tacit

Writing tools for software engineers. The `prose` plugin provides three
separate operations:

| Mode | Purpose | Invocation |
|---|---|---|
| `prose` | Conservative drafting and editing | Automatic only for explicit writing or prose-review requests; explicit with `/prose:polish` |
| `compress` | Maximum reduction under a preservation contract | `/prose:compress` or an explicit request for extreme or hard-limit concision |
| `laconic` | A terse declarative register that preserves content | `/prose:laconic` or an explicit request for that register |

Normal editing, register changes, and semantic compression are intentionally
separate. See [Foundations](plugins/prose/FOUNDATIONS.md) for the principles,
sources, exceptions, and Tacit-specific contributions behind that design.

## Install in Claude Code

```text
/plugin marketplace add dabd/tacit
/plugin install prose@tacit
```

For local testing:

```bash
claude --plugin-dir ./plugins/prose
```

## Use

```text
/prose:polish <draft>
/prose:compress <draft or target; optional hard limit>
/prose:laconic <draft>
```

The automatic `prose` skill does not load for ordinary coding answers,
incidental prose, or substantive architecture, correctness, security, or design
reviews. `compress` and `laconic` require explicit user intent, expressed either
by their slash command or a direct natural-language request.

## Codex

The skill directories use the Agent Skills layout. These commands update the
same three names without nesting a second copy:

```bash
mkdir -p \
  ~/.agents/skills/tacit-prose \
  ~/.agents/skills/tacit-compress \
  ~/.agents/skills/tacit-laconic
cp -R plugins/prose/skills/prose/. ~/.agents/skills/tacit-prose/
cp -R plugins/prose/skills/compress/. ~/.agents/skills/tacit-compress/
cp -R plugins/prose/skills/laconic/. ~/.agents/skills/tacit-laconic/
```

Codex may ignore Claude-specific frontmatter fields. The descriptions retain
the activation boundaries on both surfaces. Each skill includes its own
foundations reference.

## Validation

Run the deterministic checks:

```bash
python3 -m unittest discover -s plugins/prose/tests -v
python3 plugins/prose/scripts/run_evals.py \
  --plugin-root plugins/prose \
  --validate-only
claude plugin validate .
claude plugin validate ./plugins/prose
```

Run live behavior and activation evaluations after `claude auth login`:

```bash
python3 plugins/prose/scripts/run_evals.py \
  --plugin-root plugins/prose \
  --model sonnet \
  --model opus \
  --include-baseline \
  --output-dir eval-results
```

Each live run uses a new timestamped directory and records the plugin version
and content hash with every result.

`plugins/prose/scripts/audit_text.py` reports word count, section count, exact
duplicate sentences, lexically similar paragraphs, repeated sentence openings,
and configurable flagged patterns. It cannot prove semantic correctness.

## Versioning

The plugin manifest uses semantic versions. Tag releases and bump
`plugins/prose/.claude-plugin/plugin.json` for behavior changes.

## Credits

- The skills are by dabd and licensed under MIT.
- The structure and concision guidance is informed by Joseph M. Williams and
  Joseph Bizup, *Style: Lessons in Clarity and Grace*.
- The laconic register is informed by Verlyn Klinkenborg, *Several Short
  Sentences About Writing*, and the plain style of Grant's field orders. The
  wording in this repository is original.
- The model-phrasing review adapts ideas from Hardik Pandya's
  [stop-slop](https://github.com/hardikpandya/stop-slop), also licensed under MIT.
