# Phase 1 Deck Browser Compatibility Finding

Status: HOST REINSTALL / STARTUP SMOKE PASS; FULL PHASE 1 HOST VALIDATION PENDING
Date: 2026-08-19

Real-host inspection with the Onigiri add-on exposed a structural compatibility problem: embedding the full Anki Alive Today surface directly into Anki's Deck Browser competes with appearance/dashboard add-ons that legitimately customize the same host DOM.

Phase 1 now follows a compatibility-first boundary:

- Anki Alive does not inject Today into Deck Browser content.
- The native Deck Browser remains owned by Anki and other installed add-ons.
- Native Decks / Add / Browse / Stats / Sync flows remain available without Anki Alive reimplementing them.
- Anki Alive Today opens in a dedicated modeless AnkiWebView window.
- Today is reachable from an `Alive` top-toolbar entry outside active review and from `Tools > Anki Alive Today` as a fallback.
- The reviewer progress strip remains a small reviewer-only augmentation.
- Expedition completion exits active recall and opens the dedicated Today window for closure.

This finding supersedes the earlier Phase 1 implementation note that described Deck Browser augmentation as the Today host surface.

## Real-host evidence after the compatibility change

On 2026-08-19, after pulling/reinstalling the compatibility build, the user reported that the add-on installed and started successfully on the real desktop host with the existing setup. This closes the immediate reinstall/startup blocker introduced by the host-surface refactor.

This evidence is intentionally narrow. It does not by itself mark the full Phase 1 host checklist PASS. The remaining run must still verify the dedicated Today window, native Deck Browser coexistence in use, review progress, checkpoint/completion, pause/resume, undo/restart, Focus Mode, reduced motion, keyboard/layout behavior, filtered/custom-study smoke behavior, and reviewer performance.

## Host-hardening after the smoke pass

The follow-up audit tightened two presentation boundaries before the longer manual run:

- the `Alive` top-toolbar link is suppressed while Anki is in active review, keeping recall chrome quiet;
- the dedicated Today window minimum size was lowered to 520×420 so the existing responsive 760px breakpoint can be exercised on the real host.

Regression coverage verifies that the toolbar entry is absent in review, present outside review, and that the Today window can reach the responsive layout breakpoint.

Automated verification:

```text
GitHub Actions workflow: Anki Alive CI
Probe run: #110
Python 3.9 core-tests: PASS
Python 3.13 core-tests: PASS
Probe PR: #5
Probe merged: no
```
