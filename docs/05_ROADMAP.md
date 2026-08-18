# 05_ROADMAP.md

# Anki Alive — Roadmap

## 1. Roadmap Principle

> **Build one stable layer at a time, and never let a later feature weaken the learning core.**

Each phase is a vertical slice with product, architecture, UX, testing, accessibility, performance, and documentation gates.

---

## 2. Phase Sequence

```text
Phase 0 — Foundation
Phase 1 — Expedition
Phase 2 — Oracle
Phase 3 — Rescue
Phase 4 — Nemesis
Phase 5 — Fragments
Phase 6 — Relics
Phase 7 — Memory World
Cross-Phase Audit
Release Hardening
```

The specification audit has been completed before implementation.

---

## 3. Cross-Phase Audit Gate

Before Phase 0 implementation, repository docs must reflect:

- canonical session ownership,
- undo/reconciliation as Phase 0 blocker,
- shared EventOrchestrator direction,
- Memory Engine boundary,
- shared milestone/history ownership,
- cumulative reviewer performance strategy,
- corrected Relic/Nemesis lifecycle semantics.

---

## 4. Phase 0 — Foundation

Goal:

Build safe bootstrap, integration boundaries, persistence, events, settings, Focus Mode, tests, and performance instrumentation.

Additional audit obligations:

- validate normalized review identity,
- validate undo/reversal,
- define reconciliation architecture,
- keep SessionCoordinator runtime-only,
- preserve seams for EventOrchestrator, HistoryService, ReviewContextService, and coordinated writes.

Exit condition:

Phase 1 must not inherit unresolved foundational review-state ambiguity.

---

## 5. Phase 1 — Expedition

Goal:

Create bounded study journeys with real completion.

Additional audit obligations:

- Expedition is durable session owner,
- EventOrchestrator exists before phase close,
- duplicate/undo progress behavior proven,
- review-context aggregation direction established.

---

## 6. Phase 2 — Oracle

Goal:

Create trustworthy precommitted recall prediction.

Additional audit obligations:

- commitment references source review identity where possible,
- Memory Engine interface formalized,
- deferred presentation survives crash safely if required.

---

## 7. Phase 3 — Rescue

Goal:

Create memory recovery lifecycle from genuine fragility.

Additional audit obligations:

- Memory Engine fully usable,
- shared HistoryService introduced,
- coordinated multi-feature writes evaluated,
- persistent state does not create forced immediate tension.

---

## 8. Phase 4 — Nemesis

Goal:

Turn persistent difficulty into long-term challenge.

Audit correction:

```text
DEFEATED → ACTIVE
```

when a Nemesis returns.

`NemesisReturned` is history, not a permanent lifecycle state.

---

## 9. Phase 5 — Fragments

Goal:

Create bounded mystery from real memory history.

Additional audit obligation:

Fragment reveal candidates should consume shared milestones/projections rather than ad hoc feature-table mining.

---

## 10. Phase 6 — Relics

Goal:

Turn long-lived memories into persistent artifacts.

Audit correction:

```text
RESTORING → ACTIVE
```

when restored.

`RelicRestored` is a milestone/history event.

---

## 11. Phase 7 — Memory World

Goal:

Visualize the learner's memory ecosystem.

Additional audit obligations:

- World reads projections,
- cache is disposable,
- review never depends on World availability,
- large collections use aggregation and LOD.

---

## 12. Persistent-State Product Rule

Persistent feature state does not automatically create immediate study tension.

Examples:

- active Nemesis,
- unresolved Rescue,
- fractured Relic.

Only currently scheduled/eligible work should create immediate session urgency.

This prevents Anki Alive from becoming a permanent obligation dashboard.

---

## 13. Cross-Phase Performance Gate

Beginning no later than Phase 3:

- avoid per-feature hot-path I/O,
- aggregate review feature context,
- coordinate related writes where justified.

Measure the integrated reviewer, not only isolated features.

---

## 14. Cross-Phase Interaction Tests

Mandatory integrated cases include:

```text
Oracle + Rescue
Oracle + Nemesis
Rescue + Nemesis
Fragment ready + Oracle
Nemesis defeat + Relic formation
Relic fracture + Rescue
Expedition completion + major feature event
Undo after combined transition
```

---

## 15. Feature Entry Criteria

A feature may enter implementation only when:

- predecessor contracts are stable,
- data ownership is explicit,
- event timing is defined,
- undo impact is known,
- persistence ownership is known,
- performance impact is estimated,
- accessibility path exists.

---

## 16. Feature Deferral Rule

If an idea is useful but outside current phase:

```text
capture → backlog → target phase → return to scope
```

Do not implement future features opportunistically.

---

## 17. Phase Completion Gate

Every phase requires:

### Product
- scope complete
- critical invariant preserved
- no dishonest grading incentive

### Architecture
- state owner clear
- migration complete
- integration boundary preserved

### UX
- polished normal state
- loading/empty/error states
- Focus Mode
- reveal orchestration

### Accessibility
- keyboard
- focus
- reduced motion
- non-color semantics

### Testing
- automated evidence
- manual host evidence

### Performance
- relevant measurements
- integrated impact understood

### Documentation
- ADRs
- backlog
- architecture/data updates
- handoff

---

## 18. Release Hardening

After Phase 7:

- migration-chain test,
- cross-feature undo audit,
- integrated reviewer P50/P95,
- large-profile performance,
- full accessibility audit,
- full visual consistency audit,
- privacy/data-retention review,
- compatibility matrix,
- packaging/update-path hardening.

---

# Roadmap North Star

> **Each phase earns the right to exist by leaving the system more coherent, not merely more feature-rich.**
