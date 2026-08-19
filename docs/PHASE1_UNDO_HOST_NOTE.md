# Phase 1 Undo Reconciliation Host Evidence

Status: REAL-HOST PASS
Date: 2026-08-19

A real desktop-Anki run validated Phase 1 review undo reconciliation on the current main line.

Observed host behavior:

- an accepted review advanced Expedition progress once,
- Anki Undo reconciled that review downward exactly once,
- re-answering the same card contributed exactly once again,
- progress did not double-count the original review identity,
- ordinary review flow remained usable after the undo/re-answer cycle.

This confirms the host `state_did_undo` integration is reconciling against durable review identity instead of blindly decrementing Expedition progress.

Automated coverage also validates the full observer chain:

- a non-review undo does not emit a false review reversal while the original revlog row still exists,
- a review undo emits a reversal only after the tracked revlog row disappears,
- re-answering with a fresh revlog identity produces a fresh accepted observation.

Automated evidence:

```text
GitHub Actions workflow: Anki Alive CI
Probe run: #136
Validated main snapshot: 8615f3f49f98e0f01e5e82201245cac148fa0d08
Python 3.9 core-tests: PASS
Python 3.13 core-tests: PASS
Probe merged: no
```

Result: Phase 1 Undo reconciliation gate PASS.
