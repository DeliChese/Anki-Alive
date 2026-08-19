# Phase 1 Expedition Manual Validation

Status: PENDING REAL-HOST RE-RUN
Phase: 1
Feature: Expedition

This is the minimum desktop-Anki validation required before Phase 1 can be
marked complete. Record actual host facts and failures here. Do not infer PASS
from automated tests.

## Test host

Fill in:

```text
Date:
OS:
Anki version:
Python:
Qt:
PyQt:
Commit:
Theme: dark / light
Other appearance/dashboard add-ons:
```

Recommended commit baseline: latest `main`.

## A. Startup and host coexistence

1. Pull latest `main` into the development checkout.
2. Start Anki with Anki Alive and the existing appearance/dashboard add-ons enabled.
3. Open the normal Deck Browser.
4. Confirm Anki starts without add-on traceback.
5. Confirm Anki Alive does NOT insert its full Today panel into Deck Browser content.
6. Confirm the existing Deck Browser theme/background/add-on UI remains intact.
7. Confirm native Decks / Add / Browse / Stats / Sync flows remain reachable and usable.
8. Confirm an `Alive` entry is available in the top toolbar outside active review, or use `Tools > Anki Alive Today` as the fallback path.

PASS requires Anki Alive to coexist rather than replace or restyle the Deck Browser.

## B. Dedicated Today window

1. Open `Alive` or `Tools > Anki Alive Today`.
2. Confirm a separate `Anki Alive · Today` window opens.
3. Confirm the displayed deck/context name and due count are believable.
4. Confirm the Today visual canvas is self-contained and does not inherit the Deck Browser skin/background.
5. Confirm no horizontal scrollbar appears at normal desktop width.
6. Close/hide Today, then reopen it and confirm it appears without the previous multi-second wait.
7. Repeat open/close/reopen at least twice to exercise the retained WebView path.
8. Narrow the window substantially and confirm no horizontal overflow appears.
9. Inspect both dark and light appearance.
10. Press Escape and confirm the Today window hides without affecting Anki, then reopen it successfully.

PASS requires:

- low-chroma matte surfaces,
- readable typography,
- restrained amber Expedition signal,
- no dense RPG/dashboard treatment,
- no fake future-feature signals,
- no persistent horizontal overflow,
- no repeated multi-second WebEngine recreation on ordinary reopen.

## C. Begin and review integrity

Use a deck with at least several due cards.

1. Open Today and select `Begin Expedition`.
2. Confirm the Today window hides and Anki enters normal review.
3. Confirm the reviewer strip is small, quiet, and does not cover important card content.
4. Grade at least one card with each rating: Again, Hard, Good, Easy.
5. Confirm every accepted grade advances Expedition by exactly one.
6. Confirm no rating receives extra Expedition progress.

PASS requires normal Anki grading controls and scheduling to remain unchanged.

## D. Checkpoint

1. Continue until the first checkpoint.
2. Confirm the checkpoint appears once.
3. Confirm it is brief and non-blocking.
4. Confirm the next card remains answerable immediately.
5. If completion and final checkpoint occur on the same review, confirm only completion becomes prominent.

## E. Pause and resume

1. While a card is actively displayed, leave the reviewer normally.
2. Confirm the normal Deck Browser returns unchanged.
3. Open Anki Alive Today.
4. Confirm the existing Expedition is resumable with unchanged target/progress.
5. Resume it and confirm normal review continues.

PASS requires no penalty or guilt language.

## F. Undo reconciliation

1. Accept a review during an active Expedition.
2. Use Anki Undo for that review.
3. Confirm Expedition progress reconciles downward exactly once.
4. Re-answer the card and confirm it contributes once with a fresh source review identity.
5. Confirm a non-review Undo does not create false Expedition reversal.

## G. Restart recovery

### Paused session

1. Pause with a partially completed Expedition.
2. Close Anki completely.
3. Restart Anki.
4. Open Today and confirm the same target, progress, and checkpoint plan remain resumable.

