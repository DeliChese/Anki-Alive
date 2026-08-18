# PHASE_1_EXPEDITION.md

# Anki Alive — Phase 1: Expedition

## 1. Phase Goal

Transform an Anki review session from an open-ended queue into a bounded, meaningful journey with nearby completion points.

Expedition is the primary session container for Anki Alive.

It should create the feeling:

> "I know where I am, what is nearby, and what it means to finish."

Phase 1 is the first major user-facing feature.

It must prove that Anki Alive can increase willingness to continue studying without:

- corrupting recall,
- introducing artificial rewards,
- creating an infinite engagement loop,
- replacing Anki's scheduler,
- making the reviewer noisy.

---

# 2. Phase Status

```text
Status: SPECIFIED
Phase: 1
Name: Expedition
Depends on: Phase 0 — Foundation
Next phase: Phase 2 — Oracle
```

---

# 3. Product Role

Expedition is not a side feature.

It is the session-level structure that later mechanics plug into.

Later features may appear:

- inside an Expedition,
- at Expedition checkpoints,
- at review boundaries during an Expedition,
- in the Expedition completion summary.

Examples:

- Oracle predictions resolve during Expedition reviews.
- Rescue opportunities surface inside an Expedition.
- Nemesis encounters occur along the Expedition path.
- Fragments progress during Expedition.
- Relics may be revealed at checkpoints or completion.

Expedition must therefore remain stable, generic, and feature-agnostic.

---

# 4. Core User Problem

A large due count often feels psychologically distant.

Examples:

```text
237 due
418 due
762 due
```

These numbers communicate workload but not meaningful progress.

A learner may:

- open Anki,
- review a few cards,
- feel little sense of advancement,
- stop because the queue appears effectively endless.

Expedition reframes the session into a bounded commitment.

Instead of:

> 237 due

the learner may see:

> Today's Expedition  
> 0 / 60  
> Next checkpoint in 10 reviews

The remaining due queue still exists.

Expedition does not pretend otherwise.

It creates one meaningful study unit within that queue.

---

# 5. Behavioral Goal

Expedition should create:

- orientation,
- bounded commitment,
- nearby completion,
- progress tension,
- clean closure.

The intended loop is:

```text
Start
  ↓
Nearby checkpoint
  ↓
Review
  ↓
Progress
  ↓
Checkpoint closure
  ↓
Next bounded segment
  ↓
Final completion
  ↓
Stop or consciously continue
```

The product must not create:

```text
completion
  ↓
surprise new mandatory task
  ↓
another surprise task
  ↓
infinite chain
```

---

# 6. Critical Product Invariant

> **The finish line must be real.**

Once an Expedition begins, the target must not silently increase.

The system may explain that more due cards remain outside the Expedition.

It must not move the current Expedition's goal merely to prolong engagement.

---

# 7. In Scope

Phase 1 includes:

- Today screen foundation
- Expedition planning
- Expedition creation
- start
- pause
- resume
- progress tracking
- checkpoint plan
- reviewer HUD
- nearby closure indicator
- completion
- session summary
- interruption recovery
- local study-day grouping
- Focus Mode integration
- reduced-motion behavior
- keyboard interaction
- event hooks for later mechanics
- Expedition persistence
- Expedition history summary

---

# 8. Explicitly Out of Scope

Phase 1 does not implement:

- Oracle prediction logic
- Rescue scoring
- Nemesis promotion
- Fragment mystery payloads
- Relic formation
- Memory World
- XP
- coins
- streaks
- leaderboard
- dynamic difficulty based on user manipulation
- artificial daily punishment

Expedition may expose extension points for later phases.

It must not contain placeholder fake behavior for those features.

---

# 9. Expedition Definition

An Expedition is:

> A bounded review-session objective defined by a target number of completed review actions within a local study context.

Conceptually:

```text
Expedition
- identity
- local study date
- target reviews
- completed reviews
- checkpoint plan
- session state
- Focus Mode snapshot/policy
- timestamps
- deterministic seed if needed
```

An Expedition is not:

- a replacement for the due queue,
- a new scheduler,
- a deck,
- a review mode that changes FSRS.

