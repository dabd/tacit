# tacit

Writing tools for software engineers. The `prose` plugin keeps three operations
separate:

| Mode | Purpose and use |
|---|---|
| `prose` | Conservative drafting and editing. It activates automatically only for explicit writing or prose-review requests; use `/prose:polish <draft>` directly. It excludes ordinary coding, incidental prose, and substantive architecture, correctness, security, or design reviews. |
| `compress` | Maximum reduction under a preservation contract. Use `/prose:compress <draft or target; optional hard limit>` or explicitly request extreme or hard-limit concision. |
| `laconic` | A terse declarative register that preserves content. Use `/prose:laconic <draft>` or explicitly request that register. |

See [Foundations](plugins/prose/FOUNDATIONS.md) for the design principles,
sources, exceptions, and Tacit-specific contributions.

## Claude Code

```text
/plugin marketplace add dabd/tacit
/plugin install prose@tacit
```

Test a local checkout:

```bash
claude --plugin-dir ./plugins/prose
```

## Codex

Install or update the three Agent Skills directories without nesting another
copy:

```bash
mkdir -p \
  ~/.agents/skills/tacit-prose \
  ~/.agents/skills/tacit-compress \
  ~/.agents/skills/tacit-laconic
cp -R plugins/prose/skills/prose/. ~/.agents/skills/tacit-prose/
cp -R plugins/prose/skills/compress/. ~/.agents/skills/tacit-compress/
cp -R plugins/prose/skills/laconic/. ~/.agents/skills/tacit-laconic/
```

Codex may ignore Claude-specific frontmatter fields, but the descriptions retain
the activation boundaries on Claude Code and Codex. Each skill includes its own
Foundations reference.

## Validate

Run deterministic checks:

```bash
python3 -m unittest discover -s plugins/prose/tests -v
python3 plugins/prose/scripts/run_evals.py \
  --plugin-root plugins/prose \
  --validate-only
claude plugin validate .
claude plugin validate ./plugins/prose
```

After `claude auth login`, run live behavior and activation evaluations:

```bash
python3 plugins/prose/scripts/run_evals.py \
  --plugin-root plugins/prose \
  --model sonnet \
  --model opus \
  --include-baseline \
  --output-dir eval-results
```

Each live run writes to a new timestamped directory and records the plugin
version and content hash with every result.

`plugins/prose/scripts/audit_text.py` reports word and section counts, exact
duplicate sentences, lexically similar paragraphs, repeated sentence openings,
and configurable flagged patterns. It cannot prove semantic correctness.

## Versioning

The plugin manifest uses semantic versions. Tag releases and bump
`plugins/prose/.claude-plugin/plugin.json` when behavior changes.

## Credits

- dabd wrote the MIT-licensed skills.
- Joseph M. Williams and Joseph Bizup's *Style: Lessons in Clarity and Grace*
  informs the structure and concision guidance.
- Verlyn Klinkenborg's *Several Short Sentences About Writing* and the plain
  style of Grant's field orders inform the laconic register. The wording in this
  repository is original.
- The model-phrasing review adapts Hardik Pandya's MIT-licensed
  [stop-slop](https://github.com/hardikpandya/stop-slop).
