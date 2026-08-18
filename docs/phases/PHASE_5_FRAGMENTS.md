# PHASE_5_FRAGMENTS.md

# Anki Alive — Phase 5: Fragments

## 1. Phase Goal

Introduce bounded mystery and discovery into Anki Alive without creating a casino-style reward system.

Fragments should create the feeling:

> "Something meaningful is hidden in this session, and real study progress will reveal it."

Fragments exist to add anticipation and curiosity.

They must remain grounded in the learner's own memory state, history, and progression.

---

# 2. Phase Status

```text
Status: SPECIFIED
Phase: 5
Name: Fragments
Depends on: Phase 4 — Nemesis
Next phase: Phase 6 — Relics
```

---

# 3. Product Role

Fragments add a mystery layer to Expedition.

They are not currency.

They are not loot boxes.

They are not collectible junk.

A Fragment is a bounded hidden object/event that progresses through real review activity and eventually reveals meaningful memory-related content.

---

# 4. Core User Problem

Predictable review flows can become emotionally flat.

Even with Expedition, Oracle, Rescue, and Nemesis, the learner may eventually know exactly what kinds of events to expect.

Fragments introduce uncertainty.

The key is:

> uncertainty about what meaningful memory event will be revealed

not:

> uncertainty about whether the learner won a random prize

---

# 5. Behavioral Goal

Fragments should create:

- curiosity,
- anticipation,
- nearby completion,
- surprise,
- personal meaning.

The intended loop:

```text
Fragment discovered
    ↓
progress begins
    ↓
real reviews advance it
    ↓
signal strengthens
    ↓
Fragment becomes ready
    ↓
meaningful reveal
    ↓
closure
```

---

# 6. Critical Product Invariant

> **Fragment reveals must be grounded in real memory data, history, or meaningful learning progression.**

Allowed reveal examples:

- old memory resurfaced
- Nemesis milestone
- unusual recovery story
- Relic candidate preview
- meaningful historical statistic
- long-lived memory
- rare personal learning event

Not allowed:

- arbitrary gems
- coins
- random unrelated cosmetics
- purchasable rewards
- gambling-style rarity tiers

---

# 7. No Casino Design

Fragments must not use:

- loot box terminology
- spinning reels
- near-miss effects
- flashing rarity
- purchasable randomization
- "legendary drop" language
- time-limited purchase pressure

Mystery is about discovery.

Not gambling.

---

# 8. In Scope

Phase 5 includes:

- Fragment creation
- Fragment lifecycle
- deterministic or persisted identity
- progress
- ready state
- reveal
- reveal categories
- Expedition integration
- checkpoint integration
- EventOrchestrator integration
- history
- Focus Mode
- reduced motion
- accessibility
- migration
- testing
- performance
- crash recovery

---

# 9. Explicitly Out of Scope

Phase 5 does not implement:

- Relic system itself
- Memory World
- currency
- shop
- cosmetic economy
- loot rarity economy
- monetized randomness
- social trading
- gacha-style mechanics
- forced daily claim systems

---

# 10. Fragment Entity

Conceptual model:

```text
Fragment
- fragment_id
- expedition_id?
- local_study_date?

- created_at
- state
- reveal_type
- progress_current
- progress_target

- seed
- policy_version

- revealed_at?
- payload_ref?
- source_entity_refs?
- reconciliation_state?
```

---

# 11. Fragment Lifecycle

Recommended:

```text
HIDDEN
   ↓
DISCOVERED
   ↓
PROGRESSING
   ↓
READY
   ↓
REVEALED
   ↓
ARCHIVED
```

Additional states:

```text
INVALIDATED
ORPHANED
REVERSED
```

### HIDDEN

The Fragment exists but has not yet been surfaced.

### DISCOVERED

The learner knows a Fragment exists.

### PROGRESSING

Review progress advances it.

### READY

Reveal condition is satisfied.

### REVEALED

Meaningful content has been shown.

### ARCHIVED

Lifecycle complete.

---

# 12. Fragment Creation

Preferred initial creation points:

- Expedition start
- checkpoint planning
- Today screen initialization