---

# 10. Session Lifecycle

Recommended lifecycle:

```text
PLANNED
   ↓
ACTIVE
   ↕
PAUSED
   ↓
COMPLETED
```

Additional terminal states may include:

```text
ABANDONED
INVALIDATED
```

### PLANNED

The Expedition exists but review has not begun.

### ACTIVE

Reviews are contributing toward progress.

### PAUSED

The user left or intentionally paused.

### COMPLETED

The target was reached.

### ABANDONED

The user intentionally ends the Expedition without completion.

This state is descriptive, not punitive.

### INVALIDATED

The Expedition can no longer safely continue due to state mismatch.

Examples may include:

- incompatible profile state,
- unrecoverable persistence issue.

Use sparingly.

---

# 11. Start Flow

The Today screen should provide a clear primary action.

Example conceptual layout:

```text
TODAY

Your memory is mostly stable.

        MEMORY CORE

      143 memories due

    [ BEGIN EXPEDITION ]

Today's Signals
...
```

When the learner starts:

1. determine the available review context,
2. propose or create an Expedition target,
3. create checkpoints,
4. persist the Expedition,
5. transition to ACTIVE,
6. enter review.

If planning fails, normal review must remain available.

---

# 12. Target Size

Target selection is provisional.

The product contract is:

- target must be bounded,
- target must feel attainable,
- target must not silently change,
- target should respect available due work,
- target should not force the learner to clear the entire queue.

Potential inputs:

- user preference,
- estimated session size,
- available cards,
- historical completion behavior,
- explicit quick / standard / deep session choices.

Exact algorithm is DEFERRED until implementation evidence.

Do not lock a formula in this phase spec.

---

# 13. Potential Session Presets

Possible future UI:

```text
Quick      ~20 reviews
Standard   ~50 reviews
Deep       ~100 reviews
```

These are provisional concepts.

A preset must not imply time guarantees unless time estimation is reliable.

Alternative:

```text
Short
Standard
Long
```

This requires UX testing.

---

# 14. Checkpoint Model

Checkpoints divide the Expedition into psychologically manageable segments.

Each checkpoint has:

- target progress,
- order,
- presentation state,
- reached state.

Example:

```text
0 → 10 → 20 → 35 → 50 → 60
```

Checkpoint spacing does not need to be uniform.

The user should frequently feel:

> "The next closure point is nearby."

---

# 15. Checkpoint Principles

## CP01 — Nearby

A checkpoint should not feel too distant.

## CP02 — Meaningful

Checkpoint count should not be so high that every few cards triggers ceremony.

## CP03 — Stable

Once the Expedition starts, checkpoint targets should remain stable unless the session is explicitly invalidated/replanned.

## CP04 — Quiet

Checkpoint feedback should be brief.

## CP05 — Extensible

Later phases may attach deferred events to checkpoints without changing checkpoint ownership.

---

# 16. Checkpoint Planning

Checkpoint generation should be deterministic for a given Expedition.

Possible strategy:

- target-based template,
- bounded proportional spacing,
- seeded variation within limits.

Exact algorithm is PROVISIONAL.

What is locked:

- checkpoint plan is fixed at Expedition creation,
- reload does not reroll,
- completion target is fixed.

---

# 17. Progress Definition

Phase 1 must explicitly define what counts as one unit of Expedition progress.

Recommended initial contract:

> A completed Anki review grading action that is accepted by the host review flow contributes one unit.

Important:

- `Again` contributes progress.
- `Hard` contributes progress.
- `Good` contributes progress.
- `Easy` contributes progress.

Why?

Because Expedition rewards **doing the review work**, not choosing a higher grade.

This is compatible with the product principle that Again must not be punished.

---

# 18. Recall Integrity

Expedition progress must never pressure the learner toward a higher rating.

Therefore:

```text
Again = +1 review progress
Hard  = +1 review progress
Good  = +1 review progress
Easy  = +1 review progress
```

unless a future accepted ADR changes the definition for a strong reason.

Expedition progress measures session completion, not memory quality.

Memory quality belongs to later systems.

