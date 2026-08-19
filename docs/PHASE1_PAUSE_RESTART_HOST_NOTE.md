# Phase 1 Pause / Restart Host Evidence

Status: PASS
Date: 2026-08-19
Phase: 1
Feature: Expedition

A real desktop Anki run confirmed the paused-session recovery path after the latest Phase 1 host-hardening work.

Observed host behavior:

- an active Expedition could be left through the normal reviewer exit path,
- Anki returned to the normal Deck Browser,
- Anki Alive Today showed the same Expedition as resumable,
- target and completed progress remained unchanged,
- after fully closing and restarting Anki, the same Expedition remained resumable,
- resuming returned to normal Anki review and subsequent accepted review work continued the same Expedition.

This is real-host evidence, not an inference from unit tests.

Automated evidence already present on the same implementation family:

```text
GitHub Actions workflow: Anki Alive CI
Probe run: #133
Python 3.9 core-tests: PASS
Python 3.13 core-tests: PASS
Probe merged: no
```

The automated suite also includes durable database reopen coverage for paused Expedition target, progress, checkpoint plan, and resume transition.

Remaining Phase 1 host gates include Undo reconciliation, pending-completion restart recovery, Focus Mode, reduced motion, keyboard, filtered/custom study smoke, and reviewer performance evidence.
