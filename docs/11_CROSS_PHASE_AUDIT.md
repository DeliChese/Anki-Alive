# 11_CROSS_PHASE_AUDIT.md

# Anki Alive — Cross-Phase Audit

## 1. Purpose

This audit reviews the complete specification set from Phase 0 through Phase 7 before implementation begins.

The goal is to identify:

- conflicting ownership,
- hidden coupling,
- missing shared infrastructure,
- lifecycle inconsistencies,
- migration risks,
- undo/reconciliation hazards,
- performance accumulation,
- UX event collisions,
- accessibility drift,
- product-integrity risks.

This document does not replace the individual phase specifications.

It validates that they can coexist as one coherent product.

---

# 2. Audit Scope

Reviewed phases:

```text
Phase 0 — Foundation
Phase 1 — Expedition
Phase 2 — Oracle
Phase 3 — Rescue
Phase 4 — Nemesis
Phase 5 — Fragments
Phase 6 — Relics
Phase 7 — Memory World
```

Canonical supporting docs assumed:

```text
00_PRODUCT_VISION.md
01_PRODUCT_PRINCIPLES.md
02_DESIGN_SYSTEM.md
03_ARCHITECTURE.md
04_DATA_MODEL.md
05_ROADMAP.md
06_DECISIONS.md
07_BACKLOG.md
08_TESTING.md
09_ACCESSIBILITY.md
10_PERFORMANCE.md
```

---

# 3. Executive Result

## Overall Status

```text
Architecture coherence:      GOOD
Product coherence:           GOOD
State ownership:             GOOD WITH 3 CLARIFICATIONS
Undo/reconciliation:         HIGH-RISK / MUST RESOLVE EARLY
Event orchestration:         NEEDS SHARED CONTRACT
Persistence/migrations:      GOOD WITH VERSIONING REQUIREMENTS
Reviewer performance:        GOOD IF HOT-PATH RULES ARE ENFORCED
Accessibility:               GOOD
Cross-feature visual system: GOOD
Implementation readiness:    CONDITIONAL
```

The specification set is coherent enough to begin Phase 0 implementation.

However, several shared contracts must be finalized before Phase 1 or Phase 2 implementation begins.

---

# 4. State Ownership Audit

## 4.1 Canonical Ownership Map

The following ownership should be treated as authoritative.

| Concern | Canonical Owner |
|---|---|
| Anki scheduling state | Anki |
| Review history | Anki |
| FSRS / memory metrics | Anki / normalized Memory Engine projection |
| Session container | Expedition |
| Prediction commitment | Oracle |
| Fragility/recovery lifecycle | Rescue |
| Persistent difficulty identity | Nemesis |
| Mystery lifecycle | Fragment |
| Long-term artifact history | Relic |
| Aggregate visual world | Memory World projection |
| Major event presentation order | EventOrchestrator |
| Feature configuration | SettingsService |
| Focus Mode policy | Shared core policy |
| Durable add-on state | Anki Alive sidecar persistence |

This ownership model is coherent.

---

# 5. State Ownership Finding A — SessionCoordinator vs Expedition

## Risk

Phase 0 architecture proposes a generic `SessionCoordinator`.

Phase 1 gives Expedition direct ownership of active session state.

If both persist or mutate overlapping state, two authorities may emerge.

Example bad architecture:

```text
SessionCoordinator.active_session
ExpeditionRepository.active_expedition
```

where both can disagree.

## Required Resolution

Choose one of these patterns before Phase 1 implementation.

### Preferred

```text
SessionCoordinator
    owns only runtime coordination

Expedition
    owns canonical durable session state
```

SessionCoordinator may hold:

- active Expedition ID,
- event subscriptions,
- presentation context.

It must not duplicate:

- target,
- progress,
- checkpoint state,
- completion state.

## Audit Decision

**RECOMMENDED ADR**

> Expedition is the canonical owner of durable study-session state. SessionCoordinator is runtime orchestration only.

---

# 6. State Ownership Finding B — Memory Engine

## Risk

Rescue, Nemesis, Relics, and Memory World all require memory-derived values.

If each feature independently computes:

- stability interpretation,
- fragility,
- difficulty history,
- trend,

semantic drift will occur.

## Required Contract

Memory Engine must expose normalized, feature-neutral data.

Example:

