# PHASE_3_RESCUE.md

# Anki Alive — Phase 3: Rescue

## 1. Phase Goal

Turn fragile or declining memories into meaningful recovery opportunities grounded in real memory state.

Rescue should create the feeling:

> "This memory is becoming fragile. I still have a chance to stabilize it."

The feature must create urgency without anxiety, guilt, fake scarcity, or punishment.

Rescue is the first mechanic whose emotional core is recovery.

---

# 2. Phase Status

```text
Status: SPECIFIED
Phase: 3
Name: Rescue
Depends on: Phase 2 — Oracle
Next phase: Phase 4 — Nemesis
```

---

# 3. Product Role

Rescue creates a memory-health micro-loop inside Expedition.

The intended loop is:

```text
fragility detected
    ↓
Rescue opportunity created
    ↓
learner encounters the card normally
    ↓
recall outcome occurs
    ↓
memory state changes
    ↓
Rescue resolves or continues
    ↓
history records recovery
```

Rescue does not replace Anki scheduling.

It interprets memory state that already exists.

---

# 4. Core User Problem

Anki can tell the scheduler that a memory is weakening, but the learner often experiences only:

> another due card

This misses an emotional opportunity.

A card that is close to forgetting is meaningfully different from a routine stable review.

Rescue makes that distinction visible.

---

# 5. Behavioral Goal

Rescue should create:

- urgency grounded in real memory state,
- a desire to recover knowledge,
- satisfaction from stabilization,
- acceptance of failure as useful information,
- long-term memory-health awareness.

The emotional arc should be:

```text
fragility
  ↓
attention
  ↓
honest recall
  ↓
stabilization or continued weakness
  ↓
recovery path
```

Not:

```text
fragility
  ↓
panic
  ↓
pressure to press Good
```

---

# 6. Critical Product Invariant

> **Failure must never be punished.**

If the learner presses `Again` on a Rescue card:

- no points are lost,
- no reward is destroyed,
- no shame message appears,
- no arbitrary timer becomes harsher.

The result should simply indicate:

> the memory remains fragile and needs future recovery.

---

# 7. Urgency Must Be Real

Rescue may use urgency only when it corresponds to real memory state.

Allowed:

> This memory is fragile.

Not allowed:

> Rescue this before midnight or lose it forever.

There is no artificial countdown.

There is no fake expiry timer.

---

# 8. In Scope

Phase 3 includes:

- fragile-memory detection
- Rescue eligibility
- Rescue lifecycle
- Rescue state persistence
- post-answer Rescue result
- stabilization feedback
- history
- candidate ranking
- explainability
- undo reconciliation
- card deletion/orphan handling
- Expedition integration
- EventOrchestrator integration
- Focus Mode
- reduced motion
- accessibility
- performance profiling
- migration
- testing

---

# 9. Explicitly Out of Scope

Phase 3 does not implement:

- Nemesis
- Fragments
- Relics
- Memory World
- loss penalties
- artificial timers
- external notifications
- email/push rescue reminders
- streak rescue
- paid rescue tokens
- "skip forgetting" consumables

---

# 10. Rescue Entity

Conceptual model:

```text
Rescue
- rescue_id
- card_id
- expedition_id?

- created_at
- policy_version
- created_reason

- state
- fragility_score_at_creation?
- retrievability_at_creation?
- stability_at_creation?
- difficulty_at_creation?

- last_attempt_at?
- resolved_at?
- resolution?

- source_review_id?
- reconciliation_state?
```

---

# 11. Rescue Lifecycle

Recommended lifecycle:

```text
AVAILABLE
   ↓
ACTIVE
   ↓
STABILIZING
   ↓
RESCUED
```

Additional states:

```text
EXPIRED_BY_STATE_CHANGE
ORPHANED
ARCHIVED
REVERSED
```

### AVAILABLE

Card qualifies as fragile.

### ACTIVE

Rescue opportunity is attached to current session/context.

### STABILIZING

A successful recall occurred, but durable recovery condition is not yet fully satisfied.

### RESCUED

The memory has recovered according to the Rescue policy.

### EXPIRED_BY_STATE_CHANGE

The card no longer qualifies because memory state changed independently.

### ORPHANED

Source card no longer exists.

### ARCHIVED

Historical lifecycle completed/closed.

### REVERSED

A source review that changed Rescue state was undone.

---

# 12. Why STABILIZING Exists

A single correct recall may not be enough to claim:

> Memory saved.

Rescue should distinguish:

- immediate successful recall,
- actual recovery over time.

Possible UX:

After a good recall:

> Memory stabilized for now.

Later, after stronger memory state:

> Rescue complete.

This avoids overstating what one answer achieved.

Exact policy is PROVISIONAL.

---

# 13. Fragile Memory Definition

The exact fragility formula is DEFERRED.

Potential inputs:

- retrievability
- stability
- difficulty
- lapse history
- interval
- recent failures
- memory age
- trend over time

Locked requirements:

- based on real memory state,
- explainable,
- not arbitrary,
- should avoid selecting huge numbers of cards,
- should not rely only on due status.

---

# 14. Fragility Score

A derived score may be used internally.

Conceptual:

```text
fragility_score = f(
    retrievability,
    stability,
    difficulty,
    lapse_history,
    recent_state
)
```

Exact weights are PROVISIONAL.

Do not persist every derived score forever.

Store creation-time metrics when useful for history/explanation.

---

# 15. Rescue Eligibility

Potential rules:

- card must have enough history,
- card must be below a fragility threshold,
- card must not already be in active Rescue,
- card may need a cooldown after resolution,
- card may be excluded if data quality is insufficient.

Exact policy is versioned.

---

# 16. Number of Rescue Opportunities

Rescue must not flood the session.

Possible design:

```text
3–7 Rescue opportunities in a standard Expedition
```

PROVISIONAL.

The count should depend on actual fragile-memory population.

If no meaningful fragile memories exist:

> no Rescue signal is shown.

Do not fabricate Rescue content.

---

# 17. Candidate Selection Timing

Preferred:

- batch candidate selection at Expedition planning/start,
- or precompute outside reviewer hot path.

Do not scan the collection per review.

Potential flow:

```text
ExpeditionStarted
    ↓
Memory Engine produces fragile candidates
    ↓
Rescue service selects eligible set
    ↓
Rescue records created
```

---

# 18. Card Encounter

Before the learner answers, Rescue may be handled in one of two ways.

### Option A — Hidden Until After Answer

Best for strict recall purity.

### Option B — Generic "Fragile Memory" Label Before Answer

Potentially useful, but may alter attention and anxiety.

Default recommendation:

> Keep Rescue identity hidden until after answer in initial release, or use only a very subtle non-answer-relevant marker after careful UX testing.

Status: PROVISIONAL.

Recall integrity takes priority.

---

# 19. Post-Answer Rescue Reveal

Preferred reveal timing:

```text
review accepted
    ↓
Rescue state evaluated
    ↓
post-answer reveal
```

Example success:

```text
MEMORY STABILIZED

Estimated stability
51d → 108d
```

Only show values if they are meaningful and accurate.

Alternative simpler copy:

> Memory stabilized.

---

# 20. Failure Reveal

If the learner presses `Again`:

Preferred:

```text
MEMORY STILL FRAGILE

This one needs another recovery.
```

Avoid:

```text
RESCUE FAILED
You lost the memory.
```

The framing matters.

---

# 21. Rescue Completion

Rescue completion should require policy-defined actual improvement.

Potential criteria:

- stability crosses threshold,
- retrievability recovers,
- successful later review confirms recovery,
- recent lapse pattern improves.

Exact rule is DEFERRED.

Locked:

> Rescue completion must reflect real memory improvement, not a single button press.

---

# 22. Rescue and Honest Grading

No rating multiplier.

No:

```text
Easy = instant Rescue
Good = half Rescue
Again = lose Rescue
```

Instead, grading influences Anki's real memory state.

Rescue reacts to that state.

---

# 23. Expedition Integration

Potential flow:

```text
ExpeditionStarted
   ↓
Rescue candidates selected

ReviewAnswered
   ↓
Rescue checks whether card is active
   ↓
memory snapshot updated
   ↓
Rescue state changes
   ↓
RescueStateChanged
   ↓
EventOrchestrator
```

---

# 24. Domain Events

Phase 3 may add:

```text
MemoryMarkedFragile
RescueCreated
RescueActivated
RescueAttempted
MemoryStabilized
RescueCompleted
RescueExpired
RescueOrphaned
RescueReversed
```

Do not encode UI wording in events.

---

# 25. Memory Engine Dependency

Rescue is the first phase that strongly depends on the Memory Engine.

The Memory Engine should provide normalized access to:

- stability if available
- difficulty if available
- retrievability if available
- lapses
- interval
- recent review summaries

Rescue must not query host internals directly.

