---
name: compress
description: >-
  Use when the user explicitly invokes /prose:compress or asks for extreme, maximum, minimal, aggressive, or hard-limit concision, semantic reduction, or claim-level deduplication. Do not use for ordinary editing or a generic request to tighten prose.
argument-hint: [text or target; optional hard word, section, or format limit]
effort: high
---

# Compress

Reduce the text to the minimum length that preserves the information required
for its purpose. This mode may remove optional information and reconstruct the
document. It requires explicit user intent.

Use `$ARGUMENTS`. If it is empty, use the current selection, file, or draft
already under discussion.

Foundation: [Compression philosophy](FOUNDATIONS.md#compression-philosophy),
[Compress](FOUNDATIONS.md#compress), and
[Tacit-specific contributions](FOUNDATIONS.md#tacit-specific-contributions).

## Preservation contract

Build a private semantic inventory containing:

- required claims, conclusions, decisions, and requests;
- evidence needed to support them;
- constraints, requirements, risks, and trade-offs;
- actions, owners, and deadlines;
- uncertainty, confidence, assumptions, and attribution;
- numbers, names, identifiers, links, code symbols, and technical terms needed
  by the reader.

Determine required content from the document purpose and semantic function, not
only from labels supplied by the user. Explicitly marked content must remain.
Background, examples, and history must also remain when they support,
disambiguate, constrain, or materially qualify a required claim. Other context,
examples, transitions, repeated explanations, and framing are optional.

## Hard constraints

Treat supplied word, section, and format limits as hard when they are compatible
with the preservation contract. Preservation takes priority when they conflict.
Do not claim that both constraints were met when they were not.

## Bounded workflow

### 1. Build the semantic inventory

Record the required information in private working notes. Normalise equivalent
claims so wording differences do not hide duplication.

### 2. Group duplicate claims

Compare claims across titles, headings, summaries, sections, examples, and
conclusions. Keep one clear statement unless repeated occurrences serve
different required functions.

### 3. Reconstruct once

Write a new version from the retained inventory. Do not repeatedly shorten the
original structure.

- Put the main result, decision, or request first when appropriate.
- Use the fewest sections that preserve navigation.
- Prefer deletion to paraphrase.
- Use one term for each concept.
- Do not add scene-setting, summaries, transitions, or decorative wording.

### 4. Run independent audits

**Redundancy audit**

For every sentence, identify the unique required information it contributes.
Delete or merge a sentence if removing it loses no required information. Compare
claims across sections, not only adjacent wording.

**Wording audit**

- Literal-operation test: use a verb that names the actual action.
- Conspicuous-phrase test: replace distinctive or fashionable wording that
  adds no meaning.
- Specific-effect test: replace vague evaluation with an observable result.
- Agency test: name the relevant actor or system when known.

**Preservation audit**

Compare the candidate with both the source and semantic inventory. Find missing,
altered, weakened, strengthened, newly implied, or misattributed required
information.

For text longer than about 500 words, high-stakes material, or an explicit
request for adversarial review, use `redundancy-reviewer` and
`preservation-reviewer` independently when agent delegation is available. Give
each reviewer the source, candidate, exact semantic inventory, document purpose,
and all hard limits. If delegation is unavailable, run the audits sequentially.

### 5. Apply one repair pass

Apply the two audit reports in one repair pass. Restore only required information
and remove only confirmed redundancy. Do not start another reconstruction.

### 6. Validate without rewriting

Check the repaired result against the source, inventory, and constraints. End
the workflow after this check. If required content exceeds a hard limit, return
the constraint notice and the shortest complete version. Do not perform another
rewrite cycle.

## Exit criteria

- Every sentence contributes unique required information.
- Each material claim appears once unless repetition has a distinct function.
- No heading only repeats its first sentence.
- All required facts, qualifications, attribution, identifiers, and actions
  remain.
- No unsupported certainty, implication, or blame was introduced.
- Every compatible hard limit is met.

## Output

Return only the compressed text unless the user asks for the inventory, audits,
counts, or explanation.

When a hard limit is incompatible with preservation, use this sole exception:

```text
Constraint conflict: preserving required information needs [actual amount], above the [requested limit].

[shortest complete version]
```
