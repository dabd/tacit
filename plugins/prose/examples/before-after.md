# Worked examples

Each example isolates one behavior. These examples are not exact-output tests.

## Concrete actor and verb

**Before:** There was a failure in the retry logic that resulted in duplicate
writes.

**After:** The retry logic failed and wrote duplicates.

## Claim-level duplication

**Before:**

The migration is safe because the old column remains available during rollout.

### Rollout safety

The old column remains available while the new code rolls out, which makes the
migration safe.

**After:**

The migration is safe because the old column remains available during rollout.

## Literal operation

**Before:** This change unlocks a path for requests to land in the fallback
queue.

**After:** This change sends failed requests to the fallback queue.

`ship a release`, `land a patch`, and `unlock a mutex` can be established domain
uses. Edit them only when they fail to name the operation accurately.

## Unfamiliar conspicuous phrase

**Before:** The hinge-point observation is that retries must be idempotent.

**After:** Retries must be idempotent.

The edit removes framing that adds no information. It does not depend on a list
of known phrases.

## Preserve uncertainty and attribution

**Before:** According to Priya, connection-pool exhaustion may cause the
timeout, but the traces are incomplete.

**Bad edit:** Connection-pool exhaustion causes the timeout.

**After:** Priya said connection-pool exhaustion may cause the timeout; the
traces are incomplete.

## Extreme compression reconstructs

**Before:**

We propose moving token refresh into a single-flight section. The current
implementation permits two concurrent requests to refresh the token. The second
refresh can overwrite the first token and log the user out. The proposal
serializes token refresh so only one refresh can happen at a time.

**After:**

We propose single-flight token refresh: concurrent refreshes can overwrite the
token and log the user out.

## Compress plus Laconic

**Before:**

The old column remains available during rollout. Keeping it available preserves
compatibility while the new reader is deployed.

### Cleanup

The old column remains available during rollout. We should remove the old
column after every reader migrates.

**After:**

The old column remains available during rollout for compatibility. We should
remove it after every reader migrates.

## Clean text remains unchanged

**Input:** The worker retries failed writes three times, then sends them to the
dead-letter queue.

**Expected:** No edit.
