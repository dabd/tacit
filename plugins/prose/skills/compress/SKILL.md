---
name: compress
description: >-
  Use when the user explicitly asks for extreme, maximum, minimal, aggressive, or hard-limit compression, semantic reduction, or claim-level deduplication. Do not use for ordinary editing or a generic request to tighten prose.
---

# Compress

Select the information required for the document's purpose and express it in
the minimum compatible space.

Compress may remove optional content after building the semantic inventory. It does not choose the register.

Follow the [shared preservation contract](../../FOUNDATIONS.md#shared-preservation-contract),
the [Compress operation](../../FOUNDATIONS.md#compress), and the
[composition rule](../../FOUNDATIONS.md#composition).

## Workflow

### 1. Establish purpose and limits

Identify the reader, intended result, required format, and any word, section, or
other hard limit.

### 2. Build one semantic inventory

Inventory all semantic content before classifying it as required or optional.

Record:

- facts, claims, conclusions, decisions, requests, and proposals;
- proposal status and modality, including distinctions such as must, should,
  may, can, planned, and decided;
- evidence and reasoning, including the claims they support;
- requirements, constraints, risks, trade-offs, and qualifications;
- actions, owners, and deadlines;
- uncertainty, assumptions, confidence, and attribution;
- numbers, names, identifiers (IDs), links, code symbols, and technical terms.

Normalise equivalent claims so wording differences do not hide duplication.
Only after this inventory is complete may content be classified as optional.
Keep background, examples, history, and repetition when they support,
disambiguate, constrain, or materially qualify required information.

### 3. Reconstruct once

Write one candidate from the retained inventory. Do not repeatedly shorten the
source or candidate. Put the main result, decision, or request first when
appropriate. Use the fewest sections that preserve necessary navigation and one
stable term for each concept. Do not add framing, summaries, transitions, or
decorative wording that contributes no information.

When both modifiers are requested, apply Compress first and Laconic second.

### 4. Perform one final preservation check

After any Laconic pass, compare the final candidate with both the source and the
semantic inventory. Confirm that no retained information was dropped, altered,
weakened, strengthened, newly implied, or misattributed. Confirm that each
sentence contributes unique required information and that every compatible
limit is met. Do not start another reconstruction.

## Hard-limit conflict

Treat a supplied limit as hard when it is compatible with preservation.
Preservation takes priority when the constraints conflict. Do not claim to have
met both constraints. Return:

    Constraint conflict: preserving required information needs [actual amount], above the [requested limit].

    [shortest complete version]

## Output

Return only the paste-ready compressed text unless the user asks for the
inventory, counts, or an explanation.