---

# 26. Source Data vs Derived Data

### Source

From Anki / scheduler:

- review history
- interval
- lapses
- FSRS memory state if exposed

### Derived

From Anki Alive:

- fragility score
- Rescue eligibility
- Rescue lifecycle state
- recovery significance

The UI must not imply derived scores are native Anki fields.

---

# 27. Explainability

After or outside active recall, the learner should be able to understand:

> Why was this memory marked fragile?

Possible explanation:

```text
This memory was selected because:

• estimated recall probability was lower
• stability had weakened relative to similar cards
• it had recent lapse history
```

Only include signals actually used.

---

# 28. Scientific Wording

Avoid:

> Your brain was about to erase this.

Prefer:

> This memory had a lower estimated chance of successful recall.

Avoid:

> Memory saved permanently.

Prefer:

> Memory stabilized.

---

# 29. Rescue Visual Grammar

Per design system:

**Geometry:** pulse ring / broken curve repaired / stabilizing arc  
**Material:** soft energy / signal recovery  
**Motion:** pulse → settle → stabilize  
**Mood:** urgency without panic / recovery / relief

Avoid:

- emergency sirens
- flashing red
- medical panic imagery
- alarm sounds

---

# 30. Standard Mode UX

Possible reveal:

```text
      RESCUE

Memory stabilized.

Stability
51d → 108d
```

If exact metrics are not reliable:

```text
      RESCUE

Memory stabilized.
```

Never invent precision.

---

# 31. Focus Mode

Focus Mode preserves Rescue domain behavior.

Presentation becomes:

```text
Rescue · stabilized
```

or:

```text
Fragile memory · still recovering
```

No large animation.

No pulse loop.

---

# 32. Reduced Motion

Reduced-motion behavior:

- no expanding pulse,
- no animated repair arc,
- static icon,
- short fade or instant state swap.

---

# 33. Accessibility

Required:

- fragility not represented by color alone,
- clear text label,
- no panic language,
- keyboard dismissal,
- reduced motion,
- Focus Mode,
- readable state changes.

---

# 34. Rescue History

Potential long-term history entry:

```text
Memory rescued
Card ID: ...
Created: Aug 18
Recovered: Aug 22
```

User-facing history may later show card content live from Anki.

Do not store full text by default.

---

# 35. Rescue Significance

Not every Rescue should become a permanent milestone.

Potential permanent milestone criteria:

- unusually fragile
- long-lived memory recovered
- repeated prior lapses
- large stability improvement

Status: PROVISIONAL.

Avoid history spam.

---

# 36. Rescue Cooldown

A recently completed Rescue may need a cooldown.

Purpose:

- avoid repetitive labeling,
- preserve emotional meaning,
- prevent one card from dominating.

Exact policy is DEFERRED.

---

# 37. Rescue Expiration

A Rescue may close if memory state changes before the intended encounter.

Examples:

- card rescheduled externally,
- manual review elsewhere,
- scheduler state changes.

Preferred state:

```text
EXPIRED_BY_STATE_CHANGE
```

No user penalty.

---

# 38. Expedition Ends Before Rescue Resolution

Recommended initial behavior:

- unresolved active Rescue may remain a memory-level entity,
- but its Expedition-specific presentation closes.

Unlike Oracle, Rescue may logically outlive a single Expedition because fragility is a memory state.

This is an important difference.

Locked principle:

> Rescue lifecycle belongs primarily to the memory, not the session.

Exact carry-forward UX is PROVISIONAL.

---

# 39. Cross-Day Behavior

Rescue may continue across days if the memory remains fragile.

No artificial midnight reset.

If the memory stabilizes outside the original Expedition, Rescue state should reconcile.

---

# 40. Card Deletion

If the card is deleted:

- mark Rescue ORPHANED,
- no crash,
- preserve minimal history,
- do not store deleted card text.

---

# 41. Undo/Reversal

If a review that changed Rescue state is undone:

- restore prior Rescue state where possible,
- remove false completion,
- reconcile derived memory state.

Locked:

> A Rescue completion must not remain if its causal review was reversed.

---

# 42. Duplicate Protection

A review event must not:

- apply stabilization twice,
- create duplicate history entries,
- complete the same Rescue twice.

Use idempotent transitions.

---

# 43. Persistence

Phase 3 adds durable table:

```text
rescues
```

Potential fields:

- rescue_id
- card_id
- created_at
- policy_version
- state
- creation metrics
- last_attempt_at
- resolved_at
- resolution
- reconciliation state

