# Phase 2 — Oracle Progress

Status: IMPLEMENTATION STARTED
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
- in-memory `EventOrchestrator` integration,
- Undo reconciliation that reopens the original commitment instead of rerolling it,
- invalidation of stale pending Oracle reveal after Undo,
- re-answer resolution using the same Oracle commitment,
- Phase 2 regression tests covering schema, durability, commitment ordering, resolution, reveal, Undo, re-answer, and safe policy fallback.

## Current policy v1

The first policy deliberately avoids fake scientific complexity:

- minimum 3 prior reviews,
- normalized retrievability must be available,
- retrievability below 0.75 predicts `FAIL`, otherwise `RECALL`,
- raw normalized probability is persisted for explainability,
- cadence/frequency limiting is intentionally not embedded in memory policy and remains an integration concern for the next slice.

This policy is provisional and must be validated against actual Anki/FSRS host data before Phase 2 close.

## Validation status

Regression tests were added in `tests/test_phase2_oracle.py`.

They have **not been executed by the current agent environment** because the environment cannot clone/reach GitHub over the network and the repository currently exposes no CI status for the latest direct-to-main commit. Do not infer a passing test run from test-file existence.

The next local/host sync should run the full suite before deeper reviewer integration.

## Next slice

1. implement a real Anki-backed MemoryEngine adapter with validated FSRS/review-history fallbacks,
2. wire `ReviewContextService` into reviewer/card-show lifecycle so commitment occurs before answer outcome,
3. introduce a sparse Oracle cadence/frequency rule,
4. expose only neutral pre-answer Oracle presence (or intentionally expose nothing) per UX decision,
5. render post-answer Oracle reveal through the existing reviewer presentation path,
6. verify Expedition completion outranks Oracle reveal at the same boundary,
7. measure integrated reviewer P50/P95,
8. run real-host Undo/restart checks.

## Scope guard

No Rescue, Nemesis, Fragment, Relic, or Memory World lifecycle code is introduced by this slice.