### Pending completion

1. Complete a short Expedition.
2. Confirm Anki leaves active recall and opens the dedicated Today completion summary.
3. Do not press Done; close Anki.
4. Restart Anki and open Today.
5. Confirm the same completion summary is still pending.
6. Press `Done`.
7. Restart once more and confirm the dismissed summary does not return.

## H. Queue exhaustion before target

1. Create/start an Expedition whose fixed target is larger than the eligible work that remains after a legitimate queue change.
2. Let Anki naturally reach no-next-card state before the target.
3. Confirm the Expedition closes cleanly.
4. Confirm the dedicated Today summary states that available work ended.
5. Confirm the original planned target is still shown and was not silently rewritten.

If this is difficult to produce naturally, record the limitation rather than manufacturing collection state unsafely.

## I. Focus Mode

1. Open Today and toggle Focus Mode.
2. Start/resume a short Expedition.
3. Confirm Memory Core ambient geometry is reduced/hidden.
4. Confirm the reviewer strip becomes quieter but numeric progress remains.
5. Confirm Expedition logic and grading behavior are unchanged.

## J. Reduced Motion

Validate with the OS/browser reduced-motion preference or the available Anki Alive setting path.

Confirm:

- no travel animation is required to understand progress,
- checkpoint state is legible statically,
- completion is understandable without motion,
- no looping ambient animation remains.

## K. Keyboard

Without relying on mouse clicks, validate visible focus and activation for:

- Alive/Tools entry,
- Begin Expedition,
- Resume Expedition,
- End Expedition,
- Done,
- Continue reviewing,
- Focus Mode toggle,
- Escape to hide Today and reopen it afterward.

Normal Anki reviewer keyboard shortcuts must continue to work.

## L. Window/layout checks

1. Inspect Today at normal desktop size.
2. Narrow the Today window substantially.
3. Confirm it collapses coherently without clipped core controls or horizontal overflow.
4. Test a card with unusually long content.
5. Confirm the reviewer strip does not obscure the recall-critical region.

Capture screenshots if a visual issue needs follow-up.

## M. Normal review escape hatch

Confirm normal Anki review remains possible when:

- Today is closed/hidden,
- no Expedition is active,
- an Expedition has been ended,
- a completion summary was dismissed.

Anki Alive must never block the scheduler or require a new Expedition.

## N. Filtered deck / custom study smoke

Smoke-test:

- ordinary deck review,
- one filtered deck if available,
- custom study if practical.

Record unsupported behavior explicitly. Do not infer support from ordinary deck review alone.

## O. Performance evidence

Enable diagnostics if needed and record real samples for the reviewer path.
Compare against the Phase 0 baseline.

Required report:

```text
reviewer_did_answer_card samples:
min:
median/P50:
P95:
max:

state_did_undo samples:
min:
median/P50:
max:
```

Phase 1 must remain within the existing cumulative reviewer hot-path budget.

## P. Visual review against design contract

Use `docs/design/08_UI_REVIEW_CHECKLIST.md` and answer at minimum:

```text
Visual hierarchy PASS/FAIL:
Reviewer calmness PASS/FAIL:
Expedition cartographic identity PASS/FAIL:
Dedicated Today isolation PASS/FAIL:
Deck Browser coexistence PASS/FAIL:
Dark mode PASS/FAIL:
Light mode PASS/FAIL:
Focus Mode PASS/FAIL:
Reduced Motion PASS/FAIL:
Keyboard focus PASS/FAIL:
No fake signal content PASS/FAIL:
No excessive effects PASS/FAIL:
```

## Result

Do not change this status until the real host run is complete.

```text
Overall: PENDING
Blocking defects:
Non-blocking observations:
Performance result:
Manual screenshots reviewed:
```

After PASS, update roadmap/decisions/backlog as needed and create
`handoffs/PHASE_1_EXPEDITION_HANDOFF.md` before starting Phase 2.