---

# 19. Review Undo

Undo semantics are critical.

If a review contributing to Expedition progress is undone, the Expedition state should reconcile.

Possible strategies:

- decrement progress,
- mark the event reversed,
- reconcile against host review history.

Exact implementation depends on Phase 0 undo findings.

Locked requirement:

> Expedition progress must not drift permanently from accepted host review state.

---

# 20. Duplicate Review Events

The Expedition engine must avoid double-counting a single review.

Potential causes:

- hook duplication,
- reload behavior,
- bridge duplication,
- event replay.

Use stable source identity or reconciliation where available.

Duplicate prevention is a quality gate.

---

# 21. Reviewer HUD

During active recall, Expedition UI must remain subtle.

Suggested anatomy:

```text
EXPEDITION  28 / 60

●━━━━━━●━━━━◉━━━━○━━━━◇
10     20   30    45   60
```

Alternative compact form:

```text
28 / 60     Next: 2
```

Focus Mode may prefer the compact form.

---

# 22. Reviewer HUD Rules

During question state:

- no large animation,
- no event popup,
- no distracting glow,
- no information that biases recall.

HUD may show:

- current progress,
- next checkpoint distance,
- simple route.

HUD must not show:

- "You are about to get a rare event in 1 card"
if such wording distracts recall.

Use restrained signal language.

---

# 23. Checkpoint Reveal

When a checkpoint is reached:

Preferred timing:

- after review outcome handling,
- before next card,
- short duration,
- easily dismissible or auto-advancing.

Example:

```text
CHECKPOINT REACHED

20 / 60

Next signal in 8 reviews
```

Motion target:

- brief,
- under roughly one standard reveal,
- reduced-motion fallback.

---

# 24. Completion UX

Completion is one of the most important Phase 1 moments.

Example:

```text
EXPEDITION COMPLETE

60 reviews completed
4 checkpoints reached
Session duration: 18 min

[ DONE ]
[ CONTINUE REVIEWING ]
```

The exact stats shown are provisional.

Important:

- primary psychological goal is closure,
- the user should be allowed to stop cleanly,
- continuing should be an explicit secondary action.

---

# 25. Completion Must Not Immediately Reopen Tension

After completion, avoid:

> Great! Only 20 more to unlock another thing!

The system may say:

> 83 reviews remain due outside this Expedition.

But it should not frame that as a failure.

Possible continuation CTA:

> Continue reviewing

not:

> Keep your momentum or lose the bonus.

---

# 26. One More to Closure

This concept may be tested carefully.

If the user attempts to stop when extremely close to an already-existing checkpoint, the system may optionally surface:

> 2 reviews to the next checkpoint.

Constraints:

- optional,
- no penalty for declining,
- no artificial checkpoint creation,
- no chaining after the checkpoint,
- can be disabled,
- should be suppressed in Focus Mode if configured.

Status:

PROVISIONAL / RESEARCH.

See backlog item `BL-008`.

---

# 27. Pause Behavior

Pause should be supported when the user leaves review intentionally.

Paused state should preserve:

- progress,
- checkpoint plan,
- target,
- session identity.

It should not generate penalty.

---

# 28. Resume Behavior

When a resumable Expedition exists:

Today may show:

```text
EXPEDITION IN PROGRESS

32 / 60
Next checkpoint in 3

[ RESUME ]
[ END EXPEDITION ]
```

Do not silently create a second active Expedition.

---

# 29. Expiration / Day Boundary

This needs careful policy.

Recommended initial product behavior:

- an Expedition may survive short interruption and restart,
- local study day is recorded,
- crossing a day boundary should not automatically destroy progress.

Possible options:

A. allow resume next day,
B. prompt user to resume or archive,
C. automatically archive after configurable threshold.

Exact policy is PROVISIONAL.

Artificial midnight punishment is forbidden.

---

# 30. Ending an Incomplete Expedition

The learner must be allowed to end a session.

Example:

```text
End Expedition?

32 / 60 completed.

Your review history is safe.
This Expedition will be archived as incomplete.

[ END ]
[ KEEP GOING ]
```