```text
MemorySnapshot
- card_id
- stability?
- difficulty?
- retrievability?
- interval_days
- lapses
- review_count
- recent_outcomes
- observed_at
```

Feature-specific meaning remains outside Memory Engine.

Correct:

```text
Memory Engine → raw normalized memory facts
Rescue → fragility
Nemesis → persistent-difficulty score
Relic → formation eligibility
World → aggregate health
```

Incorrect:

```text
Memory Engine.is_nemesis
Memory Engine.is_relic
```

## Audit Decision

**LOCK BEFORE PHASE 3**

---

# 7. State Ownership Finding C — History Infrastructure

## Risk

Several phases want durable historical events:

- Rescue completion
- Nemesis defeat
- Fragment reveal
- Relic formation/fracture/restoration
- World landmarks

Creating separate narrative history systems per feature will duplicate data.

## Required Contract

Create shared canonical history infrastructure.

Suggested entity:

```text
MemoryMilestone
- milestone_id
- type
- occurred_at
- card_id?
- entity_id?
- source_event_id?
- metadata
- policy_version?
```

Feature tables retain lifecycle state.

History service retains significant cross-feature milestones.

## Audit Decision

**ADD TO PHASE 0/1 ARCHITECTURE FOUNDATION**

The table itself may be deferred until first needed.

The interface should be planned early.

---

# 8. Cross-Feature Lifecycle Audit

## Expedition

```text
PLANNED
ACTIVE
PAUSED
COMPLETED
ENDED/ABANDONED
INVALIDATED
```

Good.

## Oracle

```text
COMMITTED
HIDDEN
RESOLVED
INVALIDATED
REVERSED
```

Good.

## Rescue

```text
AVAILABLE
ACTIVE
STABILIZING
RESCUED
EXPIRED
ORPHANED
REVERSED
```

Good.

## Nemesis

```text
CANDIDATE
ACTIVE
WEAKENING
DEFEATED
RETURNED
ORPHANED
```

Good.

## Fragment

```text
HIDDEN
DISCOVERED
PROGRESSING
READY
REVEALED
ARCHIVED
```

Good.

## Relic

```text
CANDIDATE
ACTIVE
FRACTURED
RESTORING
RESTORED
```

Potential ambiguity found.

---

# 9. Relic Lifecycle Clarification

## Problem

`RESTORED` sounds terminal, but a restored Relic should function as an active Relic again.

Otherwise future fracture semantics become awkward:

```text
RESTORED → FRACTURED?
```

## Recommended Model

Use lifecycle state plus historical event.

Better:

```text
CANDIDATE
ACTIVE
FRACTURED
RESTORING
ACTIVE
```

and record:

```text
RelicRestored
```

as history.

Alternative:

```text
RESTORED_ACTIVE
```

but this adds unnecessary state complexity.

## Audit Decision

**RECOMMEND CHANGE**

Relic restoration should transition back to `ACTIVE`, while restoration is preserved in history.

---

# 10. Nemesis Return Clarification

Similar issue:

```text
DEFEATED → RETURNED
```

`RETURNED` can be either:

- event,
- state.

Preferred:

```text
DEFEATED → ACTIVE
```

with history event:

```text
NemesisReturned
```

This reduces unnecessary permanent states.

## Audit Decision

**RECOMMEND CHANGE**

Treat "returned" as a milestone/event and resume `ACTIVE`.

---

# 11. Event Architecture Audit

All phases depend increasingly on domain events.

By Phase 6, potential review-boundary events include:

```text
OraclePredictionResolved
MemoryStabilized
RescueCompleted
NemesisWeakening
NemesisDefeated
FragmentReady
FragmentRevealed
RelicFormed
RelicFractured
RelicRestored
CheckpointReached
ExpeditionCompleted
```

Without a strict presentation contract, event storms are inevitable.

---

# 12. EventOrchestrator Must Become Shared Infrastructure

## Required Responsibilities

EventOrchestrator should:

- receive presentation candidates,
- assign priority,
- classify prominence,
- merge compatible events,
- defer events,
- persist deferred events where required,
- respect Focus Mode,
- respect reduced motion,
- prevent duplicate presentation.

It should not own domain state.

---

# 13. Presentation Event Contract

Recommended:

```text
PresentationEvent
- presentation_event_id
- source_domain_event_id
- kind
- prominence
- priority
- created_at
- expires_at?
- dedupe_key?
- payload_ref
- status
```

