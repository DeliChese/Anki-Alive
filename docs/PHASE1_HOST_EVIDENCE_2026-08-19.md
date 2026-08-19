# Phase 1 Real-Host Evidence — 2026-08-19

Status: IN PROGRESS
Phase: 1 — Expedition

This file records real desktop-Anki evidence gathered during the Phase 1 host run. It is intentionally incremental and does not replace `docs/PHASE1_MANUAL_VALIDATION.md`.

## Environment context

- Real desktop Anki host on Windows.
- Existing Onigiri appearance/dashboard add-on enabled.
- Anki Alive Today uses a dedicated modeless AnkiWebView instead of Deck Browser injection.

## Confirmed evidence

### Host coexistence

- Reinstall/startup after the dedicated-Today refactor succeeded.
- The earlier Deck Browser takeover conflict with Onigiri is no longer the active presentation model.

### Dedicated Today surface

Real-host screenshots were reviewed with an active Expedition at `2 / 11`.

Observed PASS at normal desktop width:

- dedicated `Anki Alive · Today` window opens successfully,
- dark presentation is visually coherent and isolated from the Onigiri Deck Browser skin,
- no horizontal scrollbar is visible after the overflow fix,
- visual hierarchy remains restrained and consistent with the Arcane Memory Interface design contract,
- Memory Core remains quiet,
- Expedition route/progress is readable,
- no fake Oracle/Rescue/Nemesis/Fragment/Relic/World signal content is shown.

### Today opening latency

Before the reuse/prewarm patch, opening Today took multiple seconds on the real host.

After the patch, the user explicitly reported that Today opens noticeably faster. This is real-host evidence that the retained/prewarmed AnkiWebView strategy improved perceived opening latency.

Automated regression for this patch was separately verified by GitHub Actions probe run #118 on Python 3.9 and 3.13.

## Still pending

- narrow-window overflow confirmation,
- light mode visual check,
- reviewer progress integrity across all four grades,
- intermediate checkpoint presentation on an Expedition with a target large enough to contain a non-final checkpoint,
- final-checkpoint/completion precedence,
- pause/resume,
- undo reconciliation,
- restart recovery,
- Focus Mode,
- reduced motion,
- keyboard path,
- queue exhaustion,
- filtered deck/custom study smoke,
- reviewer hot-path performance evidence.

## Current Expedition note

The active real-host Expedition shown in the latest screenshot is `2 / 11`. Under the current deterministic checkpoint planner, an 11-review route has only the final checkpoint at 11. Therefore this session is suitable for validating completion and final-checkpoint suppression, but not a standalone intermediate checkpoint reveal.