---

# 44. Migration

Phase 3 adds migration from Phase 2.

Tests:

- fresh install
- Phase 2 → Phase 3
- rollback/failure
- existing Oracle/Expedition data preserved

---

# 45. Rescue Repository

Possible operations:

```text
create_rescue
get_active_for_card
list_active
apply_transition
complete
expire
orphan
archive
list_recent
```

No UI SQL.

---

# 46. Rescue Service

Responsibilities:

- candidate evaluation
- lifecycle transitions
- result interpretation
- history projection
- explanation metadata

Not responsibilities:

- scheduling
- reviewer rendering
- Nemesis logic

---

# 47. Event Orchestration Priority

Rescue reveals are meaningful but may conflict with Oracle.

Potential provisional priority:

```text
major Nemesis event
Oracle reveal
Rescue reveal
minor Fragment progress
ambient signal
```

Nemesis does not exist yet, so this is only a future placeholder.

Locked:

- one prominent reveal per review boundary,
- Rescue may defer to checkpoint/summary.

---

# 48. Combined Oracle + Rescue Card

A card may theoretically be both:

- Oracle prediction target
- Rescue memory

If both resolve on the same review:

do not show two full-screen events.

Potential handling:

### Option A

Oracle major reveal, Rescue compact footer.

### Option B

Combined reveal:

```text
ORACLE DEFEATED
Memory stabilized.
```

Status: PROVISIONAL.

EventOrchestrator owns the decision.

---

# 49. Performance

Critical work:

- candidate ranking
- per-review active Rescue lookup
- memory snapshot access
- transition update

Preferred:

```text
Expedition/start:
batch candidate selection

Review:
indexed lookup
small memory-state read
small transition
```

Do not compute all fragile cards on every review.

---

# 50. Performance Targets

Provisional:

```text
active Rescue lookup:
preferred < 1 ms

transition logic:
preferred < 2 ms

reviewer total added overhead:
within global budget
```

Candidate analysis may be heavier but should occur outside hot path.

---

# 51. Large Collections

Rescue selection must scale.

Potential strategies:

- prefiltered due candidates
- bounded candidate pool
- incremental memory-health cache
- indexed historical summaries

Do not assume small collections.

---

# 52. Calibration and Threshold Evaluation

Phase 3 should inspect whether:

- too many cards qualify,
- too few cards qualify,
- selected cards actually feel fragile,
- Rescue is dominated by one deck,
- completion is too easy/hard.

Thresholds should be adjusted from evidence.

---

# 53. Testing Requirements

## Eligibility

- qualifying fragile card selected
- stable card excluded
- duplicate active Rescue prevented
- insufficient-data behavior

## Lifecycle

- AVAILABLE → ACTIVE
- ACTIVE → STABILIZING
- STABILIZING → RESCUED
- expiration
- orphan
- archive
- reversal

## Honest Grading

- Again does not destroy progress arbitrarily
- Again does not reduce artificial score
- Hard/Good/Easy do not directly force completion

## Persistence

- restart preserves Rescue
- migration works
- completion persists
- crash recovery

## Reconciliation

- undo reverses false transition
- external state change expires/recalculates correctly

## UX

- no panic framing
- Focus Mode
- reduced motion
- one major reveal maximum

---

# 54. Crash Recovery

Test:

### Case A

Rescue created, crash before card encounter.

Expected:

- Rescue remains valid if source state still qualifies.

### Case B

Successful review, state persisted, crash before reveal.

Expected:

- domain state remains correct,
- presentation can safely summarize later.

### Case C

Completion written, crash.

Expected:

- no duplicate completion on restart.

---

# 55. Manual Host Test

Minimum:

```text
1. Start Expedition with fragile candidates.
2. Confirm no fake Rescue count if none qualify.
3. Encounter Rescue card.
4. Press Again.
5. Confirm no punishment/shame.
6. Encounter another Rescue card.
7. Press Good.
8. Confirm stabilization feedback.
9. Undo review.
10. Confirm Rescue state reconciles.
11. Restart Anki.
12. Confirm active Rescue persists.
13. Toggle Focus Mode.
14. Confirm compact presentation.
15. Cross local day boundary if practical.
16. Confirm no artificial expiry.
```

---

# 56. Success Metrics

Potential future evaluation:

- Rescue opportunities created
- percentage stabilized
- percentage eventually completed
- time to recovery
- repeated fragility rate
- user continuation after Rescue
- Focus Mode usage
- unresolved Rescue population

