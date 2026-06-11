#!/usr/bin/env bash
# Regression tests for prose-gate.sh.
# Run: ./test-prose-gate.sh  (exit 0 = all pass)
#
# Fixtures use printf octal escapes for unicode punctuation so the file
# itself stays ASCII (the normalize-dashes hook rewrites literal em dashes
# in written files).

set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
GATE="$DIR/prose-gate.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
PASS=0
FAIL=0

EMDASH=$(printf '\342\200\224')

user_line() {
  jq -nc '{type:"user", message:{role:"user", content:[{type:"text", text:"hi"}]}}'
}

assistant_line() { # $1 = text
  jq -nc --arg t "$1" '{type:"assistant", message:{role:"assistant", content:[{type:"text", text:$t}]}}'
}

run_gate() { # $1 = transcript path, $2 = stop_hook_active (true/false)
  jq -nc --arg p "$1" --argjson a "$2" \
    '{session_id:"s", transcript_path:$p, hook_event_name:"Stop", stop_hook_active:$a}' \
    | bash "$GATE"
}

expect_block() { # $1 = name, $2 = output, $3 = substring expected in reason
  if printf '%s' "$2" | jq -e '.decision == "block"' >/dev/null 2>&1 \
     && printf '%s' "$2" | grep -qi -- "$3"; then
    echo "PASS: $1"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $1"
    echo "  expected block mentioning '$3', got: $2"
    FAIL=$((FAIL + 1))
  fi
}

expect_allow() { # $1 = name, $2 = output
  if [ -z "$2" ]; then
    echo "PASS: $1"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $1"
    echo "  expected no output (allow), got: $2"
    FAIL=$((FAIL + 1))
  fi
}

# T1: slop in the final reply blocks, and the reason names the violations.
T="$TMP/t1.jsonl"
{ user_line; assistant_line "It's worth noting that we could leverage the new cache $EMDASH and this isn't just faster, it's simpler. Basically a huge win."; } > "$T"
OUT=$(run_gate "$T" false)
expect_block "T1 slop blocks" "$OUT" "worth noting"
expect_block "T1 names figurative verb" "$OUT" "leverage"
expect_block "T1 names dash" "$OUT" "dash"

# T2: clean prose passes.
T="$TMP/t2.jsonl"
{ user_line; assistant_line "The cache cut p99 latency 40%. If we deploy Friday, the nightly batch job breaks. I suggest Monday."; } > "$T"
OUT=$(run_gate "$T" false)
expect_allow "T2 clean allows" "$OUT"

# T3: slop only inside a code fence passes.
T="$TMP/t3.jsonl"
CODE_MSG="Updated the linter config.
\`\`\`
# it's worth noting that we leverage this $EMDASH basically
rule: no-em-dash
\`\`\`
Tests pass: 12 of 12."
{ user_line; assistant_line "$CODE_MSG"; } > "$T"
OUT=$(run_gate "$T" false)
expect_allow "T3 code fence exempt" "$OUT"

# T4: stop_hook_active short-circuits (no infinite revision loop).
T="$TMP/t4.jsonl"
{ user_line; assistant_line "We should leverage this basically."; } > "$T"
OUT=$(run_gate "$T" true)
expect_allow "T4 stop_hook_active allows" "$OUT"

# T5: only the final assistant message is gated.
T="$TMP/t5.jsonl"
{ assistant_line "Let me delve into this $EMDASH it's worth noting."; user_line; assistant_line "The retry logic failed and wrote duplicates. Fix is in review."; } > "$T"
OUT=$(run_gate "$T" false)
expect_allow "T5 earlier slop ignored" "$OUT"

# T6: a blockquoted draft is still the model's prose and gets gated.
T="$TMP/t6.jsonl"
QUOTE_MSG="Here is the revised message, ready to paste:
> We should leverage the cache $EMDASH it's worth noting this helps.
Let me know if you want a shorter version."
{ user_line; assistant_line "$QUOTE_MSG"; } > "$T"
OUT=$(run_gate "$T" false)
expect_block "T6 blockquoted draft gated" "$OUT" "leverage"

# T6b: verbatim third-party quotes go in code fences, which are exempt.
T="$TMP/t6b.jsonl"
FENCED_QUOTE_MSG="Your original message read:
\`\`\`
it's worth noting $EMDASH we should leverage the cache
\`\`\`
I trimmed it to: \"Use the cache.\" The shorter form keeps the ask visible."
{ user_line; assistant_line "$FENCED_QUOTE_MSG"; } > "$T"
OUT=$(run_gate "$T" false)
expect_allow "T6b fenced quote exempt" "$OUT"

# T7: inline code is exempt.
T="$TMP/t7.jsonl"
{ user_line; assistant_line "Renamed \`leverageCache()\` to \`useCache()\` across the module. All call sites updated."; } > "$T"
OUT=$(run_gate "$T" false)
expect_allow "T7 inline code exempt" "$OUT"

# T8: em dash in plain prose blocks.
T="$TMP/t8.jsonl"
{ user_line; assistant_line "The fix${EMDASH}small but real${EMDASH}shipped today and closed the incident for good."; } > "$T"
OUT=$(run_gate "$T" false)
expect_block "T8 em dash blocks" "$OUT" "dash"

# T9: tiny replies are not gated.
T="$TMP/t9.jsonl"
{ user_line; assistant_line "Done."; } > "$T"
OUT=$(run_gate "$T" false)
expect_allow "T9 tiny reply allows" "$OUT"

# T10: figurative verb blocks.
T="$TMP/t10.jsonl"
{ user_line; assistant_line "Next I will delve into the retry logic and report back with what I find there."; } > "$T"
OUT=$(run_gate "$T" false)
expect_block "T10 delve blocks" "$OUT" "delve"

# T11: telegraphed contrast blocks.
T="$TMP/t11.jsonl"
{ user_line; assistant_line "This isn't just a refactor, it's a redesign of the whole ingestion path."; } > "$T"
OUT=$(run_gate "$T" false)
expect_block "T11 contrast blocks" "$OUT" "contrast"

# T12: emphasis adverb blocks.
T="$TMP/t12.jsonl"
{ user_line; assistant_line "This is basically the same approach we took for the export job last quarter."; } > "$T"
OUT=$(run_gate "$T" false)
expect_block "T12 adverb blocks" "$OUT" "basically"

# T13: missing transcript fails open.
OUT=$(run_gate "$TMP/does-not-exist.jsonl" false)
expect_allow "T13 missing transcript allows" "$OUT"

echo
echo "passed: $PASS, failed: $FAIL"
[ "$FAIL" -eq 0 ]
