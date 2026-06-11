#!/usr/bin/env bash
# Stop hook: the prose gate. Lints the final assistant reply for mechanical
# style violations (unicode dashes, AI-tell phrases, figurative verbs,
# emphasis adverbs, telegraphed contrasts, sycophant openers) and blocks
# once so the reply gets revised. Judgment-level rules (structure, cohesion,
# emphasis) live in the prose skill; this gate is only the floor.
#
# Fail-open by design: any internal error allows the stop (exit 0).
# Loop guard: when stop_hook_active is true the gate allows the stop, so a
# turn is revised at most once.
#
# ASCII-only source: unicode punctuation is built with printf escapes because
# a PreToolUse hook normalizes literal unicode dashes in written files.

set -u

command -v jq >/dev/null 2>&1 || exit 0
command -v perl >/dev/null 2>&1 || exit 0

INPUT=$(cat) || exit 0

STOP_ACTIVE=$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null) || exit 0
[ "$STOP_ACTIVE" = "true" ] && exit 0

TRANSCRIPT=$(printf '%s' "$INPUT" | jq -r '.transcript_path // empty' 2>/dev/null) || exit 0
[ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ] || exit 0

# The last assistant message that contains text blocks (sidechains excluded).
TEXT=$(jq -rs '
  [ .[]
    | select(type == "object" and .type == "assistant" and ((.isSidechain // false) | not))
    | (.message.content // [])
    | if type == "array" then . else [] end
    | map(select(type == "object" and .type == "text") | .text)
    | select(length > 0)
    | join("\n\n")
  ] | last // ""' < "$TRANSCRIPT" 2>/dev/null) || exit 0

[ -z "$TEXT" ] && exit 0

# Gate prose only: drop fenced code, inline code, and URLs. Blockquotes are
# NOT exempt: a drafted message presented as a quote is still the model's
# prose. Verbatim third-party quotes belong in code fences.
PROSE=$(printf '%s' "$TEXT" \
  | perl -0777 -pe 's/```.*?```//gs; s/~~~.*?~~~//gs' 2>/dev/null \
  | sed -E 's/`[^`]*`//g' \
  | perl -pe 's#https?://\S+##g' 2>/dev/null) || exit 0

[ "${#PROSE}" -lt 20 ] && exit 0

NL=$'\n'
VIOLATIONS=""

add_violation() { # $1 = label, $2 = matches (newline separated, may be empty)
  local shown
  shown=$(printf '%s\n' "$2" | grep -v '^$' | sort -fu | head -3 \
    | tr '\n' '~' | sed 's/~$//; s/~/", "/g')
  [ -z "$shown" ] && return 0
  VIOLATIONS="${VIOLATIONS}- ${1}: \"${shown}\"${NL}"
}

scan() { # $1 = label, $2 = perl-compatible pattern (matched case-insensitively)
  local m
  m=$(printf '%s\n' "$PROSE" | PAT="$2" perl -ne 'while (/$ENV{PAT}/gi) { print "$&\n" }' 2>/dev/null) || return 0
  add_violation "$1" "$m"
}

# Unicode dashes (byte-wise match so locale does not matter).
EMDASH=$(printf '\342\200\224')
ENDASH=$(printf '\342\200\223')
DASHES=$(printf '%s' "$PROSE" | LC_ALL=C grep -coF -e "$EMDASH" -e "$ENDASH" 2>/dev/null) || true
if [ -n "${DASHES:-}" ] && [ "$DASHES" -gt 0 ] 2>/dev/null; then
  VIOLATIONS="${VIOLATIONS}- em/en dash x${DASHES} (use a comma, colon, period, or ' - ')${NL}"
fi

scan "AI-tell phrase (state the point directly)" \
  'worth noting|it should be noted|needless to say|let that sink in|at the end of the day|when it comes to|the key takeaway|here.{0,3}s the (?:thing|deal|kicker)|let me be clear|i hope this helps|hope (?:this|that) helps|great question|happy to help|let me walk you through|i wanted to flag|this matters because|here.{0,3}s why (?:it|this|that) matters|a testament to|game.chang\w*|revolutioniz\w*|in today.{0,3}s (?:world|landscape|environment|fast)'

scan "figurative verb (swap for a plain verb: use, examine, build, enable)" \
  '\bdelv(?:e|es|ed|ing)\b|\bleverag(?:e|es|ed|ing)\b|\btap(?:s|ped|ping)? into\b|\bdeep[- ]div(?:e|es|ing)\b|\bdiv(?:e|es|ing) into\b|\bfoster(?:s|ed|ing)?\b|\bunlock(?:s|ed|ing)? (?:the )?(?:full )?(?:value|potential|growth|insight\w*)\b'

scan "emphasis adverb (cut it; let the fact carry the weight)" \
  '\b(?:really|actually|basically|simply|literally|genuinely|honestly|truly|incredibly|remarkably|undoubtedly|seamlessly|effortlessly|fundamentally|essentially|crucially|importantly|notably|interestingly|arguably|certainly|definitely)\b'

scan "telegraphed contrast (drop the 'not X' setup; state the point)" \
  'isn.{0,3}t just|aren.{0,3}t just|wasn.{0,3}t just|\bnot just\b|\bnot only .{1,60}?\bbut\b|it.{0,3}s not about .{1,60}?it.{0,3}s about|the (?:answer|question|problem) isn.{0,3}t'

scan "sycophant opener (start with the content)" \
  '^(?:great|perfect|excellent|awesome|amazing|certainly|absolutely)[!.,]'

[ -z "$VIOLATIONS" ] && exit 0

REASON="prose-gate: the final reply violates house prose style. Revise the reply and finish again, fixing each item:${NL}${VIOLATIONS}Rules: the prose skill (prose:prose) and prose-rules.md. Only code blocks and backticked terms are exempt: name a flagged term in backticks, put verbatim third-party quotes in a code fence, and remember a blockquoted draft is still your prose."

jq -n --arg r "$REASON" '{decision: "block", reason: $r}'
exit 0
