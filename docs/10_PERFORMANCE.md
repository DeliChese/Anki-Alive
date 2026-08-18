# 10_PERFORMANCE.md

# Anki Alive — Performance Strategy

## 1. Purpose

Anki Alive runs inside a study application where latency is highly visible.

A feature that adds even modest friction to every card can make hundreds of reviews feel worse.

Performance is therefore a product requirement.

The reviewer hot path has the highest priority.

---

## 2. Performance Principles

### PERF01 — Reviewer Latency Wins

If a feature competes with immediate card responsiveness, responsiveness wins.

### PERF02 — Precompute Outside the Hot Path

Prefer work during:

- collection open,
- Expedition planning,
- checkpoint boundaries,
- idle/background periods,
- dedicated screens.

### PERF03 — Cache Rebuildable Work

If computation is expensive and safely reproducible, cache it.

### PERF04 — Do Not Scan the Whole Collection Per Card

Full-collection work in review hooks is forbidden unless proven negligible and intentionally approved.

### PERF05 — Measure Before Optimizing Deeply

Avoid speculative complexity.

### PERF06 — Degrade Gracefully

If expensive visual systems fail or lag, reviewing must continue.

---

## 3. Performance-Critical Paths

Highest sensitivity:

1. question → render
2. answer → render
3. grade → next card
4. reviewer overlay updates
5. event persistence required before next step

Medium sensitivity:

- Today screen load
- Expedition initialization
- checkpoint reveal
- history screen

Lower sensitivity:

- Relic Vault exploration
- Memory World generation
- deep historical analytics

Lower sensitivity does not mean unlimited cost.

---

## 4. Initial Performance Budgets

These are provisional budgets to validate during Phase 0.

### 4.1 Added Synchronous Reviewer Overhead

Target:

```text
Typical: < 10 ms
Preferred: < 5 ms
P95 target: < 20 ms
```

This refers to Anki Alive-added synchronous work on critical review transitions, excluding host rendering.

Any consistent addition above this should trigger profiling.

### 4.2 UI Overlay Update

Target:

```text
< 16 ms for simple reviewer HUD updates
```

Avoid forced layout/reflow chains.

### 4.3 Required Persistence Write

Target:

```text
Typical < 10 ms
```

If a durable commitment must be persisted before proceeding, keep the transaction tiny.

### 4.4 Today Screen

Target:

```text
Interactive within ~300 ms after screen availability
```

Large secondary projections may load progressively.

### 4.5 Expedition Creation

Target:

```text
Typical < 150 ms
```

Avoid blocking the user on expensive candidate analysis.

### 4.6 Memory World

No strict initial frame budget is fixed yet.

However:

- avoid blocking review,
- render progressively,
- cache expensive projections,
- support large collections.

---

## 5. Reviewer Hot-Path Rules

In card-transition hooks:

### Allowed

- capture IDs
- read lightweight state
- increment in-memory counters
- publish small events
- perform tiny indexed sidecar writes when required
- render minimal HUD changes

### Avoid

- scanning review history
- full deck aggregation
- candidate ranking across all cards
- large JSON serialization
- image generation
- network access
- filesystem crawling
- long synchronous SQL
- heavy Python object construction

---

## 6. Collection Query Rules

Collection reads should be:

- targeted,
- batched,
- indexed where possible,
- performed outside card transitions.

Prefer:

```text
one batch query for 500 candidates
```

over:

```text
500 repeated card-by-card queries
```

Feature modules should not each invent their own collection scans.

---

## 7. Sidecar Database Performance

Use small transactions.

Potential tactics:

- transaction batching
- indexes on common filters
- prepared statements / reusable query paths
- WAL mode if validated for environment
- deferred non-critical history writes

Do not introduce database tuning without testing compatibility and recovery behavior.

---

## 8. Write Classification

Classify writes into three groups.

### Critical Durable

Must survive crash before future outcome.

Example:

- Oracle prediction commitment.

Persist promptly.

### Session Durable

Should survive interruption but can be batched safely.

Example:

- Expedition progress checkpoint.

### Derived / Disposable

Can be rebuilt.

Example:

- candidate score cache.

Persist lazily or not at all.

---

## 9. Memory Engine Performance

The Memory Engine should support:

- batch snapshots
- cached derived metrics
- incremental updates after reviews
- candidate preselection

Avoid recalculating every memory metric for every card after every review.

---

## 10. Candidate Selection Performance

Oracle, Rescue, Nemesis, and Relic systems may require ranking.

Preferred approach:

1. obtain candidate pool outside reviewer hot path,
2. compute scores in batch,
3. cache/persist chosen candidates as needed,
4. consume during review.

Do not rank the entire collection right before each event.

---

## 11. Event Orchestration Performance

Event orchestration should operate on already-created event records or small in-memory state.

It should not trigger expensive feature discovery.

Discovery and presentation are separate concerns.

---

## 12. UI Rendering Strategy

### Reviewer

Prefer minimal DOM/widget updates.

Do not rerender large application surfaces on every card.

### Today

Can use richer presentation but should load core content first.

### Vault / World

