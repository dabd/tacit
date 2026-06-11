# Worked examples

Original before/after pairs, tagged by the diagnosis the skill applies.
These are auditable fixtures: each shows one principle, the broken input,
the fix, and why. All examples are original, written for this plugin. They
double as regression checks: if an edit to the skill changes how it handles
one of these, the change is visible here.

Tags map to the layers in `../skills/prose/SKILL.md`: `action-as-noun`,
`abstract-subject`, `old-to-new`, `stress-position`, `shape`, `concision`,
`surface`, `contrast`.

---

## action-as-noun

A live verb is buried in a noun (a nominalization). Find it, free it.

**Before:** The team made a decision about the deprecation of the v1 endpoint.
**After:** The team decided to deprecate the v1 endpoint.
**Why:** `decision` to decide, `deprecation` to deprecate. Two buried verbs
freed, the sentence shortens, the action becomes plain.

---

## abstract-subject

The grammatical subject is an abstraction, so the reader cannot see who acts.

**Before:** Consideration of the cache invalidation bug is happening on the
platform side.
**After:** The platform team is looking into the cache invalidation bug.
**Why:** `Consideration ... is happening` hides the actor. Put the real
character (platform team) in the subject and let it act.

---

## old-to-new

A sentence opens on new information instead of connecting to what came before.

**Before:** We added a read-through cache. A 40% latency drop came from it.
**After:** We added a read-through cache. That dropped latency 40%.
**Why:** The second sentence now opens on the familiar idea (`That` = the
cache) and ends on the new fact (the 40% drop). The reader rides the link.

---

## stress-position

The most important information sits mid-sentence, where the reader weights it
least, while a throwaway qualifier takes the end.

**Before:** This breaks the nightly reconciliation job if we deploy on
Friday, I think.
**After:** If we deploy on Friday, this breaks the nightly reconciliation job.
**Why:** The end of a sentence carries the most weight. Move the consequence
there and drop the reflex hedge.

---

## shape

The reader waits through a long wind-up and an interruption before reaching
the subject and verb.

**Before:** Because of the fact that the auth service, which another team
owns, rate-limits us, retries can fail.
**After:** Retries can fail because the auth service (owned by another team)
rate-limits us.
**Why:** Subject and verb (`Retries can fail`) arrive first. The conditions
trail behind instead of blocking the way in.

---

## concision

Inflated phrasing and filler pad the sentence without adding meaning.

**Before:** In order to facilitate the utilization of the new client, we will
be providing documentation at this point in time.
**After:** To help people use the new client, we are writing docs now.
**Why:** `in order to` to to, `facilitate the utilization of` to help use,
`at this point in time` to now. Every inflated phrase swapped for the plain
word.

---

## surface

The sentences are clear and tight, yet the prose still reads as generated:
tell-phrases, emphasis adverbs, a figurative verb.

**Before:** It's worth noting that this basically lets us leverage the
existing retry queue, which is a huge win for reliability.
**After:** This reuses the existing retry queue, so transient failures now
retry instead of dropping.
**Why:** Throat-clearing opener cut, `basically` cut, `leverage` swapped for
the plain verb, and the vague `huge win` replaced by the specific effect.

---

## contrast

A telegraphed reversal manufactures drama around a point nobody disputed.

**Before:** This isn't just a config change. It's a fundamental shift in how
we deploy.
**After:** This changes the deploy order: migrations now run before the
rollout, so a failed migration blocks the release.
**Why:** The `not just X` setup argues with no one. State what changed and
why the reader should care. (A contrast survives only when it corrects a
position the reader holds.)
