# Phase 2 — Oracle Progress

Status: LIVE REVIEWER INTEGRATION — RUNTIME VISIBILITY HARDENED
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
- Undo reconciliation that reopens the original commitment instead of rerolling it,
- invalidation of stale pending Oracle reveal after Undo,
- re-answer resolution using the same Oracle commitment.

## Slice 2 — live Anki reviewer integration

Implemented on `main`:

- `AnkiMemoryEngine` reads current host card memory facts at the integration boundary,
- FSRS retrievability is used when available,
- bounded recent review history is available as a non-FSRS fallback,
- `gui_hooks.reviewer_did_show_question(card)` is the commitment trigger,
- accepted `ReviewObservation` resolves the existing commitment and creates durable reveal state,
- post-answer reveal is small and non-interactive,
- Focus Mode suppresses presentation while preserving domain truth,
- Reduced Motion removes reveal transition dependence,
- Expedition completion wins over competing Oracle presentation.

## Visibility / compatibility hardening

Real-host feedback showed that the first live integration could appear identical to Phase 1. Two separate causes were addressed.

### Candidate visibility

- policy v2 still prefers FSRS retrievability,
- non-FSRS cards with enough review history can receive a deterministic prediction without a fabricated probability,
- the first eligible card in each five-review progress window may be selected,
- committed cards show only the neutral pre-answer cue `Prediction sealed. Reveal after your answer.`,
- no predicted outcome, probability, confidence, grading advice, or answer-bearing content is exposed before grading.

### Silent runtime hardening

A second real-host report showed no Oracle UI at all. The reviewer runtime previously depended on receiving `collection_did_load`; if registration happened after that host event, Oracle context could remain `None` and every question would silently return.

Current `main` now:

- eagerly initializes from `mw.col` when the collection already exists,
- lazily re-initializes from `mw.col` on question display if required,
- records explicit skip/error reasons in diagnostics rather than only returning silently,
- restores the neutral cue from an existing unresolved commitment after reload/restart/Undo without rerolling it,
- shows a tiny `Oracle online` status beside the Expedition reviewer strip whenever the Phase 2 reviewer assets/runtime are present for an active Expedition.

The `Oracle online` marker is not a prediction and carries no memory outcome information. It exists so host validation can distinguish UI/bootstrap failure from candidate-policy ineligibility.

## Current policy v2

- minimum 3 prior reviews,
- retrievability below `0.75` predicts `FAIL`, otherwise `RECALL`, when retrievability exists,
- without retrievability, recent review history may provide a deterministic fallback,
- fallback predicts `FAIL` when the latest review was `Again` or at least two bounded recent ratings are `Again`; otherwise it predicts `RECALL`,
- fallback persists no fabricated probability,
- one commitment is allowed per five-review Expedition progress window,
- `Again` maps to failed recall; `Hard`/`Good`/`Easy` map to recalled for Oracle resolution.

## Validation status

Regression coverage now includes:

- `tests/test_phase2_oracle.py`
- `tests/test_phase2_memory_integration.py`
- `tests/test_phase2_oracle_ui.py`
- `tests/test_phase2_oracle_visibility.py`
- `tests/test_phase2_oracle_runtime_hardening.py`

The current agent environment has **not executed the suite**. The repository also exposes no CI status for direct-to-main commits, so no passing run is claimed here.

## What should now be visibly different from Phase 1

During any active Expedition reviewer session, a small cyan-accent status should be visible near the Expedition strip:

```text
Oracle online
```

That marker should appear even when the current card is not Oracle-eligible.

When an eligible card has a durable commitment, a separate cue should appear:

```text
ORACLE
Prediction sealed. Reveal after your answer.
```

After the accepted grade, the cue changes to the Oracle result and then clears automatically.

## Next host validation

1. sync latest `main`,
2. fully exit and restart Anki,
3. start/resume an Expedition,
4. first confirm `Oracle online` appears next to the Expedition reviewer strip,
5. then review cards with prior history and look for `Prediction sealed`,
6. verify reveal occurs only after grading,
7. verify Focus Mode, Undo/re-answer, completion precedence, and reviewer performance.

## Scope guard

No Rescue, Nemesis, Fragment, Relic, or Memory World lifecycle code is introduced by these slices.