May use virtualization, incremental rendering, paging, or level-of-detail strategies.

---

## 13. Asset Performance

Generated/static assets must be optimized before shipping.

Avoid:

- huge uncompressed PNGs,
- oversized textures,
- dozens of high-resolution assets loaded in reviewer,
- unnecessary animated media.

Prefer:

- SVG for precise vector assets where suitable,
- optimized raster formats for atmospheric art,
- lazy loading outside reviewer,
- reusable textures.

---

## 14. Animation Performance

Motion should be designed for stable frame delivery.

Prefer:

- opacity
- transform
- lightweight compositing

Avoid:

- heavy layout animation
- large blur changes
- repeated expensive shadows
- massive particle systems
- continuous animation in reviewer

Reduced-motion mode should naturally reduce CPU/GPU load.

---

## 15. Memory Usage

Avoid retaining:

- full card objects indefinitely,
- full card text copies,
- large review-history arrays for entire collections,
- unbounded event queues,
- unbounded rendering caches.

Use IDs and compact summaries.

Cache policy should have clear invalidation.

---

## 16. Large Collection Strategy

The product should anticipate collections with:

- tens of thousands of cards,
- long review histories,
- many decks/tags.

Strategies may include:

- capped candidate pools
- incremental aggregation
- cached summaries
- database indexes
- background work
- level-of-detail rendering

Never assume a small demo collection.

---

## 17. History Scaling

Do not render all history entries at once.

Prefer:

- pagination
- date grouping
- lazy loading
- virtualized lists
- significance filtering

Long-term users should not be punished for having long-term history.

---

## 18. Memory World Scaling

Memory World must be designed as a projection, not a literal 1-card = 1-heavy-object scene.

Possible strategies:

- aggregate by deck/tag/topic
- cluster cards
- level of detail
- representative landmarks
- progressive refinement

The World should communicate scale without rendering every memory individually at maximum detail.

---

## 19. Startup Performance

Add-on initialization should remain light.

Defer:

- expensive history aggregation
- world generation
- candidate ranking not needed immediately

Bootstrap should prioritize:

- safe hook registration
- settings
- persistence availability
- migration check
- lightweight services

---

## 20. Migration Performance

Migrations may process significant data.

Rules:

- do not run repeated expensive migration work every startup,
- wrap changes transactionally where appropriate,
- expose progress for long migrations if ever necessary,
- never block review indefinitely without feedback,
- test migration time on realistic data sizes.

---

## 21. Logging Performance

Default logs should be moderate.

Avoid per-frame or excessive per-card debug logging in production.

Provide diagnostic verbosity levels.

Heavy debug logging should be opt-in.

---

## 22. Profiling

Phase 0 should establish simple profiling tools.

Measure:

- hook handler duration
- database write duration
- candidate calculation duration
- projection duration
- UI render timing where accessible

Prefer structured timings such as:

```text
perf.reviewer.answer_hook_ms
perf.oracle.commit_ms
perf.expedition.plan_ms
perf.world.project_ms
```

---

## 23. Performance Regression Policy

A change should trigger review if it:

- adds a new query per review,
- introduces synchronous file access in reviewer,
- increases reviewer P95 materially,
- creates repeated large allocations,
- increases Today load noticeably,
- increases sidecar write frequency substantially.

Critical regressions should block phase completion.

---

## 24. Performance Test Profiles

Test at least conceptual profiles such as:

### Small

```text
1,000 cards
short history
```

### Medium

```text
20,000 cards
multi-year history
```

### Large

```text
100,000+ cards
large review log
many decks/tags
```

Exact fixtures can evolve.

---

## 25. Background Work Safety

If background work is used:

- respect Anki thread-safety constraints,
- do not access host objects from unsafe threads,
- return results through controlled boundaries,
- cancel stale work when profile/collection changes,
- prevent duplicate work.

Host integration details must be validated during implementation.

---

## 26. Caching Policy

Every cache should answer:

- what is cached?
- why?
- what invalidates it?
- can it be rebuilt?
- how large may it grow?
- what happens if it is corrupt?

No permanent mystery caches.

---

## 27. Performance and Focus Mode

Focus Mode may reduce rendering and animation cost.

However:

- domain correctness remains identical,
- feature state should not diverge,
- performance optimizations should not depend on users enabling Focus Mode.

---

## 28. Performance and Failure

If a rich screen is too slow or fails:

- show a simplified projection,
- defer secondary details,
- preserve review access.

Do not block studying to finish a visualization.

---

## 29. Performance Definition of Done

Before phase completion:

- critical reviewer path measured,
- no unexplained slow query remains,
- major new persistence path measured,
- large-data scenario considered,
- obvious rendering waste removed,
- performance notes written into handoff.

---

## 30. Initial Performance Risks

Known likely risks:

- repeated FSRS/history calculations
- too many feature candidate scans
- event-history database growth
- over-rich reviewer animation
- World rendering
- large Relic Vault
- synchronous migrations
- unnecessary UI bridge chatter

These should be profiled as the relevant phases arrive.

---

# Performance North Star

> **Every millisecond added to review must earn its place.**