Do not optimize for maximum Rescue count.

A healthy collection may have few Rescues.

---

# 57. Trust Risks

## Risk 1 — Fake Urgency

Mitigation:

derive Rescue only from actual memory state.

## Risk 2 — Anxiety

Mitigation:

calm copy, no countdown, no flashing alarms.

## Risk 3 — Overclaiming Recovery

Mitigation:

distinguish immediate stabilization from durable Rescue completion.

## Risk 4 — Grading Bias

Mitigation:

no direct reward based on high rating.

## Risk 5 — Too Many Rescues

Mitigation:

bounded selection and candidate threshold.

---

# 58. Anti-Patterns

Do not implement:

### Rescue Timer

> 03:42 remaining.

### Permanent Loss

> You lost this memory forever.

### Rescue Currency

> Spend one token to save card.

### Grading Multiplier

> Easy rescues instantly.

### Panic UI

Flashing red alert.

### Shame Copy

> You failed to save this.

---

# 59. Copy Tone

Preferred:

```text
Fragile memory.
Memory stabilized.
Still fragile.
Recovery in progress.
Rescue complete.
This memory needs another review.
```

Avoid:

```text
Critical failure!
Memory dying!
You failed the rescue!
Act now!
```

---

# 60. Explainability Example

```text
Why was this memory selected?

Its estimated recall strength was lower than most current review candidates.

Signals included:
• lower retrievability
• recent lapse history
• weaker stability
```

Only show real inputs.

---

# 61. Open Questions

## Q3-01 — Fragility Formula

Status: DEFERRED.

---

## Q3-02 — Rescue Completion Condition

One future successful recall, threshold crossing, or multi-review confirmation?

Status: DEFERRED.

---

## Q3-03 — Pre-Answer Fragile Marker

Should user know before recall?

Status: UX RESEARCH.

Default conservative choice: hidden.

---

## Q3-04 — Carry Across Expeditions

How should active Rescue appear in later sessions?

Status: PROVISIONAL.

---

## Q3-05 — Rescue Count

Fixed cap vs proportional?

Status: PROVISIONAL.

---

## Q3-06 — History Significance

Which Rescues deserve permanent history entries?

Status: PROVISIONAL.

---

# 62. Definition of Done

Phase 3 is complete when:

- [ ] Memory Engine exposes required normalized memory data
- [ ] fragile candidate policy exists
- [ ] policy version stored
- [ ] Rescue entity persists
- [ ] lifecycle transitions are explicit
- [ ] Rescue can survive restart
- [ ] Again does not punish user
- [ ] successful recall can enter stabilization state
- [ ] completion requires actual memory improvement
- [ ] undo/reversal reconciles
- [ ] deletion/orphan handling works
- [ ] no artificial expiry exists
- [ ] no fake Rescue opportunities are shown
- [ ] Expedition integration works
- [ ] EventOrchestrator handles overlap
- [ ] Focus Mode works
- [ ] reduced motion works
- [ ] keyboard path works
- [ ] migration tested
- [ ] crash recovery tested
- [ ] performance measured
- [ ] manual host validation completed
- [ ] ADRs/backlog updated
- [ ] `PHASE_3_RESCUE_HANDOFF.md` exists

---

# 63. Phase 4 Contract

Nemesis may begin only after Rescue proves:

- persistent memory-level feature lifecycles work,
- Memory Engine access is stable,
- feature candidates can be ranked safely,
- review-driven state transitions reconcile with undo,
- cross-session feature state is durable,
- event overlap is orchestrated.

Nemesis should reuse:

- Memory Engine
- feature policy versioning
- lifecycle persistence patterns
- EventOrchestrator
- history infrastructure
- accessibility/motion components

Nemesis must not create a second parallel memory-state engine.

---

# 64. Locked vs Provisional Summary

## Locked

- Rescue urgency comes from real memory state
- no artificial countdown
- Again is never punished
- no direct grade multiplier
- completion reflects actual memory improvement
- Rescue may outlive one Expedition
- no midnight reset
- undo reconciles
- card deletion is safe
- Focus Mode preserves behavior
- one prominent reveal per review boundary

## Provisional

- fragility formula
- candidate count
- completion threshold
- pre-answer marker
- carry-forward UX
- history significance
- cooldown
- exact reveal animation

---

# Phase 3 North Star

> **Make fragile memories feel worth saving, without making forgetting feel like a crime.**
