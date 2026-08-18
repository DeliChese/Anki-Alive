# Phase 0 — Foundation Handoff

## Status

PARTIAL

Completed on: not complete
Add-on version: 0.0.1-dev0
Schema version: 1
Target Anki versions tested: no real-host manual validation yet

---

## 1. Scope Completed

- host-agnostic core package
- synchronous EventBus
- normalized ReviewObservation / ReviewReversed contracts
- deterministic observation identity from profile key + Anki revlog ID
- shared reconciliation proof with reversible derived state
- stable add-on-owned profile identity stored inside the Anki profile folder
- explicit clock and local study-day primitives
- typed SettingsService and central FocusPolicy
- sidecar SQLite schema v1 with schema_meta + migration_history only
- WAL journal mode, busy timeout, integrity check, backup API, graceful checkpoint on close
- structured privacy-safe DiagnosticsService
- PerformanceTimer primitive
- concrete idempotent Anki GUI hook wiring boundary
- semantic UI CSS tokens, visible focus baseline, Focus Mode suppression baseline, reduced-motion baseline
- GitHub Actions CI matrix for Python 3.9 and 3.13

## 2. Scope Not Completed

- real Anki smoke test
- real reviewer hook latency benchmark
- final minimum supported Anki version policy
- final bootstrap entrypoint inside packaged add-on runtime
- end-to-end settings/config adapter against Anki addonManager
- final architecture/data/ADR synchronization
- final Phase 0 completion status

## 3. Implementation Summary

Accepted reviews are observed through the reviewer integration boundary. The adapter reads the latest matching revlog row and uses its revlog ID as source review identity. Undo does not blindly mutate feature state. After Anki reports a successful undo, tracked source revlog rows are checked; ReviewReversed is emitted only when a previously observed source row is proven absent.

This keeps review truth grounded in Anki data while leaving feature policy outside the integration layer.

## 4. Architecture Changes

New implementation boundaries include:

- `anki_alive/core/`
- `anki_alive/integration/`
- `anki_alive/settings.py`
- `anki_alive/storage.py`
- `anki_alive/diagnostics.py`
- `anki_alive/performance.py`
- `anki_alive/ui/foundation.css`

No feature modules or feature tables have been introduced.

## 5. Data / Schema Changes

Schema version: 1

Tables:

- `schema_meta`
- `migration_history`

SQLite policy currently implemented:

- foreign keys ON
- WAL journal mode
- synchronous NORMAL
- busy timeout 5000 ms
- integrity-check API
- SQLite online backup API
- WAL checkpoint/truncate on graceful close

No Anki collection schema modifications.

## 6. UI / UX Changes

No product screen exists yet.

Foundation CSS now provides:

- semantic background/text/line/accent roles
- spacing/radius primitives
- visible focus styles
- Focus Mode motion/suppression baseline
- `prefers-reduced-motion` fallback
- light/dark semantic surface baseline

## 7. Tests Run

### Automated

Command used by GitHub Actions:

`python -m pytest tests -q`

Matrix:

- Python 3.9
- Python 3.13

Current latest run must be checked before declaring final Phase 0 completion.

### Manual

Not run in real Anki yet.

### Not Tested

- real Anki accepted review mapping
- real undo mapping
- profile switch/rename inside actual Anki
- sidecar lifecycle during actual profile close/reopen
- reviewer latency under real review workload
- visual rendering inside Anki WebView

## 8. Performance Findings

Performance instrumentation exists.

Real reviewer P50/P95: not measured yet.

Do not claim reviewer performance acceptance until manual host benchmark evidence exists.

## 9. Accessibility Findings

Implemented foundation:

- visible `:focus-visible`
- reduced-motion media query
- non-color status-label mechanism
- light/dark semantic tokens

Real keyboard/WebView validation remains pending.

## 10. Files Changed

Major implementation files:

- `anki_alive/core/events.py`
- `anki_alive/core/focus.py`
- `anki_alive/core/reconciliation.py`
- `anki_alive/core/review.py`
- `anki_alive/core/time.py`
- `anki_alive/integration/hooks.py`
- `anki_alive/integration/profile.py`
- `anki_alive/integration/reviewer.py`
- `anki_alive/settings.py`
- `anki_alive/storage.py`
- `anki_alive/diagnostics.py`
- `anki_alive/performance.py`
- `anki_alive/ui/foundation.css`
- `tests/test_phase0_core.py`
- `.github/workflows/phase0-ci.yml`
- `docs/PHASE0_HOST_VALIDATION.md`

## 11. Decisions Accepted / Implemented in Direction

- revlog ID is the normalized source review identity
- add-on observation IDs are deterministic from profile key + revlog ID
- successful undo is only a trigger to reconcile; source disappearance is proof of review reversal
- durable profile identity is add-on-owned and stored inside the profile folder
- Phase 0 sidecar SQLite uses WAL and explicit backup/integrity APIs
- diagnostics are disabled by default and redact content-bearing fields

Canonical `docs/06_DECISIONS.md` still needs final synchronization before Phase 0 is marked complete.

## 12. Known Issues

### KI-001 — Real-host review mapping unverified

Severity: HIGH
Impact: Phase 1 durable progress remains blocked.
Workaround: none; run the required real Anki validation.

### KI-002 — Reviewer latency unmeasured

Severity: HIGH
Impact: cannot prove hot-path budget yet.
Workaround: instrument and measure during manual smoke test.

## 13. Technical Debt

### TD-001 — Settings host adapter

Why deferred: core typed settings behavior was proven first.
Recommended future action: wire Anki addonManager config read/write at bootstrap.

### TD-002 — Final compatibility floor

Why deferred: API evidence exists, but minimum supported version should be paired with real-host validation.
Recommended future action: choose and document one supported floor after smoke testing.

## 14. Deferred Ideas

All Expedition/gameplay work remains deferred to Phase 1+.

## 15. Next Phase Dependencies

Before Phase 1 begins:

- manually validate accepted reviews in real Anki
- manually validate review undo/reversal in real Anki
- measure reviewer overhead
- resolve minimum supported Anki version
- synchronize architecture/data/decision documents
- change this handoff from PARTIAL only when Definition of Done is actually satisfied

## 16. Next Agent Startup

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

Then inspect the Phase 0 branch implementation and latest CI result before changing code.