Possible statuses:

```text
PENDING
SHOWN
DISMISSED
DEFERRED
SUPPRESSED
INVALIDATED
```

This should be different from domain lifecycle events.

---

# 14. Prominence Levels

Recommended:

```text
AMBIENT
MINOR
MAJOR
SESSION_CLOSURE
```

Rules:

### AMBIENT

May update silently.

### MINOR

Compact inline/toast.

### MAJOR

At most one per review boundary.

### SESSION_CLOSURE

Checkpoint/Expedition completion context.

This gives future phases a stable contract.

---

# 15. Event Priority Audit

The individual phase specs contain provisional priority examples.

Do not encode separate priority tables inside each feature.

Centralize priority.

Suggested initial semantic order:

```text
SESSION_CLOSURE
RELIC_RESTORED
RELIC_FORMED
NEMESIS_DEFEATED
ORACLE_RESOLUTION
RESCUE_COMPLETION
FRAGMENT_REVEAL
NEMESIS_WEAKENING
RESCUE_STABILIZED
FRAGMENT_READY
AMBIENT_PROGRESS
```

Exact numbers should be centralized and versionable.

---

# 16. Combined Event Composition

Some events should merge rather than compete.

Examples:

### Oracle + Rescue

```text
Oracle prediction defeated.
Memory stabilized.
```

### Oracle + Nemesis

```text
Oracle prediction defeated.
Nemesis weakening.
```

### Nemesis defeat + Relic formation

Potentially one significant combined history reveal.

### Expedition completion + Fragment ready

Prefer completion surface containing pending Fragment action.

## Audit Decision

EventOrchestrator needs **merge rules**, not only priority.

---

# 17. Undo/Reconciliation Audit

This is the highest-risk shared technical area.

Nearly every feature depends on review-derived state.

Undo may affect:

- Expedition progress
- Oracle result
- Rescue lifecycle
- Nemesis encounter/defeat
- Fragment progress
- Relic formation/fracture/restoration
- milestone history
- presentation events

---

# 18. Anti-Pattern — Per-Feature Undo Logic

Avoid:

```text
Oracle listens to undo
Rescue listens to undo
Nemesis listens to undo
Fragment listens to undo
Relic listens to undo
```

with each guessing what happened.

This is fragile.

---

# 19. Required Review Identity Model

Phase 0 must investigate whether a stable source review identity can be obtained.

Ideal internal normalized event:

```text
ReviewObservation
- observation_id
- card_id
- source_review_id?
- rating
- reviewed_at
- sequence
```

Reversal event:

```text
ReviewReversed
- source_review_id?
- card_id
- reversed_at
```

If host APIs cannot provide stable IDs, a reconciliation strategy is required.

---

# 20. Recommended Reconciliation Pattern

Prefer:

```text
host review event
    ↓
normalized ReviewObservation
    ↓
features derive transitions
    ↓
transition stores source observation/event reference
```

On undo:

```text
ReviewReversed
    ↓
ReconciliationService
    ↓
re-evaluate affected feature states
```

This is superior to blindly subtracting counters.

---

# 21. Undo Audit Decision

**PHASE 0 BLOCKER**

Do not implement Phase 1 durable review-derived progress until the host undo behavior has been validated.

The exact strategy may remain provisional during early Phase 0, but must be resolved before Phase 1 completion.

---

# 22. Persistence Audit

The phase-by-phase table plan is sound.

Expected schema evolution:

```text
Phase 0
schema_meta
migration_history

Phase 1
expeditions
expedition_checkpoints

Phase 2
oracle_predictions

Phase 3
rescues

Phase 4
nemeses
(optional nemesis-specific history)

Phase 5
fragments

Phase 6
relics
(optional relic history)

Phase 7
mostly cache/preferences
```

---

# 23. Shared Persistence Requirement — Entity IDs

Every Anki Alive durable entity should use a stable add-on-owned ID.

Do not rely solely on:

```text
card_id
```

because:

- one card may have historical multiple lifecycles,
- feature entities may be archived/recreated,
- references need stable identity.

Use:

```text
expedition_id
oracle_prediction_id
rescue_id
nemesis_id
fragment_id
relic_id
milestone_id
presentation_event_id
```

---

# 24. Shared Persistence Requirement — Policy Versions

The following must support policy versioning:

- Oracle selection/interpretation
- Rescue eligibility/completion
- Nemesis promotion/defeat
- Fragment reveal/progress policy
- Relic formation/fracture/restoration
- World projection formula if persisted/cached

Do not retroactively reinterpret old history silently.

---

# 25. Shared Persistence Requirement — Timestamps

Canonical:

```text
UTC timestamp
+
explicit local study date where session/day semantics matter
```

Do not use local midnight as destructive boundary.

This is consistent across all phases.

---

# 26. Migration Chain Audit

Every migration must be testable from:

```text
fresh → latest
previous phase → latest
```

Before release hardening, add full-chain test:

```text
Phase 0 schema
→ 1
→ 2
→ 3
→ 4
→ 5
→ 6
→ 7
```

with representative historical data.

---

# 27. Card Deletion Audit

All persistent memory-level features handle deletion.

Consistent required behavior:

```text
source card deleted
    ↓
entity becomes orphaned where historical meaning exists
```

Recommended:

- Oracle unresolved prediction: invalidate
- Rescue: orphan/archive
- Nemesis: orphan
- Fragment payload referencing card: preserve only safe history
- Relic: orphan but preserve artifact history
- World: omit source from live projection while historical landmark may remain

This model is coherent.

---

# 28. Review Grade Semantics Audit

Shared rule across phases:

### Expedition

All ratings count as work progress.

### Oracle

```text
Again = recall failure
Hard/Good/Easy = recall success
```

### Rescue/Nemesis/Relic

Do not interpret rating directly as reward.

Observe resulting memory state/history.

### Fragment

All accepted ratings progress equally by default.

This is coherent and strongly protects honest grading.

---

# 29. Product Integrity Audit

## No Streak Dependency

Preserved across all phases.

## Again Is Never Punished

Preserved.

## No Casino System

Preserved.

## No Artificial Midnight Urgency

Preserved.

## No Rating-Based Rewards

Preserved.

## Real Closure

Preserved in:

- Expedition
- Oracle
- Fragment

Rescue/Nemesis/Relic intentionally have long-term lifecycles.

They still require bounded presentation moments.

---

# 30. Closure Risk — Persistent Mechanics

Persistent mechanics can accidentally create permanent psychological tension.

Examples:

```text
2 active Rescues
1 Nemesis
1 fractured Relic
```

If Today constantly presents these as unfinished obligations, the product becomes stressful.

## Required Rule

Persistent state is not automatically an urgent task.

Today should distinguish:

```text
CURRENT SIGNAL
LONG-TERM STATE
```

A Nemesis existing does not mean:

> you must defeat it today.

A fractured Relic does not mean:

> fix now.

## Audit Decision

**ADD PRODUCT RULE**

> Persistent memory state may inform context, but only currently scheduled/eligible work should create immediate study tension.

---

# 31. Performance Audit

Each phase individually targets tiny reviewer overhead.

But cumulative cost matters.

Potential review-path operations by Phase 6:

```text
Expedition lookup/update
Oracle lookup
Rescue lookup
Nemesis lookup
Fragment progress
Relic lookup/evaluation
Event orchestration
persistence
HUD projection
```

Individually cheap can still become expensive.

---

# 32. Required Hot-Path Architecture

Avoid six separate database queries per review.

Preferred:

```text
ReviewContextService
    batch-load active feature state by card/session
```

Example projection:

```text
ReviewFeatureContext
- expedition
- oracle_prediction?
- rescue?
- nemesis?
- fragment_context?
- relic?
```

This may come from:

- indexed batch query,
- memory cache,
- per-session preloaded maps.

---

# 33. Performance Audit Decision

**ADD SHARED PERFORMANCE RULE**

By Phase 3 or earlier, introduce review-context aggregation.

Do not let every new feature independently add hot-path I/O.

---

# 34. Reviewer Write Strategy

Potential writes after one accepted review:

```text
Expedition progress
Oracle resolve
Rescue transition
Nemesis transition
Fragment progress
Relic transition
history
presentation event
```

Avoid separate fsync-heavy transactions.

Recommended:

- one bounded sidecar transaction per accepted review when multiple durable transitions occur,
- or a coordinated persistence unit-of-work.

## Audit Decision

**RECOMMENDED ARCHITECTURE ADDITION**

`ReviewTransactionCoordinator` or equivalent unit-of-work abstraction.

Do not make it feature-aware beyond coordinating atomic writes.

