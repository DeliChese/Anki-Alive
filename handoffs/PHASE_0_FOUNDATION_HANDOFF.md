# Phase 0 — Foundation Handoff

## Status

COMPLETE

Completed on: 2026-08-18
Add-on version: 0.0.1-dev0
Schema version: 1
Compatibility floor: Anki 25.02.7 (`250207`)
Real-host validation: Anki 25.09.4 (d52ca669), Python 3.13.5, Qt 6.9.1, PyQt 6.9.1, Windows 11 (10.0.26200)

---

## 1. Scope Completed

- host-agnostic core package and synchronous EventBus
- normalized `ReviewObservation` / `ReviewReversed`
- deterministic observation identity from profile key + Anki `revlog.id`
- shared reversible reconciliation proof
- stable add-on-owned profile identity stored inside the Anki profile folder
- explicit clock, IDs, UTC timestamps, and local study day
- typed SettingsService and central FocusPolicy
- native Anki addonManager settings adapter
- packaged root add-on entrypoint, `config.json`, and `manifest.json`
- compatibility gate with floor Anki 25.02.7 (`250207`)
- sidecar SQLite schema v1 with only `schema_meta` and `migration_history`
- sidecar storage under preserved `user_files`
- WAL, busy timeout, integrity check, online backup, transactions, checkpoint-on-close
- privacy-safe DiagnosticsService using Anki's official add-on logger
- PerformanceTimer and concrete accepted-review/undo timing instrumentation
- concrete Anki GUI hook wiring validated against real generated hook objects
- semantic UI CSS foundation, visible focus, reduced motion, Focus Mode baseline
- Windows development junction helper
- GitHub Actions CI matrix on Python 3.9 and 3.13
- canonical Phase 0 validation/status documentation

No gameplay features or feature tables were introduced.

## 2. Real Host Validation

Host:

- Anki 25.09.4 (d52ca669)
- Python 3.13.5
- Qt 6.9.1
- PyQt 6.9.1
- Windows 11 10.0.26200

Validated behavior:

- linked development add-on starts successfully
- database integrity reports true at bootstrap
- accepted review events are observed in real desktop Anki
- ratings 1, 2, 3, and 4 are normalized correctly
- source review identity is the host `revlog.id`
- undo of accepted reviews produces `ReviewReversed` only after source revlog disappearance
- re-answering an undone card creates a new source review ID and observation ID
- undo of a non-review operation triggers reconciliation timing but emits no false `ReviewReversed`
- Anki restart reboots the add-on cleanly

Two real-host-only bootstrap issues were found and corrected during validation:

1. linked development import path needed the repository root on `sys.path`
2. generated Anki GUI hook objects support append but are not iterable

These are now covered by the implementation direction.

## 3. Performance Findings

Real accepted-review hook samples: 12.

`reviewer_did_answer_card`:

- min: 0.350 ms
- median / P50: 0.397 ms
- P95: approximately 0.604 ms
- max: 0.669 ms

Observed `state_did_undo` samples ranged from 0.180 ms to 0.511 ms.

Phase 0 provisional synchronous budget:

- Preferred < 5 ms
- Typical < 10 ms
- P95 < 20 ms

Result: PASS with substantial headroom.

These numbers are a Phase 0 baseline, not a permanent budget exemption for later features. Future reviewer work must preserve cumulative hot-path discipline.

## 4. Review / Undo Mapping

Accepted review:

```text
reviewer_did_answer_card
→ resolve latest matching revlog row
→ normalize source revlog ID
→ publish ReviewObservation
```

Undo:

```text
state_did_undo
→ inspect tracked source revlog rows
→ if source row still exists: no reversal
→ if source row disappeared: publish ReviewReversed
```

The undo hook is a reconciliation trigger, not proof by itself.

## 5. Persistence Foundation

Schema version: 1

Tables:

- `schema_meta`
- `migration_history`

Policy:

- sidecar SQLite only
- no Anki collection schema modifications
- foreign keys ON
- WAL journal mode
- synchronous NORMAL
- busy timeout 5000 ms
- explicit transactions
- integrity-check API
- SQLite online backup API
- graceful WAL checkpoint on close

## 6. Compatibility Decision

Anki Alive declares a compatibility floor of **Anki 25.02.7** (`250207`).

Evidence:

- required modern hook APIs are present in the 25.02.7 upstream source
- Python 3.9 is covered by CI for the compatibility-floor era
- Python 3.13 is covered by CI and real-host validation
- real desktop validation passed on Anki 25.09.4

This does not claim every intermediate Anki build has been manually tested. It defines the supported floor and records the actual runtime version used for Phase 0 validation.

## 7. Automated Validation

GitHub Actions command:

`python -m pytest tests -q`

Matrix:

- Python 3.9 — PASS
- Python 3.13 — PASS

Automated coverage includes core/reconciliation, persistence, settings, diagnostics redaction, UI foundation, fake-host review/undo integration, compatibility metadata, and Anki config adapter behavior.

## 8. Accessibility / UI Foundation

Implemented:

- semantic UI roles
- visible `:focus-visible`
- reduced-motion support
- non-color status semantics
- light/dark token baseline
- Focus Mode presentation suppression baseline

Feature-screen-specific accessibility validation belongs to later phases.

## 9. Phase 1 Entry Contract

Phase 1 may rely on:

- stable add-on bootstrap
- stable profile scoping
- normalized accepted-review events
- proven review reversal/reconciliation path
- sidecar persistence and migrations
- settings and FocusPolicy
- measured reviewer performance baseline
- EventOrchestrator-ready architecture direction

Phase 0 no longer blocks durable Phase 1 Expedition work.

## 10. Deferred Work

Intentionally deferred rather than incomplete Phase 0 scope:

- feature-specific FSRS / Memory Engine policy
- asynchronous host-data work until a later feature requires it
- cross-feature review transaction policy, due no later than Phase 3
- all Expedition/Oracle/Rescue/Nemesis/Fragments/Relics/Memory World gameplay

## 11. Next Agent Startup

Read, in order:

1. `PROJECT.md`
2. `AGENTS.md`
3. `docs/01_PRODUCT_PRINCIPLES.md`
4. `docs/03_ARCHITECTURE.md`
5. `docs/04_DATA_MODEL.md`
6. `docs/06_DECISIONS.md`
7. `docs/PHASE0_HOST_VALIDATION.md`
8. `docs/phases/PHASE_0_FOUNDATION.md`
9. this handoff

Then inspect the current branch/PR and latest CI before changing code.
