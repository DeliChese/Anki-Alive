# PHASE_6_RELICS.md

# Anki Alive — Phase 6: Relics

## 1. Phase Goal

Create long-term ownership, identity, and historical meaning from memories that have remained stable over time.

Relics should create the feeling:

> "This is knowledge I have genuinely carried with me."

A Relic is not an arbitrary collectible.

It is a persistent historical state derived from real memory survival.

---

# 2. Phase Status

```text
Status: SPECIFIED
Phase: 6
Name: Relics
Depends on: Phase 5 — Fragments
Next phase: Phase 7 — Memory World
```

---

# 3. Product Role

Relics are the strongest long-term progression layer in Anki Alive.

They provide:

- ownership,
- identity,
- continuity,
- historical significance,
- long-term reward without currency.

Relics should become more meaningful the longer a learner uses Anki Alive.

---

# 4. Core User Problem

Long-term memory progress is often invisible.

A learner may have remembered a card reliably for:

- six months,
- one year,
- several years,

yet the experience remains visually similar to an ordinary card.

Relics make long-lived knowledge feel historically significant.

---

# 5. Behavioral Goal

Relics should create:

- pride in genuine retention,
- attachment to long-term learning history,
- motivation to preserve memory,
- meaningful recovery after forgetting,
- identity that compounds over time.

The intended loop:

```text
memory matures
    ↓
formation threshold reached
    ↓
Relic forms
    ↓
history persists
    ↓
future review maintains or changes state
    ↓
possible fracture
    ↓
genuine recovery
    ↓
restoration
```

---

# 6. Critical Product Invariant

> **Relic value must come from real memory history, not artificial rarity.**

A Relic should not be valuable because the UI declares:

> Legendary.

It should be valuable because:

- it survived,
- it was difficult,
- it became stable,
- it has history.

---

# 7. No Arbitrary Collection Economy

Relics must not become:

- tradable items,
- purchasable cosmetics,
- NFT-like objects,
- currency,
- loot drops,
- random rarity rewards.

Their value is personal memory history.

---

# 8. In Scope

Phase 6 includes:

- Relic eligibility
- formation
- persistent Relic lifecycle
- Relic Vault
- fracture
- restoration
- long-term history
- formation metadata
- visual identity
- procedural visual foundation
- Expedition/EventOrchestrator integration
- Fragment integration
- Nemesis/Rescue history integration
- Focus Mode
- reduced motion
- accessibility
- migration
- testing
- performance
- crash recovery

---

# 9. Explicitly Out of Scope

Phase 6 does not implement:

- Memory World
- social trading
- marketplace
- currency
- rarity monetization
- public ranking
- cosmetic shop
- permanent loss
- streak-based Relics
- daily Relic claims

---

# 10. Relic Entity

Conceptual model:

```text
Relic
- relic_id
- card_id

- formed_at
- formation_policy_version
- state

- first_learning_at?
- formation_stability?
- formation_interval_days?
- formation_difficulty?
- formation_success_count?
- formation_lapse_count?

- visual_seed
- visual_family?
- visual_version

- fractured_at?
- restored_at?
- archived_at?

- last_source_review_id?
- reconciliation_state?
```

---

# 11. Relic Lifecycle

Recommended:

```text
CANDIDATE
   ↓
ACTIVE
   ↓
FRACTURED
   ↓
RESTORING
   ↓
RESTORED
```

Additional states:

```text
ORPHANED
ARCHIVED
REVERSED
```

### CANDIDATE

Card approaches formation criteria.

### ACTIVE

Relic has formed and memory is currently stable.

### FRACTURED

A meaningful memory regression occurred.

### RESTORING

Recovery has begun but durable restoration is not yet complete.

### RESTORED

Memory recovered after fracture.

### ORPHANED

Source card no longer exists.

### ARCHIVED

Historical state intentionally closed.

---

# 12. Formation Philosophy

Relic formation should be rare enough to matter, but not so rare that only multi-year users ever see one.

Potential inputs:

- stability
- interval
- age
- successful recall history
- lapse history
- difficulty
- long-term survival

Exact policy is DEFERRED.

Locked:

- formation is evidence-based,
- formation policy is versioned,
- one rating cannot instantly form a Relic,
- formation history is preserved permanently unless user explicitly resets data.

---

# 13. Formation Candidate

