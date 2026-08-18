# Phase 1 Expedition Manual Validation

Status: PENDING REAL-HOST RUN
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
```

Recommended commit baseline: the latest `main` commit containing this file.

## A. Startup and Today

1. Pull latest `main` into the existing development checkout.
2. Start Anki with the linked Anki Alive development add-on.
3. Open the Deck Browser.
4. Confirm Anki starts without add-on traceback.
5. Confirm the Anki Alive Today surface appears above normal Anki deck content.
6. Confirm the displayed deck/context name and due count are believable for the selected deck.
7. Confirm normal Anki deck navigation remains usable.
8. Inspect both dark and light appearance.

PASS requires:

- low-chroma matte surfaces,
- readable typography,
- amber used as restrained Expedition signal rather than neon decoration,
- no dense RPG/dashboard treatment,
- no fake future-feature signals.

## B. Begin and review integrity

Use a deck with at least several due cards.

1. Select `Begin Expedition`.
2. Confirm Anki enters normal review.
3. Confirm the reviewer strip is small, quiet, and does not cover important card content.
4. Grade at least one card with each rating: Again, Hard, Good, Easy.
5. Confirm every accepted grade advances Expedition by exactly one.
6. Confirm no rating receives extra Expedition progress.

PASS requires normal Anki grading controls and scheduling to remain unchanged.

## C. Checkpoint

1. Continue until the first checkpoint.
2. Confirm the checkpoint appears once.
3. Confirm it is brief and non-blocking.
4. Confirm the next card remains answerable immediately.
5. If completion and final checkpoint occur on the same review, confirm only completion becomes prominent.

## D. Pause and resume

1. While a card is actively displayed, leave the reviewer normally.
2. Return to the Deck Browser.
3. Confirm Today shows the existing Expedition as resumable with unchanged target/progress.
4. Resume it.
5. Confirm review continues normally.

PASS requires no penalty or guilt language.

## E. Undo reconciliation

1. Accept a review during an active Expedition.
2. Use Anki Undo for that review.
3. Confirm Expedition progress reconciles downward exactly once.
4. Re-answer the card and confirm it contributes once with a fresh source review identity.
5. Confirm a non-review Undo does not create false Expedition reversal.

## F. Restart recovery

### Paused session

1. Pause with a partially completed Expedition.
2. Close Anki completely.
3. Restart Anki.
4. Confirm the same target, progress, and checkpoint plan remain resumable.

### Pending completion

1. Complete a short Expedition.
2. When the completion surface appears, do not press Done.
3. Close Anki.
4. Restart Anki.
5. Confirm the same completion summary is still pending.
6. Press `Done`.
7. Restart once more and confirm the dismissed summary does not return.

## G. Queue exhaustion before target

This validates a truthful fixed finish line.

1. Create/start an Expedition whose fixed target is larger than the eligible work that remains after review-state changes, filtered-deck behavior, or another legitimate Anki queue change.
2. Let Anki naturally reach no-next-card state before the Expedition target.
3. Confirm the Expedition closes cleanly instead of remaining stuck.
4. Confirm the summary states that available work ended.
5. Confirm the original planned target is still shown and was not silently rewritten.

If this scenario is difficult to produce naturally, record that limitation rather
than manufacturing collection state unsafely.

## H. Focus Mode

1. Toggle Focus Mode from Today.
2. Start/resume a short Expedition.
3. Confirm Memory Core ambient geometry is reduced/hidden.
4. Confirm the reviewer strip becomes quieter but numeric progress remains.
5. Confirm Expedition logic and grading behavior are unchanged.

## I. Reduced Motion

Validate with OS/browser reduced-motion preference or the available Anki Alive
setting path.

Confirm:

- no travel animation is required to understand progress,
- checkpoint state is legible statically,
- completion is understandable without motion,
- no looping ambient animation remains.

## J. Keyboard

Without relying on mouse clicks, validate visible focus and activation for:

- Begin Expedition,
- Resume Expedition,
- End Expedition,
- Done,
- Continue reviewing,
- Focus Mode toggle.

Normal Anki reviewer keyboard shortcuts must continue to work.

## K. Window/layout checks

1. Inspect normal desktop width.
2. Narrow the Anki window substantially.
3. Confirm Today collapses coherently without clipped core controls.
4. Test a card with unusually long content.
5. Confirm the fixed reviewer strip does not obscure the recall-critical region.

Capture screenshots if a visual issue needs follow-up.

## L. Normal review escape hatch

Confirm normal Anki review remains possible when:

- no Expedition is active,
- an Expedition has been ended,
- a completion summary was dismissed.

Anki Alive must never block the scheduler or require a new Expedition.

## M. Filtered deck / custom study smoke

Smoke-test the current implementation with:

- ordinary deck review,
- one filtered deck if available,
- custom study if practical.

Record unsupported behavior explicitly. Do not infer support from ordinary deck
review alone.

## N. Performance evidence

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

## O. Visual review against design contract

Use `docs/design/08_UI_REVIEW_CHECKLIST.md` and answer at minimum:

```text
Visual hierarchy PASS/FAIL:
Reviewer calmness PASS/FAIL:
Expedition cartographic identity PASS/FAIL:
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
