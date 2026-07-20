# prose

A Claude Code plugin for software-engineering prose.

## Components

- `FOUNDATIONS.md`: principles, sources, exceptions, and Tacit-specific
  contributions.
- `skills/prose/`: conservative drafting and editing that preserves facts,
  uncertainty, attribution, terminology, reasoning, and voice.
- `skills/compress/`: explicit extreme compression with semantic inventory,
  claim-level deduplication, reconstruction, and separate redundancy and
  preservation audits.
- `skills/laconic/`: an explicit terse register that preserves content.
- `agents/redundancy-reviewer.md`: deletion and merge recommendations only.
- `agents/preservation-reviewer.md`: missing or altered required information.
- `commands/polish.md`: compatibility command for `/prose:polish`.
- `evals/`: activation and behavior cases.
- `scripts/audit_text.py`: deterministic measurements for text.
- `scripts/run_evals.py`: corpus validation and live cross-model evaluation.

## Commands

```text
/prose:polish <draft>
/prose:compress <draft or target; optional hard limit>
/prose:laconic <draft>
```

## Design rules

1. Normal editing preserves information and voice.
2. Clear, literal, domain-specific language is the default.
3. Genre choices are preferences, not universal prohibitions.
4. Clean prose should receive few or no edits.
5. Extreme compression requires explicit user intent.
6. Compression audits claims rather than only repeated wording.
7. General tests identify new model-specific phrasing; regex patterns are smoke
   checks only.

## Test

From the repository root:

```bash
python3 -m unittest discover -s plugins/prose/tests -v
python3 plugins/prose/scripts/run_evals.py \
  --plugin-root plugins/prose \
  --validate-only
python3 plugins/prose/scripts/audit_text.py \
  plugins/prose/evals/fixtures/concise.md \
  --fail-duplicates --fail-near-duplicates --fail-patterns --json
python3 plugins/prose/scripts/audit_text.py \
  plugins/prose/evals/fixtures/duplicated.md \
  --fail-duplicates --fail-near-duplicates --json
```

The concise fixture must exit 0. The duplicated fixture must exit 1.
