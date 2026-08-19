# Phase 2 Oracle — Real-Host Smoke Checklist

Status: PENDING
Date: 2026-08-19

Use this after syncing the latest `main` into the desktop Anki add-on checkout.

## Preconditions

- FSRS is enabled on the host profile.
- Use an ordinary deck with reviewed cards; Oracle policy v1 requires at least 3 prior reviews and usable FSRS memory state.
- Start a normal Anki Alive Expedition.
- Do not alter collection state just to force a particular Oracle prediction.

## Expected cadence

Oracle gets an opportunity when durable Expedition progress is `0, 5, 10, ...`.

Eligibility is still controlled by memory policy. If the card at a cadence boundary lacks enough memory evidence, no prediction is committed and the next eligible card at the same progress boundary may be considered.

## A. No pre-answer leakage

1. Start an Expedition and reach an Oracle-eligible reviewed card.
2. Observe the question side before showing the answer.
3. Confirm there is no predicted outcome, probability, grading recommendation, or answer-bearing Oracle content.
4. Confirm normal Anki answer controls and keyboard shortcuts behave unchanged.

PASS requires Oracle to remain private before the learner answers.

## B. Post-answer reveal

1. Answer an eligible card normally.
2. Grade with the rating that honestly matches recall.
3. Confirm any Oracle reveal appears only after the accepted grade.
4. Confirm the reveal is small, non-interactive, and disappears without blocking the next card.
5. Confirm the reveal does not award points, currency, bonus Expedition progress, or praise a higher grading button.

## C. Rating semantics

Exercise honest examples where practical:

- `Again` is interpreted as failed recall.
- `Hard`, `Good`, and `Easy` are interpreted as recalled for Oracle's binary outcome.
- Expedition progress still advances exactly once for every accepted review regardless of rating.

Do not intentionally misgrade cards to make Oracle look correct.

## D. Focus Mode

1. Enable Focus Mode.
2. Reach another Oracle cadence boundary and answer an eligible card.
3. Confirm normal review and Expedition progress continue.
4. Confirm Oracle reveal is suppressed.
5. Disable Focus Mode and continue reviewing normally.

PASS requires Focus Mode to change presentation only, not review or Oracle domain history.

## E. Reduced Motion

1. Enable Anki Alive Reduced Motion.
2. Reach an Oracle reveal.
3. Confirm the reveal remains understandable without requiring an animated transition.

## F. Undo / re-answer

1. Resolve an Oracle prediction by answering its card.
2. Use Anki Undo for that review.
3. Confirm normal Expedition reconciliation still occurs.
4. Re-answer the card honestly.
5. Confirm there is no duplicate Oracle history/reveal storm.

The implementation must reuse the original commitment rather than rerolling a new prediction after Undo.

## G. Expedition completion precedence

If an Oracle-resolved review also completes the Expedition:

1. Confirm Expedition closure remains the dominant event.
2. Confirm Oracle does not interrupt or cover the completion stopping point.

## H. Performance

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

## I. Restart continuity

1. Commit an Oracle prediction by displaying an eligible question.
2. If practical, leave/restart before answering without manufacturing unsafe collection state.
3. Return to review and confirm user-visible truth is not rerolled.

If the host makes this difficult to reproduce naturally, record the limitation rather than guessing.

## Result

```text
Overall: PENDING
Anki version:
OS:
FSRS enabled: yes/no
No pre-answer leakage: PASS/FAIL
Post-answer reveal: PASS/FAIL
Focus Mode: PASS/FAIL
Reduced Motion: PASS/FAIL
Undo/re-answer: PASS/FAIL
Completion precedence: PASS/FAIL
Performance: PASS/FAIL
Restart continuity: PASS/FAIL / NOT EXERCISED
Blocking defects:
Non-blocking observations:
```
