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

Status: ACCEPTED / MANUAL HOST CONFIRMATION PENDING

Review-derived feature transitions reference normalized review observations where possible.

Undo/reversal is handled through shared reconciliation, not isolated feature-specific counter hacks.

Phase 0 source validation mapped accepted reviews to `gui_hooks.reviewer_did_answer_card`. The source review identity is Anki's `revlog.id`. `state_did_undo` signals that an undo completed but does not identify a review, so Anki Alive emits `ReviewReversed` only after verifying that a tracked source revlog row disappeared.

The mapping is covered by fake-host integration tests. A real Anki review/undo smoke test remains the final host confirmation before Phase 1 durable review-derived progression is unlocked.

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

## Phase 0 Decisions

### ADR-P01 — Minimum Supported Anki Version

Status: ACCEPTED PROVISIONALLY / MANUAL HOST CONFIRMATION PENDING

Minimum supported Anki version is **25.02.7** (`min_point_version: 250207`).

Rationale:

- required modern GUI hooks are present in the 25.02.7 upstream source,
- Anki's 25.02.7 Python project baseline is Python 3.9,
- Anki Alive CI covers Python 3.9 and 3.13,
- choosing an older version would widen the manual compatibility surface without Phase 0 evidence that it benefits the product.

The packaged manifest declares the minimum natively. A real 25.02.7-or-newer Anki smoke test is required before removing the provisional qualifier.

---

### ADR-P02 — Exact Review Hook and Undo Mapping

Status: ACCEPTED / MANUAL HOST CONFIRMATION PENDING

Mapping:

- accepted grade notification: `gui_hooks.reviewer_did_answer_card`,
- source review identity: `revlog.id`,
- normalized observation identity: deterministic UUID derived from `(profile_key, revlog.id)`,
- undo notification: `gui_hooks.state_did_undo`,
- reversal proof: tracked revlog row no longer exists after undo.

Do not infer a review reversal from the undo operation label and do not decrement feature state blindly.

---

### ADR-P03 — Frontend Rendering Stack

Status: ACCEPTED FOR PHASE 0

Phase 0 uses host webview-compatible HTML/CSS primitives and semantic CSS tokens. No frontend framework is introduced yet.

A framework may be adopted in a later phase only when a concrete UI need justifies its runtime, build, and maintenance cost.

---

### ADR-P04 — SQLite Journal / Backup Strategy

Status: ACCEPTED

The sidecar database uses:

- WAL journal mode,
- foreign keys enabled,
- a 5-second busy timeout,
- explicit transactions,
- integrity-check support,
- SQLite online backup support,
- graceful WAL checkpoint on close.

The database lives under add-on-owned `user_files` so Anki upgrades preserve it. Phase 0 creates only `schema_meta` and `migration_history`.

---

### ADR-P05 — Profile Identity Strategy

Status: ACCEPTED

Anki Alive creates an add-on-owned UUID inside the active Anki profile folder. The identity therefore survives profile folder rename and does not rely on display name alone.

Source review observation identity incorporates this profile key so local revlog IDs cannot collide across profiles.

---

### ADR-P06 — Cross-Feature Review Transaction Strategy

Status: PROPOSED

When multiple features change from one review, determine whether writes share one transaction/unit of work.

Must be decided no later than Phase 3.

---

# Decision Log North Star

> **Record the decisions future engineers would otherwise be tempted to rediscover or contradict.**
