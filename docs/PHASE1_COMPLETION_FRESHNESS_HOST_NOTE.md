# Phase 1 Completion Freshness Host Finding

Status: REAL-HOST PASS
Date: 2026-08-19

A real desktop run exposed a presentation race at Expedition completion.

Observed behavior before the fix:

- the learner finished the real Anki reviews before the Today surface visibly caught up,
- the first automatically opened Today view could still show stale pre-completion markup,
- closing/reopening Today later revealed the durable `Done` completion state,
- pressing `Done` then immediately refreshed Today into a new route proposal when reviewable work remained.

The durable Expedition and presentation records were already correct. The stale experience came from the reusable Today WebView being revealed immediately after queuing an asynchronous `eval()` that replaced its inner markup. The old DOM could therefore become visible before the fresh completion markup reached Chromium.

Phase 1 now enforces a fresh-DOM reveal boundary:

- Today updates inner markup with `evalWithCallback()`,
- a hidden Today window is revealed only after that callback returns,
- show generations invalidate late callbacks after the user closes or supersedes an opening request,
- title-bar close / Escape use the same retained-window close path,
- `Done` dismisses the durable completion presentation and closes Today instead of refreshing directly into another proposed Expedition,
- `Continue reviewing` remains the explicit path for choosing more review work.

This aligns completion with the Phase 1 clean-closure contract: finishing an Expedition must create a real stopping point and must not immediately manufacture fresh tension.

Automated evidence:

```text
GitHub Actions workflow: Anki Alive CI
Probe run: #129
Validated main snapshot: d2fee41a6799d4ec4d70ecc191c8ce372318c2f8
Python 3.9 core-tests: PASS
Python 3.13 core-tests: PASS
Probe merged: no
```

Real-host re-validation evidence:

```text
Date: 2026-08-19
Completion first reveal: PASS
Observed completion: 9 / 9, 1 checkpoint
Remaining native Anki queue shown separately: 3 reviews due
Done closure: PASS
Done returned to normal Anki: PASS
Done did not immediately manufacture a new Expedition: PASS
Manual screenshot reviewed: yes
```

Result: PASS. Completion freshness and clean closure are no longer Phase 1 blockers.
