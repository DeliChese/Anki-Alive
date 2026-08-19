# Phase 1 Performance Evidence

Status: REVIEWER HOT PATH PASS; UNDO TIMING SAMPLE STILL OPTIONAL TO CAPTURE
Date: 2026-08-19
Phase: 1 — Expedition

## Real-host reviewer timing

Captured from `Tools > Anki Alive Performance Snapshot` during a real desktop Anki run after exercising Expedition review flow.

```text
reviewer_did_answer_card:
  samples: 20
  min: 0.398 ms
  median/P50: 0.902 ms
  P95: 1.357 ms
  max: 1.739 ms

state_did_undo:
  samples: 0
```

## Phase 0 comparison

Phase 0 real-host baseline:

```text
reviewer_did_answer_card:
  samples: 12
  min: 0.350 ms
  median/P50: 0.397 ms
  P95: approximately 0.604 ms
  max: 0.669 ms
```

Phase 1 therefore adds measurable synchronous work, as expected from durable Expedition progress and presentation orchestration, but the cumulative reviewer path remains well inside the established budget.

Phase 0 budget:

```text
Preferred < 5 ms
Typical < 10 ms
P95 < 20 ms
```

Phase 1 result:

- 20 accepted-review samples captured,
- P50 = 0.902 ms,
- P95 = 1.357 ms,
- max = 1.739 ms,
- no observed sample reaches 2 ms,
- reviewer hot-path performance gate: PASS.

The current snapshot contains no `state_did_undo` sample because no Undo occurred during the lifetime of that runtime instance. Undo correctness has separate real-host validation; a timing sample may be captured opportunistically before final handoff but absence of an Undo sample does not invalidate the accepted-review hot-path result.