---

# 35. Crash Consistency

Goal:

If a review causes multiple feature transitions, crash should not leave contradictory state.

Example bad state:

```text
Nemesis defeated
but milestone missing
and Relic formation partially written
```

Transactional grouping should be used where relationships require consistency.

Presentation can be eventually consistent.

Domain state should not be contradictory.

---

# 36. Memory World Performance Audit

Phase 7 correctly treats World as projection/cache.

Important addition:

World rebuild must read:

- normalized aggregate summaries,
- milestone/history tables,

not repeatedly recompute all raw revlog history if avoidable.

Consider incremental summary projections before Phase 7.

---

# 37. UX Audit

The visual language is coherent across phases.

Feature grammar remains distinct:

```text
Expedition → path
Oracle → orbit
Rescue → repair pulse
Nemesis → fracture/pressure
Fragment → incomplete shard
Relic → artifact
World → constellation/topography
```

This is strong.

---

# 38. Reviewer Attention Audit

All phases consistently protect active recall.

Locked global reviewer rule:

### Question State

Allowed:

- card
- minimal Expedition progress
- subtle persistent identity if approved

Not allowed:

- major reveal
- answer-relevant prediction
- animated event
- urgency popup

### Post-Grade Boundary

Allowed:

- one prominent event

This is coherent.

---

# 39. Focus Mode Audit

Focus Mode is consistently defined as presentation suppression, not domain suppression.

Correct.

Required shared API:

```text
FocusPolicy
- allow_major_reveal
- allow_minor_reveal
- allow_ambient_motion
- show_compact_progress
- defer_nonessential_events
```

Avoid each feature reading a single boolean and inventing behavior.

---

# 40. Reduced Motion Audit

Consistent across phases.

Recommended shared levels:

```text
FULL
REDUCED
MINIMAL
```

If product only exposes one toggle initially:

```text
reduced_motion: bool
```

internal components may still map to standardized transition behavior.

---

# 41. Accessibility Audit

Strong consistency.

Global requirements should include:

- keyboard navigation
- visible focus
- non-color semantics
- reduced motion
- Focus Mode
- dismissible nonessential events
- scalable text
- equivalent non-spatial World view

No major conflict found.

---

# 42. Data Privacy Audit

All phases avoid storing full card content by default.

This is coherent.

Recommended global rule:

```text
History stores references + metadata.
UI resolves live card text only when needed.
```

Exception requires explicit design/ADR.

---

# 43. Analytics / Metrics Audit

Phase specs mention useful local/product metrics.

Risk:

metrics can become a shadow product incentive.

Example:

optimizing:

- session length,
- continuation rate,
- reveal frequency,

could corrupt closure.

## Required Rule

Product metrics must always be interpreted alongside:

- honest grading
- review completion
- user stopping behavior
- recall quality
- latency
- feature disable/Focus usage

Do not optimize time-spent alone.

---

# 44. Dependency Audit

## Phase 0 → Phase 1

Needs:

- event bus
- persistence
- settings
- Focus Mode
- hook normalization
- timing
- migrations

Good.

## Phase 1 → Phase 2

Needs:

- stable active Expedition
- post-grade boundary
- EventOrchestrator
- review identity

EventOrchestrator must exist by late Phase 1.

## Phase 2 → Phase 3

Needs:

- Memory Engine maturity
- feature policy version
- reconciliation

Memory Engine should begin earlier than Phase 3 architecture work.

## Phase 3 → Phase 4

Good.

## Phase 4 → Phase 5

Needs:

- milestone/history service

Ensure history service exists before Fragment reveal ranking.

## Phase 5 → Phase 6

Good.

## Phase 6 → Phase 7

Needs:

- aggregate projections
- scalable visual identity

Good.

---

# 45. Missing Shared Infrastructure

The specs imply several shared services that should be explicitly tracked.

Recommended shared infrastructure list:

```text
EventBus
EventOrchestrator
ReconciliationService
MemoryEngine
HistoryService
SettingsService
FocusPolicy
MigrationService
DiagnosticsService
PerformanceTimer
ReviewContextService
ProjectionService
```

Potential later:

```text
ReviewTransactionCoordinator
```

These should not all be built in Phase 0.

But ownership and entry phase should be clear.

---

# 46. Recommended Infrastructure Entry Phase