Creation must occur before reveal content is known to the learner.

If random selection is involved:

- seed it,
- persist it,
- do not reroll on reload.

---

# 13. Fragment Identity

A Fragment should have stable identity.

Possible sources:

```text
fragment_id
seed
reveal_type
payload_ref
```

Once created:

> reopening Anki must not generate a different Fragment.

This is LOCKED.

---

# 14. Fragment Progress

Fragment progress should be tied to genuine session activity.

Recommended initial contract:

> Accepted review actions advance Fragment progress according to a stable policy.

Important:

- `Again` must not reduce Fragment progress.
- `Hard/Good/Easy` must not create higher progress merely because of rating.
- Fragment progression must not pressure self-grading.

Possible:

```text
1 accepted review = 1 progress unit
```

This is the safest initial design.

---

# 15. Variable Progress

A future design may use variable progress based on:

- card difficulty
- meaningful memory event
- checkpoint completion

However, any variable rule must not create grading bias.

Status: PROVISIONAL.

Default recommendation:

> simple session-progress advancement first.

---

# 16. Progress Target

Possible examples:

```text
10 reviews
18 reviews
25 reviews
```

The target should be:

- bounded,
- near enough to create anticipation,
- fixed once created,
- not silently extended.

Exact distribution is PROVISIONAL.

---

# 17. Fragment and Expedition

Fragments should usually live inside Expedition.

Possible model:

```text
1 primary Fragment per Expedition
```

or:

```text
0–2 depending on session size
```

Status: PROVISIONAL.

Do not flood sessions with mystery objects.

---

# 18. Checkpoint Integration

Fragments may:

- become discovered at a checkpoint,
- progress quietly between checkpoints,
- become ready near a checkpoint,
- reveal at checkpoint or completion.

This helps avoid interrupting reviewer flow.

---

# 19. Review-Boundary Integration

Small progress signals may occur after reviews.

Example:

```text
Fragment signal strengthened.
```

These should generally be ambient/minor.

Do not show a major reveal every few cards.

---

# 20. Reveal Categories

Fragments should draw from a meaningful reveal taxonomy.

Initial categories may include:

```text
MEMORY_FROM_PAST
ANCIENT_MEMORY
RECOVERY_STORY
NEMESIS_HISTORY
UNUSUAL_STAT
MILESTONE
RELIC_PRECURSOR
COLLECTION_HISTORY
```

Each category must map to real data.

---

# 21. Memory From Past

Possible reveal:

```text
A year ago today, you first learned this card.
```

Requirements:

- history must support the claim,
- wording must remain accurate,
- no fake anniversary.

---

# 22. Ancient Memory

Possible reveal:

```text
This memory has survived for 1,142 days.
```

Only if the historical meaning is real.

---

# 23. Recovery Story

Possible:

```text
You once failed this card repeatedly.
It has now remained stable for months.
```

Requires actual historical evidence.

---

# 24. Nemesis History

Possible:

```text
One of your former Nemeses has remained stable since defeat.
```

Requires Phase 4 history.

---

# 25. Unusual Stat

Possible:

```text
This was one of the oldest memories reviewed today.
```

Avoid meaningless novelty statistics.

A stat should feel personally relevant.

---

# 26. Milestone Reveal

Possible:

```text
You now have 500 memories with stability above the current long-term threshold.
```

Threshold wording must be explainable.

---

# 27. Relic Precursor

Before Phase 6:

Fragments may hint that a memory is approaching future long-term significance.

However:

- do not call something a Relic before Relic policy exists,
- do not fake Phase 6 behavior.

Safer pre-Phase-6 wording:

> This memory has become unusually stable.

---

# 28. Reveal Selection

Reveal selection should consider:

- significance
- recency
- novelty
- user history
- cooldown
- available data quality

Exact ranking is DEFERRED.

---

# 29. Reveal Quality Gate

Before a reveal is eligible, ask:

1. Is the fact true?
2. Is it meaningful?
3. Has it been shown recently?
4. Does it fit the Fragment's narrative tone?
5. Does it preserve privacy?
6. Does it avoid fake precision?

---

# 30. Fragment Discovery UX

