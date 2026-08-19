# Phase 1 — Expedition Handoff

## Status

PARTIAL — implementation and core host gates are complete; final visual host sign-off remains in #14.

Completed on: 2026-08-19 (implementation/core host gates)
Add-on version: repository main snapshot at `f34662e`
Schema version: 3
Target Anki host validated: real desktop Anki on Windows; ordinary deck review path

---

## 1. Scope Completed

- Durable Expedition session ownership and lifecycle.
- Fixed target and deterministic checkpoint plan.
- Review progress for accepted Again/Hard/Good/Easy grades without grade-based reward differences.
- Duplicate review protection and Undo reconciliation.
- Pause/resume and restart recovery.
- Pending completion reconstruction across restart and clean `Done` closure.
- Queue-exhaustion domain behavior preserving the original target.
- Dedicated `Anki Alive · Today` window that coexists with the existing Deck Browser appearance add-on.
- Quiet reviewer progress presentation.
- EventOrchestrator/presentation-event foundation with completion taking precedence over a final checkpoint.
- Focus Mode, Reduced Motion and keyboard-accessible Today controls.
- Reviewer hot-path performance measurement/reporting.
- Phase 1 architecture/data/backlog/decision synchronization.

## 2. Scope Not Completed

Two manual visual checks from the original Phase 1 validation gate still need direct real-host evidence:

- light appearance for the dedicated Today surface;
- substantially narrowed Today window with no clipped core controls or horizontal overflow.

Tracked in GitHub issue #14. Do not infer PASS from automated tests.

Explicitly unclaimed compatibility areas, not ordinary-deck Phase 1 blockers:

- filtered-deck behavior;
- custom-study behavior;
- naturally occurring queue exhaustion before target;
- real-host intermediate checkpoint presentation forced solely for validation.

## 3. Implementation Summary

Expedition is the canonical durable session owner. It frames normal Anki review as a bounded route without changing scheduling. Accepted review actions advance the route one unit regardless of rating, so Expedition measures completed work rather than memory quality.

The host integration normalizes accepted review identity and Undo events, allowing Expedition progress to be idempotent and reversible. Completion is persisted and presented through the shared presentation layer rather than inferred only from transient UI state.

The Today experience moved to a dedicated modeless AnkiWebView so Anki Alive no longer replaces or restyles Deck Browser content. The retained/prewarmed WebView path materially improved ordinary reopen latency on the real host.

## 4. Architecture Changes

- Expedition is durable session state owner; runtime coordination does not duplicate that state.
- Shared presentation/EventOrchestrator foundation exists before Oracle.
- Review observations carry source review identity where available and are reversible.
- UI reads/writes through services/repositories; it does not own scheduling or direct SQL.
- Completion and checkpoint prominence are centralized rather than encoded as competing feature popups.

## 5. Data / Schema Changes

Current `SCHEMA_VERSION = 3`.

Phase 1 introduced:

- `expeditions`
- `expedition_checkpoints`
- `expedition_review_observations`
- `presentation_events`

Phase 2 must add a forward migration from this schema without rewriting Expedition history.

## 6. UI / UX Changes

- Dedicated `Anki Alive · Today` window.
- Begin/resume/end/completion flows.
- Quiet reviewer Expedition progress strip.
- Checkpoint and completion presentation through shared orchestration.
- Focus Mode reduces presentation intensity without changing domain behavior.
- Reduced Motion keeps state legible without travel animation.
- `Done` is a real stopping point; no automatic new Expedition is created.

## 7. Tests Run

### Automated evidence already recorded in repository

Regression coverage includes:

- duplicate delivery/idempotence;
- Undo reconciliation and re-answer;
- pause/restart recovery;
- pending completion reconstruction after restart;
- intermediate checkpoint single emission;
- completion-over-final-checkpoint precedence;
- queue exhaustion preserving fixed target;
- Focus Mode/Reduced Motion/keyboard semantics;
- performance snapshot reporting.

Temporary Phase 1 CI probe PRs #2–#13 were used to verify several host-hardening and accessibility regressions. They were explicitly test-only and not product PRs.

### Manual real-host evidence

PASS recorded for:

- startup/coexistence;
- dedicated Today ordinary desktop presentation;
- active Expedition progress and clean completion;
- pause/resume/restart;
- Undo reconciliation;
- Focus Mode;
- Reduced Motion;
- tested keyboard path;
- reviewer hot-path performance.

See `docs/PHASE1_REAL_HOST_EVIDENCE.md` and `docs/PHASE1_PERFORMANCE_EVIDENCE.md`.

### Not Tested / Not Claimed

