# Phase 0 — Anki Host Validation

Status: IN PROGRESS

This document records Phase 0 host facts separately from assumptions. It is implementation evidence, not a replacement for manual Anki validation.

## 1. Accepted Review Boundary

Use `gui_hooks.reviewer_did_answer_card` as the notification that an answer was accepted by the reviewer.

Evidence from Anki's generated GUI hook declarations:

- `reviewer_will_answer_card` may modify or bypass a rating and explicitly recommends `reviewer_did_answer_card` when code only needs notification.
- `reviewer_did_answer_card` supplies reviewer, card, and the accepted rating.

Integration rule:

- do not create durable review-derived truth from `reviewer_will_answer_card`;
- on `reviewer_did_answer_card`, resolve the newly written revlog row and normalize it to `ReviewObservation`.

## 2. Source Review Identity

Anki's scheduler constructs the revlog entry from the accepted answer and sets:

```text
revlog.id = answered_at_millis
```

The revlog row therefore supplies the host-owned source identity for one accepted review.

Anki Alive derives its own stable observation UUID from:

```text
(profile_key, revlog.id)
```

This makes observation identity deterministic across duplicate notifications and reloads while keeping profiles isolated.

## 3. Undo / Reversal Mapping

Do not blindly decrement feature state on an undo hook.

The GUI undo notification proves that an undo operation completed, but it does not itself identify a review row. The safe Phase 0 mapping is therefore:

```text
accepted review
→ remember normalized source revlog id
→ Anki undo completes
→ verify whether tracked revlog row still exists
→ only if it disappeared, emit ReviewReversed
→ reconciliation re-evaluates derived state
```

Undoing an unrelated operation must emit no `ReviewReversed` event.

This mapping still requires manual host validation with real review + undo behavior before Phase 1 durable progress is unlocked.

## 4. Profile Identity

Do not use the profile display name as durable identity.

Anki's profile manager stores the current name separately and renames the profile directory when the profile is renamed. Anki Alive therefore owns a random UUID stored in a small file inside that profile directory:

```text
<profile folder>/anki_alive_profile_id
```

Because the identifier moves with the directory rename, display-name changes do not change durable Anki Alive scope.

Manual validation still required:

- profile rename,
- profile copy/restore expectations,
- multiple profiles,
- collection replacement inside one profile.

## 5. Minimum Supported Anki Version

Not accepted yet.

Current implementation is intentionally based on modern generated GUI hooks and the modern scheduler/revlog model. The initial compatibility candidate is Anki 25.09.4 or newer, but this remains a candidate until the host smoke-test matrix is actually run.

Do not mark ADR-P01 accepted based on source inspection alone.

## 6. Source Paths Inspected

Anki upstream source areas used for Phase 0 validation:

```text
qt/tools/genhooks_gui.py
qt/aqt/reviewer.py
qt/aqt/main.py
rslib/src/scheduler/answering/mod.rs
rslib/src/scheduler/answering/revlog.rs
pylib/anki/db.py
```

## 7. Manual Host Test Required

Before Phase 0 completion:

1. Load add-on in target Anki.
2. Show question and answer.
3. Grade with Again, Hard, Good, Easy.
4. Verify exactly one normalized observation per accepted review.
5. Verify source `revlog.id`, rating, card ID, timestamp, and response time.
6. Undo the accepted review.
7. Verify the source revlog row disappears and exactly one reversal is emitted.
8. Undo a non-review operation and verify no false review reversal is emitted.
9. Rename profile and verify profile key remains stable.
10. Restart Anki and verify storage/settings/profile scoping.

Record exact Anki version and OS with results.

## 8. Phase 1 Gate

Phase 1 durable Expedition progress remains blocked until the review/undo mapping above passes manual host validation.
