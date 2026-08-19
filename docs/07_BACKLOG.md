# 07_BACKLOG.md

# Anki Alive — Backlog

## 1. Purpose

This backlog stores ideas that are valuable but not currently in scope.

The backlog protects the project from two opposite failures:

1. losing good ideas,
2. implementing every good idea immediately.

A feature belongs here when it is interesting but not part of the current phase.

---

## 2. Backlog Rules

Every backlog item should include:

- title,
- category,
- status,
- target phase or horizon,
- problem/opportunity,
- why it matters,
- dependencies,
- risks,
- recall-integrity note.

Do not use the backlog as a dumping ground for vague ideas.

---

## 3. Status Values

```text
IDEA
RESEARCH
READY_FOR_SPEC
DEFERRED
BLOCKED
REJECTED
SHIPPED
```

---

## 4. Priority Labels

```text
P0 — Critical
P1 — High
P2 — Medium
P3 — Nice to have
```

Priority does not override roadmap dependencies.

---

# Active Backlog

## BL-001 — Memory Time Machine

Category: Long-term history  
Status: IDEA  
Priority: P2  
Target: Post-Relics or World

### Opportunity

Surface meaningful memories from the learner's historical timeline.

Examples:

- first learned one year ago,
- oldest still-stable memory,
- card once difficult but now mature.

### Why It Matters

Creates nostalgia and strengthens ownership.

### Dependencies

- durable history
- reliable first-learning inference
- history UI

### Risks

Could become shallow novelty if shown too frequently.

### Recall Integrity

Should reveal after or outside active recall, not spoil answers.

---

## BL-002 — Memory Museum

Category: Long-term exploration  
Status: IDEA  
Priority: P2  
Target: Post-Relics

### Opportunity

Create curated galleries such as:

- Ancient Memories
- Hall of Pain
- Recently Stabilized
- Defeated Nemeses
- Restored Relics

### Dependencies

- Relics
- Nemesis history
- history projections

### Risks

Potential overlap with Relic Vault and Memory World.

### Recall Integrity

Exploration-only. Must not distort grading.

---

## BL-003 — Memory Weather

Category: Today / summary  
Status: IDEA  
Priority: P2  
Target: After Rescue foundation

### Opportunity

Describe collection health in a compact, atmospheric way.

Example:

> Mostly stable.  
> 7 fragile memories.  
> One high-pressure region.

### Dependencies

- memory health projection
- Rescue metrics

### Risks

Over-simplifying technical memory state.

### Recall Integrity

Pure presentation; must remain explainable.

---

## BL-004 — Memory DNA

Category: Profile / identity  
Status: IDEA  
Priority: P3  
Target: Later product maturity

### Opportunity

Create evolving learner profiles based on real study patterns.

### Risks

Overclaiming psychological traits.

### Recall Integrity

Must use conservative wording and observable behavior only.

---

## BL-005 — Anki Wrapped

Category: Sharing / retrospective  
Status: IDEA  
Priority: P3  
Target: Post-release

### Opportunity

Create periodic personal summaries.

### Risks

Could shift product toward vanity metrics.

### Recall Integrity

Summary should emphasize real memory outcomes rather than raw volume.

---

## BL-006 — Procedural Relic Families

Category: Visual system  
Status: RESEARCH  
Priority: P1  
Target: Phase 6

### Opportunity

Generate unique Relic identities from:

- card ID
- age
- difficulty
- stability
- fracture/restoration history

### Dependencies

- Relic policy
- design tokens
- asset system

### Risks

Visual complexity, rendering performance.

### Recall Integrity

Pure representation of real history.

---

## BL-007 — Memory Core Evolution

Category: Today visual  
Status: IDEA  
Priority: P1  
Target: Phase 1 onward

### Opportunity

Let the Today hero visual subtly evolve based on:

- memory health,
- collection maturity,
- active signals,
- long-term history.

### Risks

Could become decorative noise.

### Recall Integrity

Must not imply false scientific precision.

---

## BL-008 — One More to Closure

Category: Expedition  
Status: DEFERRED  
Priority: P1  
Target: Post-Phase-1 research / later UX evidence

### Opportunity

When the learner tries to stop near a real closure point, surface a small optional prompt.

Example:

> 2 reviews to the next checkpoint.

### Critical Constraint

Must never chain infinitely.

### Risks

Dark-pattern behavior.

### Recall Integrity

No penalty for stopping.

### Phase 1 Close Note