Example:

```text
UNKNOWN FRAGMENT

Signal strength
██████░░░░
```

or:

```text
Fragment detected.
```

The learner should know:

- something exists,
- it can progress,
- it will reveal something meaningful.

They should not be told fake rarity.

---

# 31. Fragment Visual Grammar

Per design system:

**Geometry:** incomplete polygon / crystalline shard / suspended facets  
**Material:** translucent crystal / encoded object  
**Motion:** assemble / resonate / unlock  
**Mood:** curiosity / discovery / hidden meaning

Avoid:

- treasure chest
- coins
- slot reels
- explosive confetti
- flashy rarity colors

---

# 32. Signal Strength

Progress may be represented as:

```text
signal strength
```

This is a presentation metaphor.

The real domain value is Fragment progress.

Do not pretend signal strength is a scientific memory metric.

---

# 33. Ready State

When progress target is reached:

```text
FRAGMENT READY
```

The reveal may occur:

- immediately after the review,
- at next checkpoint,
- at Expedition completion.

Default recommendation:

> defer major reveal to a natural closure boundary when practical.

---

# 34. Reveal UX

Example:

```text
FRAGMENT RECOVERED

This memory was first learned
418 days ago.

You failed it 4 times during its first week.
It is now stable.
```

This is stronger than:

> You won 50 gems.

---

# 35. Reveal Closure

After reveal:

- Fragment lifecycle closes,
- no immediate surprise second Fragment is created,
- the learner may continue session normally.

No infinite mystery chain.

---

# 36. Focus Mode

Focus Mode preserves Fragment domain behavior.

Presentation may become:

```text
Fragment ready
```

and reveal can be:

- deferred to checkpoint,
- deferred to completion,
- shown as compact history card.

No large assemble animation.

---

# 37. Reduced Motion

Reduced motion:

- no rotating facets
- no shard assembly animation
- static progress
- fade-based reveal
- no pulse loop

---

# 38. Accessibility

Required:

- progress not color-only
- numeric/structural progress available
- keyboard dismissal
- reduced motion
- Focus Mode
- clear ready/revealed states

---

# 39. History

A revealed Fragment may create a HistoryEntry.

However:

- not every small progress event belongs in history,
- revealed meaningful content may be stored as narrative history.

---

# 40. Persistence

Phase 5 adds:

```text
fragments
```

Potential fields:

- fragment_id
- expedition_id
- local_study_date
- created_at
- state
- reveal_type
- progress_current
- progress_target
- seed
- policy_version
- payload_ref
- revealed_at

---

# 41. Payload Storage

Prefer references to durable history/entities over copying large content.

Examples:

```text
source_card_id
source_nemesis_id
source_milestone_id
```

Flexible summary metadata may use compact JSON.

Do not store full card content by default.

---

# 42. Migration

Phase 5 adds migration from Phase 4.

Tests:

- fresh install
- Phase 4 → Phase 5
- rollback/failure
- Nemesis/Rescue/Oracle/Expedition state preserved

---

# 43. Fragment Repository

Possible operations:

```text
create
get_active_for_expedition
advance
mark_ready
reveal
archive
invalidate
list_recent
```

No UI SQL.

---

# 44. Fragment Service

Responsibilities:

- creation
- progress
- reveal eligibility
- reveal selection
- payload preparation
- lifecycle
- history projection

Not responsibilities:

- scheduling
- Relic formation
- Nemesis scoring
- reviewer rendering

---

# 45. Determinism

This is critical.

Same Fragment + same persisted state:

> same reveal.

Reload must not reroll.

Crash must not reroll.

Opening/closing screen must not reroll.

---

# 46. Randomness Policy

Randomness may choose among eligible meaningful reveals.

However:

- seed must be stable,
- eligibility must be real,
- no fake rarity weighting,
- user cannot purchase rerolls.

---

# 47. Undo/Reversal

If a review advanced Fragment progress and is undone:

Fragment progress should reconcile.

Possible:

- decrement progress,
- mark source event reversed,
- recalculate from accepted Expedition progress.

Locked:

> Fragment progress must not permanently count undone review work.

---

