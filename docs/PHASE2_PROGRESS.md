# Phase 2 — Oracle Progress

Status: LIVE REVIEWER INTEGRATION — VISIBILITY HARDENED
Date: 2026-08-19

## Slice 1 — commitment lifecycle foundation

Implemented on `main`:

- feature-neutral `MemorySnapshot` / `MemoryEngine` contract,
- `ReviewContextService` aggregation seam,
- sidecar schema migration from v3 to v4,
- durable `oracle_predictions` table,
- Oracle domain model and deterministic policy,
- persisted pre-answer commitment identity,
- duplicate commitment suppression for the same Expedition/card,
- accepted-review resolution with explicit recall mapping (`Again` = failed recall; non-`Again` = recalled),
- repository guard rejecting outcomes timestamped before commitment,
- durable post-answer `oracle_resolution` presentation event,
- in-memory `EventOrchestrator` integration for the domain slice,
- Undo reconciliation that reopens the original commitment instead of rerolling it,
- invalidation of stale pending Oracle reveal after Undo,
- re-answer resolution using the same Oracle commitment.

## Slice 2 — live Anki reviewer integration

Implemented on `main`:

- `AnkiMemoryEngine` reads current host card memory facts at the integration boundary,
- stability/difficulty come from Anki `Card.memory_state` when available,
- retrievability is derived from Anki's persisted stability, `last_review_time`, and `decay` using the FSRS forgetting curve,
- interval, lapses, review count, and a bounded recent rating history are normalized into `MemorySnapshot`,
- `gui_hooks.reviewer_did_show_question(card)` is the commitment trigger, guaranteeing commitment before an accepted answer outcome,
- `ReviewContextService` aggregates active Expedition + MemorySnapshot on the question boundary,
- accepted `ReviewObservation` resolves the existing commitment and creates durable reveal state,
- post-answer reveal is a small, non-interactive reviewer status surface,
- Focus Mode suppresses Oracle presentation while preserving domain truth,
- Reduced Motion removes reveal transition dependence,
- Expedition completion wins over competing Oracle presentation.

## Visibility/compatibility hardening

Real-host feedback exposed an important problem: the initial integration could look identical to Phase 1 because Oracle showed nothing before answer, required FSRS retrievability, and only attempted exact progress boundaries.

The current `main` fixes that gap:

- policy v2 still prefers FSRS retrievability when available,
- non-FSRS cards with enough bounded review history can receive a deterministic prediction without a fabricated probability,
- cards with neither usable FSRS state nor usable review history remain safely skipped,
- Oracle now uses the first eligible card in each five-review progress window instead of wasting the window when its first card is ineligible,
- a committed card shows a neutral `Oracle · Prediction sealed. Reveal after your answer.` cue on the question side,
- the neutral cue exposes no predicted outcome, probability, confidence, grade guidance, or answer-bearing content,
- after grading, that same surface changes to the Oracle result and then clears automatically.

## Current policy v2

- minimum 3 prior reviews,
- when normalized retrievability exists: below `0.75` predicts `FAIL`, otherwise `RECALL`,
- when retrievability is unavailable: recent review history may provide a deterministic fallback,
- fallback predicts `FAIL` when the latest accepted review was `Again` or at least two of the bounded recent ratings are `Again`; otherwise it predicts `RECALL`,
- fallback persists no probability,
- one commitment is allowed per five-review Expedition progress window, using the first eligible card,
- `Again` maps to failed recall; `Hard`/`Good`/`Easy` map to recalled for Oracle resolution.

This policy remains provisional and must be validated against real-host behavior before Phase 2 close.

## Validation status

Regression coverage now includes:

- `tests/test_phase2_oracle.py`
- `tests/test_phase2_memory_integration.py`
- `tests/test_phase2_oracle_ui.py`
- `tests/test_phase2_oracle_visibility.py`

The current agent environment has **not executed the suite**. The repository also exposes no CI status for the latest direct-to-main commits. Do not infer a passing run from test-file existence.

## What should now be visibly different from Phase 1

During an active Expedition, the first eligible reviewed card in an Oracle cadence window should show a small cyan-accent reviewer status:

```text
ORACLE
Prediction sealed. Reveal after your answer.
```

After the accepted grade, the surface changes to the Oracle result for a few seconds. Cards without enough memory evidence remain visually unchanged by design.

## Next validation slice

1. sync latest `main` and restart Anki so updated Python/JS/CSS is loaded,
2. use a deck with cards that have at least 3 prior reviews; FSRS is preferred but no longer required,
3. start a fresh Expedition and confirm the neutral Oracle cue appears on the first eligible card,
4. verify result appears only after grading,
5. verify Focus Mode suppresses cue/reveal,
6. verify Undo reopens the same commitment and re-answer resolves once,
7. verify Expedition completion outranks Oracle reveal,
8. capture integrated reviewer performance evidence.

## Scope guard

No Rescue, Nemesis, Fragment, Relic, or Memory World lifecycle code is introduced by these slices.
