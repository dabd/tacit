---
name: prose
description: >-
  Use when drafting, editing, reviewing, or giving feedback on any prose a
  human will read - a Slack/Teams message, email, PR description, code review
  comment, design doc, RFC, technical spec, incident update, postmortem,
  status report, standup note, commit message, ticket, README, or doc
  comment - including when the user pastes text and says "fix this", "tighten
  this", "make this sound better", or "is this clear?", and before sending or
  posting any of the above. Not for code itself, only the prose humans read.
---

# Prose

One skill, one pass, three layers in order: **structure** (is each sentence
clear?), **concision** (is it tight?), **surface** (does it read human?).
This skill merges the former clarity-and-grace and stop-slop pipeline. The
ordering and the tie-breakers live here, in the text you are reading now,
not in a protocol document that never loads.

Sources, encoded as method in original wording: Williams and Bizup (*Style:
Lessons in Clarity and Grace*) for structure and concision; Verlyn
Klinkenborg (*Several Short Sentences About Writing*) for sentence
discipline; Hardik Pandya's stop-slop (MIT) for the tell inventory, re-tuned
for work writing.

The audience is a software engineer writing to coworkers. The goal is
writing that a busy, distracted reader understands on the first pass,
in the author's own voice.

## Prime directives

1. **Clarity first, grace last.** Make it understood before you make it
   pretty. Rhythm and balance are the final 10%, applied once the prose is
   clear and concise.
2. **Preserve the author's voice.** You are an editor, not a ghostwriter.
   Keep their phrasing, their jokes, their directness. Fix what blocks
   understanding; leave what is merely theirs. A revision the author doesn't
   recognize is a failed revision.
3. **Teach while you fix.** Name the principle behind each change in a few
   words, so next time they catch it themselves.
4. **Don't over-edit.** If a draft is already clean, say so and stop.
5. **Drafting counts.** When you write the first version yourself, apply all
   three layers before showing it. Don't draft slop and wait to be asked to
   clean it.

## Layer 1: structure

The single most useful move, Williams's own first step: **look at the first
seven or eight words of each sentence.** Most trouble lives there - abstract
subjects, long wind-ups, the action hidden in a noun. If a sentence opens
concrete and reaches a strong verb fast, the rest usually takes care of
itself.

### 1. Characters become subjects

Find the people, teams, services, systems *doing* things and make them the
grammatical subjects.

Input: There was a failure in the retry logic that led to duplicate writes.
Output: The retry logic failed and wrote duplicates.
Why: "there was" hides the actor; name what failed and let it act.

### 2. Actions become verbs (hunt nominalizations)

A nominalization is a verb or adjective turned into a noun: *decide* into
*decision*, *fail* into *failure*, *implement* into *implementation*.
Tell-tale endings: -tion, -ment, -ance, -ence, -ity, -al, -ing-as-noun.
Suspect one whenever it sits in the subject or after a weak verb (make,
perform, conduct, provide, achieve, do).

Input: We need to make a determination about whether deprecation of the v1
endpoint will have an impact on downstream consumers.
Output: We need to determine whether deprecating the v1 endpoint will affect
downstream consumers.
Why: three buried actions freed; the sentence drops by a third.

