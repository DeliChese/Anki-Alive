# Phase 2 — Oracle Entry Pack

Status: READY FOR SPEC / ARCHITECTURE
Date: 2026-08-19
Predecessor: Phase 1 — Expedition

## 1. Goal

Oracle creates trustworthy precommitted recall prediction around selected review cards without revealing answer information before recall, biasing grading, or rewarding dishonest self-grading.

The minimum vertical slice is:

```text
candidate context
→ deterministic selection
→ durable pre-answer commitment
→ normal Anki recall
→ accepted review observation
→ result resolution
→ post-answer presentation
→ Undo/reconciliation
```

## 2. Non-negotiable recall-integrity rules

1. A prediction must be committed before the review outcome is known.
2. No prediction content may reveal answer information before recall.
3. Oracle must not recommend or imply a grading button.
4. `Again` is never punished.
5. `Good`/`Easy` are never rewarded merely for being pressed.
6. Prediction success/failure is about forecast quality and memory state, not learner virtue.
7. Normal Anki review remains usable if Oracle fails or is disabled.
8. Focus Mode must be able to suppress or defer Oracle presentation without changing Oracle domain truth.

## 3. Phase 1 contracts Oracle may rely on

- Expedition is the durable session owner.
- Normalized review observations provide traceable accepted-review identity.
- Review reversal/reconciliation seams already exist.
- Sidecar SQLite is the durable feature store.
- `EventOrchestrator` owns presentation scheduling, not domain truth.
- Presentation prominence includes `AMBIENT`, `MINOR`, `MAJOR`, and `SESSION_CLOSURE`.
- Completion outranks competing major presentation at the same boundary.
- Focus Mode and Reduced Motion are first-class presentation policies.
- Reviewer hot-path performance is measured and must stay bounded.

## 4. Required Phase 2 architecture additions

### MemoryEngine

Formalize a feature-neutral interface that can provide an explainable `MemorySnapshot` for a card without embedding Oracle policy.

Conceptual output:

```text
MemorySnapshot
- card_id
- observed_at_utc
- stability?
- difficulty?
- retrievability?
- interval_days
- lapses
- review_count
- recent_outcomes
```

Oracle policy consumes these facts; MemoryEngine must not expose fields such as `oracle_candidate` or `will_fail`.

### ReviewContextService

Introduce one reviewer-time aggregation boundary so Oracle does not start a one-query-per-feature pattern.

Minimum Phase 2 context may include:

```text
ReviewFeatureContext
- expedition?
- memory_snapshot?
- oracle_prediction?
```

The service may use indexed reads and/or a small session cache. It must not become a second durable state owner.

### Oracle repository/service

Keep Oracle lifecycle isolated from Expedition internals.

Suggested modules:

```text
anki_alive/oracle/
├─ __init__.py
├─ model.py
├─ repository.py
├─ policy.py
├─ service.py
├─ events.py
└─ viewmodel.py
```

Integration code should depend on Oracle public service contracts, not repository internals.

## 5. Durable data contract

Phase 2 should add `oracle_predictions` in the next sidecar schema migration.

Canonical fields are already defined in `docs/04_DATA_MODEL.md`:

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

Additional implementation rules:

- `committed_at` must precede the accepted outcome used to resolve the prediction.
- historical interpretation must retain `policy_version`.
- prediction identity must be persisted or deterministically reproducible; reload must not reroll user-visible truth.
- deleting a source card invalidates unresolved predictions rather than preserving full card content.
- do not modify Anki collection schema.

## 6. Candidate and commitment policy

Phase 2 should begin with a deliberately narrow, testable policy rather than a large ML-like framework.

Recommended first policy shape:

- only consider cards with enough memory evidence to make a meaningful prediction,
- use MemorySnapshot/review-history-derived facts,
- cap Oracle frequency so it remains a sparse curiosity layer,
- persist the chosen card/prediction before answer exposure,
- record reason codes for diagnostics/tests if useful, but avoid fake scientific precision in UI.

If FSRS retrievability is available and validated through the MemoryEngine boundary, it may inform the policy. Oracle must still degrade safely when a metric is unavailable.

## 7. Resolution semantics

Oracle result should be derived from the accepted review observation after grading.

The domain must define one explicit mapping for `actual_recall_success` and test it. Do not silently equate "high rating" with moral success.

