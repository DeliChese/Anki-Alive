# PHASE_0_FOUNDATION.md

# Anki Alive — Phase 0: Foundation

## 1. Phase Goal

Build the smallest technical foundation strong enough for every later mechanic to remain honest, fast, testable, and durable.

Phase 0 is complete only when the project can safely observe Anki review flow, persist owned state, reconcile review reversals in a documented way, expose shared settings/Focus Mode, and measure its own reviewer cost.

---

## 2. Status

```text
Status: IN PROGRESS — REAL ANKI HOST VALIDATION PENDING
Phase: 0
Name: Foundation
Depends on: Starter Packs + Cross-Phase Audit
Next: Phase 1 — Expedition
```

Current implementation is tracked in Draft PR #1 on `phase-0/foundation`.

Automated foundation tests pass in GitHub Actions. Phase 1 durable review-derived progress remains blocked until the manual real-Anki review/undo test and reviewer timing validation are completed.

---

## 3. Audit-Derived Critical Additions

Cross-phase audit identified the following as mandatory Phase 0 concerns:

1. normalized review observation identity,
2. undo/reversal mapping,
3. shared reconciliation foundation,
4. Expedition as future durable session owner,
5. EventOrchestrator seam,
6. Memory Engine seam,
7. HistoryService seam,
8. review-context aggregation direction,
9. cumulative reviewer performance discipline,
10. profile scoping.

---

## 4. In Scope

### Repository Bootstrap

Create minimal implementation structure.

### Safe Add-on Bootstrap

- initialize once,
- load settings,
- initialize storage,
- run migrations,
- register hooks,
- initialize services,
- fail gracefully.

### Integration Layer

Create adapters for:

- lifecycle,
- reviewer,
- collection,
- webview,
- compatibility.

### EventBus

Create small in-process event system.

### Review Observation Normalization

Normalize accepted review actions into internal events.

Conceptual:

```text
ReviewObservation
ReviewReversed
```

Exact fields depend on host validation.

### Reconciliation Foundation

Create architecture for review-derived state to be re-evaluated after undo/reversal.

Phase 0 need not implement future feature reconciliation, but must prove the base mechanism.

### Clock / IDs / Study Day

- injectable clock,
- add-on-owned IDs,
- UTC timestamps,
- explicit local study day.

### Settings

Categories:

```text
appearance
motion
focus_mode
diagnostics
feature_flags
```

### Focus Mode

Create central `FocusPolicy`, not feature-specific booleans.

### Persistence

- sidecar SQLite,
- schema version,
- ordered migrations,
- safe open/close,
- transactions,
- error handling.

### Diagnostics

Structured logging without full card content.

### Performance Timing

Measure bootstrap, hooks, storage, bridge.

### UI Foundation

- design tokens,
- typography/spacing/surface roles,
- reduced motion,
- focus styles,
- base bridge if used.

### Test Harness

Cover core primitives, persistence, settings, focus policy, hook registration, normalized review observations, and reconciliation foundation.

---

## 5. Explicitly Out of Scope

Do not implement:

- Expedition gameplay,
- Oracle,
- Rescue,
- Nemesis,
- Fragments,
- Relics,
- Memory World,
- full HistoryService tables,
- full EventOrchestrator behavior,
- feature-specific Memory Engine policy.

Phase 0 creates seams, not speculative feature code.

---

## 6. Canonical Session Ownership

Phase 0 may introduce a runtime `SessionCoordinator`.

It must not become the durable study-session owner.

Locked future contract:

```text
Expedition = durable session truth
SessionCoordinator = runtime coordination
```

---

## 7. Review Observation Blocker

Source validation has resolved the intended mapping:

- accepted grade notification: `gui_hooks.reviewer_did_answer_card`,
- source review identity: Anki `revlog.id`,
- deterministic add-on observation identity: `(profile_key, revlog.id)`,
- undo notification: `gui_hooks.state_did_undo`,
- reversal proof: tracked revlog row disappears after undo.

Fake-host integration tests cover this path. Real Anki confirmation remains mandatory before Phase 1 durable progress is allowed.

---

## 8. Reconciliation Proof

Phase 0 demonstrates a safe reversible test projection:

```text
accepted review
→ derived counter/state changes
→ undo/reversal
→ derived state returns to correct value
```

The implementation is deliberately test-only foundation state, not future gameplay state.

---

## 9. Persistence Foundation

Initial durable tables:

```text
schema_meta
migration_history
```

Do not pre-create feature tables.

Sidecar database strategy is now:

- WAL,
- foreign keys,
- 5-second busy timeout,
- explicit transactions,
- integrity check,
- online backup API,
- WAL checkpoint on close,
- storage under `user_files`.

---

## 10. Shared Service Seams

Phase 0 maintains clean future seams for:

```text
EventOrchestrator
MemoryEngine
HistoryService
ReviewContextService
ReviewTransactionCoordinator
ProjectionService
```

Do not instantiate unnecessary complexity yet.

---

## 11. Profile Identity

Resolved strategy:

- create an Anki Alive owned UUID inside the active profile folder,
- do not use display name as identity,
- allow profile-folder rename to carry the identity with it,
- include profile key when deriving normalized review identity.

---

## 12. Reviewer Performance

Provisional synchronous reviewer budget:

```text
Preferred < 5 ms
Typical < 10 ms
P95 < 20 ms
```

`PerformanceTimer` now wraps the concrete accepted-review and undo hook paths. Real-host diagnostics will provide the Phase 0 baseline.

Future features must prefer aggregated context and coordinated writes over per-feature hot-path I/O.

---

## 13. UI / Focus Foundation

Focus Policy supports:

```text
allow_major_reveal
allow_minor_reveal
allow_ambient_motion
show_compact_progress
defer_nonessential_events
```

Semantic CSS tokens, visible focus, Focus Mode presentation rules, and reduced-motion rules exist. No frontend framework is introduced in Phase 0.

---

## 14. Accessibility Baseline

Required and represented in the Phase 0 foundation:

- keyboard-friendly controls,
- visible focus,
- reduced motion,
- non-color semantics,
- readable contrast roles,
- scalable text direction.

Real feature screens will receive feature-specific accessibility validation in later phases.

---

## 15. Technical Questions Status

### Q0-01 — Minimum Supported Anki Version
RESOLVED PROVISIONALLY: Anki 25.02.7 (`250207`) or newer. Real-host confirmation pending.

### Q0-02 — Review Hook Mapping
RESOLVED IN SOURCE + AUTOMATED INTEGRATION TEST: `reviewer_did_answer_card`.

### Q0-03 — Undo/Reversal Identity
RESOLVED IN SOURCE + AUTOMATED INTEGRATION TEST: `state_did_undo` triggers reconciliation; reversal requires verified revlog disappearance. Real-host confirmation pending.

### Q0-04 — Frontend Stack
RESOLVED FOR PHASE 0: host-compatible HTML/CSS primitives, no framework yet.

### Q0-05 — SQLite Strategy
RESOLVED AND AUTOMATED-TESTED: WAL + timeout + integrity + online backup + checkpoint-on-close.

### Q0-06 — Profile Identity
RESOLVED AND AUTOMATED-TESTED: add-on UUID inside profile folder.

### Q0-07 — FSRS/Memory State Access
DEFERRED INTERFACE VALIDATION TO MEMORY ENGINE WORK. No feature-specific FSRS logic belongs in Phase 0.

### Q0-08 — Safe Background Work
NO BACKGROUND HOST-DATA WORK INTRODUCED IN PHASE 0. Validate before later asynchronous host access.

---

## 16. Testing Deliverables

### Core

- EventBus
- clock
- IDs
- local study day
- Focus Policy

### Settings

- defaults
- load/save
- invalid values
- unknown keys
- Anki add-on config adapter

### Persistence

- fresh DB
- reopen
- migration state
- rollback
- schema version
- WAL
- busy timeout
- integrity check
- backup

### Integration

- idempotent hook registration
- normalized review observation
- duplicate protection
- collection/profile lifecycle
- revlog-backed reversal verification
- packaged compatibility metadata

### Reconciliation

- accepted review → derived state
- reversal → correct re-evaluation

### Performance

- named timing samples in automated tests
- concrete review/undo hooks instrumented for real-host measurement

---

## 17. Manual Anki Validation

Canonical checklist: `docs/PHASE0_MANUAL_VALIDATION.md`.

Minimum real-host sequence:

```text
1. Load add-on.
2. Open profile/collection.
3. Review honestly across normal answer buttons.
4. Verify normalized review diagnostics.
5. Undo an accepted review.
6. Verify reversal/reconciliation diagnostic.
7. Restart Anki.
8. Verify storage/settings survive.
9. Verify normal review remains unaffected.
10. Capture reviewer hook timing evidence.
```

Record exact Anki version and OS.

---

## 18. Definition of Done

Phase 0 is complete when:

- [x] repository implementation structure exists
- [x] bootstrap is safe/idempotent by design and automated guards
- [x] integration boundary exists
- [x] EventBus exists
- [x] normalized ReviewObservation exists
- [x] undo/reversal mapping is documented
- [x] reconciliation foundation is proven in automated tests
- [x] clock/IDs/local study day exist
- [x] settings service exists
- [x] Focus Policy exists
- [x] sidecar DB exists
- [x] schema version/migrations work
- [x] profile identity strategy is resolved
- [x] logs avoid card content by default
- [x] timing instrumentation exists
- [ ] reviewer baseline is measured in real Anki
- [x] UI tokens/reduced motion/focus baseline exist
- [x] test harness works in GitHub Actions
- [ ] manual Anki smoke test is completed
- [x] architecture/data/ADRs reflect current implementation direction
- [x] `PHASE_0_FOUNDATION_HANDOFF.md` exists as a partial handoff
- [ ] final handoff is promoted from PARTIAL to COMPLETE

---

## 19. Phase 1 Entry Contract

Phase 1 may begin only when it can rely on:

- stable bootstrap,
- stable profile scoping,
- normalized review events,
- proven reversal/reconciliation path,
- persistence/migrations,
- settings/Focus Policy,
- reviewer performance baseline,
- EventOrchestrator-ready architecture.

Real-host validation is the final Phase 0 gate before this contract is considered satisfied.

---

# Phase 0 North Star

> **Before we gamify a single review, prove that we can observe, persist, reverse, and present review-derived state without lying to the learner or slowing Anki down.**
