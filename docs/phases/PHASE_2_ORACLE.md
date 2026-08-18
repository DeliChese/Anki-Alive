 # PHASE_2_ORACLE.md

# Anki Alive — Phase 2: Oracle

## 1. Phase Goal

Introduce a prediction mechanic that creates curiosity and friendly competition around genuine recall.

Oracle should create the feeling:

> "Anki thinks I may forget this. Can I prove it wrong?"

The feature must remain trustworthy.

If the product says a prediction existed before the learner answered, that prediction must actually have been committed before the outcome was known.

Oracle is the first major mechanic whose emotional value depends directly on user trust.

---

# 2. Phase Status

```text
Status: SPECIFIED
Phase: 2
Name: Oracle
Depends on: Phase 1 — Expedition
Next phase: Phase 3 — Rescue
```

---

# 3. Product Role

Oracle adds a micro-loop inside Expedition.

The intended loop is:

```text
prediction committed
    ↓
identity hidden
    ↓
learner reviews normally
    ↓
answer occurs
    ↓
prediction is revealed
    ↓
result resolves
    ↓
session/lifetime record updates
```

Oracle does not own session structure.

Expedition remains the session container.

---

# 4. Core User Problem

Anki review can be effective but emotionally uniform.

A difficult and an easy card often look identical before the answer.

Oracle creates anticipation by introducing a hidden prediction layer.

The learner should wonder:

- Which cards did Oracle choose?
- Will I beat the prediction?
- Was the system right about my weak spots?

This curiosity should increase engagement without revealing answer-relevant information.

---

# 5. Behavioral Goal

Oracle should create:

- anticipation,
- friendly competition,
- confidence-building moments,
- surprise after successful recall,
- meaningful feedback after failure.

The emotional arc should be:

```text
uncertainty
  ↓
effort
  ↓
reveal
  ↓
result
  ↓
closure
```

Not:

```text
prediction
  ↓
pressure to avoid Again
```

---

# 6. Critical Product Invariant

> **Prediction must be committed before the outcome is known.**

This is locked.

No fake retrospective prediction is allowed.

If the UI says:

> Oracle predicted this card at 61%.

the system must have stored or deterministically fixed that prediction before the answer.

---

# 7. Recall Integrity Invariant

Oracle must not bias recall.

Therefore, before the learner answers:

- no card-specific warning,
- no "this is an Oracle card" label,
- no special border that identifies prediction target,
- no reveal of predicted difficulty,
- no probability display,
- no hint that the card was selected.

The prediction is hidden until after the answer.

---

# 8. In Scope

Phase 2 includes:

- Oracle candidate selection
- prediction commitment
- hidden prediction state
- persisted commitments
- reveal after answer
- result resolution
- player vs Oracle session score
- basic lifetime score/history
- invalidation
- undo reconciliation
- duplicate protection
- Focus Mode presentation
- reduced-motion behavior
- explainability
- performance profiling
- migration
- tests

---

# 9. Explicitly Out of Scope

Phase 2 does not implement:

- Rescue
- Nemesis
- Fragments
- Relics
- Memory World
- generic AI assistant behavior
- cloud inference
- monetized predictions
- social betting
- streaks
- XP or currency

Oracle is a local memory prediction mechanic, not a gambling system.

---

# 10. Oracle Entity

Conceptual model:

```text
OraclePrediction
- oracle_prediction_id
- expedition_id
- card_id

- committed_at
- policy_version
- predicted_recall_probability?
- predicted_outcome

- hidden_until_answer

- resolved_at?
- actual_rating?
- actual_recall_success?
- result?

- seed?
- model_metadata?
- source_review_id?
- reconciliation_state?
```

---

# 11. Prediction Lifecycle

Recommended lifecycle:

```text
PLANNED
   ↓
COMMITTED
   ↓
HIDDEN
   ↓
RESOLVED
```

Additional states:

```text
INVALIDATED
REVERSED
EXPIRED
```