| Service | Introduce By |
|---|---|
| EventBus | Phase 0 |
| SettingsService | Phase 0 |
| FocusPolicy | Phase 0 |
| MigrationService | Phase 0 |
| DiagnosticsService | Phase 0 |
| PerformanceTimer | Phase 0 |
| Reconciliation foundation | Phase 0 |
| EventOrchestrator | Phase 1 |
| ReviewContextService | Phase 1/2 |
| MemoryEngine | Phase 2 foundation, required Phase 3 |
| HistoryService | Phase 3/4 |
| ProjectionService | Phase 4/5 |
| ReviewTransactionCoordinator | when multi-feature writes justify it, no later than Phase 3 |

---

# 47. Phase 0 Additions Recommended by Audit

Phase 0 spec should explicitly account for:

1. normalized review observation identity,
2. reversal/reconciliation architecture,
3. runtime-only SessionCoordinator ownership,
4. future shared unit-of-work compatibility,
5. HistoryService interface awareness,
6. EventOrchestrator interface placeholder,
7. review-context aggregation direction.

Do not necessarily implement all services in Phase 0.

Architecture must leave clean seams.

---

# 48. Phase 1 Additions Recommended by Audit

Before Phase 1 closes:

- EventOrchestrator must exist,
- durable Expedition ownership must be explicit,
- review duplicate/undo identity must be proven,
- review-context aggregation should be introduced or designed.

---

# 49. Phase 2 Additions Recommended by Audit

Oracle is where prediction trust becomes critical.

Before close:

- commitment persistence must be durable,
- source review identity must be linked,
- Memory Engine interface should be formalized even if Oracle uses only part of it,
- presentation queue must survive crash if major reveal is deferred.

---

# 50. Phase 3 Additions Recommended by Audit

Rescue should trigger:

- full Memory Engine contract,
- shared memory snapshots,
- coordinated multi-feature review writes if needed,
- initial shared HistoryService.

---

# 51. Phase 4 Additions Recommended by Audit

Nemesis should:

- reuse shared history,
- use event history rather than state `RETURNED`,
- avoid redundant revlog-like encounter storage.

---

# 52. Phase 5 Additions Recommended by Audit

Fragments should:

- select from milestone/history projections,
- not query raw feature tables ad hoc,
- preserve deterministic payload identity,
- treat incomplete Fragment closure consistently with Expedition.

---

# 53. Phase 6 Additions Recommended by Audit

Relics should:

- transition RESTORING → ACTIVE,
- record restoration as milestone,
- preserve stable procedural visual identity,
- avoid historical state duplication.

---

# 54. Phase 7 Additions Recommended by Audit

Memory World should:

- read projections, not feature internals directly,
- treat cache as disposable,
- maintain stable region identity,
- never become review dependency.

---

# 55. ADRs Recommended Before Implementation

## ADR-P0-01 — Canonical Session Ownership

Expedition owns durable session state.

SessionCoordinator coordinates runtime only.

---

## ADR-P0-02 — Review Observation and Undo Reconciliation

Document:

- review identity
- reversal event
- reconciliation strategy

This is the highest-priority technical ADR.

---

## ADR-P1-01 — Presentation Event Orchestration

Document:

- prominence
- priority
- deferral
- dedupe
- merge
- Focus Mode behavior

---

## ADR-P2-01 — Memory Engine Contract

Define feature-neutral normalized memory inputs.

---

## ADR-P3-01 — Cross-Feature Review Transaction Strategy

Define when feature transitions share one transaction.

---

## ADR-P3-02 — Canonical Milestone History

Define shared historical event ownership.

---

# 56. Provisional Decisions That Should Stay Provisional

Do not prematurely lock:

- Expedition target formula
- checkpoint spacing
- Oracle threshold/formula
- Rescue fragility formula
- Nemesis promotion/defeat threshold
- Fragment count and reveal ranking
- Relic formation/fracture thresholds
- World health formula/layout style

These require implementation evidence and UX/performance testing.

---

# 57. Decisions Safe to Lock Now

The following are mature enough to remain hard constraints:

```text
The game is the memory itself.

Again is never punished.

No arbitrary Good/Easy reward.

Anki scheduling remains authoritative.

No casino economy.

No mandatory streak dependency.

Prediction must be committed before outcome.

Expedition target cannot silently expand.

Fragment identity cannot reroll.

Relic value comes from real memory history.

Memory World is projection only.

One prominent event reveal per review boundary.

Focus Mode preserves domain logic.

No feature may block normal Anki review.
```