See section 2 and issue #14.

## 8. Performance Findings

Latest real-host snapshot recorded in repository:

```text
reviewer_did_answer_card:
  samples: 23
  min: 0.398 ms
  median/P50: 0.977 ms
  P95: 1.357 ms
  max: 1.739 ms

state_did_undo:
  samples: 3
  min: 0.913 ms
  median/P50: 1.444 ms
  P95: 1.454 ms
  max: 1.454 ms
```

This remains comfortably inside the Phase 0 cumulative synchronous reviewer budget.

## 9. Accessibility Findings

- Focus Mode preserves logic and numeric progress while reducing motivational presentation.
- Reduced Motion is exposed through an Anki Alive setting path and does not require travel animation to understand state.
- Tested Today controls use native keyboard/focus semantics; Escape hides Today without disrupting Anki.
- Remaining accessibility-adjacent visual sign-off is limited to the light-theme and narrow-window host checks in #14.

## 10. Files / Areas Most Relevant to Phase 1

- `anki_alive/expedition/`
- `anki_alive/integration/`
- `anki_alive/presentation.py`
- `anki_alive/storage.py`
- `anki_alive/ui/`
- `docs/phases/PHASE_1_EXPEDITION.md`
- `docs/PHASE1_REAL_HOST_EVIDENCE.md`
- `docs/PHASE1_MANUAL_VALIDATION.md`
- `docs/PHASE1_PERFORMANCE_EVIDENCE.md`
- `docs/06_DECISIONS.md`
- `docs/07_BACKLOG.md`

## 11. Decisions Accepted

Phase 1 close has already recorded the important host and presentation decisions in the canonical decisions document, including the dedicated Today/coexistence direction and shared presentation foundation.

Do not reintroduce Deck Browser ownership or per-feature presentation priority tables in Phase 2.

## 12. Known Issues

### KI-014 — Final visual host sign-off

Severity: LOW / release-quality gate
Impact: Phase 1 manual validation cannot honestly be marked fully complete until light appearance and narrow-window behavior are directly observed on the real host.
Workaround: ordinary dark desktop path is validated; run issue #14 checks before final Phase 1 sign-off.

## 13. Technical Debt

### TD-001 — Broader host-context compatibility evidence

Why deferred: ordinary-deck Phase 1 was the validated product path and unsafe collection mutation was avoided solely to manufacture edge cases.
Recommended future action: add filtered-deck/custom-study host smoke evidence when convenient, without coupling Oracle to those contexts prematurely.

### TD-002 — Cross-feature event compression

Why deferred: Phase 1 had only Expedition events, so a generic compression policy would be speculative.
Recommended future action: Phase 2 should introduce Oracle through the existing EventOrchestrator and add only the smallest real cross-feature merge/priority rule required by Expedition + Oracle.

## 14. Deferred Ideas

- BL-008 `One More to Closure` remains deliberately deferred.
- General cross-feature presentation compression work remains Phase 2+.
- No future-feature fake signal behavior was shipped in Expedition.

## 15. Next Phase Dependencies

Phase 2 Oracle may be designed/prepared now, but implementation should preserve these contracts:

- Expedition remains the session owner.
- Oracle prediction commitment is durably fixed before outcome is known.
- Oracle card identity stays hidden before grading.
- Review identity/Undo reconciliation is reused rather than reinvented.
- EventOrchestrator owns presentation ordering.
- Phase 2 migration starts from schema v3 and preserves Expedition history.
- The Memory Engine boundary must expose feature-neutral memory facts rather than Oracle-specific labels.

Issue #14 is the only outstanding Phase 1 manual sign-off task.

## 16. Next Agent Startup

Read in order:

1. `PROJECT.md` (note that its Current Status section is historically stale)
2. `docs/01_PRODUCT_PRINCIPLES.md`
3. `docs/03_ARCHITECTURE.md`
4. `docs/04_DATA_MODEL.md`
5. `docs/02_DESIGN_SYSTEM.md`
6. `docs/05_ROADMAP.md`
7. `docs/06_DECISIONS.md`
8. `docs/11_CROSS_PHASE_AUDIT.md`
9. this handoff
10. `docs/phases/PHASE_2_ORACLE.md`
11. `docs/PHASE2_ENTRY_PLAN.md`

Then inspect `anki_alive/expedition/`, `anki_alive/integration/`, `anki_alive/presentation.py`, `anki_alive/storage.py`, and the current tests before adding Oracle code.

Do not begin by selecting a prediction formula. First lock the Memory Engine input contract, commitment boundary, persistence migration, Undo semantics, and presentation integration.