### PLANNED

Candidate identified but not yet trusted as a user-visible commitment.

### COMMITTED

Prediction is durably fixed.

### HIDDEN

Prediction exists and is waiting for the relevant review.

### RESOLVED

Outcome observed and result calculated.

### INVALIDATED

Prediction can no longer be safely resolved.

### REVERSED

A previously resolved source review was undone/reconciled.

### EXPIRED

Prediction is no longer relevant due to session/card state.

Use cautiously.

---

# 12. Candidate Selection

Candidate selection is PROVISIONAL.

Potential inputs:

- retrievability
- stability
- difficulty
- lapse history
- interval
- recent review history
- card age
- prior Oracle history

Exact scoring formula is DEFERRED.

Locked requirements:

- candidate selection must be based on real memory data,
- selection must not rely on answer outcome that has not yet occurred,
- selection must be explainable,
- selection should avoid selecting every card,
- selection should not overload the session.

---

# 13. Number of Predictions

Possible session design:

```text
3–5 Oracle predictions per standard Expedition
```

This is PROVISIONAL.

Prediction density should be low enough that:

- reveal remains special,
- reviewer does not become noisy,
- Oracle does not dominate Expedition.

Exact count may depend on Expedition size.

---

# 14. Commitment Timing

Preferred commitment timing:

- at Expedition planning/start,
- or sufficiently before the target card answer,
- persisted before the outcome can be observed.

Strong default:

> Commit Oracle predictions when Expedition starts.

Benefits:

- simple trust model,
- stable reload behavior,
- easy testing,
- no "late prediction" suspicion.

Potential downside:

- cards may not appear as expected.

This tradeoff must be validated.

---

# 15. Prediction Target Semantics

Oracle needs a clear definition of what it predicts.

Recommended initial concept:

> Probability that the learner will successfully recall the card on its next review in this Expedition.

This wording is product-level.

Exact mapping to available FSRS/retrievability data remains technical.

Do not overclaim scientific certainty.

---

# 16. Predicted Outcome

Possible internal output:

```text
LIKELY_RECALL
LIKELY_FORGET
```

However, user-facing Oracle should likely focus only on selected risky cards.

Example:

> Oracle selected this because recall looked uncertain.

Exact threshold is PROVISIONAL.

---

# 17. Actual Recall Success

The product must define `actual_recall_success`.

Recommended initial convention:

```text
Again → recall failure
Hard/Good/Easy → recall success
```

Important:

This is a product convention derived from grading behavior.

It must not be described as direct cognitive measurement.

This mapping should be documented and versioned.

---

# 18. Oracle Result

Possible result values:

```text
PLAYER_DEFEATED_PREDICTION
ORACLE_CORRECT
UNRESOLVED
INVALIDATED
REVERSED
```

Example:

Oracle predicted likely failure.

User presses:

```text
Again → ORACLE_CORRECT
Hard  → PLAYER_DEFEATED_PREDICTION
Good  → PLAYER_DEFEATED_PREDICTION
Easy  → PLAYER_DEFEATED_PREDICTION
```

---

# 19. No Reward Pressure

Oracle must not create incentives such as:

```text
Good gives +3 score
Easy gives +5 score
```

That would bias grading.

Recommended score logic:

- Oracle point if prediction correctly identifies failure,
- Player point if predicted-failure card is successfully recalled.

No difference between Hard/Good/Easy for competition scoring.

---

# 20. Session Score

Possible session presentation:

```text
YOU 3 : 1 ORACLE
```

This is a narrative score, not XP.

It should reflect only resolved Oracle predictions.

Do not let the score influence scheduling or rewards.

---

# 21. Lifetime Record

Possible history:

```text
Lifetime
You 42 : 31 Oracle
```

This should remain secondary.

Avoid turning Oracle into a leaderboard with itself.

Potential long-term stats:

- predictions faced
- predictions defeated
- Oracle correct
- average predicted probability
- memorable reversals

