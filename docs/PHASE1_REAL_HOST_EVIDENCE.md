# Phase 1 Real-Host Evidence

Status: PASS — PHASE 1 HOST VALIDATION COMPLETE
Date: 2026-08-19
Phase: 1 — Expedition

This file records behavior actually exercised in desktop Anki during Phase 1 validation. It does not infer support for untested host contexts.

## Confirmed real-host PASS

### Startup / coexistence

- Anki Alive reinstall/startup succeeded on the real desktop host.
- Existing Onigiri appearance/dashboard customization remains active after Anki Alive stopped owning/replacing Deck Browser content.
- Native Anki main-screen functionality remains available through the normal host UI.
- Anki Alive Today is isolated in its own window instead of replacing Deck Browser.

### Today window / layout / responsiveness

- Dedicated `Anki Alive · Today` window opens successfully.
- Ordinary reopen latency improved materially after retained/prewarmed WebView changes.
- Horizontal overflow visible in an earlier build was removed at normal desktop width.
- Dark appearance was manually reviewed against the Phase 1 design direction.
- Light appearance was directly exercised and remained readable/coherent.
- A substantially narrowed Today window was directly exercised without persistent horizontal overflow or clipped core controls.

### Expedition progress / closure

- Real review progress advances in active Expeditions.
- Completion summary appeared correctly after the stale-DOM race fix.
- A completed Expedition remained complete while additional Anki reviews were still due outside the route.
- `Done` returned to normal Anki instead of automatically creating/reopening another Expedition, preserving a real stopping point.

### Pause / resume / restart

- A partially completed Expedition remained resumable with preserved progress/target.
- Closing and reopening Anki preserved the resumable Expedition.
- Resume continued normal review behavior.
- A pending completion summary survived a full Anki restart before `Done`.
- After `Done`, a later restart did not resurrect the dismissed completion summary.

### Undo reconciliation

- Review Undo reconciled Expedition progress downward correctly.
- Re-answering the undone card contributed once rather than double-counting.
- Real-host Undo correctness gate: PASS.

### Focus Mode / Reduced Motion / keyboard

- Focus Mode presentation was exercised successfully in Today and review.
- Numeric Expedition progress remained available while presentation intensity was reduced.
- Reduced Motion was exercised successfully through the Anki Alive setting path; state remained understandable without relying on travel animation.
- Keyboard navigation/activation for the tested Today flow worked, including visible focus and Escape-to-hide behavior.

### Performance

Latest recorded real-host snapshot:

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

Both accepted-review and Undo timing remain well inside the Phase 0 cumulative synchronous budget. See `docs/PHASE1_PERFORMANCE_EVIDENCE.md` for the detailed comparison.

## Automated evidence covering edge behavior

- Intermediate checkpoint logic is covered with a target-16 Expedition where checkpoint 8 emits exactly once.
- Queue exhaustion before target is covered by domain/service tests and preserves the original fixed target.
- Duplicate review delivery is covered and does not double-count progress.
- Paused and pending-completion states are covered across sidecar database reopen.
- Focus Mode, Reduced Motion, and native button keyboard semantics have regression coverage.

## Explicitly unclaimed host contexts

The following are not inferred from ordinary deck testing:

- filtered-deck behavior has not been separately claimed from this host run,
- custom-study behavior has not been separately claimed from this host run,
- naturally occurring queue exhaustion before target was not manufactured in the user's collection,
- intermediate checkpoint presentation was not forced on the real collection solely for validation.

These are documented limitations rather than Phase 1 blockers. Ordinary deck review is the validated Phase 1 host path.

## Phase 1 host gate result

The final visual gates — light appearance and substantially narrowed Today layout — were directly exercised by the project owner and reported working on 2026-08-19.

Phase 1 host validation is therefore complete.
