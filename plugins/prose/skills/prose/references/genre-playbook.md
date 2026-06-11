# Genre Playbook

Conventions for each kind of work writing a software engineer produces. The
clarity method in SKILL.md always applies - characters as subjects, actions as
verbs, old-to-new flow, emphasis at the end. This file adds the *structure*:
what goes first, how long it should be, how blunt to be.

The unifying rule across every genre: **bottom line up front (BLUF).** A
distracted reader should get the point from the first sentence or two. Detail
comes after, for the reader who needs it.

## Contents
- [Pull request descriptions](#pull-request-descriptions)
- [Code review comments](#code-review-comments)
- [Design docs / RFCs](#design-docs--rfcs)
- [Incident updates & postmortems](#incident-updates--postmortems)
- [Async / Slack messages](#async--slack-messages)
- [Status updates & standup](#status-updates--standup)
- [Commit messages](#commit-messages)
- [Tickets (JIRA)](#tickets-jira)

---

## Pull request descriptions

A PR description answers two questions the reviewer has before reading a single
line of diff: **what changed, and why.**

Use two sections, **What** then **Why**, and bullet the contents of each: one
bullet per change, one per reason. Reviewers scan; a wall of prose hides the
point. Keep prose for a one-line summary and any nuance a bullet can't carry.

Shape:
- **One-line summary** of what this does (becomes the squash-merge message).
- **What** - the changes, one bullet each. Call out anything the reviewer should
  look at hardest.
- **Why** - the problem, bug, or goal, one bullet each. Link the ticket; don't
  make them dig.
- **How it was tested / how to verify.**
- **Anything risky** - migrations, feature flags, rollout order, blast radius.

Lead with the reader's job: make it easy to say yes. Don't narrate your
debugging journey; state the result.

Input: I was looking into the thing where users get logged out and it turned out
to be a bunch of stuff with the token refresh, so I changed how we handle it and
also fixed some other things I noticed.
Output:
**Fix premature logout caused by token-refresh race.** Two concurrent requests
could each trigger a refresh; the second clobbered the first's token, logging the
user out. Now refreshes are serialized behind a single-flight lock.
Also: dropped a dead retry path in `AuthClient` (noticed while in here).
Testing: added a concurrency test that reproduced the logout; reproduces no more.

## Code review comments

Two goals in tension: the code should get better, and the author should not feel
attacked. Resolve it by being **specific and about the code, not the person**,
and by separating must-fix from preference.

- Critique the code, not the coder: "this function does X" not "you did X wrong."
- Be specific and actionable - point at the line, suggest the change.
- Mark severity so they can triage: blocking vs. suggestion vs. nit. A common
  convention is prefixing optional comments with `nit:` or `optional:`.
- Ask, don't decree, when you might be missing context: "Is there a reason this
  isn't behind the existing lock?" beats "This needs a lock."
- Say what's good too, briefly. It's not flattery; it tells the author what to
  keep doing.

Input: This is wrong, you can't do it like this, it'll break under load.
Output: Under concurrent load two callers can hit this path at once and double-
write. Could we reuse the `withLock` helper from `store.go` here? (Blocking - I
think this is the same race as INC-204.)

## Design docs / RFCs

The doc exists to help readers *decide*, not to show how much you know. Most
readers skim; the deep readers are few. Serve both.

- **Lead with the problem and the proposal**, in a few sentences, before any
  background. A reader should know what you're proposing and why from the top.
- A short **TL;DR / summary** at the top earns its space.
- Make the **decision and its alternatives** explicit. What did you consider and
  reject, and why? This is where design docs earn trust.
- State **trade-offs and what you're NOT doing.** Honesty about cost reads as
  competence.
- This is the genre most infested with nominalizations and passive voice. Run the
  clarity checks hard: "the implementation of the synchronization mechanism" →
  "how we synchronize."

## Incident updates & postmortems

**Live incident updates:** maximum clarity, minimum prose. People are stressed
and skimming.
- Lead with **current status and impact**: who/what is affected, right now.
- Then **what we're doing** and **next update time.**
- Plain timestamps. No speculation dressed as fact.

**Postmortems:** the cultural rule is **blameless** - describe systems and
decisions, not culprits. Here passive voice or system-as-subject is often the
*right* call: "the deploy script skipped the health check" rather than "Priya
forgot to..." Focus on what let the failure happen and what will catch it next
time. Be factual and specific in the timeline; save judgment for action items.

## Async / Slack messages

Optimize for a reader who is busy and context-switching.
- **Front-load the ask or the point.** If you need something, say what and by
  when in the first line. "Can you review #4821 before EOD? It blocks the release."
- One idea per message or per short paragraph; use line breaks. A wall of text
  gets skipped.
- If it needs three back-and-forths to resolve, it's a call or a thread, and say
  so.
- Skip the slow wind-up. "Hey, hope you're well, quick question, so I was
  wondering if maybe..." → just ask. (Keep the pleasantry if it's *you* - see
  voice preservation in SKILL.md.)
- Give enough context to act without a follow-up question: link, error, what you
  tried.

## Status updates & standup

Readers want signal: are we on track, and is anything blocked? Structure beats
narrative.
- **Done / in progress / blocked** - or **progress / plans / problems.**
- Lead with anything **blocked or at risk**; that's the only part most readers
  act on.
- Concrete state, not activity: "auth flow merged, in QA" beats "worked on auth."
- Cut "continued to," "started looking into," "spent time on." Report state, not
  effort.

## Commit messages

Convention most teams follow:
- **Subject line:** imperative mood, ~50 chars, no period. "Add retry backoff to
  webhook sender" - reads as "if applied, this commit will..."
- Blank line, then a **body** (wrap ~72 cols) explaining *why* when it isn't
  obvious. The diff shows what; the body justifies it.
- Many teams use Conventional Commits: `type(scope): summary`, e.g.
  `fix(auth): serialize token refresh to prevent logout`. Match the repo's
  existing style - look at the log before imposing one.

Input: fixed the bug
Output: fix(auth): serialize token refresh to prevent premature logout

## Tickets (JIRA)

A ticket is a contract for future work, often picked up by someone with no
context, months later. It describes the problem and the finish line, never
the implementation.

- **Title: the problem, findable.** Specific enough that a search next
  quarter hits it. "Token refresh races under concurrent requests" beats
  "Auth issues".
- **Problem first.** What happens, where, who it affects, and how to
  reproduce or observe it. Link the evidence (dashboard, incident, log
  query); don't paste walls of output.
- **Acceptance criteria: observable outcomes.** What must be true for the
  ticket to close. Each criterion checkable by someone other than the
  author.
- **No implementation details.** Naming the fix locks in today's guess; the
  assignee may know a better one, and the codebase will have moved. If a
  design discussion is needed, that's a comment or a doc, not the ticket
  body.
- **Severity as facts.** "Affects all EU tenants since 14:00 UTC" beats
  "critical!!". Let the reader weigh it.

Input: Auth is broken again, we should add a mutex around the token refresh
like we discussed, pretty urgent.
Output:
**Title:** Concurrent requests race on token refresh, logging users out
**Problem:** Two simultaneous 401 retries each trigger a refresh; the second
overwrites the first's token and the session drops. ~40 logouts/day since
the 2.31 rollout (dashboard link).
**Acceptance criteria:** concurrent refreshes produce one token; the logout
rate returns to pre-2.31 baseline; a regression test covers the race.
