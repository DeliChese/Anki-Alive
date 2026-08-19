# Anki Alive — Project Brief

## One-Sentence Summary

Anki Alive is an Anki add-on that transforms real memory progress into an evolving, visually rich learning journey without incentivizing dishonest reviews.

## Product Goal

The product should make learners want to:

1. open Anki,
2. begin a meaningful study session,
3. continue until reaching natural points of closure,
4. genuinely recall difficult material,
5. return later because their memory history has changed.

The system should create motivation from the learner's actual memory state rather than from arbitrary gamification.

## Core Loop

**Open → Expedition → Recall → Event → Closure → Long-term memory history**

## Core Mechanics

### Expedition

The primary study-session container.

Expedition gives the learner visible progress, checkpoints, unresolved events, and a clear sense of completion.

All other interactive mechanics should integrate with Expedition rather than feel like separate mini-apps.

### Oracle

Before a review outcome is known, the system privately commits predictions about selected cards that the learner may fail to recall.

The prediction is revealed only after the learner answers.

The goal is to create curiosity and friendly competition without biasing recall.

### Rescue

Cards with declining or fragile memory strength may become Rescue opportunities.

Successful recall should visibly stabilize the memory.

Failure must not be framed as moral failure or punished.

### Nemesis

A small number of persistently difficult cards may become Nemesis cards.

Nemesis status should reflect real learning difficulty, not arbitrary point systems.

Defeating a Nemesis should require genuine improvement over time.

### Fragments

Mystery events discovered through study progress.

Fragments should reveal content grounded in the learner's own collection, memory history, or current learning state.

They must not behave like casino-style loot boxes.

### Relics

Highly stable, long-lived memories become Relics.

Relics provide long-term ownership, identity, and historical continuity.

They may become fractured if forgotten and later restored through learning.

### Memory World

A long-term visual representation of the learner's memory ecosystem.

The world must reflect real data rather than act as a decorative virtual pet.

## Non-Goals

Anki Alive is not intended to become:

- a generic RPG layered over Anki,
- a coin or XP economy,
- a streak-pressure system,
- a leaderboard-first product,
- a replacement for Anki's scheduling system,
- a system that blocks normal studying,
- a visual layer that slows down or distracts from recall.

## Product Invariants

The following principles are currently considered foundational:

1. **Again is never punished.**
2. **Fake Good/Easy answers must never be rewarded.**
3. **Gamification must reinforce recall rather than compete with it.**
4. **Memory data is the primary source of progression.**
5. **The learner must always be able to study normally.**
6. **Animations must not delay or obscure answering.**
7. **Focus Mode must reduce or disable motivational layers without breaking review flow.**
8. **Major product or architectural changes must be documented.**

## UX Direction

Current visual direction:

**Dark Arcane + Modern Minimal**

The interface should feel refined, atmospheric, and focused rather than childish or casino-like.

Desired qualities:

- strong typography,
- restrained glow and motion,
- clear hierarchy,
- intentional use of mystery,
- elegant data visualization,
- visually distinct mechanics that still share one design system.

The UI should feel like one coherent product.

## Development Model

The project is developed in phases.

Each phase should include:

**Spec → UI → Architecture → Implementation → Tests → UX Review → Performance → Handoff**

A phase is complete only when:

- the feature works,
- the UX is polished,
- tests are meaningful,
- performance is acceptable,
- recall integrity is preserved,
- documentation is updated,
- a handoff exists for the next phase.

## Current Roadmap

1. Phase 0 — Foundation
2. Phase 1 — Expedition
3. Phase 2 — Oracle
4. Phase 3 — Rescue
5. Phase 4 — Nemesis
6. Phase 5 — Fragments
7. Phase 6 — Relics
8. Phase 7 — Memory World
9. Final polish and release preparation

## Canonical Documentation

As the repository grows, project knowledge should live in files rather than chat history.

Future canonical documents are expected to cover:

- Product Vision
- Product Principles
- Design System
- Architecture
- Data Model
- Roadmap
- Decisions
- Backlog
- Testing
- Accessibility
- Performance
- Phase specifications
- Phase handoffs

## Current Status

**Stage:** Phase 1 close / Phase 2 preparation

**Implementation:** Expedition engineering scope is complete on `main`, including durable session ownership, review-driven progress, pause/resume, completion, Undo reconciliation, presentation orchestration foundation, Focus Mode, Reduced Motion handling, accessibility coverage, and performance evidence.

**Phase 1 close gate:** Core real-host gates pass. Two direct visual spot-checks remain before `docs/PHASE1_MANUAL_VALIDATION.md` can truthfully be marked PASS: light appearance and a substantially narrowed Today window.

**Current handoff:** `handoffs/PHASE_1_EXPEDITION_HANDOFF.md`

**Next phase:** Phase 2 — Oracle. Specification/architecture preparation may begin now; formal implementation entry should preserve the Phase 1 close gate and the pre-answer commitment/reveal-after-answer recall-integrity contract.
