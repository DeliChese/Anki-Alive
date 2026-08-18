# PHASE_7_MEMORY_WORLD.md

# Anki Alive — Phase 7: Memory World

## 1. Phase Goal

Create a long-term visual world that represents the learner's evolving memory ecosystem.

Memory World should create the feeling:

> "This is the world my learning built."

The World must reflect real memory state, history, and progression.

It must not become a decorative virtual pet, idle game, or fake progression layer detached from learning.

---

# 2. Phase Status

```text
Status: SPECIFIED
Phase: 7
Name: Memory World
Depends on: Phase 6 — Relics
Next phase: Release Hardening / Cross-Phase Audit
```

---

# 3. Product Role

Memory World is the highest-level visualization layer in Anki Alive.

It brings together:

- Expedition history
- Oracle outcomes
- Rescue history
- Nemesis history
- Fragment milestones
- Relics
- memory-health projections
- deck/tag/topic grouping

Its job is to turn long-term learning history into a coherent visual landscape.

---

# 4. Core User Problem

Long-term Anki progress is difficult to perceive holistically.

Users may know:

- how many cards they reviewed,
- how many are due,
- how many days they studied,

but not:

> what their knowledge has become.

Memory World provides a visual answer.

---

# 5. Behavioral Goal

Memory World should create:

- ownership
- continuity
- legacy
- orientation
- curiosity about long-term knowledge structure
- pride grounded in actual learning

The emotional arc is:

```text
weeks/months of learning
    ↓
world slowly evolves
    ↓
history leaves landmarks
    ↓
stable regions emerge
    ↓
fragile regions shift
    ↓
learner sees accumulated knowledge
```

---

# 6. Critical Product Invariant

> **The World must be a projection of real data.**

It must not create fake buildings, levels, or progress unrelated to actual memory state.

If something grows, changes, fractures, stabilizes, or appears, there must be a meaningful data reason.

---

# 7. Memory World Is Not the Scheduler

World state does not determine:

- due dates
- FSRS behavior
- grading
- review order
- scheduling priorities

It visualizes.

It does not control learning.

---

# 8. In Scope

Phase 7 includes:

- World projection model
- region/grouping logic
- long-term growth
- memory-health visualization
- Relic landmarks
- Nemesis landmarks/history
- Rescue/fragility signals
- historical event integration
- region detail
- level-of-detail strategy
- large-collection performance
- accessibility mode
- simplified World view
- Focus Mode relationship
- deterministic layout
- caching
- migration if needed
- testing
- crash/failure degradation
- visual polish

---

# 9. Explicitly Out of Scope

Phase 7 does not implement:

- a game economy
- building placement by user for rewards
- farming mechanics
- virtual pets
- currency
- trading
- social worlds
- leaderboard
- real-time multiplayer
- world actions that affect scheduling
- mandatory World interaction before review

---

# 10. World Philosophy

The World should be:

- observational
- exploratory
- personal
- data-grounded
- evolving
- beautiful

It should not be:

- demanding
- noisy
- mechanically mandatory
- full of fake chores
- detached from study outcomes

---

# 11. Projection Architecture

Memory World should primarily be a projection layer.

Conceptually:

```text
Anki source data
+
Anki Alive durable history
+
Memory Engine summaries
    ↓
World Projection Service
    ↓
World Cache
    ↓
World UI
```

Do not duplicate all source card data into a second canonical world database.

---

# 12. World Projection Model

Conceptual model:

```text
MemoryWorldProjection
- generated_at
- projection_version
- profile_key

- regions[]
- landmarks[]
- global_health
- world_age?
- summary_metrics
```

This object is rebuildable.

It is not canonical history.

---

# 13. Region Model

A region represents an aggregate knowledge grouping.

Potential grouping sources:

- deck
- subdeck
- tag cluster
- topic cluster
- user-configured grouping

Recommended initial grouping:

> deck/subdeck hierarchy

