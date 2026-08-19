# Phase 1 Performance Evidence

Status: PASS
Date: 2026-08-19
Phase: 1 — Expedition

## Real-host timing

Captured from `Tools > Anki Alive Performance Snapshot` during a real desktop Anki run after exercising Expedition review and Undo flows.

```text
reviewer_did_answer_card:
  samples: 23
  min: 0.398 ms
  median/P50: 0.977 ms
  P95: 1.357 ms
  max: 1.739 ms

state_did_undo:
  samples: 3
  min: 0.913 ms
  median/P50: 1.444 ms
  P95: 1.454 ms
  max: 1.454 ms
```

## Phase 0 comparison

Phase 0 real-host accepted-review baseline:

```text
reviewer_did_answer_card:
  samples: 12
  min: 0.350 ms
  median/P50: 0.397 ms
  P95: approximately 0.604 ms
  max: 0.669 ms
```

Phase 0 provisional synchronous budget:

```text
Preferred < 5 ms
Typical < 10 ms
P95 < 20 ms
```

Phase 1 adds measurable synchronous work, as expected from durable Expedition progress, reversal reconciliation, presentation orchestration, and sidecar persistence. The cumulative reviewer path nevertheless remains far inside the established budget.

## Result

Accepted review:

- samples: 23,
- P50: 0.977 ms,
- P95: 1.357 ms,
- max: 1.739 ms,
- no observed accepted-review sample reached 2 ms,
- reviewer hot-path performance gate: PASS.

Undo reconciliation:

- samples: 3,
- P50: 1.444 ms,
- P95: 1.454 ms,
- max: 1.454 ms,
- all observed Undo reconciliation samples remained below 2 ms,
- Undo hot-path timing gate: PASS.

Overall Phase 1 reviewer/Undo synchronous performance result: PASS.
