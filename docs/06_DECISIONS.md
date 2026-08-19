# 06_DECISIONS.md

# Anki Alive — Decision Log

This file records accepted and proposed architectural/product decisions.

Accepted ADRs are constraints unless explicitly superseded.

---

## Accepted

### ADR-001 — The Game Is the Memory
Status: ACCEPTED

Anki Alive progression is grounded in genuine memory state/history, not detached XP, coins, or arbitrary game progress.

### ADR-002 — Again Is Never Punished
Status: ACCEPTED

`Again` may represent forgetting, but must not cause artificial punishment, currency loss, shame, or arbitrary regression.

### ADR-003 — No Reward for Arbitrary Good/Easy Presses
Status: ACCEPTED

No major progression/reward may be earned merely by selecting higher grading buttons.

### ADR-004 — Expedition Is the Primary Session Container
Status: ACCEPTED

Expedition provides bounded study-session structure.

### ADR-005 — Anki Scheduling Remains Authoritative
Status: ACCEPTED

Anki Alive never replaces scheduler authority.

### ADR-006 — Anki-Specific APIs Stop at Integration Layer
Status: ACCEPTED

Volatile host APIs are isolated behind adapters.

### ADR-007 — Durable Feature State Uses Sidecar Storage
Status: ACCEPTED

Anki Alive durable state uses add-on-owned storage and does not modify Anki collection schema.

### ADR-008 — Rebuildable Data Is Not Canonical
Status: ACCEPTED

Caches, projections, rankings, and World state are rebuildable unless a specific historical commitment requires durability.

### ADR-009 — Full Card Content Is Not Stored by Default
Status: ACCEPTED

Persist references and metadata. Resolve card content live when needed.

### ADR-010 — Oracle Predictions Are Committed Before Outcome
Status: ACCEPTED

A prediction represented as pre-existing must be durably or deterministically committed before review outcome.

### ADR-011 — One Prominent Event Reveal per Review Boundary
Status: ACCEPTED

Major presentation events are orchestrated so only one prominent reveal interrupts a review boundary.

### ADR-012 — Focus Mode Is First-Class
Status: ACCEPTED

Focus Mode suppresses presentation intensity without changing domain truth.

### ADR-013 — Behavioral Design Must End in Closure
Status: ACCEPTED

No infinite "one more" chain.

### ADR-014 — Generated Art Supports UI but Does Not Replace It
Status: ACCEPTED

Generated visual assets may support atmosphere and identity, not core controls or layout.

### ADR-015 — Visual Direction Is Arcane Memory Interface
Status: ACCEPTED

Dark Arcane + Modern Minimal is the shared visual language.

### ADR-016 — Reviewer Latency Has Priority Over Feature Immediacy
Status: ACCEPTED

Feature work may defer or precompute rather than degrade active review responsiveness.

### ADR-017 — Local Study Day Is Explicit Data
Status: ACCEPTED

Store UTC durable timestamps plus explicit local study-day identity where needed.

### ADR-018 — Durable Rule-Dependent State Stores Policy Version
Status: ACCEPTED

Historical state whose meaning depends on policy must retain version context.

### ADR-019 — Expedition Owns Durable Session State
Status: ACCEPTED

Expedition owns canonical durable session target, progress, checkpoints, lifecycle, and completion. `SessionCoordinator` is runtime coordination only.

### ADR-020 — Shared Undo/Reconciliation Architecture
Status: ACCEPTED

Review-derived feature transitions reference normalized review observations where possible. Undo/reversal is handled through shared reconciliation, not isolated feature-specific counter hacks.

Validated Phase 0 host mapping:

- accepted review: `gui_hooks.reviewer_did_answer_card`
- source identity: `revlog.id`
- undo trigger: `gui_hooks.state_did_undo`
- reversal proof: tracked source revlog row disappears

### ADR-021 — Presentation Events Are Centrally Orchestrated
Status: ACCEPTED

