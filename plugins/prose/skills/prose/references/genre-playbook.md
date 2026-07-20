# Genre playbook

Use the structure that helps the reader act. These are defaults, not fixed
templates.

## Pull request description

Lead with what changed and why. Include when relevant:

1. a one-line summary;
2. the material changes;
3. the reason or defect;
4. how the change was tested;
5. rollout, migration, compatibility, or review risks.

Do not narrate the investigation unless it explains a decision.

## Code-review comment

Describe the code and its effect, not the author.

- Identify the line or behavior.
- Explain the consequence.
- State whether the comment is blocking, optional, or a question when useful.
- Suggest a concrete change or ask for missing context.

## Design document or RFC

Help readers decide. Lead with the problem, proposed decision, and reason for
the decision. Then cover constraints, alternatives, trade-offs, risks, rollout,
and unresolved questions. Keep reasoning that distinguishes the chosen option
from plausible alternatives.

## Live incident update

Readers need current state, impact, action, and timing. Use this order:

1. current status and impact;
2. what the team is doing;
3. known facts and uncertainty;
4. next update time.

Use explicit timestamps. Do not present speculation as fact.

## Postmortem

Describe how the system and process allowed the failure. Include impact,
timeline, contributing conditions, detection and response, and owned action
items. Use blameless language without making the account vague. Name systems,
controls, and decisions when known.

## Slack, Teams, or asynchronous message

Put the request, decision, blocker, or update first. Include enough context,
links, and timing for the reader to act without another exchange. Use short
paragraphs for separate points.

## Status update or standup

Report state instead of effort. Prioritise blockers and risks, then completed
work, current work, and next steps. Use concrete outcomes such as merged,
deployed, in review, or waiting on a dependency.

## Commit message

Match the repository's existing convention. Use an imperative subject when that
is the local style. Explain why in the body only when the diff does not make it
clear. Keep identifiers that help future searches.

## Ticket

Describe the problem and observable completion criteria. Include:

- a specific, searchable title;
- affected behavior and scope;
- evidence or reproduction details;
- acceptance criteria that another person can verify.

Avoid prescribing an implementation unless the implementation is itself a
requirement.
