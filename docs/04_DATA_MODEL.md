# 04_DATA_MODEL.md

# Anki Alive — Data Model

## 1. Data North Star

> **Store durable meaning, reference Anki truth, and recompute everything else.**

---

## 2. Data Classes

Anki Alive data falls into three classes.

### Source Truth

Owned by Anki:

- card/note/deck identity,
- review history,
- scheduler state,
- scheduler-exposed FSRS values.

### Durable Meaning

Owned by Anki Alive:

- feature lifecycle,
- commitments,
- milestones,
- significant history,
- deterministic visual identity.

### Rebuildable Projection

Derived:

- candidate scores,
- Memory World,
- health summaries,
- presentation models,
- caches.

---

## 3. Core Reference Types

### CardReference

```text
card_id
note_id?
deck_id?
profile_key
```

Full card content is not stored by default.

---

## 4. ReviewObservation

Normalized accepted review event.

```text
observation_id
card_id
source_review_id?
rating
reviewed_at_utc
response_time_ms?
sequence?
```

Purpose:

- deduplication,
- transition causality,
- undo reconciliation,
- crash recovery.

---

## 5. ReviewReversal

```text
observation_id?
source_review_id?
card_id
reversed_at_utc
```

Exact host mapping is implementation-dependent.

---

## 6. MemorySnapshot

Feature-neutral normalized memory state.

```text
card_id
observed_at_utc
stability?
difficulty?
retrievability?
interval_days
lapses
review_count
recent_outcomes
```

This is usually runtime/rebuildable.

Persist only when a feature needs a historical snapshot for explainability or policy evidence.

---

## 7. Expedition

```text
expedition_id
profile_key
local_study_date
status
created_at
started_at?
paused_at?
completed_at?
ended_at?
target_reviews
completed_reviews
checkpoint_plan_version
seed?
schema_version
```

Expedition is canonical durable session state.

---

## 8. ExpeditionCheckpoint

```text
checkpoint_id
expedition_id
ordinal
target_progress
reached_at?
status
```

---

## 9. OraclePrediction

```text
oracle_prediction_id
expedition_id
card_id
committed_at
policy_version
predicted_recall_probability?
predicted_outcome
resolved_at?
actual_rating?
actual_recall_success?
result?
source_observation_id?
reconciliation_state?
```

Commitment must exist before outcome.

---

## 10. Rescue

```text
rescue_id
card_id
expedition_id?
created_at
policy_version
state
creation_metrics?
last_attempt_at?
resolved_at?
source_observation_id?
reconciliation_state?
```

Rescue primarily belongs to the memory, not the session.

---

## 11. Nemesis

Recommended state:

```text
CANDIDATE
ACTIVE
WEAKENING
DEFEATED
ORPHANED
ARCHIVED
```

A returned Nemesis transitions:

```text
DEFEATED → ACTIVE
```

and records `NemesisReturned` as history.

Conceptual fields:

```text
nemesis_id
card_id
promoted_at
promotion_policy_version
state
encounter_count
successful_encounters
failed_encounters
current_strength_score?
weakened_at?
defeated_at?
last_source_observation_id?
reconciliation_state?
```

Do not store redundant review history without feature-specific value.

---

## 12. Fragment

```text
fragment_id
expedition_id?
local_study_date?
created_at
state
reveal_type
progress_current
progress_target
seed
policy_version
payload_ref?
revealed_at?
reconciliation_state?
```

Identity and reveal must not reroll.

---

## 13. Relic

Recommended state:

```text
CANDIDATE
ACTIVE
FRACTURED
RESTORING
ORPHANED
ARCHIVED
```

Restoration transitions:

```text
RESTORING → ACTIVE
```

and records `RelicRestored` as history.

Conceptual fields:

```text
relic_id
card_id
formed_at
formation_policy_version
state
formation_stability?
formation_interval_days?
formation_difficulty?
formation_lapse_count?
visual_seed
visual_family?
visual_version
fractured_at?
last_source_observation_id?
reconciliation_state?
```

Formation metadata is historical and must not be overwritten by current state.

---

## 14. MemoryMilestone

Shared significant history.

```text
milestone_id
type
occurred_at_utc
card_id?
entity_id?
source_domain_event_id?
source_observation_id?
metadata
policy_version?
```

Possible types:

```text
RESCUE_COMPLETED
NEMESIS_PROMOTED
NEMESIS_DEFEATED
NEMESIS_RETURNED
FRAGMENT_REVEALED
RELIC_FORMED
RELIC_FRACTURED
RELIC_RESTORED
```

Not every review becomes a milestone.

---

## 15. PresentationEvent

Presentation queue entry.

```text
presentation_event_id
source_domain_event_id
kind
prominence
priority
created_at
status
dedupe_key?
payload_ref?
```

Possible status:

```text
PENDING
SHOWN
DISMISSED
DEFERRED
SUPPRESSED
INVALIDATED
```

Presentation state is not domain state.

---

## 16. FocusModeSettings

```text
enabled
allow_major_reveal?
allow_minor_reveal?
allow_ambient_motion?
show_compact_progress?
defer_nonessential_events?
```

Exact public settings can remain simpler than internal policy.

---

## 17. AnkiAliveSettings

Categories:

```text
appearance
motion
focus_mode
diagnostics
feature_flags
```

Feature code should not read raw config dictionaries directly.

---

## 18. CandidateScore

Rebuildable.

```text
card_id
feature
score
reason_codes
computed_at
policy_version
```

Do not treat as canonical history.

---

## 19. MemoryHealthProjection

Rebuildable aggregate.

Possible:

```text
scope_id
scope_type
computed_at
stable_count
fragile_count
recovering_count
relic_count
nemesis_count
health_state
```

Used by Today and Memory World.

---

## 20. HistoryEntry

UI-facing projection of milestones/history.

This may combine:

- milestone,
- live card metadata,
- feature state.

Do not duplicate canonical history unnecessarily.

---

## 21. SchemaMeta

```text
schema_version
created_at
updated_at
```

---

## 22. Policy Versions

Persist policy version when historical interpretation depends on rules.

Required or strongly recommended for:

- Oracle
- Rescue
- Nemesis
- Fragment
- Relic
- persisted/cached World projection versions.

Do not silently reinterpret old historical entities under new rules.

---

## 23. Time Model

Durable timestamps:

```text
UTC
```

Day-based session behavior:

```text
local_study_date
```

No destructive midnight reset.

---

## 24. Stable Identity

Use Anki IDs for source references.

Use Anki Alive IDs for durable entities.

Examples:

```text
card_id
expedition_id
oracle_prediction_id
rescue_id
nemesis_id
fragment_id
relic_id
milestone_id
presentation_event_id
```

---

## 25. Deletion Model

If a source card disappears:

- unresolved Oracle prediction → invalidate,
- Rescue → orphan/archive,
- Nemesis → orphan,
- Relic → orphan while preserving history,
- World → remove from live projection,
- milestones → retain minimal safe history.

Do not retain full deleted card content by default.

---

## 26. Cache Model

World and large projections may use disposable cache.

Cache must be:

- versioned,
- rebuildable,
- safe to delete,
- scoped by profile,
- never canonical history.

---

## 27. Schema Evolution by Phase

```text
Phase 0
schema_meta
migration_history

Phase 1
expeditions
expedition_checkpoints
expedition_review_observations
presentation_events

Phase 2
oracle_predictions

Phase 3
rescues

Phase 4
nemeses
shared milestones when needed

Phase 5
fragments

Phase 6
relics
additional milestone/history support if justified

Phase 7
minimal preferences/layout seed/cache metadata if required
```

`expedition_review_observations` is a compact traceability table that maps accepted source review identities to the Expedition that consumed them. It exists to guarantee deduplication and correct reversal reconciliation; it is not a second copy of Anki review history.

`presentation_events` stores durable presentation lifecycle independently from Expedition domain truth. Phase 1 uses it so a completion summary can survive restart until explicitly dismissed.

Do not pre-create every future table in Phase 0.

---

## 28. Full Migration Test

Before release hardening, test:

```text
Phase 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7
```

with representative historical data.

---

## 29. Phase 1 Implemented Schema Note

Phase 1 closes on sidecar schema version `3`.

The schema contains:

```text
schema_meta
migration_history
expeditions
expedition_checkpoints
expedition_review_observations
presentation_events
```

Phase 1 does not modify Anki collection tables and does not persist card fronts/backs.

---

# Data North Star

> **Store durable meaning, reference Anki truth, and make every review-derived transition traceable enough to reconcile.**
