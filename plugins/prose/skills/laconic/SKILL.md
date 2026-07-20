---
name: laconic
description: >-
  Use when the user explicitly invokes /prose:laconic or asks for laconic, terse, clipped, spare, Grant-like, or Klinkenborg-style prose. Do not use for generic editing, tightening, clarification, or compression requests.
argument-hint: [draft]
---

# Laconic

Change the register, not the information. Preserve facts, intent, reasoning,
evidence, uncertainty, attribution, numbers, identifiers, links, technical
terms, constraints, risks, and actions.

Use `$ARGUMENTS`. If it is empty, use the current selection or draft already
under discussion.

Foundation: [Laconic](FOUNDATIONS.md#laconic) and
[Preserve meaning](FOUNDATIONS.md#preserve-meaning).

Apply these rules:

1. Put one main thought in each sentence when splitting does not obscure a
   logical relation.
2. Prefer a period when a comma joins independent thoughts.
3. Remove a transition when sentence order already expresses the relation.
4. Keep transitions that express a required contrast, cause, condition, or
   sequence.
5. Remove lexical filler and semantic duplication. Do not remove a detail,
   qualification, emphasis, or explanation that changes meaning, urgency, or
   reader action.
6. Use literal verbs and ordinary technical wording.
7. Avoid a long sequence of equal-length sentences when small variation can be
   introduced without adding content.
8. Preserve necessary hedges and connected reasoning in every genre, including
   design arguments, diplomatic messages, and trade-off analysis.

Do not apply this register automatically. Return only the revised text unless
the user asks for an explanation. If the draft already uses this register,
return it unchanged.
