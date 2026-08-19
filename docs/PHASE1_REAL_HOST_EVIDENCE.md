# Phase 1 Real-Host Evidence

Status: PARTIAL PASS — FINAL HOST GATES REMAIN
Date: 2026-08-19
Phase: 1 — Expedition

This file records only behavior actually exercised in desktop Anki during Phase 1 validation. It must not be used to infer untested gates.

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
- Dark-mode screenshots were manually reviewed against the Phase 1 design direction.

### Expedition progress / closure

- Real review progress advances in active Expeditions.
- Completion summary appeared correctly after the stale-DOM race fix.
- A completed Expedition remained complete while additional Anki reviews were still due outside the route.
- `Done` returned to normal Anki instead of automatically creating/reopening another Expedition, preserving a real stopping point.

### Pause / resume / restart

- A partially completed Expedition remained resumable with preserved progress/target.
- Closing and reopening Anki preserved the resumable Expedition.
- Resume continued normal review behavior.

### Undo reconciliation

- Review Undo reconciled Expedition progress downward correctly.
- Re-answering the undone card contributed once rather than double-counting.
- Real-host Undo correctness gate: PASS.

### Performance

Latest real-host snapshot:

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

## Still pending real-host confirmation

The following must remain PENDING until explicitly exercised or documented as an accepted limitation:

- pending-completion summary survives full Anki restart before `Done`, then stays dismissed after `Done` + restart,
- Focus Mode presentation in Today and reviewer,
- Reduced Motion setting / static meaning preservation,
- keyboard-only path and visible focus across core Today actions,
- narrow-window responsive layout beyond the already observed normal-width overflow fix,
- light appearance visual pass,
- intermediate checkpoint presentation when a route has a non-final checkpoint,
- queue exhaustion before fixed target when naturally reproducible,
- filtered deck / custom study smoke where practical.

Do not mark overall Phase 1 manual validation complete until the required remaining host gates are resolved in `docs/PHASE1_MANUAL_VALIDATION.md`.
