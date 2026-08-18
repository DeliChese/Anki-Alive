# 06_DECISIONS.md

# Anki Alive — Decision Log

This file records accepted and proposed architectural/product decisions.

Accepted ADRs are constraints unless explicitly superseded.

---

## Accepted

### ADR-001 — The Game Is the Memory

Status: ACCEPTED

Anki Alive progression is grounded in genuine memory state/history, not detached XP, coins, or arbitrary game progress.

---

### ADR-002 — Again Is Never Punished

Status: ACCEPTED

`Again` may represent forgetting, but must not cause artificial punishment, currency loss, shame, or arbitrary regression.

---

### ADR-003 — No Reward for Arbitrary Good/Easy Presses

Status: ACCEPTED

No major progression/reward may be earned merely by selecting higher grading buttons.

---

### ADR-004 — Expedition Is the Primary Session Container

Status: ACCEPTED

Expedition provides bounded study-session structure.

---

### ADR-005 — Anki Scheduling Remains Authoritative

Status: ACCEPTED

Anki Alive never replaces scheduler authority.

---

### ADR-006 — Anki-Specific APIs Stop at Integration Layer

Status: ACCEPTED

Volatile host APIs are isolated behind adapters.

---

### ADR-007 — Durable Feature State Uses Sidecar Storage

Status: ACCEPTED

Anki Alive durable state uses add-on-owned storage and does not modify Anki collection schema.

---

### ADR-008 — Rebuildable Data Is Not Canonical

Status: ACCEPTED

Caches, projections, rankings, and World state are rebuildable unless a specific historical commitment requires durability.

---

### ADR-009 — Full Card Content Is Not Stored by Default

Status: ACCEPTED

Persist references and metadata. Resolve card content live when needed.

---

### ADR-010 — Oracle Predictions Are Committed Before Outcome

Status: ACCEPTED

A prediction represented as pre-existing must be durably or deterministically committed before review outcome.

---

### ADR-011 — One Prominent Event Reveal per Review Boundary

Status: ACCEPTED

Major presentation events are orchestrated so only one prominent reveal interrupts a review boundary.

---

### ADR-012 — Focus Mode Is First-Class

Status: ACCEPTED

Focus Mode suppresses presentation intensity without changing domain truth.

---

### ADR-013 — Behavioral Design Must End in Closure

Status: ACCEPTED

No infinite "one more" chain.

---

### ADR-014 — Generated Art Supports UI but Does Not Replace It

Status: ACCEPTED

Generated visual assets may support atmosphere and identity, not core controls or layout.

---

### ADR-015 — Visual Direction Is Arcane Memory Interface

Status: ACCEPTED

Dark Arcane + Modern Minimal is the shared visual language.

---

### ADR-016 — Reviewer Latency Has Priority Over Feature Immediacy

Status: ACCEPTED

Feature work may defer or precompute rather than degrade active review responsiveness.

---

### ADR-017 — Local Study Day Is Explicit Data

Status: ACCEPTED

Store UTC durable timestamps plus explicit local study-day identity where needed.

---

### ADR-018 — Durable Rule-Dependent State Stores Policy Version

Status: ACCEPTED

Historical state whose meaning depends on policy must retain version context.

---

### ADR-019 — Expedition Owns Durable Session State

Status: ACCEPTED

Expedition owns canonical durable session target, progress, checkpoints, lifecycle, and completion.

`SessionCoordinator` is runtime coordination only.

---

### ADR-020 — Shared Undo/Reconciliation Architecture

Status: ACCEPTED IN PRINCIPLE / HOST MAPPING PENDING PHASE 0

Review-derived feature transitions should reference normalized review observations where possible.

Undo/reversal is handled through shared reconciliation, not isolated feature-specific counter hacks.

Exact Anki hook/source-review identity mapping must be validated in Phase 0.

---

### ADR-021 — Presentation Events Are Centrally Orchestrated

Status: ACCEPTED

`EventOrchestrator` owns presentation prominence, priority, deferral, dedupe, merge, Focus Mode suppression, and one-major-event enforcement.

It does not own domain lifecycle.

---

### ADR-022 — Memory Engine Is Feature-Neutral

Status: ACCEPTED

Memory Engine normalizes memory facts such as stability, difficulty, retrievability, interval, lapses, and review summaries.

Feature-specific meaning belongs to Rescue/Nemesis/Relic/etc.

---

### ADR-023 — Significant Cross-Feature History Uses Shared Milestones

Status: ACCEPTED

A shared milestone/history layer records high-significance events.

Feature tables remain canonical lifecycle owners.

---

### ADR-024 — Persistent State Is Not Automatic Immediate Urgency

Status: ACCEPTED

A Nemesis, Rescue, fractured Relic, or other persistent state may inform context, but only currently scheduled/eligible work should create immediate study tension.

---

### ADR-025 — Reviewer Hot Path Uses Aggregated Feature Context

Status: ACCEPTED IN DIRECTION

As features accumulate, reviewer code should use batched/cached feature context rather than one independent database query per feature.

Exact implementation is evidence-driven.

---

### ADR-026 — Restoration and Return Are Milestones, Not Permanent States

Status: ACCEPTED

Relic restoration:

```text
RESTORING → ACTIVE
```

with `RelicRestored` history.

Nemesis return:

```text
DEFEATED → ACTIVE
```

with `NemesisReturned` history.

---

## Proposed / Phase 0 Validation

### ADR-P01 — Minimum Supported Anki Version

Status: PROPOSED

Resolve during Phase 0 using current host APIs and test evidence.

---

### ADR-P02 — Exact Review Hook and Undo Mapping

Status: PROPOSED / HIGH PRIORITY

Resolve:

- question shown,
- answer shown,
- grade accepted,
- source review identity,
- undo/reversal.

---

### ADR-P03 — Frontend Rendering Stack

Status: PROPOSED

Choose the smallest stack justified by real UI needs.

---

### ADR-P04 — SQLite Journal / Backup Strategy

Status: PROPOSED

Validate connection lifecycle, journal mode, backup behavior, and corruption recovery.

---

### ADR-P05 — Profile Identity Strategy

Status: PROPOSED

Choose stable local profile/collection scoping that does not rely on display name alone.

---

### ADR-P06 — Cross-Feature Review Transaction Strategy

Status: PROPOSED

When multiple features change from one review, determine whether writes share one transaction/unit of work.

Must be decided no later than Phase 3.

---

# Decision Log North Star

> **Record the decisions future engineers would otherwise be tempted to rediscover or contradict.**
