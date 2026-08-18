# PHASE_0_FOUNDATION.md

# Anki Alive — Phase 0: Foundation

## 1. Phase Goal

Build the smallest technical foundation strong enough for every later mechanic to remain honest, fast, testable, and durable.

Phase 0 is complete only when the project can safely observe Anki review flow, persist owned state, reconcile review reversals in a documented way, expose shared settings/Focus Mode, and measure its own reviewer cost.

---

## 2. Status

```text
Status: NOT STARTED
Phase: 0
Name: Foundation
Depends on: Starter Packs + Cross-Phase Audit
Next: Phase 1 — Expedition
```

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

Before Phase 1 durable progress is allowed, Phase 0 must validate:

- what hook means a grade is accepted,
- whether stable source review identity is available,
- how undo is surfaced,
- whether duplicate hooks can occur,
- how restart affects event identity.

This is a Phase 0 blocker.

---

## 8. Reconciliation Proof

Phase 0 must demonstrate at least one safe reversible derived state in tests or test harness.

Example test-only state:

```text
accepted review
→ derived counter/state changes
→ undo/reversal
→ derived state returns to correct value
```

This proves architecture before features depend on it.

---

## 9. Persistence Foundation

Initial durable tables:

```text
schema_meta
migration_history
```

Do not pre-create feature tables.

---

## 10. Shared Service Seams

Phase 0 should make clean future seams for:

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

Resolve a stable profile/collection scoping strategy.

Do not use display name alone.

All future durable feature state depends on this decision.

---

## 12. Reviewer Performance

Provisional synchronous reviewer budget:

```text
Preferred < 5 ms
Typical < 10 ms
P95 < 20 ms
```

Phase 0 must measure baseline hook overhead.

Important:

Future features will accumulate cost.

Architecture should therefore prefer aggregated context and coordinated writes over per-feature hot-path I/O.

---

## 13. UI / Focus Foundation

Focus Policy should support concepts such as:

```text
allow_major_reveal
allow_minor_reveal
allow_ambient_motion
show_compact_progress
defer_nonessential_events
```

Public UI may initially expose only a simple toggle.

---

## 14. Accessibility Baseline

Required:

- keyboard-friendly controls,
- visible focus,
- reduced motion,
- non-color semantics,
- readable contrast,
- scalable text.

---

## 15. Open Technical Questions

### Q0-01 — Minimum Supported Anki Version
BLOCKER FOR COMPATIBILITY.

### Q0-02 — Review Hook Mapping
BLOCKER.

### Q0-03 — Undo/Reversal Identity
BLOCKER FOR PHASE 1.

### Q0-04 — Frontend Stack
DECIDE FROM ACTUAL UI NEED.

### Q0-05 — SQLite Strategy
DECIDE AND TEST.

### Q0-06 — Profile Identity
BLOCKER FOR DURABLE STATE.

### Q0-07 — FSRS/Memory State Access
DOCUMENT INTERFACE FOR LATER MEMORY ENGINE.

### Q0-08 — Safe Background Work
VALIDATE BEFORE USING THREADS WITH HOST DATA.

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

### Persistence

- fresh DB
- reopen
- migration order
- rollback
- schema version

### Integration

- idempotent hook registration
- normalized review observation
- duplicate protection where possible
- collection lifecycle

### Reconciliation

- accepted review → derived state
- reversal → correct re-evaluation

### Performance

- baseline reviewer hook timing
- persistence timing

---

## 17. Manual Anki Validation

Minimum:

```text
1. Load add-on.
2. Open profile/collection.
3. Start review.
4. Show question.
5. Show answer.
6. Grade cards with all buttons.
7. Verify normalized review events.
8. Undo accepted review.
9. Verify reversal/reconciliation signal.
10. Restart Anki.
11. Verify storage and settings.
12. Verify normal review remains unaffected.
```

Record Anki version and OS.

---

## 18. Definition of Done

Phase 0 is complete when:

- [ ] repository implementation structure exists
- [ ] bootstrap is safe/idempotent
- [ ] integration boundary exists
- [ ] EventBus exists
- [ ] normalized ReviewObservation exists
- [ ] undo/reversal mapping is documented
- [ ] reconciliation foundation is proven
- [ ] clock/IDs/local study day exist
- [ ] settings service exists
- [ ] Focus Policy exists
- [ ] sidecar DB exists
- [ ] schema version/migrations work
- [ ] profile identity strategy is resolved
- [ ] logs avoid card content by default
- [ ] timing instrumentation exists
- [ ] reviewer baseline is measured
- [ ] UI tokens/reduced motion/focus baseline exist
- [ ] test harness works
- [ ] manual Anki smoke test is completed
- [ ] architecture/data/ADRs reflect actual implementation
- [ ] `PHASE_0_FOUNDATION_HANDOFF.md` exists

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

---

# Phase 0 North Star

> **Before we gamify a single review, prove that we can observe, persist, reverse, and present review-derived state without lying to the learner or slowing Anki down.**
