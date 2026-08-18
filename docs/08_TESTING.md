# 08_TESTING.md

# Anki Alive — Testing Strategy

## 1. Purpose

This document defines the testing strategy for Anki Alive.

The add-on interacts with a host application, persistent user state, review events, UI overlays, and scheduling-derived data.

Testing must therefore cover more than isolated functions.

The primary goals are:

- preserve review integrity,
- prevent data corruption,
- prevent migration failures,
- prevent state drift,
- preserve performance,
- make feature behavior deterministic where required.

---

## 2. Testing Principles

### T01 — Test Learning-Critical Logic First

Prioritize logic that can affect:

- recall flow,
- grading interpretation,
- session progress,
- persistent state,
- user trust.

### T02 — Prefer Deterministic Tests

Randomness should be seeded or injected.

Clock access should be injectable.

IDs should be controllable where useful.

### T03 — Test Domain Logic Without Anki

Core feature logic should be testable without launching the full host.

### T04 — Host Integration Still Needs Integration Tests

Unit tests cannot prove hook behavior.

### T05 — Migrations Are Production Code

Migration tests are mandatory once durable user data exists.

### T06 — Never Claim a Test Passed Unless It Was Run

Test documentation must distinguish:

- automated and run,
- automated but not run,
- manually verified,
- not yet tested.

---

## 3. Test Pyramid

Suggested layers:

```text
              ┌───────────────┐
              │ Manual / E2E  │
              └───────┬───────┘
                  Integration
              ┌───────┴───────┐
              │ Domain / Unit │
              └───────────────┘
```

Most logic should be covered at the domain/unit level.

Integration coverage should focus on boundaries.

Manual testing should focus on host behavior and visual quality.

---

## 4. Unit / Domain Tests

Test pure or near-pure logic such as:

- checkpoint generation,
- Expedition completion,
- candidate scoring,
- Oracle prediction resolution,
- Rescue eligibility,
- Nemesis lifecycle transitions,
- Fragment progression,
- Relic lifecycle,
- event orchestration priority,
- Focus Mode policy,
- projection creation.

Use fake clocks and seeded randomness.

---

## 5. Integration Tests

Integration tests should validate:

- Anki hook → internal event translation,
- repository behavior,
- SQLite transactions,
- migration execution,
- settings load/save,
- UI bridge message validation,
- lifecycle bootstrap/shutdown behavior.

Where a full Anki runtime is difficult to automate, build thin adapter tests and supplement with explicit manual host checks.

---

## 6. End-to-End / Host Tests

Critical host scenarios should eventually include:

- install add-on
- start Anki
- open collection
- begin review
- answer cards
- use undo
- interrupt session
- restart
- resume
- complete Expedition
- enable Focus Mode
- disable optional mechanic
- upgrade add-on version
- migration runs
- uninstall/reinstall behavior where relevant

These scenarios may begin as manual scripts and later become more automated where practical.

---

## 7. Review Integrity Tests

These are high-priority.

Validate that:

- Oracle does not reveal before answer,
- event UI does not cover card content during recall,
- feature progression cannot be gained solely through UI clicks,
- `Again` does not produce artificial punishment,
- `Good/Easy` spam does not trivially maximize rewards,
- Focus Mode does not alter scheduling,
- add-on failure does not prevent normal review.

---

## 8. Expedition Tests

### Core

- creates valid Expedition
- target count is valid
- progress increments correctly
- checkpoints trigger once
- completion triggers once
- pause/resume preserves progress
- restart recovery works
- abandoned sessions do not corrupt future sessions

### Edge Cases

- zero due cards
- target larger than available cards
- collection closed mid-session
- profile switched
- crash before first review
- crash near completion
- Focus Mode toggled mid-session

---

## 9. Oracle Tests

### Commitment Integrity

- prediction stored before answer
- persisted commitment survives reload
- result is not rerolled
- deterministic seed behavior works
- invalidated card does not produce fake result

### Resolution

- expected outcome resolved correctly
- actual grade is captured
- undo/reversal reconciles state
- session summary matches resolved predictions

### UX Contract

- reveal occurs post-answer
- suppressed reveal still preserves domain result

---

## 10. Rescue Tests

- eligibility policy identifies expected candidates
- fragile state is explainable
- success transitions correctly
- failure does not create punishment
- source card deletion is handled
- state change may invalidate stale Rescue
- Focus Mode suppresses flourish without losing state

---

## 11. Nemesis Tests

- promotion policy triggers correctly
- duplicate active Nemesis is prevented if policy requires uniqueness
- encounter counts are consistent
- defeat requires actual policy condition
- repeated Good alone cannot trivially defeat
- return state requires valid regression
- deleted card becomes orphaned/archived safely

---

## 12. Fragment Tests

- identity persists across reload
- seeded generation is deterministic
- progress cannot be advanced by unrelated UI actions
- ready state triggers correctly
- reveal occurs once
- reveal type is valid
- no accidental reroll on reopening screen

---

## 13. Relic Tests

- formation policy triggers correctly
- formation metadata is preserved
- fracture state is recoverable
- restoration works
- card deletion is handled
- historical formation remains after fracture
- visual/projection data is rebuildable

---

## 14. Memory World Tests

Focus on projections:

- grouping is deterministic
- large collection projection remains bounded
- cache invalidation works
- missing cards are tolerated
- world failure does not affect review
- simplified/accessibility projection works

