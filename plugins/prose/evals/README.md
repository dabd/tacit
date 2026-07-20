# Evaluations

The corpus separates activation from behavior:

- `prompts.csv` checks which skill should activate.
- `cases.jsonl` defines behavior requirements and review tags.

Validate the corpus without making model calls:

```bash
python3 plugins/prose/scripts/run_evals.py \
  --plugin-root plugins/prose \
  --validate-only
```

Run live cases in fresh Claude Code sessions and retain raw events:

```bash
python3 plugins/prose/scripts/run_evals.py \
  --plugin-root plugins/prose \
  --model sonnet \
  --model opus \
  --include-baseline \
  --output-dir eval-results
```

Use `--case CASE_ID` to run selected cases. The command requires an authenticated
Claude Code installation. It records the Claude Code version, model, plugin or
baseline arm, plugin version, plugin content hash, raw stream events, available
slash commands, invoked skills, output, and deterministic grade. Each invocation
writes to a new timestamped run directory, so later evaluations do not overwrite
earlier results.

The deterministic grader checks exact text, prohibited text, word and section
limits, unchanged clean prose, conflict notices, and common explanation prefixes.
Activation cases require runtime evidence: an invocation event for automatic
skills or a registered command for a direct slash invocation. Behavior cases
also fail when the requested skill has no runtime evidence.
The runner passes `--setting-sources ''` to both arms and `--safe-mode` to the
baseline arm. This keeps user and project skills out of the baseline while the
plugin arm loads the explicit `--plugin-dir` under test.
Cases marked `manual` still require semantic review. Neither this runner nor
`audit_text.py` can prove that meaning, uncertainty, attribution, or reasoning was
preserved. Compare outputs across supported models and add observed failures as
new cases.
