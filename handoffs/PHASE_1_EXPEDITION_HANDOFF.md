# Phase 1 — Expedition Handoff

Status: ENGINEERING COMPLETE; FINAL HOST VISUAL GATE PENDING
Date: 2026-08-19
Phase: 1 — Expedition
Next phase: 2 — Oracle

## 1. Executive summary

Phase 1 has a coherent Expedition vertical slice in `main`: durable session ownership, review-driven progress, checkpoints, completion, pause/resume, restart recovery, Undo reconciliation, Focus Mode, Reduced Motion handling, Today/reviewer presentation, performance instrumentation, and the Phase 1 EventOrchestrator foundation.

Core real-host gates have passed and automated tests cover the remaining deterministic edge behavior. Two direct visual host spot-checks remain before the manual validation document can truthfully move from PENDING to PASS:

- light appearance in the dedicated Today window,
- substantially narrowed Today window with no clipped core controls or horizontal overflow.

Do not infer those two results. Record them in `docs/PHASE1_MANUAL_VALIDATION.md` when actually exercised.

## 2. Completed scope

### Expedition domain and persistence

- Expedition is the durable owner of session target, progress, checkpoint plan, lifecycle, and completion.
- Fixed targets are preserved instead of being silently rewritten when available work changes.
- Progress is tied to accepted review observations rather than grade quality.
- `Again`, `Hard`, `Good`, and `Easy` all contribute exactly one accepted review; no rating receives bonus progress.
- Duplicate review delivery is idempotent.
- Pause/resume and sidecar reopen preserve Expedition state.
- Completion can survive restart until explicitly dismissed.

### Undo / reconciliation

- Review Undo reconciles Expedition progress downward.
- Re-answering an undone card contributes once under the fresh review identity.
- Non-review Undo does not fabricate Expedition progress reversal.

### Presentation / UX

- Anki Alive Today is isolated in a dedicated window instead of replacing Deck Browser content.
- Reviewer presentation is intentionally quiet and leaves normal Anki grading controls authoritative.
- Completion has stronger prominence than a final checkpoint on the same boundary.
- `Done` creates a real stopping point and does not auto-create another Expedition.
- Focus Mode reduces motivational presentation while retaining necessary numeric progress.
- Reduced Motion preserves static meaning.
- Native/host review flow remains available when Today is hidden, no Expedition is active, an Expedition ends, or completion is dismissed.

### Shared architecture introduced in Phase 1

- `EventOrchestrator` and `PresentationEvent` exist as presentation scheduling primitives.
- Domain truth remains outside the orchestrator.
- At most one major/session-closure presentation is surfaced at a boundary; quieter events may coexist.
- Review-context aggregation direction is established for Phase 2/3.

## 3. Important implementation locations

- `anki_alive/expedition/model.py` — durable Expedition model/lifecycle.
- `anki_alive/expedition/repository.py` — Expedition persistence and review association.
- `anki_alive/expedition/service.py` — domain transitions and review-driven progress.
- `anki_alive/expedition/events.py` — Expedition domain events.
- `anki_alive/expedition/viewmodel.py` — presentation projection.
- `anki_alive/core/presentation.py` — `PresentationEvent`, prominence, and `EventOrchestrator`.
- `anki_alive/integration/reviewer.py` — normalized reviewer integration.
- `anki_alive/integration/expedition_ui.py` — Today/reviewer Expedition presentation integration.
- `anki_alive/integration/today_window.py` — dedicated Today host window.
- `anki_alive/core/reconciliation.py` — shared reconciliation seam.

## 4. Validation evidence

### Real host

Recorded core PASS evidence includes:

- startup and Deck Browser coexistence,
- dedicated Today window,
- active Expedition progress,
- completion and real stopping point,
- pause/resume/restart,
- pending-completion restart behavior,
- Undo correctness,
- Focus Mode,
- Reduced Motion,
- keyboard navigation for the tested Today flow,
- reviewer/Undo performance samples inside the established hot-path budget.

