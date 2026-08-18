# 03_ARCHITECTURE.md

# Anki Alive — Architecture

## 1. Architectural North Star

> **Keep Anki integration thin, memory logic testable, reviewer latency low, and user history durable.**

Anki Alive is a layered add-on. Anki remains authoritative for scheduling, cards, notes, review history, and scheduler-exposed memory state. Anki Alive owns only its feature narratives, durable feature lifecycle, projections, and presentation.

---

## 2. High-Level Architecture

```text
ANKI HOST
   ↓
Integration Layer
   ↓
Normalized Review/Lifecycle Events
   ↓
Core + Shared Services
   ↓
Feature Services
   ↓
Persistence + History
   ↓
Projection / Presentation Events
   ↓
UI
```

### Dependency rule

Host-specific objects terminate at the Integration Layer.

Feature code must not depend directly on volatile Anki UI internals.

---

## 3. Integration Layer

Expected modules:

```text
integration/
├─ hooks.py
├─ reviewer.py
├─ collection.py
├─ scheduler.py
├─ webview.py
├─ compatibility.py
└─ lifecycle.py
```

Responsibilities:

- register hooks centrally,
- normalize Anki events,
- isolate compatibility differences,
- provide stable internal contracts,
- fail gracefully.

No feature policy belongs here.

---

## 4. Normalized Review Observation

Review-derived feature state must be based on a normalized internal observation.

Conceptual contract:

```text
ReviewObservation
- observation_id
- card_id
- note_id?
- deck_id?
- source_review_id?
- rating
- reviewed_at_utc
- response_time_ms?
- sequence?
```

A reversal/undo should normalize to:

```text
ReviewReversed
- observation_id?
- source_review_id?
- card_id
- reversed_at_utc
```

The exact host mapping is a Phase 0 validation item.

### Critical rule

Phase 1 must not ship durable review-derived state until undo/reconciliation behavior is validated.

---

## 5. EventBus

Use a small in-process EventBus.

Good uses:

- lifecycle notification,
- normalized review events,
- cross-service decoupling.

Bad uses:

- turning every method call into an event,
- hiding ownership,
- creating an elaborate event framework.

Events should be small, immutable where practical, and free from UI references.

---

## 6. Session Ownership

### Canonical durable owner

`Expedition` owns durable study-session state:

- target,
- progress,
- checkpoint plan,
- lifecycle,
- completion.

### Runtime coordination

`SessionCoordinator` may coordinate:

- current Expedition ID,
- subscriptions,
- transient presentation context,
- integration lifecycle.

It must not duplicate durable Expedition state.

> **Expedition is the source of truth for study-session state. SessionCoordinator is runtime orchestration only.**

---

## 7. Memory Engine

Memory Engine provides feature-neutral normalized facts.

Example:

```text
MemorySnapshot
- card_id
- observed_at_utc
- stability?
- difficulty?
- retrievability?
- interval_days
- lapses
- review_count
- recent_outcomes
```

Memory Engine may normalize scheduler/FSRS/review-history data.

It must not expose feature-owned meaning such as:

```text
is_nemesis
is_relic
needs_rescue
```

Those belong to feature services.

---

## 8. Feature Services

Feature boundaries remain separate:

```text
expedition/
oracle/
rescue/
nemesis/
fragments/
relics/
world/
```

Features communicate through:

- domain events,
- public service interfaces,
- shared projections/history.

They must not reach into each other's repositories or internal state.

---

## 9. EventOrchestrator

EventOrchestrator owns presentation scheduling, not domain truth.

Responsibilities:

- assign prominence,
- apply priority,
- merge compatible events,
- defer events,
- deduplicate presentation,
- respect Focus Mode,
- respect reduced motion,
- prevent multiple major reveals at one review boundary.

Recommended prominence:

```text
AMBIENT
MINOR
MAJOR
SESSION_CLOSURE
```

At most one `MAJOR` event may surface at a review boundary.

---

## 10. Presentation Event

Conceptual:

```text
PresentationEvent
- presentation_event_id
- source_domain_event_id
- kind
- prominence
- priority
- created_at
- dedupe_key?
- payload_ref?
- status
```

Possible status:

```text
PENDING
SHOWN
DISMISSED
DEFERRED
SUPPRESSED
INVALIDATED
```

Presentation state is distinct from domain lifecycle state.

---

## 11. Reconciliation Service

Undo/reversal is a shared concern.

Avoid feature-specific ad hoc undo listeners.

Preferred flow:

```text
Anki review
    ↓
ReviewObservation
    ↓
feature transitions reference observation
    ↓
ReviewReversed
    ↓
ReconciliationService
    ↓
re-evaluate affected feature state
```

