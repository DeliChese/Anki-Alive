# Phase 2 — Oracle Entry Plan

Status: READY FOR DESIGN/ARCHITECTURE START; FEATURE IMPLEMENTATION NOT STARTED
Prepared: 2026-08-19
Depends on: Phase 1 Expedition contracts and final visual sign-off issue #14

## Purpose

This document converts the Phase 2 spec and cross-phase audit into an implementation entry sequence. It is intentionally contract-first. Oracle's emotional value depends on the learner trusting that a prediction was genuinely committed before the review outcome was known.

## Phase 2 entry invariants

1. Prediction is durably fixed before the relevant review outcome is observable.
2. Card-specific Oracle identity remains hidden until after grading.
3. Again means recall failure; Hard/Good/Easy mean recall success for Oracle competition only. No higher grade earns extra reward.
4. Expedition remains the session owner.
5. Oracle does not modify Anki scheduling.
6. Undo/reversal reuses the normalized review identity and reconciliation path established in Phase 0/1.
7. EventOrchestrator owns reveal ordering and deferral.
8. Oracle persistence starts from schema v3 and preserves all Expedition history.
9. Memory inputs are feature-neutral facts; do not put `is_oracle_target` or equivalent feature policy into the Memory Engine.
10. Focus Mode and Reduced Motion change presentation only, never commitments/results.

## Recommended implementation order

### P2-0 — Close predecessor sign-off

- Run GitHub issue #14 on real desktop Anki.
- Update `docs/PHASE1_MANUAL_VALIDATION.md` and the Phase 1 handoff from PARTIAL to COMPLETE only after direct evidence exists.
- Do not block architecture/spec work for Oracle while this visual-only check is pending, but do not erase the gate.

### P2-1 — Lock Memory Engine v1 contract

Define a feature-neutral `MemorySnapshot` (exact naming may vary) that can be populated from host/FSRS-accessible facts without Oracle semantics.

Minimum candidate fields to evaluate:

```text
card_id
stability?
difficulty?
retrievability?
interval_days
lapses
review_count
recent_outcomes
observed_at
```

Required properties:

- missing metrics are representable;
- snapshot timing is explicit;
- no outcome leakage from the review being predicted;
- no feature-specific classification.

Deliverables:

- interface/types;
- host adapter boundary;
- tests using deterministic fixtures;
- architecture/data-model update if the final contract differs from current docs.

### P2-2 — Define commitment boundary and identity

Prefer commitment at Expedition start unless host evidence proves this is unreliable.

A committed prediction must include enough immutable evidence to prove/reconstruct what was fixed:

```text
oracle_prediction_id
expedition_id
card_id
committed_at
policy_version
predicted_recall_probability? / predicted_outcome
seed/model metadata as needed
status
```

Rules:

- commitment write completes before any matching review can resolve it;
- reload/cross-day resume does not reroll;
- one committed prediction cannot resolve twice;
- unresolved predictions end/expire with their Expedition unless an ADR changes this.

### P2-3 — Add schema v4 migration

Expected new table: `oracle_predictions`.

Migration tests must cover:

- fresh install → latest;
- schema v3 (Phase 1) → v4;
- existing Expedition/checkpoint/review-observation/presentation data preserved;
- reopen after migration;
- migration failure does not silently destroy prior data.

Do not add broad future-feature tables in the Oracle migration.

### P2-4 — Oracle repository/service without UI

Repository responsibilities should stay narrow:

- commit prediction;
- get hidden prediction(s);
- get prediction for card;
- resolve prediction idempotently;
- reverse/invalidate;
- list session results/history summary.

Service responsibilities:

- candidate scoring policy;
- commitment selection;
- resolution mapping;
- explanation data;
- session/lifetime summary.

Keep prediction formula behind a policy version so tuning does not reinterpret old history.

### P2-5 — Reconciliation and duplicate protection first

Before visual reveal work, prove:

- one accepted matching review resolves once;
- duplicate hook delivery does not double-resolve;
- review Undo reverses the Oracle result/session score;
- re-answer resolves from the fresh source review identity;
- non-review Undo creates no false reversal;
- deleted/unavailable cards invalidate safely.

Oracle must consume the established review normalization/reconciliation infrastructure rather than adding a second Undo system.

### P2-6 — Integrate with Expedition lifecycle

At minimum:

```text
ExpeditionStarted -> commit predictions
Review accepted -> resolve matching hidden prediction
Expedition completion/end -> expire/archive unresolved predictions
Cross-day resume -> keep commitments fixed
```

Avoid coupling Oracle candidate policy to Expedition UI classes.

### P2-7 — Presentation/EventOrchestrator integration

Introduce a real Oracle presentation candidate only after domain resolution is correct.

Required first rule:

- Expedition completion/final closure remains dominant when it coincides with Oracle resolution.

Prefer deferring or composing Oracle into the closure surface rather than showing competing major overlays.

Do not create a feature-local priority table.

### P2-8 — Oracle UI

Pre-answer:

- session-level count such as `N predictions locked` may be visible;
- card identity/probability/difficulty must remain hidden.

Post-answer:

- concise reveal;
- clear remembered/missed result;
- optional estimated probability/explanation using calibrated language;
- no extra points for Good/Easy versus Hard;
- keyboard dismissal and predictable return to reviewer;
- compact Focus Mode version;
- static/fade Reduced Motion version.

### P2-9 — Performance and trust instrumentation

Measure cumulative reviewer impact, not only isolated Oracle code.

Track at least:

- candidate/commit planning cost outside the hot path;
- matching + resolution cost on accepted review;
- Undo reconciliation cost;
- presentation enqueue cost;
- DB write cost as part of the integrated path.

Add local aggregate calibration diagnostics only if they can be stored without retaining card content unnecessarily.

## First test matrix

### Domain/repository

- commit is immutable for a prediction ID;
- commit survives reopen;
- no late outcome data enters commitment;
- resolve Again -> Oracle correct;
- resolve Hard/Good/Easy -> player defeats prediction;
- duplicate resolve is idempotent;
- reverse resolved review -> score/history reconciles;
- expire unresolved on Expedition end;
- cross-day resume does not reroll;
- card deletion invalidates safely.

### Migration

- fresh -> v4;
- v3 -> v4 with representative Phase 1 history;
- failed migration rollback behavior.

### Integration

- Expedition start commits bounded number of predictions;
- only cards in committed set resolve Oracle;
- pre-answer UI never exposes target identity;
- completion + Oracle same boundary follows EventOrchestrator precedence;
- Focus Mode does not change result;
- Reduced Motion does not change result;
- ordinary review remains possible with Oracle disabled/unavailable.

## Decisions to make before candidate-policy tuning

- exact `MemorySnapshot` host fields available on supported Anki versions;
- whether commitment at Expedition start can reliably target cards that will actually appear;
- behavior when committed cards do not appear before Expedition end;
- exact policy-version format;
- minimum history required before a card is eligible;
- initial prediction density and confidence threshold;
- explanation wording and which raw metrics are safe/useful to expose.

## Non-goals for the first Oracle slice

Do not add:

- Rescue/Nemesis/Fragment/Relic logic;
- cloud inference;
- generic AI chat behavior;
- XP/currency/streaks;
- distance-to-next-Oracle teasers by default;
- aggressive probability claims;
- speculative generalized event compression beyond the real Expedition + Oracle case.

## Definition of ready-to-code

Oracle feature implementation can begin when these four contracts are written and testable:

1. Memory Engine v1 input snapshot;
2. commitment timing/identity;
3. schema v4 `oracle_predictions` migration shape;
4. resolution/Undo/EventOrchestrator sequence.

The safest first code PR should be mostly domain + persistence + tests, with minimal or no user-facing Oracle reveal UI.