Phase 1 intentionally shipped without this prompt. Real completion and a clean `Done` stopping point were validated first. Revisit only with evidence that the prompt improves orientation without weakening closure or creating pressure.

---

## BL-009 — Fractured Relic Restoration

Category: Relics  
Status: IDEA  
Priority: P1  
Target: Phase 6

### Opportunity

A forgotten Relic becomes fractured and can later be restored through genuine memory recovery.

### Risks

Loss aversion could become punitive.

### Recall Integrity

No permanent loss. No pressure to grade dishonestly.

---

## BL-010 — Nemesis Return

Category: Nemesis  
Status: IDEA  
Priority: P2  
Target: Phase 4+

### Opportunity

A defeated Nemesis may return after genuine regression.

### Risks

Could feel unfair if rule is opaque.

### Recall Integrity

Return must reflect real memory deterioration.

---

## BL-011 — Session Event Compression

Category: UX orchestration  
Status: READY_FOR_SPEC  
Priority: P1  
Target: Phase 2+

### Opportunity

When multiple minor events occur, combine them into one concise checkpoint or completion summary.

### Why It Matters

Protects reviewer attention.

### Dependencies

- EventOrchestrator
- PresentationEvent model

### Phase 1 Close Note

Phase 1 shipped the EventOrchestrator/presentation-state foundation and enforced completion-over-final-checkpoint prominence. General cross-feature event compression remains deferred until Phase 2 introduces another real feature event to compress.

---

## BL-012 — Reduced Information Mode

Category: Accessibility  
Status: IDEA  
Priority: P2  
Target: Phase 1+

### Opportunity

Offer an intermediate presentation between standard mode and Focus Mode.

### Risks

Too many modes/settings.

---

## BL-013 — Exportable Memory History

Category: Data portability  
Status: IDEA  
Priority: P3  
Target: Release hardening

### Opportunity

Allow users to export Anki Alive history without exporting card content.

### Why It Matters

Trust and portability.

---

## BL-014 — Reset Feature State Selectively

Category: Settings / recovery  
Status: IDEA  
Priority: P2  
Target: Release hardening

### Opportunity

Reset:

- Oracle history
- Fragments
- World cache

without deleting all Anki Alive state.

### Risks

Need clear distinction between history and cache.

---

## BL-015 — Support Diagnostics Bundle

Category: Supportability  
Status: IDEA  
Priority: P1  
Target: Phase 0 / release hardening

### Opportunity

Generate privacy-safe diagnostics containing:

- add-on version
- Anki version
- enabled feature flags
- migration state
- recent errors
- performance summaries

### Constraint

No card text by default.

---

# Rejected / Guardrail Ideas

## BL-R01 — Generic Coin Economy

Status: REJECTED

Reason:

Conflicts with product identity and can reward interaction independently of recall.

---

## BL-R02 — Mandatory Daily Streak

Status: REJECTED

Reason:

Creates pressure unrelated to actual memory state.

---

## BL-R03 — Loot Boxes

Status: REJECTED

Reason:

Conflicts with the no-casino principle.

Fragments may use mystery, but reveals must be grounded in memory history.

---

## BL-R04 — Leaderboard as Core Motivation

Status: REJECTED

Reason:

Shifts motivation toward social comparison and quantity.

---

## BL-R05 — Permanent Loss for Missing Days

Status: REJECTED

Reason:

Artificial loss aversion.

---

# Phase 1 Close Review

- `BL-008` was deliberately deferred rather than smuggled into completion UX.
- `BL-011` keeps only the cross-feature compression work; the orchestration foundation itself now exists.
- No Oracle/Rescue/Nemesis/Fragment/Relic placeholder behavior was added during Expedition.
- Appearance/dashboard coexistence findings were promoted to ADR-P07 instead of becoming a feature backlog item.
- Filtered deck/custom study validation remains a documented host-support limitation, not a new gameplay backlog item.

---

# Backlog Intake Template

```text
## BL-XXX — Title

Category:
Status:
Priority:
Target:

### Problem / Opportunity

### Proposed Direction

### Why It Matters

### Dependencies

### Risks

### Recall Integrity

### Notes
```

---

# Backlog Review Cadence

Review backlog:

- at phase start,
- at phase close,
- when roadmap changes,
- before public release.

Do not repeatedly reshuffle priorities without evidence.

---

# Backlog North Star

> **Capture exciting ideas without letting excitement hijack the current phase.**
