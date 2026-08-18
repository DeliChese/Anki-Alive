# AGENTS.md

# Anki Alive — Agent Working Rules

This file defines mandatory working rules for AI assistants, coding agents, and contributors working inside the Anki Alive repository.

The purpose is continuity.

A new agent should be able to enter the repository, inspect the canonical documentation, and continue the project without relying on hidden chat history.

---

## 1. Read Before Editing

Before making meaningful changes, read:

1. `PROJECT.md`
2. `docs/01_PRODUCT_PRINCIPLES.md` if it exists
3. `docs/03_ARCHITECTURE.md` if it exists
4. `docs/04_DATA_MODEL.md` if it exists
5. the current phase specification
6. the latest relevant handoff
7. recent accepted decisions in `docs/06_DECISIONS.md` if it exists

If one of these files does not exist yet, do not invent its contents.

Use the existing canonical documents as the source of truth.

---

## 2. Protect Product Intent

Anki Alive exists to make genuine learning more compelling.

Do not silently introduce mechanics that reward superficial activity.

### Never

- punish the learner for pressing `Again`,
- reward arbitrary `Good` or `Easy` presses,
- encourage dishonest self-grading,
- introduce artificial XP or currency without an explicit product decision,
- create infinite engagement loops designed only to keep the user inside the add-on,
- block access to normal Anki reviewing,
- obscure Anki's core controls,
- turn difficult cards into shame or guilt mechanics,
- use excessive animation that delays recall,
- convert mystery rewards into casino-style loot systems.

### Prefer

- FSRS-backed or memory-history-backed progression,
- genuine recall outcomes,
- visible stability improvements,
- meaningful session completion,
- reversible and optional presentation layers,
- Focus Mode,
- restrained animation,
- learner-owned history and identity,
- data-derived events rather than arbitrary rewards.

---

## 3. Expedition Is the Primary Session Container

Unless an accepted architecture decision says otherwise:

- Expedition is the main motivational structure around review sessions.
- Oracle, Rescue, Nemesis, Fragments, and similar mechanics should integrate with Expedition.
- Avoid building isolated dashboards or mini-apps that fragment the experience.
- Long-term systems such as Relics or Memory World may have dedicated views, but they should still connect back to real review history.

---

## 4. Do Not Change Architecture Silently

If a task requires changing:

- module boundaries,
- persistent storage,
- state ownership,
- event contracts,
- data schemas,
- review hooks,
- rendering strategy,
- major dependency choices,

then:

1. identify the architectural impact,
2. update or propose an architecture decision,
3. preserve backward compatibility when practical,
4. document migration requirements.

Do not casually refactor foundational architecture while implementing a feature.

---

## 5. Scope Discipline

Each development phase has a defined scope.

When a good idea appears outside the current phase:

- do not immediately implement it,
- add it to the backlog,
- describe why it matters,
- note dependencies,
- return to the current phase.

Avoid scope creep disguised as polish.

---

## 6. Vertical Slice First

Prefer the smallest coherent end-to-end slice that proves the feature.

A useful order is:

1. domain behavior,
2. data flow,
3. minimal UI,
4. integration,
5. testing,
6. polish,
7. edge cases,
8. documentation.

Do not build large speculative frameworks for features that do not yet exist.

---

## 7. Recall Integrity Is a Quality Gate

Every motivational feature must answer:

> Does this make the learner more likely to perform honest recall?

If the answer is unclear, the design needs review.

A feature must not:

- reveal answer information before recall,
- bias the learner toward a grading button,
- reward dishonest grading,
- create pressure to avoid `Again`,
- interrupt concentration at critical recall moments.

Oracle predictions, for example, must be committed before the answer and revealed only after the learner responds.

---

## 8. UI and Visual Quality Are Part of Done

Do not treat visual polish as a final cleanup phase.

For each feature, consider:

- hierarchy,
- spacing,
- typography,
- motion,
- accessibility,
- dark/light compatibility,
- focus states,
- error states,
- empty states,
- loading states,
- reduced-motion behavior,
- performance.

A working feature with poor UX is not finished.

---

## 9. Motion Rules

Animations should support meaning.

Prefer motion for:

- reveal,
- transition,
- progress,
- state change,
- completion.

Avoid motion that:

- blocks answering,
- repeats excessively,
- adds latency,
- competes visually with the card,
- cannot be disabled.

Respect reduced-motion settings when they exist.

---

## 10. Focus Mode Must Remain First-Class

Users must be able to reduce motivational layers.

Focus Mode should:

- preserve normal review,
- suppress or minimize non-essential animation,
- reduce event interruptions,
- retain necessary progress information,
- never reduce scheduling quality.

Do not make Focus Mode feel like a degraded or punished version of the product.

---

## 11. Testing Expectations

New behavior should include meaningful tests where practical.

Prioritize tests for:

- state transitions,
- persistence,
- review event handling,
- grading integrity,
- deterministic selection logic,
- migration behavior,
- session resume behavior,
- failure recovery.

Do not rely only on manual visual testing for core logic.

---

## 12. Performance Expectations

Anki review flow must remain responsive.

Avoid:

- expensive synchronous work on every card,
- unnecessary database scans,
- repeated full-collection queries,
- blocking network calls,
- large UI rerenders during review.

Prefer cached, incremental, or precomputed data where appropriate.

Performance regressions in card review are high priority.

---

## 13. Documentation Rules

Important knowledge must live in the repository.

Do not leave significant decisions only in chat.

When appropriate, update:

- project documentation,
- architecture,
- data model,
- decision log,
- backlog,
- phase specification,
- handoff notes.

Documentation should explain **why**, not only **what**.

---

## 14. Decision Logging

When a significant decision is made, record:

- decision ID,
- status,
- context,
- decision,
- reasoning,
- consequences,
- alternatives considered if relevant.

Accepted decisions should be treated as constraints until intentionally changed.

---

## 15. Handoff Rules

At the end of a phase, create or update a handoff containing:

- completed scope,
- important implementation details,
- files changed,
- accepted decisions,
- tests completed,
- known issues,
- technical debt,
- deferred ideas,
- migration notes,
- next phase dependencies.

The next agent should not need the previous chat to continue.

---

## 16. Communication Style for Development Work

When reporting work:

- be concise but precise,
- identify assumptions,
- surface risks early,
- distinguish completed work from proposed work,
- avoid claiming tests passed unless they were actually run,
- avoid claiming a file was changed unless it was actually changed.

If blocked, state the exact blocker and provide the best next step.

---

## 17. Definition of Done

A phase or feature is not done until the relevant items below are satisfied:

- behavior is implemented,
- UX is coherent,
- visual treatment matches the design system,
- recall integrity is preserved,
- tests are meaningful,
- performance is acceptable,
- accessibility is considered,
- documentation is current,
- handoff is written.

---

## 18. Core Product Reminder

When uncertain, return to this principle:

> **The game is the memory itself.**

Anki Alive should make the learner care about remembering, not merely about interacting with the add-on.
