# prose

A Claude Code and Codex plugin for software-engineering prose.

## Model

Prose is the conservative base skill. Compress selects the information required
for the document's purpose. Laconic changes the register of retained
information. When both modifiers are requested, apply Compress first and
Laconic second. The final preservation check compares the result with the
source and the retained semantic inventory.

## Package

- One canonical Foundations file: `FOUNDATIONS.md`.
- Three skills: `skills/prose/SKILL.md`, `skills/compress/SKILL.md`, and
  `skills/laconic/SKILL.md`.
- One Claude compatibility command: `commands/polish.md`. Compress and Laconic
  are exposed directly from their skills.
- One worked example file: `examples/before-after.md`.
- One contract test file: `tests/test_plugin_contracts.py`.
- Two plugin manifests: `.claude-plugin/plugin.json` and
  `.codex-plugin/plugin.json`.

## Invoke

Claude Code:

```text
/prose:polish <draft>
/prose:compress <draft or target; optional hard limit>
/prose:laconic <draft>
```

Codex:

```text
$prose:prose <draft>
$prose:compress <draft or target; optional hard limit>
$prose:laconic <draft>
```

## Validate

From the repository root:

```bash
python3 -B -m unittest discover -s plugins/prose/tests -v
claude plugin validate .
claude plugin validate ./plugins/prose
python3 -m json.tool .agents/plugins/marketplace.json
python3 -m json.tool plugins/prose/.codex-plugin/plugin.json
```