`EventOrchestrator` owns presentation prominence, priority, deferral, dedupe, merge, Focus Mode suppression, and one-major-event enforcement. It does not own domain lifecycle.

### ADR-022 — Memory Engine Is Feature-Neutral
Status: ACCEPTED

Memory Engine normalizes memory facts such as stability, difficulty, retrievability, interval, lapses, and review summaries. Feature-specific meaning belongs to Rescue/Nemesis/Relic/etc.

### ADR-023 — Significant Cross-Feature History Uses Shared Milestones
Status: ACCEPTED

A shared milestone/history layer records high-significance events. Feature tables remain canonical lifecycle owners.

### ADR-024 — Persistent State Is Not Automatic Immediate Urgency
Status: ACCEPTED

A Nemesis, Rescue, fractured Relic, or other persistent state may inform context, but only currently scheduled/eligible work should create immediate study tension.

### ADR-025 — Reviewer Hot Path Uses Aggregated Feature Context
Status: ACCEPTED IN DIRECTION

As features accumulate, reviewer code should use batched/cached feature context rather than one independent database query per feature. Exact implementation is evidence-driven.

### ADR-026 — Restoration and Return Are Milestones, Not Permanent States
Status: ACCEPTED

Relic restoration is `RESTORING → ACTIVE` with `RelicRestored` history. Nemesis return is `DEFEATED → ACTIVE` with `NemesisReturned` history.

---

## Phase 0 Decisions

### ADR-P01 — Minimum Supported Anki Version
Status: ACCEPTED

Compatibility floor is **Anki 25.02.7** (`min_point_version: 250207`).

Evidence:

- required modern GUI hooks are present in upstream 25.02.7 source
- Anki's 25.02.7 Python baseline is compatible with the Python 3.9 CI leg
- Anki Alive CI covers Python 3.9 and Python 3.13
- real desktop host validation passed on Anki 25.09.4 / Python 3.13.5 / Windows 11

This is a supported compatibility floor, not a claim that every intermediate Anki build has been manually tested.

### ADR-P02 — Exact Review Hook and Undo Mapping
Status: ACCEPTED

Mapping:

- accepted grade notification: `gui_hooks.reviewer_did_answer_card`
- source review identity: `revlog.id`
- normalized observation identity: deterministic UUID derived from `(profile_key, revlog.id)`
- undo notification: `gui_hooks.state_did_undo`
- reversal proof: tracked revlog row no longer exists after undo

Real-host validation confirmed ratings 1/2/3/4, review reversal after Undo, re-answer identity renewal, and no false `ReviewReversed` from a non-review Undo.

### ADR-P03 — Frontend Rendering Stack
Status: ACCEPTED FOR PHASE 0

Use host-compatible HTML/CSS primitives. Introduce no frontend framework until later UI needs justify one.

### ADR-P04 — SQLite Journal / Backup Strategy
Status: ACCEPTED

Use add-on-owned sidecar SQLite with WAL, `synchronous=NORMAL`, 5-second busy timeout, explicit transactions, integrity checks, SQLite online backup API, and graceful checkpoint-on-close. Do not naively file-copy a live WAL database as the backup strategy.

### ADR-P05 — Profile Identity Strategy
Status: ACCEPTED

Use an Anki Alive-owned UUID stored inside the profile folder. Do not use display profile name as durable identity.

### ADR-P06 — Cross-Feature Review Transaction Strategy
Status: PROPOSED

When multiple features change from one review, determine whether writes share one transaction/unit of work. Must be decided no later than Phase 3.

---

## Phase 1 Decisions

### ADR-P07 — Today Is a Dedicated Surface, Not a Deck Browser Replacement
Status: ACCEPTED

Anki and other add-ons retain ownership of Deck Browser content and native top-level actions. Anki Alive Today is presented in a dedicated `AnkiWebView` window, reachable from the Alive/Tools entry points.