Copy must avoid guilt.

"ABANDONED" is an internal state.

User-facing language should prefer:

- Ended
- Incomplete
- Paused

depending on context.

---

# 31. Available Cards Less Than Target

If fewer reviewable cards remain than the target:

Options may include:

- clamp target during planning,
- complete when no eligible cards remain,
- explain that the Expedition ended because review queue was exhausted.

The target must not become impossible.

Exact behavior should be determined during implementation.

---

# 32. Filtered Deck / Custom Study Considerations

Expedition should not assume only ordinary deck review.

Phase 1 implementation should validate behavior with:

- standard deck review,
- filtered decks,
- custom study if applicable.

If unsupported initially, document limitations explicitly.

Do not guess.

---

# 33. Profile / Collection Switching

Only one active Expedition should exist per relevant local profile context unless future design explicitly supports more.

When collection/profile changes:

- pause safely,
- persist state,
- prevent cross-profile contamination.

---

# 34. Domain Events

Phase 1 may add:

```text
ExpeditionPlanned
ExpeditionStarted
ExpeditionPaused
ExpeditionResumed
ExpeditionProgressed
CheckpointReached
ExpeditionCompleted
ExpeditionEnded
ExpeditionInvalidated
```

Events should contain only required data.

Do not include UI wording in domain events.

---

# 35. Domain Model

Conceptual model:

```text
Expedition
- expedition_id
- profile_key
- local_study_date

- status
- created_at
- started_at?
- paused_at?
- completed_at?
- ended_at?

- target_reviews
- completed_reviews

- checkpoint_plan_version
- seed

- focus_mode_at_start?
- schema_version
```

Checkpoint:

```text
ExpeditionCheckpoint
- checkpoint_id
- expedition_id
- ordinal
- target_progress
- reached_at?
- status
- presentation_kind?
```

Exact fields remain subject to implementation evidence.

---

# 36. Persistence

Phase 1 adds durable tables for:

```text
expeditions
expedition_checkpoints
```

Potential supporting data:

- progress events,
- session summary.

Avoid storing every UI interaction.

---

# 37. Migration

Phase 1 must introduce an explicit schema migration.

Migration must support:

- fresh install,
- Phase 0 schema → Phase 1 schema,
- failure rollback,
- reopen after migration.

---

# 38. Expedition Repository

Create an explicit repository/service boundary.

Possible operations:

```text
create_expedition
get_active_expedition
save_progress
pause
resume
complete
end
list_recent
```

UI must not directly execute SQL.

---

# 39. Expedition Engine

Responsibilities:

- plan target,
- plan checkpoints,
- create session,
- apply valid review progress,
- determine checkpoint transitions,
- determine completion,
- handle pause/resume,
- reconcile reversals.

Not responsibilities:

- Oracle scoring,
- Rescue scoring,
- Nemesis lifecycle,
- UI rendering.

---

# 40. SessionCoordinator Relationship

If Phase 0 creates a general SessionCoordinator:

- Expedition becomes its primary Phase 1 implementation context,
- ownership must remain clear.

Avoid two overlapping state owners.

If no coordinator is needed in Phase 0, Expedition may own active-session state directly.

Document the final decision.

---

# 41. Extension Points for Later Features

Expedition should expose stable hooks/events for:

- review boundary,
- checkpoint boundary,
- completion boundary.

Potential integration examples:

```text
CheckpointReached
    ↓
EventOrchestrator may surface deferred Fragment event

ReviewAnswered
    ↓
Oracle may resolve prediction

ExpeditionCompleted
    ↓
Relic/history summary may appear later
```

Phase 1 should not know those feature implementations.

---

# 42. Event Orchestration

Phase 1 introduces the first real need for presentation scheduling.

At minimum:

- checkpoint reveal has a priority,
- completion reveal has a priority,
- later feature events can be inserted safely.

A checkpoint and a later major feature event should not both explode onto the screen simultaneously.

The EventOrchestrator contract may be created now if Phase 0 foundation does not already include it.

---

# 43. Today Screen Scope

Phase 1 owns the first production Today screen.

Required content:

- date/context
- concise memory status placeholder or safe summary
- due count
- active Expedition status
- primary start/resume action
- Today's Signals shell

Important:

Today's Signals may show only actual implemented signals.

Do not fake Oracle/Rescue/Nemesis counts before those phases exist.

Possible Phase 1 shell:

```text
TODAY

143 memories due

[ BEGIN EXPEDITION ]

EXPEDITION
No active Expedition
```

The richer signal panel grows later.

---

# 44. Memory Core Scope

Phase 1 may introduce the Memory Core visual in a limited form.

Allowed:

- ambient hero state
- simple collection/due response
- static or lightly animated visual

Not yet allowed:

- scientifically unsupported health claims,
- rich behavior tied to unimplemented memory engine states.

Memory Core evolution remains partially backlog-driven.

---

# 45. Focus Mode

Focus Mode behavior for Expedition:

### Standard Mode

May show:

- path track,
- checkpoint animation,
- completion reveal.

### Focus Mode

Prefer:

- compact progress,
- minimal checkpoint toast,
- reduced or no hero animation,
- no One More prompt by default.

Expedition logic remains identical.

---

# 46. Reduced Motion

When reduced motion is enabled:

- checkpoint motion becomes static/fade,
- progress changes without animated travel,
- completion reveal uses minimal transition,
- ambient Memory Core motion pauses or simplifies.

---

# 47. Keyboard Interaction

Required:

- begin Expedition
- resume
- pause/end where UI exposes it
- dismiss checkpoint reveal
- dismiss completion
- continue review
- navigate Today screen core actions

Keyboard focus must remain visible.

---

# 48. Copy Language

Preferred:

```text
Begin Expedition
Resume Expedition
Checkpoint reached
Expedition complete
End Expedition
Continue reviewing
```

Avoid:

```text
Don't give up!
You're breaking your momentum!
Only quitters stop here!
Claim reward!
```

---

# 49. Accessibility

Required:

- numeric progress in addition to graphical route,
- non-color checkpoint states,
- visible keyboard focus,
- reduced-motion fallback,
- Focus Mode,
- no rapidly animated progress,
- no guilt language.

---

# 50. Performance

Critical paths:

- review progress update,
- checkpoint detection,
- HUD update,
- persistence.

Target:

```text
Expedition progress application:
Preferred < 2 ms domain logic

Added reviewer synchronous overhead:
Remain within Phase 0 budget

Checkpoint persistence:
small indexed transaction
```

Exact measured targets should be reported in Phase 1 handoff.

---

# 51. Persistence Write Strategy

Do not perform unnecessarily heavy writes per review.

Possible model:

- update in-memory progress each accepted review,
- persist compact progress frequently enough for crash recovery,
- checkpoint writes are durable,
- completion is durable immediately.

The exact batching policy is PROVISIONAL.

Data integrity beats micro-optimization.

---

# 52. Crash Recovery

Test interruption:

- immediately after start,
- after several reviews,
- exactly at checkpoint,
- one review before completion,
- at completion before summary dismiss.

On restart:

- no double-counting,
- no target reroll,
- correct active/completed state.

---

# 53. Testing Requirements

## Domain

- target planning validity
- checkpoint plan determinism
- checkpoint ordering
- progress increments
- Again counts as progress
- Hard counts as progress
- Good counts as progress
- Easy counts as progress
- checkpoint triggers once
- completion triggers once
- no target drift

## Lifecycle

- start
- pause
- resume
- end incomplete
- complete
- invalidation

## Persistence

- create
- reopen
- resume
- completion durability
- migration

## Undo

- reversed review does not leave permanent incorrect progress

## Duplicate

- repeated host event does not double-count

## Day Boundary

- local-day behavior
- resume behavior after midnight

## Accessibility

- keyboard
- reduced motion
- Focus Mode

---

# 54. Manual Host Test

Minimum manual script:

