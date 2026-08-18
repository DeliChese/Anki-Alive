# PHASE_4_NEMESIS.md

# Anki Alive — Phase 4: Nemesis

## 1. Phase Goal

Turn persistently difficult cards into long-term, meaningful challenges grounded in real learning difficulty.

Nemesis should create the feeling:

> "This card has beaten me repeatedly. I want to finally conquer it."

The feature must make difficult material more interesting to engage with.

It must not reward dishonest grading, create shame, or reduce learning quality.

---

# 2. Phase Status

```text
Status: SPECIFIED
Phase: 4
Name: Nemesis
Depends on: Phase 3 — Rescue
Next phase: Phase 5 — Fragments
```

---

# 3. Product Role

Nemesis is a persistent memory-level mechanic.

It is not a one-session boss.

A Nemesis may:

- emerge after repeated evidence of difficulty,
- appear across multiple Expeditions,
- weaken as the learner genuinely improves,
- eventually be defeated,
- potentially return after real regression.

This gives Anki Alive a long-term challenge loop based on genuine learning history.

---

# 4. Core User Problem

Some cards are repeatedly difficult:

- multiple lapses,
- slow recall,
- low stability growth,
- repeated Again,
- unusually persistent difficulty.

In standard Anki, these cards may feel like annoying failures.

Nemesis reframes them as:

> "This is a challenge with history."

The goal is not to glorify failure.

The goal is to make hard material feel worth confronting.

---

# 5. Behavioral Goal

Nemesis should create:

- challenge,
- persistence,
- mastery,
- identity,
- meaningful long-term victory.

The intended emotional arc is:

```text
repeated difficulty
    ↓
recognition
    ↓
Nemesis promotion
    ↓
future encounters
    ↓
real improvement
    ↓
weakening
    ↓
defeat
    ↓
historical victory
```

Not:

```text
card appears
    ↓
Good button
    ↓
-20 HP
```

---

# 6. Critical Product Invariant

> **A Nemesis can only be defeated through genuine memory improvement over time.**

This is LOCKED.

A single grade must never instantly defeat a Nemesis.

---

# 7. No Fake HP

Nemesis may use a visual strength meter.

However, it must represent a meaningful derived memory state.

Do not implement arbitrary boss HP such as:

```text
100 HP
Good = -20
Easy = -35
Again = +15
```

That system would pressure grading.

If a strength bar exists, it should map to real factors such as:

- stability,
- difficulty,
- lapse trend,
- successful future recalls,
- recovery over time.

---

# 8. In Scope

Phase 4 includes:

- Nemesis candidate detection
- promotion policy
- persistent lifecycle
- encounter history
- weakening state
- defeat
- optional future return foundation
- Nemesis strength projection
- history
- explanation
- Expedition integration
- Rescue interaction
- Oracle interaction
- undo reconciliation
- deletion/orphan handling
- Focus Mode
- reduced motion
- accessibility
- migration
- testing
- performance profiling

---

# 9. Explicitly Out of Scope

Phase 4 does not implement:

- fantasy characters
- actual combat minigames
- damage numbers based on grading
- equipment
- currency
- boss loot
- leaderboard
- Fragment system
- Relic system
- Memory World
- artificial "rage mode"
- permanent punishment

---

# 10. Nemesis Entity

Conceptual model:

```text
Nemesis
- nemesis_id
- card_id

- promoted_at
- promotion_policy_version
- promotion_reason

- state
- encounter_count
- successful_encounters
- failed_encounters

- peak_difficulty_score?
- current_strength_score?
- strength_projection_version?

- weakened_at?
- defeated_at?
- returned_at?
- archived_at?

- last_source_review_id?
- reconciliation_state?
```

---

# 11. Nemesis Lifecycle

Recommended lifecycle:

```text
CANDIDATE
   ↓
ACTIVE
   ↓
WEAKENING
   ↓
DEFEATED
```

Possible later states:

```text
RETURNED
ORPHANED
ARCHIVED
REVERSED
```

### CANDIDATE

Card meets early difficulty signals but has not yet earned Nemesis status.

### ACTIVE

Card is an active Nemesis.

### WEAKENING

Memory metrics show real improvement but defeat threshold is not yet satisfied.

### DEFEATED

Policy-defined durable improvement has occurred.

### RETURNED

A previously defeated Nemesis regressed enough to return.

### ORPHANED

Card no longer exists.

### ARCHIVED

Lifecycle is historical and no longer active.

---

# 12. Promotion Philosophy

Nemesis status should be rare enough to feel meaningful.

A card should not become Nemesis merely because:

- it received one Again,
- it is difficult once,
- it has a high difficulty value without history.

Promotion should require persistent evidence.

---

# 13. Promotion Inputs

Potential inputs:

- lapse count
- recent lapse frequency
- repeated Again history
- stability growth
- difficulty
- response time
- repeated short intervals
- Rescue history
- age/history depth

Exact formula is DEFERRED.

Locked:

- promotion is evidence-based,
- promotion is explainable,
- promotion policy is versioned,
- repeated difficulty matters more than one bad review.

---

# 14. Promotion Score

Conceptual:

```text
nemesis_score = f(
    lapses,
    recent_failures,
    difficulty,
    stability_growth,
    review_history,
    response_time?
)
```

This is a derived score.

Do not present it as native Anki truth.

---

# 15. Candidate Pool

Nemesis selection should not scan the full collection per review.

Preferred:

- precompute candidates outside hot path,
- update incrementally after relevant reviews,
- maintain bounded active set.

---

# 16. Number of Active Nemeses

Nemesis should be scarce.

Possible initial design:

```text
1 primary Nemesis
plus a small archived/secondary set
```

Alternative:

```text
up to 3 active Nemeses
```

Status: PROVISIONAL.

The concept should avoid turning every hard card into a boss.

---

# 17. Primary Nemesis

One particularly difficult card may be designated the primary Nemesis.

Potential UX:

```text
CURRENT NEMESIS

Anterior spinothalamic tract

Encounters: 14
Current state: Weakening
```

Whether Phase 4 ships a single-primary or small-pool model is PROVISIONAL.

---

# 18. Encounter

A Nemesis encounter occurs when the learner naturally reviews the card.

Do not schedule extra forced boss reviews outside Anki.

Nemesis follows Anki's review schedule.

---

# 19. Pre-Answer Presentation

Nemesis identity may be visible before recall.

Unlike Oracle, revealing Nemesis status does not leak prediction information.

However, it may affect anxiety and response behavior.

Possible initial presentation:

```text
NEMESIS
```

as a subtle label before the card.

Alternative:

Reveal only after answer.

Status: UX RESEARCH.

Default recommendation:

> A restrained pre-answer identity marker may be allowed because Nemesis is a known persistent identity, not a hidden prediction.

It must not contain answer-relevant hints.

---

# 20. Encounter Result

After grading, Nemesis state may update.

Important:

The grade itself does not directly deal "damage."

Instead:

1. Anki updates scheduling state.
2. Memory Engine observes new state.
3. Nemesis service evaluates meaningful change.
4. Nemesis projection updates.

---

# 21. Strength Projection

Nemesis may have a visible strength representation.

Example:

```text
NEMESIS STRENGTH
████████░░
```

This is allowed only if the strength metric is meaningful and explainable.

Potential meaning:

- relative distance from defeat criteria,
- normalized difficulty/stability recovery state.

Exact mapping is DEFERRED.

---

# 22. Weakening

A Nemesis enters WEAKENING when memory evidence improves meaningfully.

Examples:

- stability increases across reviews,
- lapse frequency falls,
- successful recalls accumulate,
- difficulty trend improves.

One successful recall may contribute but should not guarantee WEAKENING.

---

# 23. Defeat

Defeat is a long-term event.

Potential criteria:

- stability exceeds threshold,
- sustained successful recalls,
- sufficient time survived without lapse,
- difficulty normalized,
- combination of the above.

Exact defeat policy is DEFERRED.

Locked:

> Defeat must require durable evidence.

---

# 24. No Rating Shortcut

Forbidden:

```text
Easy = massive Nemesis damage
Good = normal damage
Again = Nemesis heals
```

This directly biases grading.

Allowed:

A user's honest grade affects Anki scheduling.

Later memory state may change Nemesis strength.

---

# 25. Failure Encounter

If the learner presses Again:

Preferred framing:

```text
NEMESIS HOLDS

This memory is still resisting.
```

or simply:

```text
Nemesis remains active.
```

Avoid:

```text
YOU LOST
Nemesis destroyed you
```

Failure should create persistence, not shame.

---

# 26. Successful Encounter

Possible feedback:

```text
NEMESIS WEAKENING

Stability improved.
```

If state did not meaningfully change:

```text
Encounter recorded.
```

Do not invent weakening just because the user pressed Good.

---

# 27. Defeat Reveal

This should be one of the more meaningful long-term events.

Example:

```text
NEMESIS DEFEATED

14 encounters
9 prior failures
Current stability: 92 days

You finally stabilized this memory.
```

Only show real metrics.

---

# 28. Defeat as Historical Milestone

Nemesis defeat should create durable history.