A candidate may be surfaced before formation.

Possible:

```text
This memory is approaching Relic status.
```

However:

- do not show fake countdowns,
- do not imply exact future formation if scheduler state may change.

Status: PROVISIONAL.

---

# 14. Formation Event

When criteria are satisfied:

```text
RELIC FORMED

First learned: ...
Current stability: ...
Successful recalls: ...
```

Only real metrics.

This is a major event.

---

# 15. Formation Timing

Preferred:

- after review state is accepted,
- checkpoint,
- Expedition completion,
- or another natural closure boundary.

Avoid interrupting active recall.

---

# 16. Formation History

Formation metadata should be preserved even if the memory later changes.

Why:

> "This memory became a Relic on this date."

remains historically true.

Do not overwrite formation history with current state.

---

# 17. Relic Vault

Phase 6 introduces the Relic Vault.

Purpose:

- browse Relics,
- inspect history,
- see active/fractured/restored states,
- reinforce ownership.

The Vault is exploratory.

It is not part of critical review flow.

---

# 18. Relic Vault Information Architecture

Potential sections:

```text
All Relics
Active
Fractured
Restored
Oldest
Recent
```

Avoid too many categories initially.

---

# 19. Relic Tile

Conceptual tile:

```text
[ procedural artifact ]

First learned: 2024-03-17
Age: 2.4y
State: Active
Stability: ...
```

Card content may be resolved live from Anki when appropriate.

Do not store full card text by default.

---

# 20. Relic Detail

Potential information:

- formation date
- first learning date
- current state
- formation metrics
- current memory metrics
- fracture history
- restoration history
- former Nemesis status
- Rescue history
- meaningful milestones

Keep hierarchy clear.

Do not turn it into a raw analytics dump.

---

# 21. Fracture

A Relic may fracture when real memory regression occurs.

Potential signals:

- meaningful lapse after long stability,
- large stability decrease,
- repeated failure after formation.

Exact fracture policy is DEFERRED.

Locked:

> fracture must represent real memory regression.

---

# 22. Fracture Is Not Destruction

When a Relic fractures:

- its history remains,
- formation date remains,
- visual identity remains,
- it becomes recoverable.

No permanent deletion.

---

# 23. Fracture UX

Possible:

```text
RELIC FRACTURED

A long-held memory became unstable.
```

Avoid:

```text
You lost your Relic!
```

The event should feel meaningful but not punitive.

---

# 24. Restoration

Restoration requires genuine recovery.

Potential criteria:

- stability rebuilt,
- successful future recall,
- sustained recovery,
- threshold re-crossed.

Exact policy is DEFERRED.

Locked:

> restoration must require real memory improvement.

---

# 25. Restoration State

Recommended:

```text
FRACTURED
   ↓
RESTORING
   ↓
RESTORED
```

A single successful answer may begin restoration but should not necessarily complete it.

---

# 26. Restoration UX

Possible:

```text
RELIC RESTORED

This memory became stable again.
```

This should be one of the strongest recovery moments in the product.

---

# 27. Multiple Fractures

A Relic may fracture more than once.

History should preserve meaningful cycles.

Avoid flattening everything into one boolean.

Potential:

```text
RelicHistoryEvent
- formed
- fractured
- restored
- fractured
- restored
```

Do not store redundant review log.

---

# 28. Relic and Nemesis

A former Nemesis may later become a Relic.

This is particularly meaningful.

Possible history:

```text
Nemesis defeated
    ↓
months later
    ↓
Relic formed
```

This may create a high-significance milestone.

---

# 29. Relic and Rescue

A fractured Relic may enter Rescue.

This overlap is allowed.

Rescue describes current fragility.

Relic describes long-term historical identity.

Do not merge them.

---

# 30. Relic and Fragments

Fragments may reveal:

- a newly formed Relic,
- an unusually old Relic,
- a restored Relic,
- a Relic precursor.

Phase 6 should provide stable history interfaces for this.

---

# 31. Event Priority

Relic formation/restoration are major long-term events.

Provisional priority:

```text
Relic formation
Relic restoration
Nemesis defeat
Oracle reveal
Rescue major recovery
Fragment reveal
minor events
```

Exact ordering may be refined.

Locked:

- one prominent reveal per review boundary.

---

# 32. Domain Events

Phase 6 may add:

```text
RelicCandidateDetected
RelicFormed
RelicFractured
RelicRestorationStarted
RelicRestored
RelicOrphaned
RelicArchived
RelicReversed
```

---

# 33. Persistence

Phase 6 adds:

```text
relics
```

Potential supporting table:

```text
relic_history_events
```

Use a separate history table only if needed to preserve multiple fracture/restoration cycles cleanly.

---

# 34. Migration

Phase 6 adds migration from Phase 5.

Tests:

- fresh install
- Phase 5 → Phase 6
- rollback/failure
- Fragment/Nemesis/Rescue/Oracle/Expedition data preserved

---

# 35. Relic Repository

Possible operations:

```text
create_candidate
form
get_for_card
list_active
fracture
begin_restore
restore
orphan
archive
list_history
```

No UI SQL.

---

# 36. Relic Service

Responsibilities:

- eligibility
- formation
- fracture
- restoration
- lifecycle
- history
- visual identity seed
- explanation metadata

Not responsibilities:

- scheduling
- reviewer rendering
- Memory World layout

---

# 37. Policy Versioning

Store:

```text
formation_policy_version
fracture_policy_version?
restoration_policy_version?
```

At minimum, formation policy must be versioned.

Separate versions may be justified if rules evolve independently.

---

# 38. Explainability

Users should be able to understand:

> Why did this become a Relic?

Possible:

```text
This memory formed a Relic because it remained stable over a long period and survived repeated reviews.
```

Signals may include:

- long stability
- interval length
- successful recall history
- low recent lapse rate

Only real signals.

---

# 39. Scientific Wording

Avoid:

> This memory is permanent.

Prefer:

> This memory has remained highly stable.

Avoid:

> Immortal memory.

If poetic language is used, pair it with accurate metadata.

---

# 40. Visual Identity

Relics should feel unique.

However, uniqueness should be generated from stable data.

Potential inputs:

```text
card_id
formed_at
age
difficulty
stability
history
```

Output:

```text
visual_seed
visual_family
shape parameters
fracture parameters
```

---

# 41. Procedural Relic System

Recommended approach:

- small number of base families,
- procedural variation,
- deterministic seed,
- reusable vector/material system,
- no per-card AI image generation at runtime.

Possible families:

```text
MONOLITH
RING
PRISM
SEAL
ORBITAL
SHARD_CORE
```

Names are PROVISIONAL.

---

# 42. Procedural Parameters

Potential parameters:

- symmetry
- facet count
- ring count
- core shape
- luminous vein pattern
- crack topology
- surface density
- glow intensity
- silhouette complexity

These should be derived deterministically.

---

# 43. Generated Asset Role

Image generation may be used during design/development to create:

- base Relic family concepts,
- material studies,
- lighting studies,
- visual reference sheets.

Production should prefer reproducible assets/components.

Do not generate each user's Relic from a remote model.

---

# 44. Fracture Visual

Fracture should preserve the same artifact identity.

Do not replace the Relic with an unrelated image.

Use:

- crack topology,
- dimmed core,
- separated facets,
- broken ring.

Restoration should visibly reconnect the same object.

---

# 45. Relic Visual Grammar

Per design system:

**Geometry:** symmetric artifact / preserved structure  
**Material:** matte stone / mineral / translucent core  
**Motion:** awaken / fracture / restore / settle  
**Mood:** history / permanence / ownership

Avoid:

- treasure chest
- trophy cup
- gem rarity UI
- ornate medieval relics
- weapon imagery

---

# 46. Focus Mode

Focus Mode:

- Relic domain behavior unchanged,
- formation may surface as compact toast,
- larger reveal can defer to session completion/history,
- no major animation during review.

Vault remains available outside review.

---

# 47. Reduced Motion

Reduced motion:

- no assembling artifact animation,
- no long fracture effect,
- static state transition,
- short fade,
- no looping glow.

---

# 48. Accessibility

Required:

- state labels in text,
- fracture not color-only,
- keyboard Vault navigation,
- visible focus,
- reduced motion,
- scalable tiles/details,
- non-essential art must not hide data.

---

# 49. Vault Performance

Relic Vault may contain many items.

Use:

- pagination
- virtualization
- lazy rendering
- cached projections

Do not render hundreds/thousands of complex artifacts at full fidelity simultaneously.

---

