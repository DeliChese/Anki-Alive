# Phase 1 Expedition UI Implementation Notes

Status: PRE-HOST RE-VALIDATION
Phase: 1
Feature: Expedition
Canonical art direction: Arcane Memory Interface

## Purpose

This note records the current Phase 1 presentation decisions. It is not the
final Phase 1 handoff.

## Canonical sources applied

The implementation treats these documents as constraints:

- `docs/02_DESIGN_SYSTEM.md`
- `docs/design/00_VISUAL_CONSTITUTION.md`
- `docs/design/01_COLOR_AND_SURFACE_DNA.md`
- `docs/design/02_TYPOGRAPHY_AND_INFORMATION_HIERARCHY.md`
- `docs/design/03_MOTION_LANGUAGE.md`
- `docs/design/04_EFFECTS_CATALOG.md`
- `docs/design/05_COMPONENT_CANON.md`
- `docs/design/06_FEATURE_MOOD_MAPPING.md`
- `docs/design/08_UI_REVIEW_CHECKLIST.md`
- `docs/phases/PHASE_1_EXPEDITION.md`

## Host-surface decision

Real-host inspection with the Onigiri add-on showed that a full Today surface
embedded in Anki's Deck Browser is too invasive. Deck Browser is a shared host
surface and other add-ons legitimately customize it.

The current boundary is therefore:

- Anki Alive does not inject Today into Deck Browser content.
- Deck Browser remains owned by Anki and installed appearance/dashboard add-ons.
- Native Decks / Add / Browse / Stats / Sync flows remain native and available.
- Anki Alive Today opens in a dedicated modeless `AnkiWebView` window.
- Today is reachable from an `Alive` top-toolbar entry and from
  `Tools > Anki Alive Today`.
- Reviewer presentation remains the only Phase 1 WebView augmentation.

This avoids reimplementing Anki's main dashboard merely to preserve functionality
that Anki already owns well.

See `docs/PHASE1_ONIGIRI_HOST_NOTE.md` for the host finding.

## Today

Canonical components:

- `AA-MemoryCore`
- `AA-ExpeditionTrack`
- `AA-CheckpointNode`
- shared button, section, and empty-state anatomy

Memory Core uses only the real current Anki queue. It does not invent memory
health, stability, fragility, or later-phase meaning.

Today's Signals remains truthfully empty until a real implemented feature has a
signal. No Oracle, Rescue, Nemesis, Fragment, Relic, or World signal is faked.

The dedicated Today window has its own canvas stylesheet so its visual identity
does not inherit arbitrary Deck Browser backgrounds or skin CSS.

Real-host screenshot review on 2026-08-19 confirmed the intended restrained
hierarchy with an active Expedition at 2 / 11, while also exposing horizontal
overflow and multi-second opening latency. Those two host defects are now fixed
in implementation but remain pending re-validation on the desktop host.

### Today host performance strategy

The dedicated surface now treats WebEngine setup as reusable host infrastructure:

- create one hidden `AnkiWebView` shell after startup settles,
- load CSS/JS once,
- keep the dialog/WebView alive when the user closes Today,
- update only the inner Today markup on reopen/refresh,
- release the retained WebView only when the add-on runtime is torn down.

This avoids recreating Chromium/page state on every Today open. The prewarm is
scheduled after bootstrap so add-on startup itself is not synchronously blocked.
Perceived opening latency must still be re-measured by real-host observation.

## Reviewer

Canonical component:

- `AA-ReviewProgressStrip`

Rules:

- Tier 0–1 presentation,
- M0 during question state,
- compact progress only,
- pointer-transparent,
- no particles,
- no animated blur,
- no ambient loop,
- no secondary dashboard,
- card remains visually dominant.

Checkpoint feedback is a small non-blocking status cue after a real checkpoint
transition.

## Completion

Completion leaves active recall, returns Anki to a safe non-review state, and
opens the dedicated Today window with the closure summary.

Reasons:

- no closure overlay on top of the next question,
- `Done` is psychologically primary,
- `Continue reviewing` is explicit and secondary,
- completion does not manufacture another mandatory Expedition.

Completion presentation state is durable and separate from Expedition domain
state. A pending summary survives restart until dismissed. Undo reconciliation
that reopens the Expedition invalidates stale completion presentation.

## Expedition visual DNA

```text
Metaphor
cartography + pathfinding + measured travel

Geometry
route line + checkpoint nodes + current position + completion marker

Material
matte low-chroma surfaces + restrained amber path-light

Motion verbs
advance + arrive + connect + settle + complete

Density
low to medium
```

Explicitly rejected:

- RPG quest framing,
- racing metaphors,
- treasure-map styling,
- neon HUD treatment,
- reward confetti,
- casino motion,
- card-wall dashboard composition.