---

## 15. Persistence Tests

Required once sidecar storage exists:

- create database
- reopen database
- transaction rollback
- schema version read/write
- corrupted optional cache recovery
- missing database creation
- unexpected shutdown safety
- WAL/journal strategy if used
- concurrent access assumptions

---

## 16. Migration Tests

Every migration should test:

- fresh install path
- previous schema → new schema
- migration idempotence where applicable
- rollback/failure behavior
- preservation of user history
- invalid/corrupt state behavior
- backup behavior if destructive migration exists

Maintain fixtures representing historical schema versions once public releases exist.

---

## 17. Settings Tests

Validate:

- defaults
- load
- save
- missing keys
- unknown future keys
- invalid values
- feature flags
- Focus Mode settings
- reduced motion settings

Settings migrations should be tested if configuration schema evolves.

---

## 18. Event Orchestration Tests

Critical scenarios:

- one major event
- multiple major events
- major + minor
- queue ordering
- Focus Mode suppression
- deferred checkpoint reveal
- session completion flush
- duplicate event prevention

The test should prove:

> At most one prominent reveal is surfaced per review boundary.

---

## 19. Compatibility Tests

For every explicitly supported Anki version:

- add-on loads
- hooks register
- review flow works
- webview bridge works
- settings work
- persistence works
- no known unsupported API path is used accidentally

Do not claim support for versions not tested.

---

## 20. UI Component Tests

Where practical, test:

- view model → rendered state
- empty state
- error state
- loading state
- Focus Mode state
- reduced motion state
- keyboard focus behavior

Pixel-perfect snapshot testing may be useful selectively, but should not replace behavior tests.

---

## 21. Accessibility Tests

Manual or automated checks should validate:

- keyboard-only path
- focus visibility
- non-color status distinction
- reduced-motion behavior
- readable contrast
- dismissible event reveal
- text scaling
- Focus Mode coherence

---

## 22. Performance Tests

Performance testing should cover:

- review hook overhead
- event publication
- sidecar write cost
- candidate ranking
- Today screen load
- large history rendering
- Relic Vault scale
- Memory World projection

See `10_PERFORMANCE.md` for budgets and methodology.

---

## 23. Data Privacy Tests

Validate that default logs do not contain:

- card question text
- card answer text
- typed answers
- media content

Diagnostics should use IDs and numeric state by default.

---

## 24. Test Data Builders

Create reusable builders/factories for:

- fake card reference
- memory snapshot
- review observation
- expedition
- oracle prediction
- rescue
- nemesis
- fragment
- relic

Avoid repetitive hand-built dictionaries in every test.

---

## 25. Time Testing

Time-sensitive systems should use an injectable clock.

Test:

- UTC persistence
- local study date
- crossing midnight
- timezone change
- DST-like offset change where relevant
- resumed sessions on a later calendar date

Do not directly call wall-clock time deep inside domain logic.

---

## 26. Randomness Testing

Mystery features must use injected or persisted randomness.

Test:

- same seed → same result
- persisted commitment wins over new seed
- restart does not reroll
- different seed can produce different candidate order when expected

---

## 27. Undo Tests

Undo behavior must be explicitly tested once implementation details are known.

Potential cases:

- undo ordinary review
- undo Oracle-target review
- undo Rescue resolution
- undo Nemesis encounter
- undo review that completes Expedition
- redo/re-answer if host supports relevant flow

State should reconcile rather than silently diverge.

---

## 28. Crash Recovery Tests

Simulate interruption at meaningful points:

- after Expedition created
- after Oracle committed
- after review observed
- before presentation shown
- after persistence write
- before checkpoint reveal
- before Expedition completion summary

On restart:

- domain state should be valid
- presentation state may recover or safely suppress
- Anki review state remains authoritative

---

## 29. Manual UX Test Script

Each phase should include a short manual review script.

Example structure:

```text
1. Fresh profile
2. Existing profile with large deck
3. Begin Expedition
4. Review 20+ cards
5. Trigger feature
6. Toggle Focus Mode
7. Resize window
8. Use keyboard only
9. Interrupt and resume
10. Verify completion
```

The script should be updated per phase.

---

## 30. Bug Regression Policy

Any fixed bug involving:

- data loss,
- state corruption,
- review integrity,
- migrations,
- crash recovery,
- duplicate events,
- user-visible incorrect history

should receive a regression test where practical.

---

## 31. CI Expectations

Once repository implementation begins, CI should eventually run:

- formatting/linting
- unit tests
- integration tests that do not require full desktop host
- migration tests
- type checking if adopted
- package/build validation

Host-version matrix testing may require a separate strategy.

---

## 32. Test Naming

Prefer behavior-oriented names.

Good:

```text
test_oracle_prediction_survives_restart_before_resolution
test_again_does_not_reduce_fragment_progress_reward
test_expedition_completion_emits_once
```

Avoid:

```text
test_func_1
test_oracle_basic
```

---

## 33. Phase Exit Test Report

Before closing a phase, record:

- test suites run
- result
- manual scenarios run
- supported host versions tested
- performance checks run
- known gaps

Do not write "all tests pass" without evidence.

---

# Testing North Star

> **If a feature can affect user trust, memory state, or session continuity, it deserves a test.**
