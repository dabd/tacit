---
name: prose
description: >-
  Use when the user explicitly asks to draft, rewrite, tighten, clarify, proofread, or review the wording, grammar, style, or readability of software-engineering work prose. Do not use for ordinary coding answers, incidental prose, or substantive code, architecture, correctness, security, or design review unless the user also asks for prose editing. Do not use for extreme compression or an explicitly terse register.
user-invocable: false
---

# Prose

Edit software-engineering work prose conservatively. Preserve the author's
meaning and recognisable voice. A clear draft may need no changes.

## Rule priority

### Semantic invariants

Unless the user explicitly requests a content change, preserve:

- facts, intent, decisions, and requirements;
- uncertainty, assumptions, confidence, and attribution;
- numbers, identifiers, links, code symbols, and technical terms;
- reasoning, evidence, constraints, risks, trade-offs, and actions;
- the author's recognisable voice.

Do not invent context, increase certainty, or assign unsupported blame.

Foundation: [Preserve meaning](FOUNDATIONS.md#preserve-meaning),
[Preserve uncertainty](FOUNDATIONS.md#preserve-uncertainty), and
[Preserve terminology](FOUNDATIONS.md#preserve-terminology).

### Strong defaults

Prefer:

- known people, teams, services, components, or processes as subjects;
- verbs that name the action;
- literal, domain-specific wording;
- one stable term for each concept;
- one clear occurrence of each claim;
- the result, request, decision, or status near the start when that helps the
  reader act.

Foundation: [Prefer concrete agency](FOUNDATIONS.md#prefer-concrete-agency),
[Remove unnecessary words](FOUNDATIONS.md#remove-unnecessary-words),
[Eliminate duplicated claims](FOUNDATIONS.md#eliminate-duplicated-claims),
[Prefer literal language](FOUNDATIONS.md#prefer-literal-language), and
[Prefer common technical vocabulary](FOUNDATIONS.md#prefer-common-technical-vocabulary).

### Genre-dependent preferences

Punctuation, sentence length, passive voice, fragments, repetition, headings,
and paragraph structure depend on the genre. Change them only when they reduce
clarity or add unnecessary rhetoric. Read `references/genre-playbook.md` when
the genre is identifiable.

## Activation boundary

Use this skill only for an explicit writing or prose-review request. A request
to review an RFC, design, pull request, incident, or ticket for technical
correctness does not qualify unless the user also asks about its writing.

Do not apply this skill to code. Do not interpret `tighten` as permission to
remove useful information or reconstruct the document. Use `compress` only for
an explicit request for extreme reduction or a hard limit. Use `laconic` only
for an explicit request for that terse register.

## Editing sequence

### 1. Establish purpose and constraints

Identify the genre, reader, intended result, and any explicit tone, length, or
format constraint.

### 2. Improve sentence structure

- Move a known and relevant actor or system into the subject.
- Express the main action as a verb.
- Move the subject and verb earlier when introductory wording delays them.
- Connect sentences by placing known information before new information when
  that improves comprehension.
- Keep passive voice when the actor is unknown, irrelevant, intentionally
  omitted in a blameless account, or less important than the affected system.

### 3. Remove unnecessary wording and duplication

- Remove words that add no meaning.
- Keep one honest hedge when uncertainty is real.
- Replace inflated phrases with ordinary equivalents.
- Find repeated claims across headings, summaries, body sections, and
  conclusions. Keep more than one occurrence only when each serves a distinct
  function.
- Preserve evidence, examples, alternatives, and qualifications that support a
  decision or prevent ambiguity.

Normal editing is conservative. Do not reconstruct the document only to make it
shorter.

### 4. Check for model-specific wording

Use general tests instead of treating individual words as prohibited:

- **Literal-operation test:** Does the verb name the actual action? If not,
  replace it with the literal operation.
- **Conspicuous-phrase test:** Is the wording fashionable, unusually memorable,
  or reusable in unrelated documents without adding meaning? Replace it with
  ordinary wording or delete it.
- **Specific-effect test:** Does an evaluative word replace an observable
  result? State the result.
- **Agency test:** Does an abstraction act when a relevant person, team,
  service, component, or process is known? Name the actor. Keep abstract or
  system agency when it is accurate.

Terms such as `land`, `ship`, `unlock`, `leverage`, `drive`, and
`load-bearing` are examples, not prohibited words. Keep literal and established
domain uses. Edit a use only when it obscures the actual operation or adds no
information.

Foundation: [Prefer literal language](FOUNDATIONS.md#prefer-literal-language),
[Prefer common technical vocabulary](FOUNDATIONS.md#prefer-common-technical-vocabulary),
and [Tacit-specific contributions](FOUNDATIONS.md#tacit-specific-contributions).

Also remove introductory wording, emphasis adverbs, transitions, and rhetorical
reversals when they add no information.

### 5. Verify the result

Before returning the text:

- confirm that all required content and qualifications remain;
- confirm that terminology and attribution are unchanged;
- confirm that repeated claims serve distinct functions;
- confirm that no sentence was added only to improve rhythm;
- leave clean text unchanged.

## Response behavior

For drafting and rewriting, return only the paste-ready text unless the user
asks for critique, alternatives, annotations, or rationale.

For feedback, identify only issues that materially affect meaning or reader
action. Offer a revision when useful.

Do not append an unsolicited explanation, change summary, or offer of further
work.