A conservative starting rule can distinguish recall outcome from grade strength, for example treating `Again` as failed recall and non-`Again` as recalled for Oracle's binary forecast, while retaining the raw `actual_rating` for explainability. Any richer mapping must be documented as a policy decision.

## 8. Undo / reconciliation contract

Every resolved Oracle prediction must reference the source review observation where possible.

On `ReviewReversed`:

- identify prediction(s) resolved by the reversed observation,
- remove or invalidate the resolved outcome,
- return the prediction to the correct committed/unresolved state when safe,
- invalidate any stale queued reveal tied to the reversed result,
- do not reroll the original prediction,
- allow the re-answer to resolve the same commitment from a fresh accepted observation when product policy permits.

Reconciliation should re-evaluate state rather than blindly decrement counters.

## 9. Presentation contract

Before answer:

- no answer-bearing text,
- no reveal of the prediction's selected outcome if that would bias recall,
- only a neutral indication that Oracle has committed a prediction, if product design explicitly wants such a cue.

After accepted answer:

- reveal may be `MINOR` or `MAJOR` depending on final design,
- Expedition `SESSION_CLOSURE` remains stronger than Oracle reveal,
- at most one major event surfaces at a review boundary,
- Focus Mode may suppress/defer nonessential reveal,
- Reduced Motion must preserve all semantic information statically.

If a reveal is deferred across boundaries or restart, durable presentation state must survive safely and deduplicate correctly.

## 10. Minimum test matrix

### Commitment integrity

- commitment exists before resolution,
- restart does not reroll commitment,
- duplicate candidate evaluation does not create duplicate commitments,
- disabled/Focus presentation does not mutate committed domain truth.

### Review integrity

- no pre-answer answer leakage,
- all Anki grading controls remain native/unchanged,
- Oracle adds no grade-dependent Expedition progress or reward.

### Resolution

- predicted fail + `Again`,
- predicted fail + recalled outcome,
- predicted recall + `Again`,
- predicted recall + recalled outcome,
- raw rating retained for explainability.

### Undo

- reveal resolved from review then Undo,
- queued reveal invalidated after Undo,
- re-answer resolves without duplicate history,
- non-review Undo leaves Oracle untouched.

### Persistence

- committed unresolved prediction survives restart,
- resolved prediction survives restart,
- deferred presentation does not duplicate after restart.

### Orchestration

- Oracle major + Expedition completion → completion wins,
- Oracle reveal + minor Expedition/checkpoint signal → boundary remains coherent,
- Focus Mode suppression/defer behavior,
- Reduced Motion semantics.

### Performance

- no collection-wide scan on each reviewed card,
- MemoryEngine/ReviewContextService reviewer-time reads are measured,
- integrated reviewer P50/P95 remains inside the cumulative budget.

## 11. Decisions to record during Phase 2

Before implementation stabilizes, add accepted decisions for:

- Oracle recall-success mapping,
- initial candidate/selection policy and frequency cap,
- whether pre-answer neutral "commitment exists" presentation is shown at all,
- reveal prominence and deferral rules,
- MemoryEngine host data sources/fallbacks,
- ReviewContextService cache/read strategy,
- exact Undo state transition for a committed prediction whose resolution is reversed.

## 12. Definition of done for Phase 2

Phase 2 is complete only when:

- commitment-before-outcome is mechanically proven,
- reload cannot reroll a visible commitment,
- reveal occurs only after accepted answer,
- Undo/re-answer behavior is correct,
- Oracle integrates with Expedition/EventOrchestrator,
- Focus Mode and Reduced Motion paths work,
- tests cover commitment, persistence, reconciliation, and orchestration,
- reviewer performance remains acceptable,
- architecture/data/decisions/backlog are updated,
- real-host validation is recorded,
- `handoffs/PHASE_2_ORACLE_HANDOFF.md` exists.

## 13. Immediate first slice

Implement the smallest end-to-end proof in this order:

1. formalize `MemoryEngine` interface with a test fake,
2. add schema migration for `oracle_predictions`,
3. implement Oracle model/repository with persisted commitment identity,
4. implement a simple deterministic policy,
5. commit one prediction before outcome,
6. resolve it from normalized accepted review observation,
7. reconcile it on Undo,
8. surface a post-answer reveal through `EventOrchestrator`,
9. add persistence/restart/orchestration tests,
10. only then polish candidate policy and UI.

Do not build Rescue/Nemesis/Fragments infrastructure during this phase.