Potential milestone:

```text
NEMESIS_DEFEATED
```

This may later appear in:

- Memory Museum
- Memory World
- Relic history
- Time Machine

---

# 29. Nemesis Return

A defeated Nemesis may return only after real memory regression.

Potential conditions:

- new lapse after long stability,
- significant stability collapse,
- repeated failure after defeat.

Status: PROVISIONAL.

Locked:

> Return cannot be artificial or scheduled for drama.

No:

> Nemesis returns every 30 days.

---

# 30. Return UX

Possible:

```text
NEMESIS RETURNED

A memory you once conquered has become unstable again.
```

This should feel meaningful, not punitive.

---

# 31. Rescue Relationship

Rescue and Nemesis overlap conceptually.

Rescue means:

> memory is fragile now.

Nemesis means:

> memory has a persistent history of difficulty.

A Nemesis may also become a Rescue.

Do not merge the entities.

They represent different concepts.

---

# 32. Oracle Relationship

A Nemesis may also be an Oracle prediction target.

This is allowed.

Potential combined event after review:

```text
ORACLE DEFEATED
NEMESIS WEAKENING
```

But only one prominent reveal.

EventOrchestrator controls presentation.

---

# 33. Event Priority

Provisional major-event priority:

```text
Nemesis defeat
Relic formation/restoration
Oracle reveal
Rescue major recovery
Nemesis weakening
Fragment progress
ambient signals
```

Future phases may revise this.

Locked:

- one prominent reveal per review boundary.

---

# 34. Domain Events

Phase 4 may add:

```text
NemesisCandidateDetected
NemesisPromoted
NemesisEncountered
NemesisStrengthChanged
NemesisWeakening
NemesisDefeated
NemesisReturned
NemesisOrphaned
NemesisReversed
```

---

# 35. Persistence

Phase 4 adds durable table:

```text
nemeses
```

Optional supporting table if justified:

```text
nemesis_encounters
```

However, avoid duplicating review history unnecessarily.

An encounter table should exist only if it stores Nemesis-specific meaning.

---

# 36. Migration

Phase 4 adds migration from Phase 3.

Tests:

- fresh install
- Phase 3 → Phase 4
- rollback/failure
- Rescue/Oracle/Expedition state preserved

---

# 37. Nemesis Repository

Possible operations:

```text
create_candidate
promote
get_active_for_card
list_active
record_transition
mark_weakening
defeat
return_nemesis
orphan
archive
```

No UI SQL.

---

# 38. Nemesis Service

Responsibilities:

- candidate evaluation
- promotion
- lifecycle transition
- strength projection
- defeat evaluation
- return evaluation
- history projection
- explanation metadata

Not responsibilities:

- scheduling
- review rendering
- Rescue policy
- Oracle scoring

---

# 39. Memory Engine Dependency

Nemesis requires stable normalized access to:

- lapses
- recent review outcomes
- stability
- difficulty
- interval
- possibly response time
- long-term trend

This should reuse the Memory Engine created/refined in Rescue.

Do not build a second history-analysis system.

---

# 40. Explainability

User should be able to understand:

> Why did this card become a Nemesis?

Possible explanation:

```text
This memory became a Nemesis because it remained unusually difficult over time.

Signals:
• repeated lapses
• low stability growth
• frequent recent failures
```

Only show used signals.

---

# 41. Scientific Wording

Avoid:

> This is your worst brain weakness.

Prefer:

> This card has been unusually difficult to retain.

Avoid:

> Enemy strength: 83 scientifically.

Prefer:

> Nemesis strength reflects how far this memory is from the current defeat criteria.

---

# 42. Visual Grammar

Per design system:

**Geometry:** angular shard / crest / fracture  
**Material:** obsidian / compressed mineral  
**Motion:** pressure / fracture / weakening  
**Mood:** challenge / resistance / earned victory

Avoid:

- monsters
- swords
- gore
- fantasy boss portraits
- aggressive flashing

The "enemy" is the difficult memory, not a fictional creature.

---

# 43. Encounter Visual

Pre-answer if enabled:

```text
NEMESIS
```

subtle sigil.

Post-answer:

```text
NEMESIS WEAKENING
```

or:

```text
NEMESIS REMAINS
```

Defeat:

larger event reveal.

---

# 44. Focus Mode

Focus Mode preserves all Nemesis domain behavior.

Presentation:

```text
Nemesis · active
Nemesis · weakening
Nemesis · defeated
```

Minimal animation.

No dramatic encounter transition.

---

# 45. Reduced Motion

Reduced motion:

- no fracture animation
- no pressure pulse
- static state change
- short fade
- no continuous glow

---

# 46. Accessibility

Required:

- Nemesis state not color-only
- challenge framing without aggression
- keyboard dismissal
- reduced motion
- Focus Mode
- readable strength representation
- no flashing

---

# 47. Long-Term History

Nemesis history may include:

- promoted date
- encounter count
- failed encounters
- successful encounters
- weakening date
- defeat date
- return history

Avoid storing redundant full review history.

---

# 48. Encounter Counting

Encounter should correspond to a valid review of the Nemesis card.

Duplicate host events must not create duplicate encounters.

Undo should reconcile encounter state where relevant.

---

# 49. Undo/Reversal

If a review caused:

- weakening
- defeat
- return

and that review is undone:

Nemesis state must reconcile.

Locked:

> A Nemesis cannot remain defeated if the causal evidence was reversed and defeat policy no longer holds.

---

# 50. Card Deletion

If source card is deleted:

- mark ORPHANED
- preserve meaningful history
- no crash
- no retained full card content by default

---

# 51. Cross-Session Behavior

Nemesis persists across Expeditions.

This is LOCKED.

Nemesis is memory-level identity.

---

# 52. Cross-Day Behavior

No midnight reset.

No artificial daily boss cycle.

---

# 53. Promotion Frequency

Avoid promoting several Nemeses at once.

Potential rules:

- one promotion event per Expedition,
- promotion cooldown,
- bounded active pool.

Status: PROVISIONAL.

---

# 54. Nemesis Fatigue

Risk:

The same card appears often and Nemesis label becomes annoying.

Mitigations:

- restrained pre-answer marker
- cooldown on large reveals
- major animation only on state transitions
- ordinary encounters remain quiet

---

# 55. Defeat Frequency

Defeat should be rare enough to feel earned.

Do not tune criteria merely to manufacture frequent celebrations.

---

# 56. Performance

Critical operations:

- candidate update
- per-review active Nemesis lookup
- strength transition
- defeat evaluation

Preferred:

```text
Review:
indexed lookup by card_id
small state calculation
small persistence write if transition occurs
```

Heavy candidate scoring happens outside hot path.

---

# 57. Performance Targets

Provisional:

```text
active Nemesis lookup:
preferred < 1 ms

transition evaluation:
preferred < 2 ms

reviewer total:
within global budget
```

Long-term candidate recomputation may be batched.

---

# 58. Large Collection Strategy

Nemesis candidate analysis should:

- use bounded recent-history windows where valid,
- use cached summaries,
- update incrementally,
- avoid scanning all revlog data frequently.

Exact optimization depends on implementation profiling.

---

# 59. Testing Requirements

## Promotion

- persistent difficulty promotes
- one bad review does not promote
- policy version stored
- duplicate promotion prevented

## Lifecycle

- candidate → active
- active → weakening
- weakening → defeated
- defeated → returned if real regression
- orphan
- archive

## Honest Grading

- no direct damage from Good/Easy
- Again does not create arbitrary punishment
- defeat cannot occur from one grade alone

## Persistence

- restart preserves Nemesis
- migration works
- defeat persists
- return persists

## Undo

- weakening reverses if required
- defeat reconciles
- encounter count reconciles if source review removed

## Cross-Feature

- Rescue + Nemesis
- Oracle + Nemesis
- event orchestration

## UX

- restrained pre-answer marker if enabled
- Focus Mode
- reduced motion
- no aggressive copy

---

# 60. Crash Recovery

Test:

### Case A

Nemesis promotion persisted, crash before reveal.

Expected:

- state remains active
- reveal can defer safely

### Case B

Defeat transition persisted, crash before presentation.

Expected:

- history remains correct
- no duplicate defeat event

### Case C

Review recorded, crash before transition write.

Expected:

- reconciliation detects current memory state on restart if needed.

---

# 61. Manual Host Test

Minimum:

```text
1. Prepare candidate with difficult history.
2. Confirm one bad review alone does not promote.
3. Trigger promotion.
4. Restart Anki.
5. Confirm Nemesis remains active.
6. Encounter card.
7. Press Again.
8. Confirm no arbitrary punishment.
9. Encounter in later review.
10. Recall successfully.
11. Confirm only real state improvement changes strength.
12. Trigger weakening.
13. Trigger defeat under test conditions.
14. Undo causal review if supported.
15. Confirm reconciliation.
16. Toggle Focus Mode.
17. Test overlap with Oracle/Rescue.
18. Delete source card in test profile.
19. Confirm orphan handling.
```

---

# 62. Success Metrics

Potential evaluation:

- active Nemesis count
- time from promotion to defeat
- encounter count
- defeat rate
- return rate
- repeated lapse improvement
- user engagement with difficult cards
- Focus Mode behavior

Do not optimize for creating more Nemeses.

---

# 63. Trust Risks

## Risk 1 — Fake Boss Mechanics

Mitigation:

strength maps to real memory state.

## Risk 2 — Grading Bias

Mitigation:

no button damage.

## Risk 3 — Shame

Mitigation:

neutral challenge language.

## Risk 4 — Too Many Nemeses

Mitigation:

scarcity and promotion threshold.

## Risk 5 — Arbitrary Return

Mitigation:

real regression only.

---

# 64. Anti-Patterns

Do not implement:

### HP Damage by Rating

```text
Easy = -30 HP
Again = +20 HP
```

### Forced Boss Review

Extra reviews outside scheduler.

### Fantasy Monster Art

The difficult memory itself is the Nemesis.

### Public Failure Counter

Designed to shame.

### Daily Boss Reset

Artificial schedule.

### Boss Loot

Unrelated reward economy.

---

# 65. Copy Tone

Preferred:

```text
Nemesis detected.
Nemesis active.
Nemesis weakening.
Nemesis remains.
Nemesis defeated.
Nemesis returned.
This memory has been unusually difficult to retain.
```

Avoid:

```text
Boss fight!
You got destroyed!
Critical hit!
Finish him!
```

---

# 66. Open Questions

## Q4-01 — Promotion Formula

Status: DEFERRED.

---

## Q4-02 — Active Nemesis Count

One primary vs small pool?

Status: PROVISIONAL.

---

## Q4-03 — Strength Projection

What normalized metric best represents progress?

Status: DEFERRED.

---

## Q4-04 — Defeat Criteria

How much durable improvement is enough?

Status: DEFERRED.

---

## Q4-05 — Pre-Answer Marker

Should Nemesis identity be shown before recall?

Status: UX RESEARCH.

---

## Q4-06 — Return Threshold

When should a defeated Nemesis return?

Status: DEFERRED.

---

## Q4-07 — Encounter Table

Do we need dedicated Nemesis encounter rows, or can history/milestones suffice?

Status: IMPLEMENTATION DECISION.

---

# 67. Definition of Done

Phase 4 is complete when:

- [ ] Nemesis candidate policy exists
- [ ] one bad review cannot promote by itself
- [ ] policy version stored
- [ ] active Nemesis state persists
- [ ] encounter tracking works
- [ ] strength projection is meaningful/explainable
- [ ] no rating-based damage system exists
- [ ] Again creates no arbitrary punishment
- [ ] weakening requires actual improvement
- [ ] defeat requires durable improvement
- [ ] defeat persists
- [ ] return, if implemented, requires real regression
- [ ] cross-session behavior works
- [ ] no midnight reset
- [ ] undo/reversal reconciles
- [ ] deletion/orphan handling works
- [ ] Rescue overlap works
- [ ] Oracle overlap works
- [ ] EventOrchestrator prevents stacked major reveals
- [ ] Focus Mode works
- [ ] reduced motion works
- [ ] keyboard path works
- [ ] migration tested
- [ ] crash recovery tested
- [ ] performance measured
- [ ] manual host validation completed
- [ ] ADRs/backlog updated
- [ ] `PHASE_4_NEMESIS_HANDOFF.md` exists

---

# 68. Phase 5 Contract

Fragments may begin only after Nemesis proves:

- persistent long-term memory identities work,
- cross-feature overlap is orchestrated,
- history infrastructure can record meaningful milestones,
- memory-derived progression can remain honest over multiple sessions,
- major state transitions can produce polished reveals without harming review flow.

Fragments should reuse:

- Expedition checkpoints
- EventOrchestrator
- deterministic seed infrastructure
- history/milestone services
- design-system event surfaces
- Focus Mode presentation rules

Fragments must not become a separate reward economy.

---

# 69. Locked vs Provisional Summary

## Locked

- Nemesis represents persistent real difficulty
- no rating-based HP/damage
- defeat requires genuine long-term improvement
- Again is not punished
- no forced reviews outside scheduler
- persists across Expeditions
- no midnight reset
- return requires real regression
- undo reconciles
- one prominent reveal per boundary
- difficult memory itself is the "enemy"

## Provisional

- promotion formula
- active count
- strength metric
- defeat threshold
- return threshold
- pre-answer marker
- encounter storage shape
- exact reveal animation

---

# Phase 4 North Star

> **Turn persistent difficulty into a challenge worth conquering, without turning honest grading into combat mechanics.**