# 50. Large Collection Strategy

Long-term users may eventually have many Relics.

Possible strategy:

- lightweight tile previews,
- detail render on selection,
- LOD for procedural assets,
- indexed filters.

---

# 51. Current vs Formation State

Relic detail should distinguish:

### Formation state

Historical snapshot when Relic formed.

### Current state

Current Anki-derived memory state.

Do not overwrite historical data.

---

# 52. First Learning Date

First-learning inference may be imperfect depending on available history.

If uncertain:

- use accurate wording,
- document inference,
- avoid false precision.

Example:

> Earliest observed learning date

if exact first learning cannot be guaranteed.

---

# 53. Card Deletion

If source card is deleted:

- mark Relic ORPHANED,
- preserve historical entity,
- avoid full content retention,
- UI may show "source card no longer exists."

Do not silently delete Relic history.

---

# 54. Undo/Reversal

If a review triggers:

- formation
- fracture
- restoration

and is undone:

state must reconcile.

Important nuance:

Formation may be based on broader historical thresholds, not only one review.

Reconciliation should re-evaluate policy rather than blindly reverse if the state remains valid.

---

# 55. Duplicate Protection

Ensure:

- one formation event
- one fracture transition per causal state
- one restoration event
- no duplicate history entries after reload/crash

Transitions should be idempotent.

---

# 56. Crash Recovery

### Case A

Formation persisted, crash before reveal.

Expected:

- Relic exists,
- reveal may defer.

### Case B

Fracture persisted, crash.

Expected:

- state remains fractured,
- no duplicate fracture history.

### Case C

Restoration persisted, crash before completion UI.

Expected:

- restored history remains correct.

---

# 57. History Significance

Relic events are high-significance by default.

Persist:

- formation
- fracture
- restoration

Potentially also:

- major age milestones

Do not create daily Relic history noise.

---

# 58. Age Milestones

Possible future milestones:

```text
1 year
2 years
5 years
```

These are PROVISIONAL.

Avoid arbitrary celebration inflation.

---

# 59. Performance

Critical reviewer-path operations:

- active Relic lookup by card
- fracture/formation/restore evaluation when relevant
- event creation

Heavy Vault rendering stays outside reviewer.

---

# 60. Performance Targets

Provisional:

```text
Relic lookup:
preferred < 1 ms

state transition evaluation:
preferred < 2 ms

reviewer total:
within global budget
```

Vault should remain interactive with large Relic counts.

---

# 61. Candidate Evaluation Strategy

Preferred:

- incremental memory-state updates
- bounded candidate set
- periodic eligibility analysis
- no full collection scan per review

---

# 62. Testing Requirements

## Formation

- qualifying memory forms Relic
- non-qualifying memory does not
- one grade alone cannot form if policy requires durable history
- policy version stored
- formation metadata preserved

## Lifecycle

- candidate → active
- active → fractured
- fractured → restoring
- restoring → restored
- orphan
- archive

## Integrity

- no permanent loss
- fracture requires real regression
- restoration requires real improvement
- duplicate transitions prevented

## Persistence

- migration
- restart
- history persistence
- visual seed persistence

## Undo

- formation reconciliation
- fracture reconciliation
- restoration reconciliation

## UX

- Vault keyboard navigation
- Focus Mode
- reduced motion
- state labels
- no rarity/casino language

## Cross-Feature

- Nemesis → Relic
- Relic + Rescue
- Fragment reveal
- EventOrchestrator overlap

---

# 63. Manual Host Test

Minimum:

```text
1. Prepare qualifying Relic candidate.
2. Trigger formation.
3. Confirm formation metadata.
4. Restart Anki.
5. Confirm Relic persists.
6. Open Vault.
7. Navigate with keyboard.
8. Trigger fracture under test conditions.
9. Confirm history remains.
10. Trigger restoration.
11. Undo causal review where supported.
12. Confirm reconciliation.
13. Toggle Focus Mode.
14. Test overlap with Rescue/Nemesis/Fragment.
15. Delete source card.
16. Confirm orphaned historical state.
17. Test many Relics in Vault fixture.
```

---

# 64. Success Metrics

Potential evaluation:

- Relics formed
- time-to-formation
- fracture rate
- restoration rate
- age distribution
- former Nemesis → Relic transitions
- Vault usage
- large-Vault performance