Why:

- stable
- understandable
- already meaningful to users
- low inference risk

More advanced semantic grouping can be researched later.

---

# 14. Region Entity Projection

Conceptual:

```text
WorldRegion
- region_id
- source_group_type
- source_group_id

- title
- card_count
- mature_count
- fragile_count
- relic_count
- active_nemesis_count

- stability_summary?
- retrievability_summary?
- health_state

- visual_seed
- layout_position
- size_class
```

Most fields are projections.

---

# 15. Region Health

Region health may represent aggregate memory quality.

Potential inputs:

- retrievability distribution
- stability distribution
- fragile-memory share
- lapse trend
- mature-memory share

Exact formula is DEFERRED.

Locked:

- health is derived from real memory state,
- health is explainable,
- UI must avoid false scientific precision.

---

# 16. Region State Language

Possible states:

```text
STABLE
GROWING
FRAGILE
MIXED
RECOVERING
```

These are presentation categories.

They must map to explainable aggregate thresholds.

---

# 17. World Growth

The World may grow as:

- more memories become stable
- new long-term regions develop
- Relics accumulate
- difficult areas recover

Growth should not simply map:

```text
100 reviews = bigger city
```

unless review count is used only as secondary context.

---

# 18. Visual Scale

World size should reflect meaningful collection scale.

Possible drivers:

- stable memory count
- region diversity
- long-term history
- Relic count
- matured knowledge

Exact mapping is PROVISIONAL.

---

# 19. World Age

Potential concept:

```text
World age = age of meaningful learning history
```

This could reference:

- earliest observed review history
- earliest Anki Alive history

Status: PROVISIONAL.

Avoid fake precision if source history is incomplete.

---

# 20. Landmarks

Landmarks represent significant persistent history.

Potential landmark types:

```text
RELIC_CLUSTER
NEMESIS_VICTORY
RESTORED_RELIC
MAJOR_RECOVERY
ANCIENT_MEMORY
LONG_TERM_REGION
```

Landmarks should be relatively rare.

---

# 21. Relic Integration

Relics are natural World landmarks.

Possible representation:

- luminous monuments
- preserved mineral structures
- region anchors

A region with many Relics may look more established.

Do not render every Relic at full detail in overview.

Use aggregation or representative selection.

---

# 22. Nemesis Integration

Nemesis history may appear as:

- scar/fault landmark
- conquered marker
- active pressure zone

Avoid monster imagery.

A defeated Nemesis may leave a permanent subtle landmark.

---

# 23. Rescue Integration

Active fragile memories may influence:

- region pulse
- instability marker
- recovery glow

Do not create alarm-style flashing.

Rescue is current health.

World should show it quietly.

---

# 24. Fragment Integration

Fragments may reveal World-related historical content.

Examples:

- hidden landmark discovered
- region history surfaced
- old milestone revealed

Phase 7 should expose World projections without changing Fragment lifecycle.

---

# 25. Oracle Integration

Oracle history may contribute to analytics/history but should not dominate the World.

Potential:

- optional region prediction trend
- not a primary landmark by default

Oracle is a micro-loop.

World is long-term identity.

---

# 26. Expedition Integration

Completed Expeditions may contribute:

- historical activity timeline
- region exposure
- journey history

But World growth should not be based on raw Expedition count alone.

---

# 27. World Layout

Layout must be deterministic.

Reloading should not randomly move regions.

Possible inputs:

```text
region_id
visual_seed
hierarchy
region size
adjacency
```

---

# 28. Deterministic Layout Rule

For a stable set of regions:

> layout should remain visually stable across sessions.

Minor smooth adjustments may occur as region sizes change.

Avoid full reshuffling.

This preserves spatial memory.

---

# 29. Layout Strategies

Potential:

- constellation graph
- archipelago
- terrain map
- orbital region system
- clustered topography

Status: DESIGN RESEARCH.