---

# 58. Cross-Phase Test Matrix

Before release hardening, test interactions.

## Review Boundary Pairs

```text
Oracle + Rescue
Oracle + Nemesis
Oracle + Fragment
Oracle + Relic

Rescue + Nemesis
Rescue + Fragment
Rescue + Relic

Nemesis + Fragment
Nemesis + Relic

Fragment + Relic
```

---

# 59. High-Significance Combined Cases

Mandatory integration tests:

### Case 1

Oracle target is also Rescue.

### Case 2

Oracle target is active Nemesis.

### Case 3

Nemesis defeat and Relic formation occur from same accepted review.

### Case 4

Relic fracture triggers Rescue eligibility.

### Case 5

Fragment becomes READY on review that also resolves Oracle.

### Case 6

Expedition completion occurs on major feature event.

### Case 7

Undo after combined transition.

These cases are likely to reveal architecture defects.

---

# 60. Full Restart Test Matrix

For every durable feature, test crash/restart:

```text
before transition
after domain write
before presentation
after presentation
before dismissal
```

The UI event may be replayed/deferred.

The domain transition must never duplicate.

---

# 61. Cross-Profile Audit

All durable state must remain scoped to the correct local profile/collection context.

Requirements:

- no active Expedition leaks
- no Oracle prediction leaks
- no Relic cross-profile collision
- no World cache collision

Profile identity strategy must be stable and tested.

---

# 62. Large Collection Audit

Baseline profile sizes:

```text
Small: 1k cards
Medium: 20k cards
Large: 100k+ cards
```

Test cumulative behavior after multiple features exist.

Important:

Performance audits must test the integrated product, not only isolated modules.

---

# 63. Security / Robustness Audit

Sidecar database operations must:

- use parameterized SQL,
- avoid card-content logging,
- validate bridge messages,
- tolerate malformed settings,
- tolerate old cache,
- fail safely.

WebView messages must be namespaced/versioned.

---

# 64. Documentation Drift Audit

After each phase:

- update architecture if actual implementation differs,
- update data model,
- promote provisional decision to ADR when justified,
- update backlog,
- write handoff.

Before entering a new phase:

> trust repository state over original phase speculation.

---

# 65. Recommended Pre-Implementation Sequence

Before coding Phase 0:

```text
1. Add this audit to docs/
2. Update 03_ARCHITECTURE.md with shared service clarifications
3. Update 04_DATA_MODEL.md with milestone/presentation/review-observation concepts
4. Add proposed ADRs to 06_DECISIONS.md
5. Update 05_ROADMAP.md with audit gate
6. Update Phase 0 spec with audit findings
7. Begin Phase 0 implementation
```

Do not rewrite all phase specs immediately.

Record corrections centrally first.

Apply phase-specific corrections when that phase begins.

---

# 66. Implementation Readiness Gate

Anki Alive may begin Phase 0 implementation when:

- [ ] Cross-Phase Audit accepted
- [ ] session ownership clarified
- [ ] undo/reconciliation marked Phase 0 blocker
- [ ] EventOrchestrator planned as shared service
- [ ] Memory Engine role clarified
- [ ] HistoryService role clarified
- [ ] Relic RESTORED lifecycle correction accepted
- [ ] Nemesis RETURNED lifecycle correction accepted
- [ ] persistent-state urgency rule accepted
- [ ] cumulative reviewer performance rule accepted

---

# 67. Final Audit Verdict

No fundamental product contradiction was found across Phases 0–7.

The strongest parts of the specification set are:

- recall integrity,
- bounded session design,
- memory-centered progression,
- clear separation between scheduler truth and product narrative,
- consistent accessibility expectations,
- consistent anti-casino constraints,
- durable long-term identity.

The primary engineering risk is not feature logic.

It is **cross-feature reconciliation around one review event**.

The primary UX risk is not visual quality.

It is **too many meaningful systems competing for attention at the same boundary**.

The primary product risk is not lack of engagement.

It is **allowing persistent memory states to become permanent psychological obligations**.

All three risks are manageable with the shared contracts identified in this audit.

---

# Cross-Phase Audit North Star

> **One review may affect many stories, but there must still be one truth, one owner for each state, and one coherent experience for the learner.**