Canonical evidence: `docs/PHASE1_REAL_HOST_EVIDENCE.md` and `docs/PHASE1_PERFORMANCE_EVIDENCE.md`.

### Automated tests

Phase 1 regression suites include:

- `tests/test_phase1_expedition.py`
- `tests/test_phase1_undo_reconciliation.py`
- `tests/test_phase1_completion_restart.py`
- `tests/test_phase1_completion_freshness.py`
- `tests/test_phase1_presentation.py`
- `tests/test_phase1_accessibility.py`
- `tests/test_phase1_performance.py`
- `tests/test_phase1_host_hardening.py`

These cover checkpoint behavior, queue exhaustion semantics, duplicate delivery, persistence/reopen, presentation ordering, accessibility contracts, and performance-oriented paths.

## 5. Known limitations / unclaimed host contexts

The following are not claimed from the ordinary-deck real-host run:

- filtered deck behavior as a separately validated host path,
- custom study behavior as a separately validated host path,
- naturally occurring queue exhaustion before target in the user's collection,
- a forced real-host intermediate checkpoint solely for validation.

These are documented limitations, not reasons to mutate a collection unsafely.

## 6. Final Phase 1 close gate

Before changing `docs/PHASE1_MANUAL_VALIDATION.md` to PASS, directly exercise and record:

1. light appearance in `Anki Alive · Today`,
2. substantially narrowed Today window with no persistent horizontal overflow or clipped core controls.

If either fails, treat it as a Phase 1 UX defect and fix it before declaring the phase fully closed.

## 7. Decisions carried forward

- Anki remains authoritative for scheduling, cards, notes, review history, and grading semantics.
- Expedition is the durable study-session owner.
- Presentation scheduling is separate from domain truth.
- Completion is a real stopping point; no automatic infinite engagement loop.
- No reward is attached to arbitrary `Good`/`Easy` presses.
- Future feature presentation must integrate through shared orchestration rather than isolated mini-app behavior.
- Cross-feature event compression remains deferred until Phase 2 provides a second real feature event to orchestrate.

## 8. Deferred ideas / technical debt

- “One more to closure” remains deliberately deferred pending UX evidence; do not add it automatically.
- General cross-feature presentation compression is Phase 2+ work.
- Filtered deck/custom study support should be validated when practical without unsafe collection manipulation.
- ReviewContextService should be introduced in Phase 2 rather than allowing per-feature hot-path lookups to proliferate.

## 9. Migration notes

No new migration is introduced by this handoff.

Phase 2 must preserve existing Expedition rows and review associations. Oracle must not require rewriting Expedition history or changing Anki collection schema.

## 10. Phase 2 dependencies

Oracle may rely on the following Phase 1 contracts:

- normalized review observations and source review identity,
- shared EventBus/reconciliation seams,
- EventOrchestrator presentation boundary,
- Expedition session ownership,
- existing Focus Mode / Reduced Motion presentation policies,
- sidecar SQLite persistence conventions,
- reviewer performance instrumentation.

Oracle must add or formalize:

- a feature-neutral Memory Engine interface,
- ReviewContextService or equivalent aggregation for reviewer-time reads,
- durable pre-answer prediction commitment,
- deterministic/persisted commitment identity,
- post-answer reveal only,
- Undo/reversal behavior for committed/revealed predictions,
- crash/restart-safe deferred presentation if the final design requires deferred reveal.

## 11. Phase 2 entry rule

Phase 2 specification and architecture work may begin immediately from this handoff.

Phase 2 implementation should not be considered formally entered until the two remaining Phase 1 visual host spot-checks are recorded as PASS (or a documented decision explicitly accepts a limitation).

The core invariant remains:

> Oracle may create curiosity, but it must never reveal answer information before recall or bias the learner toward a grading button.