Do not optimize for maximizing Relic count.

Scarcity should emerge from real memory criteria.

---

# 65. Trust Risks

## Risk 1 — Fake Rarity

Mitigation:

no arbitrary rarity tiers.

## Risk 2 — Permanent Loss Anxiety

Mitigation:

fracture is recoverable.

## Risk 3 — Overclaiming Memory Permanence

Mitigation:

accurate stability wording.

## Risk 4 — Visual System Overwhelms UX

Mitigation:

procedural assets remain subordinate to readable data.

## Risk 5 — Too Many Relics

Mitigation:

meaningful formation threshold and scalable Vault.

---

# 66. Anti-Patterns

Do not implement:

### Legendary / Epic Loot Tier

### Relic Coins

### Paid Relic Skins

### Permanent Relic Deletion on Failure

### Daily Relic Claim

### Rating-Based Formation

```text
Easy = instant Relic
```

### Remote Runtime AI Generation per Card

---

# 67. Copy Tone

Preferred:

```text
Relic formed.
Relic fractured.
Restoration in progress.
Relic restored.
This memory has remained highly stable.
```

Avoid:

```text
Legendary drop!
Your Relic died!
Epic artifact unlocked!
```

---

# 68. Open Questions

## Q6-01 — Formation Formula

Status: DEFERRED.

---

## Q6-02 — Fracture Threshold

Status: DEFERRED.

---

## Q6-03 — Restoration Criteria

Status: DEFERRED.

---

## Q6-04 — Procedural Family Count

Status: DESIGN RESEARCH.

---

## Q6-05 — Formation Candidate Preview

Should users see "approaching Relic"?

Status: UX TEST.

---

## Q6-06 — First Learning Date Reliability

Status: IMPLEMENTATION RESEARCH.

---

## Q6-07 — Relic History Table

Separate event table vs general history service?

Status: ARCHITECTURE DECISION.

---

# 69. Definition of Done

Phase 6 is complete when:

- [ ] Relic candidate policy exists
- [ ] formation is evidence-based
- [ ] formation policy version stored
- [ ] formation metadata preserved
- [ ] Relic persists across restart
- [ ] Vault exists
- [ ] Vault supports keyboard navigation
- [ ] visual seed is deterministic/persisted
- [ ] fracture requires real regression
- [ ] fracture is recoverable
- [ ] restoration requires real improvement
- [ ] history preserves formation/fracture/restoration
- [ ] current state does not overwrite formation state
- [ ] no arbitrary rarity economy exists
- [ ] no permanent failure loss exists
- [ ] undo/reversal reconciles
- [ ] card deletion/orphan handling works
- [ ] Nemesis/Rescue/Fragment overlap works
- [ ] EventOrchestrator prevents stacked major reveals
- [ ] Focus Mode works
- [ ] reduced motion works
- [ ] migration tested
- [ ] crash recovery tested
- [ ] Vault scaling tested
- [ ] performance measured
- [ ] manual host validation completed
- [ ] ADRs/backlog updated
- [ ] `PHASE_6_RELICS_HANDOFF.md` exists

---

# 70. Phase 7 Contract

Memory World may begin only after Relics proves:

- long-term history is durable,
- visual identities can be generated deterministically,
- persistent memory entities remain scalable,
- historical state can coexist with current Anki state,
- rich exploratory UI can remain accessible and performant.

Memory World should reuse:

- Relic history
- Nemesis history
- Rescue history
- Fragment milestones
- Memory Engine projections
- design tokens
- accessibility modes
- procedural visual primitives

Memory World should primarily be a projection layer.

It must not duplicate all canonical memory data.

---

# 71. Locked vs Provisional Summary

## Locked

- Relics come from real long-term memory history
- no arbitrary rarity economy
- formation metadata preserved
- fracture represents real regression
- fracture is recoverable
- restoration requires real improvement
- no permanent loss
- persists across sessions
- visual identity deterministic
- current state does not overwrite formation state
- no runtime AI generation dependency
- one prominent reveal per boundary

## Provisional

- formation threshold
- fracture threshold
- restoration threshold
- candidate preview
- procedural family count
- age milestones
- history storage shape
- exact reveal animation

---

# Phase 6 North Star

> **Turn long-lived knowledge into something worth keeping, and forgotten knowledge into something worth restoring.**
