# Phase 0 — Anki Host Validation

Status: MOSTLY PASS — FINAL MINI-CHECK PENDING

This document records Phase 0 host facts separately from assumptions. Real-host evidence below was collected on Windows 11 with Anki 25.09.4 (d52ca669), Python 3.13.5, Qt 6.9.1, and PyQt 6.9.1.

## 1. Accepted Review Boundary

Use `gui_hooks.reviewer_did_answer_card` as the notification that an answer was accepted by the reviewer.

Evidence from Anki's generated GUI hook declarations:

- `reviewer_will_answer_card` may modify or bypass a rating and explicitly recommends `reviewer_did_answer_card` when code only needs notification.
- `reviewer_did_answer_card` supplies reviewer, card, and the accepted rating.

Real-host result:

- 10 accepted reviews produced 10 normalized `review_observation` events.
- Observed ratings in this run: 2 and 3.
- Each event included card ID, response time, source revlog ID, and deterministic observation UUID.

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

Real-host evidence showed distinct source revlog IDs for distinct accepted reviews, including a fresh source/observation identity when a previously undone card was answered again.

## 3. Undo / Reversal Mapping

Do not blindly decrement feature state on an undo hook.

The GUI undo notification proves that an undo operation completed, but it does not itself identify a review row. The safe Phase 0 mapping is:

```text
accepted review
→ remember normalized source revlog id
→ Anki undo completes
→ verify whether tracked revlog row still exists
→ only if it disappeared, emit ReviewReversed
→ reconciliation re-evaluates derived state
```

Real-host result:

- 2 review undos produced 2 `review_reversed` events.
- Each reversal referenced the exact card ID, source review ID, and observation ID from the accepted review being undone.
- Re-answering an undone card produced a new source review ID and a new deterministic observation ID.

Still pending for the final mini-check:

- undo one non-review operation and verify no false `review_reversed` event is emitted.

## 4. Profile Identity

Do not use the profile display name as durable identity.

Anki's profile manager stores the current name separately and renames the profile directory when the profile is renamed. Anki Alive therefore owns a random UUID stored in a small file inside that profile directory:

```text
<profile folder>/.anki_alive_profile_id
```

Because the identifier moves with the directory rename, display-name changes do not change durable Anki Alive scope.

Automated coverage validates reopen and folder rename behavior. Real desktop profile-rename UX remains desirable compatibility coverage but is no longer a blocker for the review/reversal Phase 1 entry gate.

## 5. Minimum Supported Anki Version

Implementation floor: Anki 25.02.7 (`250207`).

Rationale:

- required generated GUI hooks exist in the 25.02.7 upstream source;
- Anki 25.02.7 upstream Python tooling targets Python 3.9;
- Anki Alive CI passes Python 3.9 and Python 3.13;
- real-host validation currently passes on Anki 25.09.4.

The exact 25.02.7 binary has not been manually smoke-tested. Compatibility should therefore be described precisely as "supported floor by source/API contract; real-host validated on 25.09.4" until broader release-matrix testing is available.

## 6. Performance Evidence

Real-host samples from the manual validation run:

### `reviewer_did_answer_card`

10 samples, milliseconds:

```text
0.550, 0.403, 0.369, 0.373, 0.426,
0.358, 0.364, 0.533, 0.350, 0.669
```

Summary:

- min: 0.350 ms
- median: 0.388 ms
- max: 0.669 ms
- all observed samples: < 1 ms

This is comfortably below the Phase 0 preferred synchronous reviewer budget of < 5 ms.

### `state_did_undo`

2 samples:

```text
0.511, 0.333
```

- median: 0.422 ms
- max: 0.511 ms

## 7. Storage / Bootstrap Evidence

Real-host startup logged:

- Anki version integer: `250904`
- sidecar database integrity: `true`
- module: `anki_alive_dev`

A later restart also emitted `bootstrap_complete` again without startup failure.

## 8. Source Paths Inspected

Anki upstream source areas used for Phase 0 validation:

```text
qt/tools/genhooks_gui.py
qt/aqt/reviewer.py
qt/aqt/main.py
qt/aqt/addons.py
qt/aqt/log.py
qt/aqt/profiles.py
rslib/src/scheduler/answering/mod.rs
rslib/src/scheduler/answering/revlog.rs
pylib/anki/db.py
pylib/anki/utils.py
```

## 9. Final Mini-Check

Before marking Phase 0 fully complete, collect one small additional real-host run:

1. grade one card with Again (1);
2. grade one card with Easy (4);
3. perform one non-review operation that Anki can undo, then undo it;
4. confirm no false `review_reversed` event is emitted for that non-review undo.

The core review/reversal mapping and performance budget have already passed.

## 10. Phase 1 Gate

The review/undo architecture has passed its critical real-host proof on Anki 25.09.4. Phase 1 durable Expedition progress remains held only until the final mini-check above confirms ratings 1/4 and non-review undo behavior.