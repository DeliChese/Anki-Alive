# Anki Alive Development Skill

## Purpose

Use this skill whenever working on the Anki Alive repository.

This skill defines the operating procedure for design, implementation, debugging, testing, review, and phase handoff.

It should be used together with the repository's canonical documentation.

---

## 1. Role

Act as a senior cross-functional owner for:

- Anki add-on engineering,
- Python architecture,
- host integration,
- product design,
- UX,
- accessibility,
- testing,
- performance,
- durable-data safety.

Optimize for long-term product coherence, not local cleverness.

---

## 2. First Action

Before editing:

1. inspect `PROJECT.md`,
2. inspect `AGENTS.md`,
3. inspect relevant canonical docs,
4. inspect latest handoff,
5. inspect current source/tests,
6. verify current phase.

Never assume chat history is the source of truth.

---

## 3. Core Invariants

Always preserve:

### Learning

- `Again` is not punished.
- `Good/Easy` spam is not rewarded.
- recall is not biased by pre-answer UI.
- difficult cards become meaningful, not shameful.

### Product

- behavioral loops terminate in closure.
- mystery is truthful.
- no casino-style design.
- no mandatory streak dependency.
- Memory itself is the progression substrate.

### Host

- Anki scheduler is authoritative.
- review remains usable if optional systems fail.
- normal review can be used without gamification.

### UX

- reviewer stays quiet during recall.
- one prominent reveal per review boundary.
- Focus Mode remains first-class.

---

## 4. Architecture Workflow

When implementing a feature:

### A. Domain

Define:

- entity/state,
- lifecycle,
- inputs,
- outputs,
- invariants,
- failure modes.

### B. Data

Define:

- Anki-owned source data,
- Anki Alive-owned durable state,
- rebuildable projections,
- migration needs,
- policy version.

### C. Integration

Define:

- host hook(s),
- adapter behavior,
- compatibility risk,
- undo/reconciliation behavior.

### D. Application

Define:

- service/use case,
- event emissions,
- orchestration interaction.

### E. UI

Define:

- view model,
- reviewer timing,
- event priority,
- Focus Mode,
- reduced-motion behavior.

### F. Tests

Define:

- deterministic domain tests,
- persistence tests,
- integration tests,
- manual host checks,
- regression risks.

### G. Performance

Define:

- reviewer-path cost,
- query count,
- cache strategy,
- large-collection behavior.

---

## 5. Feature Acceptance Checklist

Before accepting a mechanic:

- [ ] grounded in real memory data
- [ ] preserves honest grading
- [ ] does not leak answer information
- [ ] creates meaningful user value
- [ ] has bounded closure
- [ ] works in Focus Mode
- [ ] explainable
- [ ] testable
- [ ] performant
- [ ] accessible
- [ ] documented

---

## 6. Domain Event Rule

Prefer domain events over direct feature coupling.

Good:

```text
ReviewAnswered
    ↓
Oracle resolves
    ↓
OraclePredictionResolved
    ↓
EventOrchestrator
```

Avoid:

```text
reviewer.py
    directly calls Oracle UI
    directly updates Fragment
    directly updates Nemesis
    directly writes history
```

---

## 7. Persistence Rule

Use sidecar storage for durable Anki Alive state.

Never modify Anki collection schema.

Do not store full card content by default.

Durable writes should include policy/schema versions where relevant.

---

## 8. Randomness Rule

Mystery must be deterministic or persisted when user trust depends on it.

If a result is supposedly predetermined:

- seed it,
- persist it,
- or commit it.

Reload must not secretly reroll outcomes.

---

## 9. Time Rule

Use injectable clocks in domain logic.

Store durable timestamps in UTC.

Store explicit local study-day identity where product behavior is day-based.

---

## 10. Undo Rule

Never assume observed review outcomes are permanent.

For review-derived durable transitions, define reconciliation behavior.

If undo semantics are not yet known, mark the path provisional and investigate before shipping.

---

## 11. UI Rule

During question/recall:

- no large reveal,
- no distracting motion,
- no mystery hint that biases answer.

After response:

- one primary reveal maximum,
- other events may queue/defer.

Follow the Arcane Memory Interface design system.

---

## 12. Generated Asset Rule

Generated assets are appropriate for:

- atmosphere,
- sigils,
- Relic concepts,
- Memory Core,
- World landmarks,
- texture.

They are not appropriate replacements for:

- buttons,
- typography,
- precision controls,
- core layout,
- small functional icons.

Generated assets must follow the asset bible in `02_DESIGN_SYSTEM.md`.

---

## 13. Performance Rule

Every reviewer-path operation must justify itself.

Before adding synchronous work to grading/question transitions:

- estimate cost,
- inspect query count,
- prefer precompute/cache,
- measure after implementation.

Reviewer responsiveness beats immediate spectacle.

---

## 14. Debugging Workflow

When fixing a bug:

1. reproduce,
2. identify state transition involved,
3. inspect persistence,
4. inspect relevant host event ordering,
5. isolate root cause,
6. implement smallest correct fix,
7. add regression test,
8. update docs if behavior/decision changed.

Do not mask inconsistent state with UI workarounds.

---

## 15. Migration Workflow

For schema changes:

1. define source schema,
2. define target schema,
3. preserve durable history,
4. write migration,
5. test fresh install,
6. test previous-version upgrade,
7. test failure path,
8. document schema version.

---

## 16. Review Workflow

When reviewing code or a PR, prioritize:

1. recall integrity
2. data safety
3. host compatibility
4. architecture boundaries
5. correctness
6. performance
7. accessibility
8. UX consistency
9. maintainability
10. style

Do not spend most review effort on cosmetic style while a lifecycle bug exists.

---

## 17. Phase Close Workflow

Before closing:

1. run tests,
2. run manual host scenarios,
3. measure performance where relevant,
4. review accessibility,
5. update docs,
6. update ADRs,
7. update backlog,
8. create handoff.

A phase without a handoff is not closed.

---

## 18. Out-of-Scope Rule

When something belongs later:

```text
capture → backlog → dependency note → return to phase
```

Do not implement future features "while already in the file."

---

## 19. Communication Rule

When reporting:

Use explicit labels when useful:

- Implemented
- Verified
- Measured
- Proposed
- Not tested
- Deferred
- Known issue

Never imply certainty that the repository does not support.

---

## 20. Final Quality Filter

Ask:

> Does this implementation make real learning more compelling without reducing trust, recall quality, or review responsiveness?

If not, revise.

---

# Skill North Star

> **Build the experience around memory truth, not around gamification shortcuts.**
