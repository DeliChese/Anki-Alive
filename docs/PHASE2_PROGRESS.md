# Phase 2 — Oracle Progress

Status: LIVE REVIEWER INTEGRATION STARTED
Date: 2026-08-19

## Slice 1 — commitment lifecycle foundation

Implemented on `main`:

- feature-neutral `MemorySnapshot` / `MemoryEngine` contract,
- `ReviewContextService` aggregation seam,
- sidecar schema migration from v3 to v4,
- durable `oracle_predictions` table,
- Oracle domain model and deterministic first policy,
- persisted pre-answer commitment identity,
- duplicate commitment suppression for the same Expedition/card,
- accepted-review resolution with explicit recall mapping (`Again` = failed recall; non-`Again` = recalled),
- repository guard rejecting outcomes timestamped before commitment,
- durable post-answer `oracle_resolution` presentation event,
- in-memory `EventOrchestrator` integration for the domain slice,
- Undo reconciliation that reopens the original commitment instead of rerolling it,
- invalidation of stale pending Oracle reveal after Undo,
- re-answer resolution using the same Oracle commitment,
- Phase 2 regression tests covering schema, durability, commitment ordering, resolution, reveal, Undo, re-answer, and safe policy fallback.

## Slice 2 — live Anki/FSRS reviewer integration

Implemented on `main`:

- `AnkiMemoryEngine` reads current host card memory facts at the integration boundary,
- stability/difficulty come from Anki `Card.memory_state`,
- retrievability is derived from Anki's persisted stability, `last_review_time`, and `decay` using the current FSRS forgetting curve,
- interval, lapses, review count, and a bounded recent rating history are normalized into `MemorySnapshot`,
- missing FSRS state degrades to `retrievability=None` instead of inventing a probability,
- `gui_hooks.reviewer_did_show_question(card)` is the commitment trigger, guaranteeing the hook runs before an accepted answer outcome,
- `ReviewContextService` aggregates active Expedition + MemorySnapshot on the question boundary,
- Oracle cadence is sparse and deterministic from durable Expedition progress: first eligible boundary, then every 5 accepted reviews,
- no pre-answer Oracle prediction text or probability is shown,
- accepted `ReviewObservation` resolves the existing commitment and creates durable reveal state,
- post-answer reveal is a small, non-interactive reviewer status surface,
- Focus Mode suppresses presentation while preserving resolved Oracle domain truth,
- Reduced Motion removes reveal transition dependence,
- if Expedition completion moves the host out of review before the scheduled Oracle reveal, session closure wins and the stale reveal is suppressed,
- presentation state now supports explicit `SHOWN` and `SUPPRESSED` transitions,
- additional regression tests cover the FSRS forgetting curve and host-memory normalization adapter.

## Current policy v1

The first policy deliberately avoids fake scientific complexity:

- minimum 3 prior reviews,
- normalized retrievability must be available,
- retrievability below 0.75 predicts `FAIL`, otherwise `RECALL`,
- raw normalized probability is persisted for explainability but is not shown pre-answer,
- initial cadence is one Oracle opportunity per 5 durable Expedition progress units,
- `Again` maps to failed recall; `Hard`/`Good`/`Easy` map to recalled for the binary Oracle outcome.

This policy is provisional and must be validated against actual Anki/FSRS host data before Phase 2 close.

## Upstream host contract used

Current Anki exposes FSRS memory state on `Card.memory_state`, plus `last_review_time` and `decay`. The reviewer question hook is `gui_hooks.reviewer_did_show_question(card)`. Anki's own browser/statistics code derives retrievability from stability, elapsed time since the last review, and decay; Anki Alive mirrors that calculation inside the integration adapter rather than adding scheduler policy.

## Validation status

Regression tests now include:

- `tests/test_phase2_oracle.py`
- `tests/test_phase2_memory_integration.py`

They have **not been executed by the current agent environment** because the environment cannot clone/reach GitHub over the network and the repository currently exposes no CI status for direct-to-main commits. Do not infer a passing test run from test-file existence.

The next local/host sync should run the full suite and then exercise a real FSRS-enabled Expedition.

## Next slice

1. run the full automated suite locally after sync,
2. real-host smoke: confirm Oracle commits on an eligible FSRS card before answer and reveals only after grading,
3. verify no reveal occurs outside an active Expedition,
4. verify Focus Mode suppresses reveal without deleting Oracle history,
5. real-host Undo → same commitment reopens → re-answer resolves once,
6. verify Expedition completion suppresses competing Oracle reveal,
7. measure integrated reviewer P50/P95 with Oracle enabled,
8. decide whether Oracle reveals should be `MINOR` instead of `MAJOR` for long-term orchestration,
9. add durable deferred-reveal recovery only if real UX evidence requires it.

## Scope guard

No Rescue, Nemesis, Fragment, Relic, or Memory World lifecycle code is introduced by these slices.