# 48. Expedition Ends Early

If Expedition ends before Fragment is ready:

Possible options:

A. archive incomplete Fragment  
B. carry Fragment into next Expedition  
C. convert to historical incomplete state

Recommended initial behavior:

> Archive the Expedition-bound Fragment as incomplete.

Reason:

- preserves bounded closure,
- avoids permanent unresolved mystery.

Status: PROVISIONAL.

No punishment.

---

# 49. Cross-Day Behavior

No artificial daily reset while an Expedition remains legitimately resumable.

But an Expedition-bound Fragment should follow the Expedition lifecycle.

---

# 50. Multiple Events Same Boundary

Example:

- Oracle resolved
- Nemesis weakened
- Fragment became ready

EventOrchestrator must decide.

Potential:

```text
major Oracle reveal
Fragment ready becomes subtle signal
actual Fragment reveal deferred to checkpoint
```

This is the preferred use of orchestration.

---

# 51. Event Priority

Provisional future ordering:

```text
Nemesis defeat
Relic formation/restoration
Oracle major reveal
Rescue major recovery
Fragment reveal
Nemesis weakening
Fragment progress
ambient signals
```

Exact order may change.

---

# 52. Performance

Critical operations:

- per-review progress increment
- ready check
- payload lookup when reveal occurs

Heavy reveal candidate generation should happen:

- at Fragment creation,
- checkpoint,
- or outside hot path.

---

# 53. Performance Targets

Provisional:

```text
progress update:
preferred < 1 ms domain logic

ready check:
near-zero/simple threshold

reveal projection:
outside critical recall path when possible
```

Total reviewer overhead remains within global budget.

---

# 54. Large Collections

Reveal selection should not scan entire long-term history on every review.

Use:

- cached meaningful candidates
- indexed history
- bounded candidate pool
- precomputed milestones

---

# 55. Reveal Cooldown

Repeated reveal categories may need cooldown.

Example:

Do not show:

> oldest memory

three Expeditions in a row.

Cooldown policy is PROVISIONAL.

---

# 56. Fragment Rarity

Do not create commercial rarity tiers.

If internal significance levels are useful:

```text
common / rare
```

should not be user-facing by default.

Better:

```text
significance score
```

used only for selection.

Avoid loot language.

---

# 57. Testing Requirements

## Creation

- Fragment creates once
- identity stable
- seed stable
- no reroll after reload

## Progress

- accepted review advances
- Again advances equally
- Hard/Good/Easy advance equally
- duplicate review does not double-count
- undo reconciles

## Lifecycle

- hidden → discovered
- progressing
- ready
- revealed
- archived

## Reveal

- payload is real
- payload type valid
- same persisted Fragment reveals same content
- no fake unavailable data

## Expedition End

- incomplete handling works
- no punishment

## Cross-Feature

- Oracle overlap
- Rescue overlap
- Nemesis overlap
- EventOrchestrator deferral

## UX

- Focus Mode
- reduced motion
- keyboard
- no casino visuals/copy

---

# 58. Crash Recovery

### Case A

Fragment created, crash.

Expected:

- same Fragment returns.

### Case B

Progress advanced, crash before UI update.

Expected:

- durable/session state remains correct.

### Case C

Fragment ready, crash before reveal.

Expected:

- same reveal remains pending.

### Case D

Reveal persisted, crash before dismissal.

Expected:

- no reroll or duplicate history.

---

# 59. Manual Host Test

Minimum:

```text
1. Start Expedition.
2. Confirm Fragment identity created once.
3. Review cards with mixed ratings.
4. Confirm equal progress behavior.
5. Restart Anki.
6. Confirm same Fragment/progress.
7. Undo a review.
8. Confirm progress reconciliation.
9. Trigger ready state.
10. Trigger overlap with Oracle/Nemesis if test fixtures allow.
11. Confirm only one major reveal.
12. Reveal Fragment.
13. Restart.
14. Confirm reveal does not reroll.
15. Toggle Focus Mode.
16. End incomplete Expedition and confirm no penalty.
```

---

# 60. Success Metrics

Potential evaluation:

- Fragment discovery rate
- ready rate
- reveal rate
- incomplete Fragment rate
- category diversity
- repeat-category rate
- reveal dismissal time
- Focus Mode behavior
- session continuation after reveal

Do not optimize for maximum Fragment frequency.

---

# 61. Trust Risks

## Risk 1 — Loot Box Feel

Mitigation:

memory-centered reveals and restrained art.

## Risk 2 — Fake Randomness

Mitigation:

persisted seed/identity.

## Risk 3 — Meaningless Reveal

Mitigation:

reveal quality gate.

## Risk 4 — Grading Bias

Mitigation:

equal progress across ratings.

## Risk 5 — Infinite Curiosity Chain

Mitigation:

one bounded Fragment lifecycle and real closure.

---

# 62. Anti-Patterns

Do not implement:

### Treasure Chest

### Rarity Explosion

### Gem Rewards

### Paid Reroll

### Near-Miss Animation

### "Almost Legendary!"

### Rating Multiplier

```text
Easy = +3 Fragment energy
```

### Surprise Second Fragment Immediately After Reveal

---

# 63. Copy Tone

Preferred:

```text
Fragment detected.
Signal strengthened.
Fragment ready.
Fragment recovered.
A memory from your past.
An unusual memory surfaced.
```

Avoid:

```text
Loot acquired!
Epic drop!
Legendary!
Open now before it disappears!
```

---

# 64. Open Questions

## Q5-01 — Fragment Count per Expedition

Status: PROVISIONAL.

---

## Q5-02 — Progress Target Distribution

Status: PROVISIONAL.

---

## Q5-03 — Reveal Timing

Immediate vs checkpoint vs completion?

Status: UX TEST.

---

## Q5-04 — Incomplete Carry-Forward

Archive or carry?

Status: PROVISIONAL.

Default conservative answer: archive.

---

## Q5-05 — Reveal Ranking

How to balance significance, novelty, and diversity?

Status: DEFERRED.

---

## Q5-06 — Variable Progress

Should difficulty ever affect progress?

Status: RESEARCH.

Default: no.

---

# 65. Definition of Done

Phase 5 is complete when:

- [ ] Fragment entity exists
- [ ] creation is deterministic/persisted
- [ ] reload does not reroll
- [ ] progress target is fixed
- [ ] Again/Hard/Good/Easy advance equally
- [ ] duplicate review protection works
- [ ] undo reconciles
- [ ] lifecycle transitions work
- [ ] ready state persists
- [ ] reveal is meaningful and data-grounded
- [ ] reveal does not reroll
- [ ] no loot/currency system exists
- [ ] incomplete Expedition handling exists
- [ ] EventOrchestrator handles overlap
- [ ] Focus Mode works
- [ ] reduced motion works
- [ ] keyboard path works
- [ ] migration tested
- [ ] crash recovery tested
- [ ] performance measured
- [ ] manual host validation completed
- [ ] ADRs/backlog updated
- [ ] `PHASE_5_FRAGMENTS_HANDOFF.md` exists

---

# 66. Phase 6 Contract

Relics may begin only after Fragments proves:

- deterministic mystery works,
- history candidates can be selected safely,
- meaningful reveals can be generated from real memory data,
- event orchestration can defer major moments,
- long-term narrative history remains trustworthy.

Relics should reuse:

- history infrastructure
- significance scoring
- generated-asset rules
- event reveal surfaces
- deterministic visual identity primitives
- policy versioning

Relics must remain memory history, not arbitrary collectibles.

---

# 67. Locked vs Provisional Summary

## Locked

- Fragment reveal grounded in real memory/history
- no casino design
- no currency
- no rating-based progress bonus
- deterministic/persisted identity
- no reroll after reload
- bounded lifecycle
- real closure
- undo reconciliation
- EventOrchestrator controls overlap
- Focus Mode preserves logic

## Provisional

- Fragment count
- progress target
- exact reveal taxonomy
- reveal ranking
- reveal timing
- incomplete carry-forward
- category cooldown
- variable progress

---

# Phase 5 North Star

> **Use mystery to reveal the learner's own memory story, not to manufacture artificial rewards.**