```text
1. Open Today.
2. Start Expedition.
3. Review with Again/Hard/Good/Easy.
4. Confirm each accepted review advances exactly once.
5. Reach checkpoint.
6. Pause/leave.
7. Resume.
8. Undo a review.
9. Confirm progress reconciliation.
10. Restart Anki.
11. Resume.
12. Complete Expedition.
13. Confirm completion stays complete after restart.
14. Continue reviewing outside Expedition if desired.
15. Toggle Focus Mode and repeat a short session.
```

Record exact host version and OS.

---

# 55. Success Metrics

Phase 1 should instrument product-safe metrics locally where useful.

Potential future evaluation:

- start → completion rate
- average stopping point
- resume rate
- checkpoint continuation rate
- incomplete session rate
- Focus Mode usage

Do not optimize blindly for longer sessions.

A shorter completed session may be healthier than a longer forced one.

---

# 56. Anti-Patterns

Do not implement:

### Endless Progress Bar

A target that keeps expanding.

### Reward Ladder

Checkpoint 1 unlocks checkpoint 2 unlocks surprise checkpoint 3 forever.

### Rating Bias

Good/Easy produce more Expedition progress.

### Guilt Copy

Shaming incomplete sessions.

### Fake Mystery

Showing placeholder signals for mechanics that do not exist.

### Heavy HUD

A dense RPG overlay during recall.

---

# 57. Open Questions

## Q1-01 — Target Planning

What session sizing produces the best balance of agency and structure?

Status: DEFERRED TO IMPLEMENTATION/UX TEST.

---

## Q1-02 — Checkpoint Spacing

Uniform or slightly varied?

Status: PROVISIONAL.

---

## Q1-03 — Resume Across Day Boundary

How long should an Expedition remain resumable?

Status: PROVISIONAL.

---

## Q1-04 — Progress Persistence Frequency

Per review vs batched?

Status: PROVISIONAL / PERFORMANCE TEST.

---

## Q1-05 — One More Prompt

Should Phase 1 ship it at all?

Status: RESEARCH.

Default answer should be conservative.

---

## Q1-06 — Memory Core Phase 1 Richness

How much ambient behavior is justified before Rescue/Memory Engine exist?

Status: PROVISIONAL.

---

# 58. Definition of Done

Phase 1 is complete when:

- [ ] Today screen production shell exists
- [ ] Expedition can be planned
- [ ] Expedition can start
- [ ] target is fixed once started
- [ ] checkpoint plan is fixed
- [ ] progress increments from accepted review grades
- [ ] Again counts without penalty
- [ ] duplicate reviews are not double-counted
- [ ] checkpoint fires once
- [ ] pause works
- [ ] resume works
- [ ] restart recovery works
- [ ] undo is reconciled
- [ ] incomplete Expedition can end without punishment
- [ ] completion fires once
- [ ] completion persists
- [ ] user may stop cleanly
- [ ] user may continue normal review
- [ ] reviewer HUD is restrained
- [ ] Focus Mode presentation exists
- [ ] reduced motion works
- [ ] keyboard path works
- [ ] Phase 1 migration is tested
- [ ] performance is measured
- [ ] manual host validation is completed
- [ ] roadmap/ADRs/backlog updated
- [ ] `PHASE_1_EXPEDITION_HANDOFF.md` exists

---

# 59. Phase 2 Contract

Oracle may begin only after Expedition provides stable:

- active session identity,
- review-boundary events,
- review progress,
- persistence,
- post-answer reveal timing,
- event orchestration,
- checkpoint/completion boundaries.

Oracle should plug into Expedition.

Oracle must not require rewriting Expedition's session model.

---

# 60. Locked vs Provisional Summary

## Locked

- Expedition is bounded.
- Target does not silently grow.
- Again/Hard/Good/Easy each count equally as review progress.
- Completion provides real closure.
- Normal Anki review remains available.
- Checkpoint plan does not reroll after start.
- Incomplete sessions are not punished.
- Later features plug into Expedition via stable events/services.
- Reviewer HUD remains quiet during recall.

## Provisional

- exact target algorithm,
- checkpoint spacing,
- session presets,
- One More prompt,
- cross-day resume policy,
- progress persistence batching,
- Memory Core richness.

---

# Phase 1 North Star

> **Turn an endless queue into a journey with a real destination, without changing what honest studying means.**
