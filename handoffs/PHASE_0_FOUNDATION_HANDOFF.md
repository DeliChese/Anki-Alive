# Phase 0 — Foundation Handoff

## Status

PARTIAL — REAL ANKI HOST VALIDATION PENDING

Completed on: not complete
Add-on version: 0.0.1-dev0
Schema version: 1
Minimum Anki version: 25.02.7 (`250207`), provisional until real-host confirmation

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
- Anki addonManager settings adapter
- packaged root add-on entrypoint and default `config.json`
- compatibility gate and `manifest.json`
- sidecar SQLite schema v1 with schema_meta + migration_history only
- storage under preserved `user_files`
- WAL journal mode, busy timeout, integrity check, backup API, graceful checkpoint on close
- structured privacy-safe DiagnosticsService
- official Anki add-on logger integration
- PerformanceTimer primitive
- real review/undo hook timing instrumentation
- concrete idempotent Anki GUI hook wiring boundary
- semantic UI CSS tokens, visible focus baseline, Focus Mode suppression baseline, reduced-motion baseline
- one-time Windows dev junction helper
- simple real-host validation checklist
- GitHub Actions CI matrix for Python 3.9 and 3.13
- canonical Phase 0 ADR/status synchronization

## 2. Scope Not Completed

- real Anki smoke test
- real reviewer hook latency benchmark
- final removal of provisional qualifier from the Anki 25.02.7 compatibility floor
- final Phase 0 completion status

## 3. Implementation Summary

Accepted reviews are observed through `gui_hooks.reviewer_did_answer_card`. The adapter reads the latest matching revlog row and uses its revlog ID as source review identity. Normalized observation IDs are deterministic from `(profile_key, revlog.id)`.

Undo does not blindly mutate feature state. `gui_hooks.state_did_undo` only triggers reconciliation. Tracked source revlog rows are checked, and `ReviewReversed` is emitted only when a previously observed source row is proven absent.

Packaged bootstrap now loads native Anki config, opens the sidecar database, registers hooks once, wires privacy-safe diagnostics to Anki's official add-on logger, and instruments accepted-review/undo hook latency.

## 4. Architecture Changes

Implementation boundaries include:

- `anki_alive/core/`
- `anki_alive/integration/`
- `anki_alive/bootstrap.py`
- `anki_alive/settings.py`
- `anki_alive/storage.py`
- `anki_alive/diagnostics.py`
- `anki_alive/performance.py`
- `anki_alive/ui/foundation.css`

Add-on package/runtime files include:

- root `__init__.py`
- `config.json`
- `manifest.json`
- `user_files/README.txt`

No feature modules or feature tables have been introduced.

## 5. Data / Schema Changes

Schema version: 1

Tables:

- `schema_meta`
- `migration_history`

SQLite policy:

- foreign keys ON
- WAL journal mode
- synchronous NORMAL
- busy timeout 5000 ms
- integrity-check API
- SQLite online backup API
- WAL checkpoint/truncate on graceful close
- sidecar path under add-on `user_files`

No Anki collection schema modifications.

## 6. UI / UX Changes

No product screen exists yet.

Foundation CSS provides:

- semantic background/text/line/accent roles
- spacing/radius primitives
- visible focus styles
- Focus Mode motion/suppression baseline
- `prefers-reduced-motion` fallback
- light/dark semantic surface baseline

## 7. Tests Run

### Automated

GitHub Actions command:

`python -m pytest tests -q`

Matrix:

- Python 3.9 — PASS
- Python 3.13 — PASS

Latest code-changing workflow checked during this handoff update: run `32110194168`, both matrix jobs successful.

Coverage includes core/reconciliation, persistence, settings, diagnostics redaction, UI foundation, fake-host review/undo integration, compatibility metadata, and Anki config adapter behavior.

### Manual

Not run in real Anki yet.

Canonical checklist: `docs/PHASE0_MANUAL_VALIDATION.md`.

### Not Yet Validated in Real Host

