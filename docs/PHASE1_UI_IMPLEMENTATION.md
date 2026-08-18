# Phase 1 Expedition UI Implementation Notes

Status: PRE-HOST VALIDATION
Phase: 1
Feature: Expedition
Canonical art direction: Arcane Memory Interface

## Purpose

This note records the Phase 1 UI implementation decisions that must survive
outside chat history. It is not the final Phase 1 handoff.

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

## UI slice

### Today

The Anki Deck Browser WebView is augmented rather than replaced. Normal Anki
navigation remains available if Anki Alive presentation fails.

Canonical components:

- `AA-MemoryCore`
- `AA-ExpeditionTrack`
- `AA-CheckpointNode`
- shared button, section, and empty-state anatomy

Memory Core uses only the current real Anki review queue in Phase 1. It does not
invent stability, fragility, health, or other Memory Engine meaning that does
not yet exist.

Today's Signals renders a truthful empty state. No Oracle, Rescue, Nemesis,
Fragment, Relic, or World signal is fabricated before its phase exists.

### Reviewer

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

### Completion

Completion leaves active recall and returns to the Deck Browser Today surface.

Reasons:

- no closure overlay on top of the next question,
- `Done` is psychologically primary,
- `Continue reviewing` is explicit and secondary,
- completion does not manufacture another mandatory Expedition.

Completion presentation state is durable and separate from Expedition domain
state. A pending completion summary survives restart until dismissed. If undo
reconciliation reopens the Expedition, the stale completion presentation is
invalidated.

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

Phase 1 includes the small central `EventOrchestrator` required by ADR-021.

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

This remains PROVISIONAL implementation policy, not a locked product formula.
The locked constraints remain: positive target, bounded target, and no silent
target growth after creation.

## Queue exhaustion

A route may run out of eligible Anki reviews before reaching its fixed target.
The implementation distinguishes this from a manual exit using Anki's reviewer
lifecycle:

- leaving review while a card still exists -> PAUSED,
- reviewer cleanup after Anki has no next card -> COMPLETED due to queue exhaustion.

The planned target does not change. If an Expedition planned for 50 reviews
closes after 43 because Anki has no eligible review left, durable state remains:

```text
target_reviews = 50
completed_reviews = 43
status = COMPLETED
```

The completion copy explains the reason instead of pretending that the target
was 43. Undo may make work eligible again; reconciliation can reopen the
Expedition and invalidates stale completion presentation.

## Focus Mode and Reduced Motion

Focus Mode keeps bounded progress, numeric meaning, and core actions while
reducing ambient Memory Core geometry, glow, expressive transition, and reviewer
strip weight. Domain behavior is identical.

Both the explicit Anki Alive reduced-motion setting and
`prefers-reduced-motion` are respected. Meaning never depends on animation
order.

## Accessibility

Implemented before host validation:

- native keyboard-reachable buttons,
- visible `:focus-visible`,
- numeric progress plus route geometry,
- `role="progressbar"` with ARIA values,
- non-color checkpoint state labels,
- `aria-live` checkpoint feedback,
- pointer-transparent reviewer strip.

Real desktop keyboard and screen-reader-adjacent behavior still requires host
validation.

## Contrast audit

Dark-mode Expedition amber on the main dark surface is comfortably readable.
The original amber was too light for small text on the light surface, so light
mode now uses a darker Expedition amber (`#80612c`) while preserving the same
semantic family. The revised small-text contrast is above the intended readable
threshold on the light surfaces used by Phase 1.

## Performance approach

Reviewer UI updates:

- no collection-wide scan,
- compact sidecar Expedition lookup,
- presentation work scheduled after the review event,
- one small DOM update call,
- transform-based progress,
- no JavaScript animation loop,
- no canvas/WebGL/particle system.

Measured Phase 1 reviewer overhead remains a real-host validation item.

## Data hygiene

Local sidecar SQLite files under `user_files/` are ignored by Git while
`user_files/README.txt` remains tracked.

## Automated-validation status

Automated test coverage has been added for:

- all four grades counting equally,
- duplicate review suppression,
- checkpoint transition uniqueness,
- completion uniqueness,
- undo reopening,
- one resumable Expedition per profile,
- bounded target planning,
- EventOrchestrator prominence/dedupe,
- Today and reviewer projections,
- Focus Mode command path,
- durable completion presentation after reopen,
- stale completion invalidation after undo,
- manual reviewer exit -> pause,
- natural queue exhaustion -> truthful early closure,
- quiet reviewer CSS/JS constraints.

GitHub Actions is configured for pushes to `main` on Python 3.9 and 3.13.
The available connector does not expose push-triggered workflow runs for these
commits, and the execution sandbox cannot resolve github.com for a local clone.
Therefore this note does not claim CI PASS.

## Pre-host UI review

Overall status: NEEDS HOST INSPECTION

No known canonical design blocker is intentionally accepted in code.

Still required before visual acceptance:

- real Anki screenshot inspection,
- dark and light mode inspection,
- narrow-window inspection,
- Focus Mode inspection,
- Reduced Motion inspection,
- keyboard path inspection,
- reviewer overlap check against real card layouts,
- performance measurement,
- completion/restart/continue flow validation,
- filtered deck/custom study smoke test.

Use `docs/PHASE1_MANUAL_VALIDATION.md` for the host run. The final Phase 1
handoff must record actual evidence rather than claiming it in advance.