Rationale:

- preserves native Decks / Add / Browse / Stats / Sync behavior,
- avoids reimplementing host navigation,
- reduces collisions with appearance/dashboard add-ons such as Onigiri,
- lets Anki Alive fail or close without blocking normal review.

Reviewer augmentation remains intentionally narrow: a restrained Expedition strip may be injected only in review context.

### ADR-P08 — Completion Presentation State Is Durable but Separate from Expedition Truth
Status: ACCEPTED

Expedition completion is canonical domain state. Whether the completion summary is still pending or has been dismissed is presentation state stored separately in `presentation_events`.

This separation allows:

- completion summary recovery after restart,
- `Done` to dismiss presentation without rewriting Expedition history,
- future presentation orchestration to evolve without coupling UI lifecycle to feature lifecycle.

### ADR-P09 — Phase 1 Keeps the Reviewer Path Synchronous Only While Measured Headroom Exists
Status: ACCEPTED FOR PHASE 1

Phase 1 sidecar progress/reconciliation work remains synchronous because real-host evidence shows the integrated path comfortably inside the cumulative budget:

- accepted review P95: `1.357 ms`, max `1.739 ms`,
- Undo P95: `1.454 ms`, max `1.454 ms`.

This is not permission for later features to add independent synchronous I/O indefinitely. ADR-025 remains the forward constraint: Phase 2/3 must aggregate/collapse reviewer feature context as evidence requires.

---

## Phase 2 Decisions

### ADR-P10 — Oracle Commits on Question Display and Shows No Pre-Answer Prediction
Status: ACCEPTED FOR PHASE 2

Oracle uses `gui_hooks.reviewer_did_show_question(card)` as its host commitment boundary. The selected prediction is persisted from a normalized memory snapshot before an accepted review outcome can exist.

Phase 2 intentionally shows no predicted outcome, probability, or grading guidance before answer. This is stricter than merely avoiding answer text: it prevents Oracle from biasing confidence or self-grading before recall is complete.

### ADR-P11 — Oracle Reads Live FSRS Facts Through MemoryEngine
Status: ACCEPTED FOR PHASE 2

The Anki integration adapter reads `Card.memory_state`, `last_review_time`, `decay`, interval, lapse/review counts, and a bounded recent revlog summary. It computes current retrievability with the FSRS forgetting curve and returns only feature-neutral `MemorySnapshot` facts.

If FSRS memory state is absent, Oracle receives no retrievability and skips prediction instead of fabricating confidence. Anki scheduling remains authoritative.

### ADR-P12 — Initial Oracle Cadence Is Sparse and Progress-Based
Status: ACCEPTED PROVISIONALLY

The initial live-review cadence creates an Oracle opportunity at durable Expedition progress `0, 5, 10, ...`, subject to candidate policy eligibility. This gives a predictable first opportunity and avoids turning every card into a prediction event.

The cadence is presentation/selection policy, not memory truth. It may be tuned after real-host UX and performance evidence without reinterpreting historical predictions.

### ADR-P13 — Binary Oracle Recall Mapping Uses Again as Failure
Status: ACCEPTED FOR POLICY V1

For Oracle policy v1:

- `Again` → failed recall,
- `Hard`, `Good`, `Easy` → recalled.

The raw rating is retained for explainability. This maps to Anki/FSRS grading semantics without rewarding higher passing buttons.

### ADR-P14 — Oracle Reveal Is Post-Answer and Non-Interactive
Status: ACCEPTED FOR INITIAL UI

The initial Oracle reveal is a short reviewer status surface shown only after an accepted answer. It contains no button, reward, score, or action request. Focus Mode may suppress it without changing Oracle domain truth, Reduced Motion removes transition dependence, and session closure wins if review has already ended.

---

# Decision Log North Star

> **Record the decisions future engineers would otherwise be tempted to rediscover or contradict.**