- accepted review mapping in desktop Anki
- undo mapping in desktop Anki
- real add-on startup through linked development folder
- settings/config behavior through Anki Add-ons UI
- sidecar lifecycle in actual Anki process
- real reviewer latency

## 8. Performance Findings

Performance instrumentation now wraps:

- `reviewer_did_answer_card`
- `state_did_undo`

When diagnostics are enabled, samples are emitted through Anki's add-on logger.

Real reviewer P50/P95: not measured yet.

Provisional budget:

- Preferred < 5 ms
- Typical < 10 ms
- P95 < 20 ms

Do not claim reviewer performance acceptance until real-host evidence exists.

## 9. Accessibility Findings

Implemented foundation:

- visible `:focus-visible`
- reduced-motion media query
- non-color status-label mechanism
- light/dark semantic tokens

Real keyboard/WebView feature validation belongs to later UI slices.

## 10. Major Files Changed

- `__init__.py`
- `config.json`
- `manifest.json`
- `anki_alive/bootstrap.py`
- `anki_alive/core/events.py`
- `anki_alive/core/focus.py`
- `anki_alive/core/reconciliation.py`
- `anki_alive/core/review.py`
- `anki_alive/core/time.py`
- `anki_alive/integration/compatibility.py`
- `anki_alive/integration/hooks.py`
- `anki_alive/integration/profile.py`
- `anki_alive/integration/reviewer.py`
- `anki_alive/integration/settings_adapter.py`
- `anki_alive/settings.py`
- `anki_alive/storage.py`
- `anki_alive/diagnostics.py`
- `anki_alive/performance.py`
- `anki_alive/ui/foundation.css`
- `tests/test_phase0_core.py`
- `tests/test_phase0_packaging.py`
- `.github/workflows/phase0-ci.yml`
- `scripts/link_dev_addon.ps1`
- `docs/PHASE0_HOST_VALIDATION.md`
- `docs/PHASE0_MANUAL_VALIDATION.md`

## 11. Decisions Accepted / Implemented

- provisional minimum Anki version: 25.02.7 (`250207`)
- accepted review hook: `reviewer_did_answer_card`
- source review identity: revlog ID
- deterministic normalized observation identity: profile key + revlog ID
- undo hook is a reconciliation trigger, not reversal proof
- source revlog disappearance is reversal proof
- durable profile identity is add-on-owned and stored inside the profile folder
- Phase 0 frontend uses host-compatible HTML/CSS primitives, no framework
- Phase 0 sidecar SQLite uses WAL and explicit backup/integrity APIs
- diagnostics are disabled by default and redact content-bearing fields
- official Anki add-on logger is used when diagnostics are enabled

Canonical decisions are synchronized in `docs/06_DECISIONS.md`.

## 12. Known Issues

### KI-001 — Real-host review mapping unverified

Severity: HIGH
Impact: Phase 1 durable progress remains blocked.
Required action: run `docs/PHASE0_MANUAL_VALIDATION.md` in real Anki.

### KI-002 — Reviewer latency unmeasured

Severity: HIGH
Impact: cannot prove hot-path budget yet.
Required action: collect diagnostic timing samples during the same manual smoke test.

## 13. Technical Debt

No known Phase 0 code debt currently blocks the manual validation gate.

Cross-feature transaction policy remains intentionally deferred to no later than Phase 3.

## 14. Deferred Ideas

All Expedition/gameplay work remains deferred to Phase 1+.

## 15. Next Phase Dependencies

Before Phase 1 begins:

- manually validate accepted reviews in real Anki
- manually validate review undo/reversal in real Anki
- measure reviewer overhead
- record exact Anki version and OS
- promote the provisional compatibility floor if evidence passes
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
8. `docs/PHASE0_MANUAL_VALIDATION.md`
9. `docs/phases/PHASE_0_FOUNDATION.md`
10. this handoff

Then inspect the Phase 0 branch implementation and latest CI result before changing code.