Reconciliation should favor re-evaluation over blindly decrementing counters.

---

## 12. Review Context Aggregation

By Phase 2/3, avoid one database lookup per feature per review.

Introduce `ReviewContextService` or equivalent.

Conceptual:

```text
ReviewFeatureContext
- expedition?
- oracle_prediction?
- rescue?
- nemesis?
- fragment_context?
- relic?
```

It may be backed by:

- indexed batch query,
- in-memory session cache,
- preloaded maps.

---

## 13. Coordinated Review Writes

One accepted review may affect multiple durable features.

When necessary, use a bounded unit-of-work / transaction coordinator.

Potential abstraction:

```text
ReviewTransactionCoordinator
```

Purpose:

- group related sidecar writes,
- prevent contradictory partial feature state,
- keep presentation eventually consistent.

It must not own feature policy.

Introduce when multi-feature writes justify it, no later than Phase 3.

---

## 14. History Service

Shared history must prevent duplicate narrative systems.

Canonical history concept:

```text
MemoryMilestone
- milestone_id
- type
- occurred_at_utc
- card_id?
- entity_id?
- source_event_id?
- metadata
- policy_version?
```

Examples:

- Rescue completed
- Nemesis defeated
- Nemesis returned
- Fragment revealed
- Relic formed
- Relic fractured
- Relic restored

Feature repositories own lifecycle. HistoryService owns significant cross-feature milestones.

---

## 15. Persistence

Use:

- Anki add-on config for lightweight settings,
- Anki Alive sidecar SQLite for durable feature state,
- rebuildable caches for projections.

Recommended storage:

```text
user_files/anki_alive.sqlite3
```

Do not modify Anki collection schema.

---

## 16. Data Authority

### Anki authoritative

- cards
- notes
- decks
- review history
- scheduler
- scheduler-exposed memory state

### Anki Alive authoritative

- Expedition lifecycle
- Oracle commitments/results
- Rescue lifecycle
- Nemesis identity/history
- Fragment lifecycle
- Relic history
- feature milestones
- presentation queue if durability is required

### Rebuildable

- Memory World projection
- aggregate health views
- cached candidate summaries
- UI projections

---

## 17. Profile Scoping

All durable state must be scoped safely to the correct local profile/collection context.

Do not use profile display name alone as a durable technical identity.

Exact profile identity strategy is a Phase 0 decision.

---

## 18. Time

Durable timestamps use UTC.

Day-based behavior also records explicit local study date.

Midnight is never a destructive boundary by default.

---

## 19. Determinism

Mystery or commitment-based mechanics must use persisted identity or deterministic seeds.

Examples:

- Oracle committed predictions
- Fragment identity
- Relic visual seed
- Memory World layout seed

Reload must not reroll user-visible truth.

---

## 20. Reviewer Performance

The reviewer hot path is sacred.

Avoid:

- collection-wide scans,
- full-history scans,
- heavy serialization,
- large UI rebuilds,
- network calls,
- one-query-per-feature architecture.

Prefer:

- session caches,
- batch queries,
- indexed lookups,
- coordinated writes,
- precomputation.

Cumulative reviewer cost matters more than isolated feature benchmarks.

---

## 21. Graceful Degradation

If optional systems fail:

- normal review remains usable,
- feature presentation may suppress itself,
- caches may rebuild,
- diagnostics record the failure.

Memory World, Vault, generated visuals, and nonessential presentation must never become review dependencies.

---

## 22. Frontend Boundary

UI consumes projections/view models.

Do not place:

- SQL,
- feature policy,
- scheduler calls

inside presentation code.

WebView bridge messages should be namespaced and versioned.

---

## 23. Shared Service Entry Plan

```text
Phase 0:
EventBus
SettingsService
FocusPolicy
MigrationService
DiagnosticsService
PerformanceTimer
Reconciliation foundation

Phase 1:
EventOrchestrator
ReviewContext direction

Phase 2:
ReviewContextService
MemoryEngine interface formalization

Phase 3:
HistoryService
ReviewTransactionCoordinator if needed

Phase 4+:
Projection infrastructure grows as evidence requires
```

---

## 24. Architecture Decisions to Resolve

Phase 0 must validate:

- minimum supported Anki version,
- exact review hooks,
- undo/reversal contract,
- profile identity,
- SQLite lifecycle/journal/backup,
- frontend stack,
- safe threading/background work,
- FSRS/memory-state access.

---

# Architecture North Star

> **One review may affect many stories, but each state has one owner and every volatile host detail stops at the boundary.**
