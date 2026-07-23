# Changelog

## 0.3.0 - 2026-07-23

- Define Prose as the base skill, Compress and Laconic as modifiers, and
  Compress-then-Laconic as the required composition order.
- Simplify the package by removing the custom evaluator, text auditor, reviewer
  agents, fixtures, and tests used only by that machinery.
- Consolidate shared rules and citations in one canonical `FOUNDATIONS.md`.
- Add native Codex plugin and marketplace metadata alongside the Claude
  packaging.
- Correct the compression example and document installation, invocation,
  updates, and validation for both surfaces.

## 0.2.0 - 2026-07-20

- Narrow automatic prose activation to explicit writing and wording requests.
- Make paste-ready output the default for drafts and rewrites.
- Separate semantic invariants, strong defaults, and genre-dependent
  preferences.
- Add general tests for literal operations, conspicuous phrasing, specific
  effects, and agency.
- Add explicit `compress` mode with bounded reconstruction, redundancy review,
  preservation review, and hard-limit conflict reporting.
- Rewrite `laconic` as a content-preserving register change.
- Add independent redundancy and preservation reviewers.
- Add documented foundations and citations for the main rules.
- Package the foundations reference with each standalone skill.
- Add a Markdown-aware audit tool, an executable evaluation runner, fixtures,
  versioned result artifacts, and regression tests.
- Add semantic versioning.
