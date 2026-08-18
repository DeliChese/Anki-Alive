# PHASE_0_FOUNDATION.md

# Anki Alive — Phase 0: Foundation

## 1. Phase Goal

Build the smallest technical foundation strong enough for every later mechanic to remain honest, fast, testable, and durable.

Phase 0 proves that Anki Alive can safely observe accepted reviews, persist owned state, reconcile review reversals, expose shared settings/Focus Mode, and measure reviewer cost without slowing study.

---

## 2. Status

```text
Status: COMPLETE
Phase: 0
Name: Foundation
Depends on: Starter Packs + Cross-Phase Audit
Next: Phase 1 — Expedition
```

Implementation is tracked in PR #1 on `phase-0/foundation`.

Real-host validation completed on Anki 25.09.4 / Python 3.13.5 / Windows 11. Phase 1 durable Expedition work is no longer blocked by the Phase 0 review/reversal foundation.

---

## 3. Locked Phase 0 Contracts

### Review Observation

Accepted grade notification:

`gui_hooks.reviewer_did_answer_card`

Source identity:

`Anki revlog.id`

Normalized add-on identity:

`UUID(profile_key, revlog.id)`

### Undo / Reversal

`gui_hooks.state_did_undo` is a reconciliation trigger only.

A `ReviewReversed` event is emitted only when a previously observed source `revlog.id` is verified to have disappeared.

Undoing a non-review operation must not emit a false review reversal. This behavior passed real-host validation.

### Session Ownership

```text
Expedition = future durable session truth
SessionCoordinator = runtime coordination only
```

### Persistence

Initial durable tables remain only:

```text
schema_meta
migration_history
```

No feature tables are pre-created in Phase 0.

### Profile Identity

Anki Alive owns a UUID stored in the active profile folder. Display name is not durable identity.

---

## 4. Foundation Implemented

- host-agnostic core package
- synchronous EventBus
- normalized ReviewObservation / ReviewReversed
- deterministic source identity
- shared reconciliation proof
- injectable clock, IDs, UTC timestamps, local study day
- typed SettingsService
- central FocusPolicy
- native Anki add-on config adapter
- sidecar SQLite schema/version/migrations
- WAL, transactions, integrity check, online backup, checkpoint-on-close
- privacy-safe structured diagnostics
- official Anki add-on logger integration
- PerformanceTimer
- concrete real Anki hook wiring
- packaged bootstrap and compatibility metadata
- semantic UI CSS foundation
- visible focus, reduced motion, non-color status semantics
- Windows linked-development helper
- CI on Python 3.9 and Python 3.13

---

## 5. Compatibility

Compatibility floor:

**Anki 25.02.7 (`250207`)**

Evidence:

- required modern GUI hooks exist in upstream 25.02.7 source
- CI covers Python 3.9 and 3.13
- real desktop host validation passed on Anki 25.09.4 with Python 3.13.5

The compatibility floor is a supported policy floor, not a claim that every intermediate Anki release has been manually tested.

---

## 6. Real Host Validation

Validated host:

- Anki 25.09.4 (d52ca669)
- Python 3.13.5
- Qt 6.9.1
- PyQt 6.9.1
- Windows 11 10.0.26200

Passed:

- add-on startup
- database integrity at bootstrap
- ratings 1 / 2 / 3 / 4 normalize correctly
- exactly one normalized observation per accepted review in the tested sequence
- accepted review source identity resolves to `revlog.id`
- review Undo produces matching ReviewReversed
- re-answer after Undo creates a new source review identity
- non-review Undo emits no false ReviewReversed
- restart bootstrap succeeds

---

## 7. Reviewer Performance Baseline

Synchronous budget:

```text
Preferred < 5 ms
Typical < 10 ms
P95 < 20 ms
```

Real accepted-review samples: 12.

`reviewer_did_answer_card`:

- min 0.350 ms
- P50 approximately 0.397 ms
- P95 approximately 0.604 ms
- max 0.669 ms

Observed `state_did_undo` samples ranged from 0.180 ms to 0.511 ms.

Result: PASS with substantial headroom.

Future phases must treat this as a baseline and preserve cumulative reviewer latency discipline.

---

## 8. Technical Questions Status

### Q0-01 — Minimum Supported Anki Version
RESOLVED: Anki 25.02.7 (`250207`) compatibility floor.

### Q0-02 — Review Hook Mapping
RESOLVED: `reviewer_did_answer_card`.

### Q0-03 — Undo/Reversal Identity
RESOLVED: `state_did_undo` triggers reconciliation; verified revlog disappearance proves reversal.

### Q0-04 — Frontend Stack
RESOLVED FOR PHASE 0: host-compatible HTML/CSS primitives, no framework.

### Q0-05 — SQLite Strategy
RESOLVED: WAL + timeout + transactions + integrity + online backup + checkpoint-on-close.

### Q0-06 — Profile Identity
RESOLVED: add-on-owned UUID inside profile folder.

### Q0-07 — FSRS/Memory State Access
INTENTIONALLY DEFERRED to Memory Engine work. Phase 0 does not implement feature-specific FSRS policy.

### Q0-08 — Safe Background Work
INTENTIONALLY DEFERRED until a feature actually requires asynchronous host-data work. Phase 0 introduces no background host-data access.

---

## 9. Definition of Done

- [x] repository implementation structure exists
- [x] bootstrap is safe/idempotent
- [x] integration boundary exists
- [x] EventBus exists
- [x] normalized ReviewObservation exists
- [x] undo/reversal mapping is documented and host-validated
- [x] reconciliation foundation is proven
- [x] clock/IDs/local study day exist
- [x] settings service exists
- [x] Focus Policy exists
- [x] sidecar DB exists
- [x] schema version/migrations work
- [x] profile identity strategy is resolved
- [x] logs avoid card content by default
- [x] timing instrumentation exists
- [x] reviewer baseline is measured in real Anki
- [x] UI tokens/reduced motion/focus baseline exist
- [x] test harness works in GitHub Actions
- [x] manual Anki smoke test is completed
- [x] architecture/data/ADRs reflect implementation direction
- [x] final `PHASE_0_FOUNDATION_HANDOFF.md` is COMPLETE

---

## 10. Phase 1 Entry Contract

Phase 1 may rely on:

- stable bootstrap
- stable profile scoping
- normalized review events
- proven reversal/reconciliation path
- persistence/migrations
- settings/FocusPolicy
- reviewer performance baseline
- EventOrchestrator-ready architecture direction

---

# Phase 0 North Star

> **Before we gamify a single review, prove that we can observe, persist, reverse, and present review-derived state without lying to the learner or slowing Anki down.**