## Approved effects

The implementation reuses catalog semantics for:

- `AA-FadeRise-01`
- `AA-Press-01`
- `AA-ProgressFlow-01`
- `AA-CheckpointActivate-01`
- `AA-ExpeditionComplete-01`

No new effect family is introduced.

## Event orchestration

Phase 1 includes the central `EventOrchestrator` required by ADR-021.

At one boundary:

- ambient/minor presentation may coexist,
- at most one major/closure event is selected,
- `SESSION_CLOSURE` outranks checkpoint `MAJOR`.

The final checkpoint therefore never competes visually with Expedition
completion on the same accepted review.

## Target sizing

Initial implementation policy:

```text
target = min(50, currently available review actions)
```

This remains provisional. Locked constraints are positive target, bounded
target, and no silent target growth after creation.

## Queue exhaustion

Natural queue exhaustion before the fixed target closes the route truthfully.
The target is not rewritten. Completion copy explains that available work ended.
Undo can reopen the Expedition if host truth changes.

## Focus Mode and Reduced Motion

Focus Mode keeps bounded progress, numeric meaning, and core actions while
reducing ambient geometry and presentation weight. Domain behavior is identical.

Both explicit Anki Alive reduced-motion policy and `prefers-reduced-motion` are
respected. Meaning never depends on animation order.

## Accessibility

Implemented before host validation:

- native keyboard-reachable buttons,
- visible `:focus-visible`,
- numeric progress plus route geometry,
- `role="progressbar"` with ARIA values,
- non-color checkpoint state labels,
- `aria-live` checkpoint feedback,
- pointer-transparent reviewer strip,
- Escape hides the dedicated Today window without destroying its WebView.

Real desktop keyboard behavior still requires host validation.

## Contrast and visual isolation

Dark-mode Expedition amber remains restrained. Light mode uses the darker
Expedition amber `#80612c` for readable small text.

The dedicated Today window uses `today.css` for its canvas, which prevents an
installed Deck Browser skin from becoming the accidental background of the
Anki Alive visual system. The Today root now uses border-box sizing and a hard
100% maximum width so its own padding cannot create horizontal overflow.

## Performance approach

Reviewer UI updates:

- no collection-wide scan,
- compact sidecar lookup,
- presentation work scheduled after the review event,
- one small DOM update call,
- transform-based progress,
- no JavaScript animation loop,
- no canvas/WebGL/particle system.

Measured reviewer overhead remains a real-host validation item.

## Automated-validation status

Automated coverage includes:

- all four grades counting equally,
- duplicate suppression,
- checkpoint/completion uniqueness,
- undo reopening,
- bounded target planning,
- durable completion presentation,
- natural queue exhaustion,
- Focus Mode,
- quiet reviewer CSS/JS constraints,
- dedicated Today rendering,
- non-review WebViews remaining unmodified,
- toolbar entry opening Today,
- toolbar suppression during active review,
- completion reopening the dedicated Today surface,
- responsive Today breakpoint reachability,
- Today root overflow guard,
- single-document Today reuse and delayed prewarm wiring,
- collection-independent hidden Today prewarm.

Latest latency/overflow patch CI evidence:

```text
GitHub Actions workflow: Anki Alive CI
Probe run: #118
Validated main snapshot: d4662fdc565357ca6d63c5bd493b38b6db5b0cf1
Python 3.9 core-tests: PASS
Python 3.13 core-tests: PASS
Probe merged: no
```

The probe branch differed from the tested `main` snapshot only by a disposable
text sentinel and was closed without merge. Automated validation is therefore
PASS for the current Today reuse/prewarm and overflow implementation. Real-host
perceived latency and layout still require desktop re-validation.

## Pre-host review status

Overall status: NEEDS HOST RE-VALIDATION

The real-host run has already exposed and driven fixes for Deck Browser conflict,
Today overflow, and perceived Today opening latency. After the latest patch,
verify:

- Onigiri/default Deck Browser is visually and functionally untouched,
- `Alive` or `Tools > Anki Alive Today` opens the dedicated Today window,
- Today reopens without a multi-second wait,
- no horizontal scrollbar appears at normal or narrow widths,
- Today dark/light presentation is coherent in its own window,
- Begin/Resume hides Today and enters normal review,
- reviewer strip remains calm and does not cover recall-critical content,
- completion opens the dedicated Today summary,
- keyboard, Focus Mode, reduced motion, restart recovery, queue exhaustion,
  filtered/custom study, and reviewer performance still pass.

Use `docs/PHASE1_MANUAL_VALIDATION.md` for the final real-host run. Phase 1 is
not complete until that evidence is recorded and the handoff is created.
