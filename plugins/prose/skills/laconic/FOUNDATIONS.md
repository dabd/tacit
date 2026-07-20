# Foundations

Tacit is an editorial framework for technical writing. It does not prescribe a
house style. It combines established guidance from technical communication,
scientific writing, software documentation, and RFC editorial practice into a
small set of editorial principles.

Where established sources disagree, Tacit prefers conventions that maximise
precision, minimise unnecessary prose, and preserve the author's intent.

The framework distinguishes between three tasks:

- **Prose** improves clarity while preserving meaning, structure, and voice.
- **Laconic** changes the writing style to a terse register without materially
  changing the information.
- **Compress** removes information that is not required for the document's
  purpose.

This separation keeps editing, stylistic transformation, and summarisation as
distinct operations.

## Design principles

### Preserve meaning

**Rule**

Editing must preserve facts, reasoning, uncertainty, attribution, terminology,
constraints, and decisions unless the user explicitly requests otherwise.

**Rationale**

Editors improve expression, not content.

**Sources**

- Joseph M. Williams, *Style: Lessons in Clarity and Grace*
- Google Developer Documentation Style Guide
- Microsoft Writing Style Guide

### Prefer concrete agency

**Rule**

Prefer explicit subjects performing observable actions.

Prefer:

> The scheduler retries the request.

Over:

> The request eventually gets handled.

**Rationale**

Concrete agency reduces ambiguity and makes behaviour easier to understand.

**Sources**

- Joseph M. Williams, *Style: Lessons in Clarity and Grace*
- George D. Gopen and Judith A. Swan, *The Science of Scientific Writing*

**Exceptions**

- Blameless postmortems
- Intentional abstraction
- Mathematical and scientific writing

### Remove unnecessary words

**Rule**

Delete words that do not change the meaning. Prefer deletion to substitution
when both produce the same result.

**Rationale**

Extra words increase cognitive load without increasing information.

**Sources**

- William Strunk Jr. and E. B. White, *The Elements of Style*, applied selectively
- Joseph M. Williams, *Style: Lessons in Clarity and Grace*
- Google Developer Documentation Style Guide

### Eliminate duplicated claims

**Rule**

Each semantic claim should appear once unless repetition serves a clear
rhetorical or navigational purpose.

**Rationale**

Models often repeat conclusions across introductions, headings, summaries, and
body text. Tacit removes duplicate ideas rather than only shortening sentences.

**Source**

Tacit contribution.

### Prefer literal language

**Rule**

Prefer literal descriptions of technical behaviour over metaphorical or
fashionable language.

Prefer:

> The handler stores the result.

Over:

> The handler unlocks performance.

**Rationale**

Literal language is usually more precise and remains clear as usage changes.

**Sources**

Inspired by established technical documentation practice and formalised by
Tacit.

### Prefer common technical vocabulary

**Rule**

Prefer ordinary, widely understood technical terms over distinctive or
fashionable wording.

**Rationale**

Technical documents should prioritise recognition over novelty.

**Sources**

- Google Developer Documentation Style Guide
- Microsoft Writing Style Guide

### Preserve uncertainty

**Rule**

Retain uncertainty, confidence levels, assumptions, and attribution. Never
convert qualified statements into certainty.

**Rationale**

Editorial changes must not alter epistemic meaning.

**Sources**

- Scientific writing practice
- RFC editorial guidance

### Preserve terminology

**Rule**

Do not replace established domain terminology merely for stylistic variety.

**Rationale**

Consistency is more valuable than lexical variation.

**Sources**

- Software documentation practice
- API documentation conventions

## Compression philosophy

Tacit's compression mode intentionally removes optional information. Its
objective is to minimise length while preserving the required semantic content.

Compression follows four stages:

1. Extract the semantic inventory.
2. Detect duplicated claims.
3. Reconstruct the document from retained information.
4. Verify that no required information was lost.

Compression stops when every remaining sentence contributes unique required
information.

## Stylistic modes

### Prose

- Improves clarity.
- Preserves voice.
- Preserves information.
- May make no changes.

### Laconic

- Changes register.
- Preserves information.
- Optimises for directness and economy.

### Compress

- Changes information density.
- May remove examples, repetition, historical context, explanations, and
  optional rationale.
- Always requires explicit user intent.

## Tacit-specific contributions

The following principles are Tacit contributions rather than rules taken
directly from a published style guide:

- Separation of editing, stylistic transformation, and semantic compression.
- Claim-level deduplication.
- Semantic reconstruction instead of iterative shortening.
- Detection of fashionable model phrasing through general editorial tests
  rather than expanding blacklists.
- Independent redundancy and preservation review during compression.
- The requirement that every sentence in an extremely compressed document
  contribute unique required information.

## Primary influences

### Technical writing

- Joseph M. Williams, *Style: Lessons in Clarity and Grace*
- George D. Gopen and Judith A. Swan, *The Science of Scientific Writing*

### Software documentation

- Google Developer Documentation Style Guide
- Microsoft Writing Style Guide
- Linux kernel documentation
- Go project documentation
- PostgreSQL documentation
- Rust standard library documentation

### Standards

- RFC 7322, *RFC Style Guide*
- Well-edited IETF RFCs

Tacit is informed by these sources. It does not implement any one source as a
complete style guide.