Recommended initial direction:

> constellation / archipelago hybrid

Why:

- fits Arcane Memory Interface
- supports clustering
- scales gracefully
- avoids literal city-building implications

---

# 30. Art Direction

Memory World follows:

> **Arcane Memory Interface — Dark Arcane + Modern Minimal**

World-specific mood:

- atmospheric
- spatial
- quiet
- luminous
- ancient-modern
- contemplative

Avoid:

- fantasy kingdoms
- cartoon islands
- game-map quest markers everywhere
- noisy neon cyberpunk

---

# 31. World Visual Grammar

**Geometry:** constellation / terrain clusters / region networks  
**Material:** atmospheric slate / mineral topology / luminous markers  
**Motion:** slow drift / beacon pulse / subtle atmospheric response  
**Mood:** scope / continuity / legacy

---

# 32. World Overview

Potential structure:

```text
MEMORY WORLD

            [ region ]
       [ region ]   [ region ]

       [ landmark clusters ]

Global memory state
Mostly stable

12 regions
47 Relics
2 active Nemeses
```

This is conceptual.

---

# 33. Region Detail

Selecting a region may show:

- card count
- stable/fragile distribution
- Relics
- Nemesis history
- recovery history
- meaningful milestones
- current memory health

Avoid raw spreadsheet-style overload.

---

# 34. World Navigation

Required:

- mouse
- keyboard
- zoom if needed
- region selection
- back navigation
- simplified list alternative

Do not require precision dragging for essential access.

---

# 35. Simplified World View

Accessibility requires an alternative representation.

Possible:

```text
Region list

Japanese
Stable · 12 Relics · 1 Nemesis

Biology
Mixed · 7 fragile memories

History
Stable · 5 Relics
```

This is not a degraded mode.

It is an equivalent information path.

---

# 36. Focus Mode Relationship

Focus Mode primarily affects review.

World is an exploratory surface.

However:

- reduced ambient motion should respect global settings
- Focus Mode may default World to lower-motion presentation

World should never auto-open during review in Focus Mode.

---

# 37. Reduced Motion

Reduced-motion behavior:

- no drifting regions
- no continuous pulse
- static landmarks
- instant/short zoom transitions
- no parallax

---

# 38. Accessibility

Required:

- keyboard navigation
- visible focus
- simplified list view
- region state not color-only
- scalable text
- reduced motion
- contrast-safe labels
- no essential meaning encoded only spatially

---

# 39. World State and Color

Color may support:

- stable
- fragile
- recovering
- active

But state must also use:

- icon
- label
- texture/pattern
- shape
- marker style

---

# 40. Performance Philosophy

Memory World is visually ambitious.

Performance must be designed from the start.

The World should not block review.

If generation is slow:

- load cached projection
- render summary first
- refine progressively

---

# 41. Large Collection Strategy

Assume:

```text
100,000+ cards
many decks
multi-year history
many Relics
```

Do not map every card to a full visual object.

Use aggregation.

---

# 42. Level of Detail

Recommended:

### Level 0 — World

Regions only.

### Level 1 — Region

Subregions / landmark clusters.

### Level 2 — Detail

Relics, significant histories, selected memories.

Do not render card-level detail at World overview.

---

# 43. Projection Caching

Cache:

- region aggregates
- layout
- landmark selections
- summary metrics

Cache must be rebuildable.

Cache should include:

```text
projection_version
generated_at
source_version/signature
```

---

# 44. Cache Invalidation

Potential triggers:

- meaningful review batch
- collection structure change
- Relic transition
- Nemesis transition
- major Rescue state change
- phase migration

Do not rebuild World fully after every review.

---

# 45. Incremental Updates

Preferred:

- update affected region summary
- mark World projection dirty
- rebuild lazily/background

Exact strategy depends on performance profiling.

---

# 46. Persistence

World canonical state should be minimal.

Potential durable data:

```text
world_preferences
world_layout_seed?
manual region preferences?
```

Most World data should remain projection/cache.

Do not store a shadow copy of every memory.

---

# 47. Migration

Phase 7 may add little or no canonical schema.

If World preferences/layout seed require persistence:

- add explicit migration
- keep schema small

World cache format may version independently and be disposable.

---

# 48. World Projection Service

Responsibilities:

- aggregate memory data
- create regions
- create health summaries
- choose landmarks
- maintain deterministic layout inputs
- generate UI-ready projection

Not responsibilities:

- scheduling
- Relic lifecycle
- Nemesis lifecycle
- review integration logic

---

# 49. World Cache Service

Responsibilities:

- save projection cache
- validate version
- invalidate
- rebuild
- recover from corruption

Cache corruption must not affect review.

---

# 50. Region Grouping Service

Initial implementation should likely use deck hierarchy.

Future options:

- tag clusters
- manual groups
- semantic grouping

Do not implement semantic AI clustering in Phase 7 unless separately approved.

---

# 51. Privacy

World should not require sending card content externally.

Default:

- local computation
- IDs
- aggregate metrics
- live card content only when user opens detail

No remote AI dependency.

---

# 52. Generated Asset Role

Image generation may help create:

- World concept art
- landmark families
- terrain/mineral textures
- empty-state illustrations
- visual references

Production World should use reproducible local assets and procedural components.

Do not generate live World images remotely.

---

# 53. World Landmark Families

Potential visual families:

```text
RELIC_SPIRE
RESTORATION_RING
NEMESIS_SCAR
ANCIENT_BEACON
MEMORY_CLUSTER
REGION_CORE
```

Names are PROVISIONAL.

---

# 54. Memory Core Relationship

The Today-screen Memory Core may become a compact summary of World state.

Possible:

```text
Today Memory Core
    ↔
World global projection
```

Do not duplicate independent health calculations.

One projection service should support both.

---

# 55. History Integration

World may show a timeline of meaningful changes:

- region stabilized
- Relic formed
- Nemesis defeated
- major recovery
- region emerged

Avoid recording every small visual change as permanent history.

---

# 56. Region Emergence

A new region may appear when meaningful source grouping exists.

Do not create arbitrary unlock levels.

Example:

New deck with meaningful active cards → new region.

---

# 57. Region Dormancy

A region with no active/remaining cards may become dormant.

Potential states:

```text
ACTIVE
DORMANT
ARCHIVED
```

Status: PROVISIONAL.

Do not treat inactivity as punishment.

---

# 58. Deleted Decks / Structure Changes

Decks may be renamed, moved, deleted.

World should reconcile:

- stable region IDs where possible
- preserve meaningful landmarks/history
- avoid duplicating region on rename

Exact identity strategy must be implementation-tested.

---

# 59. Region Identity

Do not use display title alone.

Prefer stable source IDs where available.

If deck structure changes:

- update title
- preserve region history if source identity remains valid

---

# 60. World Failure Degradation

If World projection fails:

- Today remains usable
- review remains usable
- show simplified error/summary
- allow cache rebuild
- log diagnostics

World is never a critical review dependency.

---

# 61. Loading Strategy

Preferred:

1. load cached shell
2. show region overview
3. refine metrics
4. load landmark detail
5. render high-fidelity visuals

Avoid blank loading screens for long periods.

---

# 62. Performance Targets

Provisional:

### Cached World Open

```text
Interactive target: < 500 ms
```

### Projection Rebuild

No strict initial hard limit.

Target:

- background/lazy
- no reviewer blocking
- progressive update

### Region Detail

```text
Interactive target: < 300 ms from cached/indexed data
```

Measure on small, medium, and large profiles.

---

# 63. Rendering Budget

Prefer:

- bounded visible objects
- virtualized lists
- LOD
- efficient transforms
- optimized SVG/raster assets

Avoid:

- thousands of DOM nodes
- large blur layers
- constant particle systems
- full-world rerender on hover

---

# 64. Testing Requirements

## Projection

- stable input → stable projection
- deterministic region IDs
- deterministic layout
- correct aggregation
- empty profile behavior
- large profile behavior

## Health

- stable/fragile summaries correct
- explainability metadata matches inputs

## Landmarks

- Relic landmarks
- Nemesis landmarks
- restoration landmarks
- no duplicate landmark generation

## Cache

- load
- invalidate
- rebuild
- corrupt cache recovery
- version mismatch recovery

## Structure Changes

- deck rename
- deck move
- deck deletion
- card deletion
- profile switch

## Accessibility

- keyboard
- simplified view
- reduced motion
- non-color state

## Performance

- small profile
- medium profile
- large profile

---

# 65. Crash Recovery

### Case A

Projection rebuild interrupted.

Expected:

- previous valid cache remains usable or fallback summary appears.

### Case B

Cache corrupted.

Expected:

- rebuild safely.

### Case C

World UI crashes.

Expected:

- review unaffected.

---

# 66. Manual Host Test

Minimum:

```text
1. Open World with small collection.
2. Verify regions match deck structure.
3. Open region detail.
4. Verify Relic/Nemesis/Rescue history.
5. Navigate by keyboard.
6. Enable reduced motion.
7. Switch to simplified view.
8. Rename deck.
9. Confirm region identity/history remains sensible.
10. Delete test deck/card.
11. Confirm reconciliation.
12. Open large fixture/profile.
13. Measure cached open.
14. Trigger projection rebuild.
15. Begin review while World cache rebuild is pending.
16. Confirm review unaffected.
17. Corrupt/delete cache in test environment.
18. Confirm safe rebuild.
```

---

# 67. Success Metrics

Potential evaluation:

- World open frequency
- region detail exploration
- Relic landmark interaction
- simplified-view usage
- cached open time
- projection rebuild time
- large-profile rendering performance

Do not optimize World for time spent.

Exploration quality matters more than session duration.

---

# 68. Trust Risks

## Risk 1 — Fake Progress

Mitigation:

every visual state maps to real data.

## Risk 2 — False Precision

Mitigation:

use qualitative state where aggregate metrics are uncertain.

## Risk 3 — World Becomes a Game Separate From Anki

Mitigation:

no chores/economy/actions that affect review.

## Risk 4 — Performance Collapse

Mitigation:

aggregation, LOD, caching.

## Risk 5 — Visual Clutter

Mitigation:

calm art direction and hierarchical detail.

---

# 69. Anti-Patterns

Do not implement:

### City Building

```text
100 reviews = tower
```

unless clearly tied to real knowledge structure.

### Resource Collection

### Idle Production

### World Energy

### Daily World Chores

### Mandatory Region Unlock Grind

### Social Ranking

### Remote AI World Generation

### One Visual Object per Card at Full Detail

---

# 70. Copy Tone

Preferred:

```text
Memory World
Region stable.
Region recovering.
2 active Nemeses.
12 Relics.
A long-term memory cluster has formed.
```

Avoid:

```text
Kingdom level up!
Your city is dying!
Collect resources!
```

---

# 71. Open Questions

## Q7-01 — World Layout Style

Constellation, archipelago, orbital, or hybrid?

Status: DESIGN RESEARCH.

---

## Q7-02 — Region Health Formula

Status: DEFERRED.

---

## Q7-03 — Initial Grouping

Deck hierarchy only or deck + tags?

Status: PROVISIONAL.

Default: deck hierarchy.

---

## Q7-04 — Landmark Density

Status: UX/PERFORMANCE TEST.

---

## Q7-05 — Region Dormancy

Status: PROVISIONAL.

---

## Q7-06 — World Age

Is it useful or decorative?

Status: RESEARCH.

---

## Q7-07 — Manual Layout Customization