Keep statistics concise.

---

# 22. Reveal Timing

Locked rule:

> Oracle reveal occurs only after the learner has answered/graded the card.

Preferred sequence:

```text
card question
    ↓
answer shown
    ↓
grade selected
    ↓
review accepted
    ↓
Oracle reveal
    ↓
next card
```

Exact Anki hook boundary must match Phase 0/1 integration.

---

# 23. Reveal UX

Example:

```text
        ORACLE REVEALED

      Predicted recall
            58%

       YOU REMEMBERED

         YOU 3 : 1
          ORACLE
```

Alternative wording:

```text
Oracle expected a miss.
You recalled it.
```

Copy should remain concise.

---

# 24. Reveal Duration

Target:

- short,
- approximately one standard reveal,
- not blocking review unnecessarily,
- dismissible,
- keyboard-friendly.

Reduced-motion mode should use static/fade behavior.

---

# 25. Oracle Visual Grammar

Per design system:

**Geometry:** circle / eye / orbit / eclipse  
**Material:** luminous glass / celestial instrument  
**Motion:** lock / align / reveal / rotate  
**Mood:** foresight / uncertainty / quiet challenge

Avoid:

- skulls,
- gambling chips,
- slot-machine effects,
- aggressive red warning screens.

---

# 26. Hidden State UX

The user may know that Oracle has predictions locked for the Expedition.

Example Today/Expedition signal:

```text
Oracle
4 predictions locked
```

This is allowed.

What is not allowed:

```text
Card #17 is one of them.
```

Identity remains hidden until resolution.

---

# 27. Oracle and Curiosity

The system may create anticipation by showing:

```text
4 predictions locked
2 resolved
```

It should not constantly tease exact distance to the next Oracle card if that distracts recall.

Distance hints are PROVISIONAL and should default to conservative behavior.

---

# 28. Explainability

Oracle must be explainable after resolution.

Possible details panel:

```text
Why this card?

- lower predicted recall
- longer interval
- recent lapse history
```

Exact explanation depends on available model inputs.

Do not expose raw technical metrics unless useful.

---

# 29. Scientific Wording

Avoid:

> Oracle knew you would forget.

Prefer:

> Oracle estimated this memory was fragile.

Avoid:

> 58% chance your brain would fail.

Prefer:

> Estimated recall probability: 58%

Use probabilistic language.

---

# 30. Calibration

Oracle accuracy may matter for trust.

Future evaluation may measure:

- predicted probability calibration
- failure hit rate
- false positives
- user-defeated predictions

Phase 2 should instrument enough local aggregate data to inspect whether the system is wildly miscalibrated.

Do not claim predictive quality without evidence.

---

# 31. Candidate Diversity

Oracle should avoid selecting:

- the same card too frequently,
- only one deck repeatedly,
- cards with insufficient history if prediction quality is poor.

Exact diversity policy is PROVISIONAL.

Potential inputs:

- cooldown
- recent Oracle selection history
- deck distribution
- confidence threshold

---

# 32. Oracle Cooldown

A card may need a cooldown after being selected.

Purpose:

- preserve novelty,
- avoid harassment,
- avoid overfitting user attention to a single card.

Exact cooldown is DEFERRED.

---

# 33. Persistence

Phase 2 adds durable storage for Oracle predictions.

Expected table:

```text
oracle_predictions
```

Core fields:

- prediction ID
- expedition ID
- card ID
- commit timestamp
- policy version
- predicted probability/outcome
- resolution state
- result
- reconciliation metadata

---

# 34. Migration

Phase 2 must add a schema migration from Phase 1.

Tests must cover:

- fresh install
- Phase 1 → Phase 2
- rollback/failure
- reopen
- existing Expedition history preservation

---

# 35. Repository Boundary

Possible operations:

```text
commit_prediction
get_hidden_predictions
get_prediction_for_card
resolve_prediction
invalidate_prediction
reverse_resolution
list_session_results
```