Keep nominalizations that are the real subject ("the **decision** was
reversed") or terms of art (*authentication*, *deployment*).

### 3. Old information before new (cohesion)

Open each sentence with something familiar from the previous one; end on the
new thing. Choppy "and then... and then" prose is usually new information
crashing in at the front.

Input: We added a cache layer. A 40% latency drop came from it.
Output: We added a cache layer. That dropped latency 40%.
Why: the second sentence now opens on the familiar idea and ends on the new
fact.

### 4. Consistent topics (coherence)

Across a paragraph, keep the subjects consistent and concrete so the passage
feels like it is about one thing. If every sentence opens on a different
abstract noun, the paragraph wanders even when each sentence is fine.

### 5. Emphasis in the stress position

The end of a sentence is where the reader's mind puts the weight. Put the
most important or newest information there; don't let a throwaway qualifier
("in most cases", "I think", "for now") dribble off the end.

Input: This will probably break the nightly batch job if we ship Friday, in
my opinion.
Output: If we ship Friday, this will probably break the nightly batch job.
Why: the consequence, the thing they act on, now sits last.

### 6. Subject and verb arrive fast

Open with the subject and verb, then extend with conditions and clauses.
Long wind-ups and big interruptions between subject and verb are the main
reason a sentence feels hard.

Input: Because of the fact that, as was mentioned in the sync, the auth
service, which is owned by another team, has rate limits, retries can fail.
Output: Retries can fail because the auth service (owned by another team)
has rate limits, as we mentioned in the sync.

## Layer 2: concision

Cut without changing meaning, in order of payoff:

- **Delete meaningless words:** actually, really, basically, just, very,
  quite, in order to, the fact that, it should be noted that.
- **Cut what's implied:** "future plans", "past history", "end result",
  "completely eliminate", "advance warning".
- **Phrase to word:** "due to the fact that" = because; "at this point in
  time" = now; "in the event that" = if; "has the ability to" = can.
- **Affirm the negative:** "not many" = few; "did not include" = omitted.
- **Hedge once, honestly.** Keep one hedge when the uncertainty is real; cut
  the reflex stack ("I think maybe we could possibly").
- **Plain over inflated:** utilize = use; facilitate = help; commence =
  start; methodology = method. Inflated diction signals effort, not
  competence. Keep genuine terms of art (idempotent, backpressure,
  eventual consistency); plainness cuts fake sophistication, never real
  technical vocabulary.
- **One name per thing.** Pick a term and reuse it. Elegant variation ("the
  service"... "the system"... "the component" for one thing) costs the
  reader certainty.

**Figurative-verb tics.** A verb borrowed from physical action to dress up
an abstract one is a tell. The test is metaphor, not the word: the literal
or domain sense is fine.

| Tic (figurative) | Use instead | Fine (literal/domain) |
|---|---|---|
| land a point/message | make, put, end on | a plane lands |
| ship a decision/narrative | make, finalize, send | ship a release |
| leverage the tooling | use, apply | financial leverage |
| delve/dive into | examine, look at | a diver dives |
| unlock value/potential | enable, allow | unlock a file |
| tap into | use, draw on | tap a pipe |
| foster/drive/fuel engagement | build, cause, support | drive a car |

**The guardrail: cut words, never load-bearing reasoning.** In a design doc,
PR, or postmortem, the *why* (why this approach, why not the alternative,
what the risk is) is the payload, not filler. Be economical with words and
generous with reasons.

## Layer 3: surface

Run last, on finished sentences. This layer removes the patterns that make
prose read as generated.

1. **Tell-phrases die on sight:** "it's worth noting", "here's the thing",
   "let me be clear", "let that sink in", "at the end of the day",
   "the key takeaway", "I wanted to flag", "this matters because", and
   vague declaratives ("the implications are significant") - name the
   implication instead.
2. **Adverbs:** cut emphasis adverbs (really, actually, basically, simply,
   literally, genuinely, honestly, truly, incredibly, fundamentally,
   essentially, importantly, crucially, notably, interestingly). Keep
   information adverbs (not, never, often, still, already, only). Restore an
   emphasis adverb only if its removal changes meaning.
3. **Active voice, named actors.** No false agency: decisions don't
   "emerge", cultures don't "shift" - someone decides, people change
   behavior. Exception: blameless postmortems and genuinely unknown actors;
   the genre playbook governs there.
4. **No em or en dashes.** Use a comma, colon, period, parenthesis, or
   ' - '. (House rule; hooks normalize files and gate replies.)
5. **The contrast templates are banned, even for earned contrasts.** "Not
   just X but Y", "isn't X, it's Y", "the answer isn't X", and negative
   listings ("It's not A. It's not B. It's C.") never appear. When the
   contrast is real content (X is a position the reader holds and you are
   correcting it), state Y first with its evidence, then demote X
   explicitly: "This is a correctness bug: writes duplicate. The latency
   hit is secondary." When X is a strawman nobody holds, delete it and
   state Y. Genuine parallel ideas may keep parallel form ("first...,
   then..."); the manufactured-reversal template goes regardless.
6. **Fragments are rationed.** At most one deliberate fragment per message,
   where the emphasis is earned. A staccato run reads as performance. (When
   the user asked for the laconic register, that skill governs sentence
   length instead.)
7. **Rhythm:** vary sentence length and paragraph endings; don't close every
   paragraph on a punchline. Three-item lists are fine here - this is work
   writing, where completeness beats blog cadence.
8. **Trust the reader.** No meta-commentary ("let me walk you through"), no
   permission-granting ("and that's okay"), no quotable-isms. State facts
   plainly.

## Genres

Each genre has a shape: what goes first, how long, how blunt. When the task
names or implies one (PR description, code review comment, design doc or
RFC, incident update or postmortem, async message, status update, commit
message, ticket), read `references/genre-playbook.md` before editing. The
unifying rule: bottom line up front.

## The laconic register (opt-in)

A terse, declarative voice lives in the separate `laconic` skill. It is a
register choice, never a correction: apply it only when the user explicitly
asks for laconic, terse, clipped, or spare prose, or runs /prose:laconic.
Generic "edit this" requests never trigger it.

## How to respond

- **"Fix this" / "tighten this":** revised version first, ready to paste.
  Then the 2-4 highest-value changes and the principle behind each. Don't
  annotate every comma.
- **"Is this clear?" / "feedback?":** diagnose before you rewrite. Point at
  the sentences that block the reader, name why, then offer a revision.
- **"Help me write a [PR / doc / update]":** draft it through all three
  layers, then point out the one or two structural choices you made.

Keep your own explanation as clean as the revision; practice what the skill
preaches. Two presentation rules: a draft you produce is your prose and gets
gated wherever it appears (inline or blockquoted), so write it clean; and
when you name a phrase you cut, put it in backticks (`worth noting`), and
put any verbatim third-party text you quote in a code fence. Backticks and
fences are the only gate exemptions.

## Enforcement

A Stop hook (`prose-gate`) lints final replies for the mechanical floor:
unicode dashes, tell-phrases, figurative verb tics, emphasis adverbs,
telegraphed contrasts. If it blocks a reply, fix the listed items and finish
again; don't argue with the gate. The judgment layers - structure, cohesion,
emphasis - are yours alone; no linter checks them.
