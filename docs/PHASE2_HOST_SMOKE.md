# Phase 2 Oracle — Real-Host Smoke Checklist

Status: PENDING
Date: 2026-08-19

Use this after syncing the latest `main` into the desktop Anki add-on checkout and fully restarting Anki so Python, JS, and CSS reload.

## Preconditions

- Use an ordinary deck with cards that have at least 3 prior reviews.
- FSRS is preferred but no longer required: policy v2 can fall back to bounded recent review history without inventing a probability.
- Start a normal Anki Alive Expedition.
- Do not alter collection state just to force a particular Oracle prediction.

## Expected cadence

Oracle allows at most one new commitment per five accepted-review Expedition progress units.

The first eligible card in each window may receive Oracle. If an earlier card in that window lacks enough memory evidence, the window stays available for a later eligible card instead of being silently wasted.

## A. Neutral pre-answer commitment cue

1. Start an Expedition and reach an Oracle-eligible reviewed card.
2. On the question side, look for the small cyan-accent status surface:

```text
ORACLE
Prediction sealed. Reveal after your answer.
```

3. Confirm the cue contains no predicted outcome, probability, confidence, grading recommendation, or answer-bearing content.
4. Confirm normal Anki answer controls and keyboard shortcuts behave unchanged.

PASS requires Oracle to be visibly present without leaking the private prediction.

## B. Post-answer reveal

1. Answer the committed card normally.
2. Grade with the rating that honestly matches recall.
3. Confirm the Oracle surface changes to a result only after the accepted grade.
4. Confirm the result is small, non-interactive, and disappears without blocking the next card.
5. Confirm it does not award points, currency, bonus Expedition progress, or praise a higher grading button.

## C. Non-FSRS fallback

If practical, use a reviewed card/deck without usable FSRS memory state.

1. Confirm a card with at least 3 reviews and usable recent revlog history can still receive the neutral Oracle cue.
2. Confirm no probability is shown before or after answer merely because the fallback was used.
3. Confirm cards without sufficient history are simply skipped.

## D. Rating semantics

Exercise honest examples where practical:

- `Again` is interpreted as failed recall.
- `Hard`, `Good`, and `Easy` are interpreted as recalled for Oracle's binary outcome.
- Expedition progress still advances exactly once for every accepted review regardless of rating.

Do not intentionally misgrade cards to make Oracle look correct.

## E. Focus Mode

1. Enable Focus Mode.
2. Reach another Oracle-eligible card.
3. Confirm normal review and Expedition progress continue.
4. Confirm both the neutral commitment cue and result reveal are suppressed.
5. Disable Focus Mode and continue reviewing normally.

PASS requires Focus Mode to change presentation only, not review or Oracle domain history.

## F. Reduced Motion

1. Enable Anki Alive Reduced Motion.
2. Reach an Oracle commitment and reveal.
3. Confirm both states remain understandable without requiring animated transitions.

## G. Undo / re-answer

1. Resolve an Oracle prediction by answering its card.
2. Use Anki Undo for that review.
3. Confirm normal Expedition reconciliation still occurs.
4. Re-answer the card honestly.
5. Confirm there is no duplicate Oracle history/reveal storm.

The implementation must reuse the original commitment rather than rerolling a new prediction after Undo.

## H. Expedition completion precedence

If an Oracle-resolved review also completes the Expedition:

1. Confirm Expedition closure remains the dominant event.
2. Confirm Oracle does not interrupt or cover the completion stopping point.

## I. Performance

Use `Tools > Anki Alive Performance Snapshot` after enough samples.

Record:

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

Also note whether question display feels delayed when Oracle evaluates a candidate. If it does, treat that as a Phase 2 performance defect even if the accepted-answer timing remains low.

## J. Restart continuity

1. Reach a card showing `Prediction sealed`.
2. If practical, leave/restart before answering without manufacturing unsafe collection state.
3. Return to review and confirm user-visible prediction truth is not rerolled.

If the host makes this difficult to reproduce naturally, record the limitation rather than guessing.

## Result

```text
Overall: PENDING
Anki version:
OS:
FSRS enabled: yes/no
Neutral commitment cue: PASS/FAIL
No pre-answer leakage: PASS/FAIL
Post-answer reveal: PASS/FAIL
Non-FSRS fallback: PASS/FAIL / NOT EXERCISED
Focus Mode: PASS/FAIL
Reduced Motion: PASS/FAIL
Undo/re-answer: PASS/FAIL
Completion precedence: PASS/FAIL
Performance: PASS/FAIL
Restart continuity: PASS/FAIL / NOT EXERCISED
Blocking defects:
Non-blocking observations:
```