Should users rearrange regions?

Status: POST-V1 RESEARCH.

---

# 72. Definition of Done

Phase 7 is complete when:

- [ ] World projection service exists
- [ ] projection derives from real data
- [ ] region grouping works
- [ ] deterministic region identity exists
- [ ] deterministic layout exists
- [ ] health states are explainable
- [ ] Relic landmarks work
- [ ] Nemesis/history landmarks work
- [ ] Rescue/fragility signals work
- [ ] World overview exists
- [ ] region detail exists
- [ ] simplified accessibility view exists
- [ ] keyboard navigation works
- [ ] reduced motion works
- [ ] cache exists
- [ ] cache invalidation works
- [ ] cache corruption is recoverable
- [ ] large collections are tested
- [ ] review remains unaffected during World failure/rebuild
- [ ] generated visuals remain local/reproducible
- [ ] no fake game economy exists
- [ ] migration tested if required
- [ ] crash recovery tested
- [ ] performance measured
- [ ] manual host validation completed
- [ ] ADRs/backlog updated
- [ ] `PHASE_7_MEMORY_WORLD_HANDOFF.md` exists

---

# 73. Release Hardening Contract

After Phase 7, implementation should not immediately jump to more major mechanics.

The next stage is:

```text
CROSS-PHASE AUDIT
    ↓
RELEASE HARDENING
```

Audit should inspect:

- architectural drift
- duplicate state ownership
- event priority conflicts
- migration chain
- performance across all mechanics
- accessibility consistency
- visual consistency
- policy-version compatibility
- undo/reconciliation correctness
- data retention
- privacy
- documentation accuracy

---

# 74. Cross-Phase Data Audit

Verify:

- Expedition owns session state
- Oracle owns prediction commitments
- Rescue owns fragility/recovery lifecycle
- Nemesis owns persistent difficulty identity
- Fragment owns mystery lifecycle
- Relic owns long-term artifact history
- World owns projections only

No two systems should claim the same canonical state.

---

# 75. Cross-Phase Event Audit

Review all major event combinations.

Examples:

```text
Oracle + Rescue
Oracle + Nemesis
Rescue + Nemesis
Nemesis defeat + Relic formation
Fragment ready + Oracle reveal
Relic restoration + Expedition completion
```

Ensure EventOrchestrator provides coherent presentation.

---

# 76. Cross-Phase Performance Audit

Measure:

- reviewer P50/P95 overhead
- active feature lookup cost
- persistence write cost
- Today load
- Vault load
- World load
- large collection behavior

The sum matters more than each phase in isolation.

---

# 77. Cross-Phase Accessibility Audit

Verify:

- Focus Mode
- reduced motion
- keyboard path
- focus management
- non-color semantics
- sensory load
- simplified World view
- event dismissal consistency

---

# 78. Cross-Phase Visual Audit

Check that:

- Oracle
- Rescue
- Nemesis
- Fragments
- Relics
- World

still feel like one product.

Remove visual drift.

---

# 79. Cross-Phase Product Audit

Ask:

1. Does each mechanic still serve recall?
2. Are there any accidental grading incentives?
3. Are there any infinite loops?
4. Does each feature have real closure?
5. Is memory history still the primary reward?
6. Can users study normally without engaging the meta layer?

---

# 80. Locked vs Provisional Summary

## Locked

- World is a real-data projection
- no scheduler control
- no economy
- no mandatory interaction
- deterministic region/layout identity
- aggregation instead of full card rendering
- cache is rebuildable
- failure never blocks review
- accessibility alternative exists
- World remains local/reproducible
- Relics/Nemesis/Rescue/history integrate through projections

## Provisional

- exact layout style
- health formula
- region grouping beyond deck hierarchy
- landmark density
- World age
- dormancy
- manual layout customization
- exact visual effects

---

# Phase 7 North Star

> **Let the learner see the shape of what they have truly remembered.**