UI must not write SQL directly.

---

# 36. Oracle Service

Responsibilities:

- candidate scoring
- commitment
- resolution
- invalidation
- history summary
- explanation data

Not responsibilities:

- reviewer rendering
- Expedition ownership
- scheduling
- Rescue logic

---

# 37. Expedition Integration

Oracle requires:

- active Expedition ID
- stable review events
- session start boundary
- post-grade reveal boundary
- completion boundary

Potential flow:

```text
ExpeditionStarted
   ↓
Oracle commits predictions

ReviewAnswered
   ↓
Oracle checks card ID
   ↓
prediction resolves
   ↓
OraclePredictionResolved
   ↓
EventOrchestrator
```

---

# 38. Event Orchestration

Oracle reveal is a major narrative event.

If another major event exists at the same review boundary:

- priority rules apply,
- one reveal surfaces,
- others defer or collapse.

Exact priority relative to future Rescue/Nemesis is DEFERRED.

Phase 2 should only implement a clean priority contract.

---

# 39. Focus Mode

Focus Mode should preserve Oracle domain logic but simplify presentation.

Standard:

```text
full reveal
score update
short animation
```

Focus Mode:

```text
small inline result
or compact toast
no orbit animation
```

Oracle commitments and results remain identical.

---

# 40. Reduced Motion

Reduced-motion behavior:

- no rotating orbit
- no zoom
- no pulsing
- static symbol
- short fade or immediate reveal

---

# 41. Keyboard Interaction

Required:

- dismiss reveal
- inspect explanation if exposed
- continue review

Focus must return predictably to reviewer flow.

---

# 42. Undo/Reversal

If the source review is undone:

- resolved Oracle state must reconcile,
- session score must reconcile,
- history must not permanently preserve a false result.

Potential approaches depend on Phase 0 undo strategy.

Locked:

> Oracle result must not remain permanently resolved against a review that no longer exists.

---

# 43. Card Deletion

If a committed Oracle card is deleted before review:

- mark prediction invalidated/orphaned,
- do not crash,
- do not count result,
- preserve minimal audit history if useful.

Do not retain card content by default.

---

# 44. Expedition Ends Before Resolution

If Expedition ends with unresolved Oracle predictions:

Possible states:

- archive unresolved,
- expire,
- carry none forward.

Recommended initial behavior:

> Unresolved predictions close with the Expedition and do not silently move to another Expedition.

Status: PROVISIONAL.

This keeps session semantics clean.

---

# 45. Cross-Day Resume

If an Expedition resumes later:

- committed Oracle predictions remain fixed,
- no reroll,
- no recalculation unless explicitly invalidated.

This is LOCKED.

---

# 46. Duplicate Event Protection

A single review must not resolve the same Oracle prediction twice.

Use:

- source review identity,
- resolved state guard,
- idempotent update.

---

# 47. Determinism

Where candidate selection involves randomness:

- seed it,
- persist chosen predictions,
- avoid reroll on reload.

Once committed, persisted state is authoritative.

---

# 48. Time Handling

Store:

- committed_at UTC
- resolved_at UTC
- Expedition local study date via parent relationship

Do not use midnight to invalidate predictions artificially.

---

# 49. Privacy

Oracle storage should not include full card text by default.

Prefer:

- card ID
- numeric memory metadata
- policy version
- result

Explanation can be generated from state metadata.

---

# 50. Performance

Critical paths:

- Expedition-start candidate selection
- commitment writes
- per-review lookup
- resolution write
- reveal projection

Preferred strategy:

```text
Expedition start:
batch candidate analysis

Review path:
indexed lookup by card_id + expedition_id
tiny resolution update
```

Avoid:

- full collection scans per review
- recalculating Oracle score on every card transition

---

# 51. Performance Targets

Provisional targets:

```text
Oracle lookup on review:
preferred < 1 ms domain/repository hot lookup

Resolution logic:
preferred < 2 ms

Commit transaction:
small and bounded

Added reviewer overhead:
remain inside global reviewer budget
```

Measure actual implementation.

---

# 52. Candidate Computation Strategy

Potential implementation:

1. fetch eligible cards in batch
2. obtain memory metrics
3. calculate risk score
4. apply diversity/cooldown
5. choose fixed set
6. persist commitments

This is PROVISIONAL.

Exact algorithm must be justified by available Anki/FSRS data.

---

# 53. Prediction Policy Version

Each prediction stores:

```text
oracle_policy_version
```

Why:

- scoring rules may evolve,
- threshold may change,
- explanation must remain interpretable,
- historical comparisons need context.

---

# 54. Testing Requirements

## Commitment

- prediction commits before answer
- persisted before outcome
- reload preserves prediction
- same Expedition does not reroll

## Candidate Selection

- deterministic under same seed
- only eligible cards selected
- no duplicates
- respects count limit
- cooldown if implemented

## Resolution

- Again → Oracle correct for predicted-failure target
- Hard/Good/Easy → player defeats prediction
- result only resolves once
- unresolved card stays unresolved

## Undo

- resolved prediction reverses/reconciles
- score updates accordingly

## Invalidations

- deleted card
- ended Expedition
- missing source card
- profile switch

## UX

- reveal post-answer only
- no pre-answer marker
- Focus Mode compact behavior
- reduced-motion fallback

## Persistence

- migration
- reopen
- crash before reveal
- crash after resolution write

---

# 55. Crash Recovery

Test:

### Case A

Prediction committed, Anki crashes before card appears.

Expected:

- prediction remains committed.

### Case B

Card answered, resolution persisted, crash before reveal.

Expected:

- domain result remains correct,
- presentation may safely reappear or be summarized.

### Case C

Reveal shown, crash before dismissal.

Expected:

- no duplicate domain resolution.

---

# 56. Manual Host Test

Minimum:

```text
1. Start Expedition.
2. Confirm Oracle count locked.
3. Restart before Oracle card appears.
4. Confirm prediction set unchanged.
5. Reach Oracle card.
6. Verify no pre-answer visual marker.
7. Grade Again.
8. Verify Oracle result appears after answer.
9. Reach another predicted card.
10. Grade Good.
11. Verify player result.
12. Undo one Oracle review.
13. Confirm score/state reconciliation.
14. Toggle Focus Mode.
15. Verify compact result.
16. Complete Expedition.
17. Confirm unresolved Oracle handling.
```

---

# 57. UX Success Criteria

Oracle succeeds if users understand:

- prediction existed before answer,
- selection is probabilistic,
- recalling successfully "beats" the prediction,
- Again is not punished beyond Oracle being correct,
- Oracle score does not affect scheduling.

---

# 58. Trust Risks

## Risk 1 — Fake Prediction Suspicion

Mitigation:

persist commitments and make system behavior consistent.

## Risk 2 — Prediction Too Accurate

Could feel discouraging.

Mitigation:

framing should remain playful and probabilistic.

## Risk 3 — Prediction Too Poor

Could feel random.

Mitigation:

calibration evaluation and explainability.

## Risk 4 — Biasing Recall

Mitigation:

hide identity until post-answer.

## Risk 5 — Grading Bias

Mitigation:

Hard/Good/Easy all count equally as successful recall for Oracle score.

---

# 59. Anti-Patterns

Do not implement:

### Oracle Warning Before Recall

> "Careful, this is a risky card."

### Score Multipliers

> Easy gives 3 points.

### Fake Retrospective Prediction

Calculate after answer and pretend it was earlier.

### Oracle Currency

Earn gems by beating Oracle.

### Public Shame

> Oracle destroyed you today.

### Infinite Rematch

Immediately generate new Oracle prediction after every resolution.

---

# 60. Explainability Example

Potential user-facing explanation:

```text
Why did Oracle choose this?

This memory had a lower estimated recall probability than most cards in this Expedition.

Signals included:
• longer time since review
• weaker recent stability
• prior lapse history
```

Only show signals actually used.

---

# 61. Copy Tone

Preferred:

```text
Oracle revealed.
Oracle expected a miss.
You remembered.
Prediction defeated.
Oracle was correct.
4 predictions locked.
```

Avoid:

```text
You destroyed the AI!
Oracle owns you!
Your brain failed!
Bet again!
```

---

# 62. Success Metrics

Potential local/opt-in product metrics:

- predictions per Expedition
- prediction resolution rate
- player defeat rate
- Oracle correct rate
- reveal dismiss time
- unresolved prediction rate
- calibration buckets
- Focus Mode usage

Do not optimize Oracle for maximum failure prediction.

The goal is meaningful challenge, not making the user lose.

---

# 63. Open Questions

## Q2-01 — Candidate Formula

Which combination of retrievability/stability/difficulty/history is best?

Status: DEFERRED.

---

## Q2-02 — Threshold

What probability range produces useful tension?

Status: DEFERRED.

---

## Q2-03 — Prediction Count

Fixed count or proportional to Expedition size?

Status: PROVISIONAL.

---

## Q2-04 — Reveal Probability Number

Should the user always see a percentage?

Potential concern:

false scientific precision.

Status: UX TEST.

---

## Q2-05 — Lifetime Score

How prominent should You vs Oracle lifetime history be?

Status: PROVISIONAL.

---

## Q2-06 — Unresolved Predictions

Archive vs expire at Expedition end?

Status: PROVISIONAL.

---

## Q2-07 — Candidate Cooldown

Needed from first release?

Status: PROVISIONAL.

---

# 64. Definition of Done

Phase 2 is complete when:

- [ ] Oracle candidate service exists
- [ ] predictions are committed before answer
- [ ] commitments persist across restart
- [ ] prediction identity remains hidden before answer
- [ ] review lookup is efficient
- [ ] Again resolves as recall failure
- [ ] Hard/Good/Easy resolve as recall success
- [ ] grading buttons do not change Oracle reward magnitude
- [ ] result resolves exactly once
- [ ] undo/reversal reconciles
- [ ] deleted/missing cards invalidate safely
- [ ] cross-day resume does not reroll
- [ ] Expedition end handles unresolved predictions
- [ ] session score works
- [ ] basic lifetime/history works
- [ ] explanation is available or architecture-ready
- [ ] Focus Mode works
- [ ] reduced motion works
- [ ] keyboard path works
- [ ] migration tested
- [ ] crash recovery tested
- [ ] performance measured
- [ ] manual host validation completed
- [ ] ADRs/backlog updated
- [ ] `PHASE_2_ORACLE_HANDOFF.md` exists

---

# 65. Phase 3 Contract

Rescue may begin only after Oracle proves:

- memory-derived feature selection can happen outside reviewer hot path,
- review events are stable,
- feature state can persist safely,
- post-answer reveals are orchestrated,
- undo reconciliation works,
- per-card feature lookup is fast.

Rescue should reuse:

- Memory Engine access patterns,
- EventOrchestrator,
- feature policy versioning,
- presentation infrastructure.

Rescue must not duplicate Oracle infrastructure.

---

# 66. Locked vs Provisional Summary

## Locked

- prediction committed before outcome
- no pre-answer card identity reveal
- no recall bias
- no grading reward difference between Hard/Good/Easy
- persisted commitments survive reload
- no reroll after commitment
- undo reconciles
- one result per source review
- session belongs to Expedition
- Oracle does not affect scheduling

## Provisional

- candidate formula
- threshold
- number of predictions
- percentage display
- cooldown
- unresolved prediction end behavior
- lifetime score prominence
- exact reveal animation

---

# Phase 2 North Star

> **Create tension through honest prediction, then let genuine recall decide who was right.**
