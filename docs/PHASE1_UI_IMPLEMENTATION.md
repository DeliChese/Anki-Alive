# Phase 1 Expedition UI Implementation Notes

Status: IN PROGRESS
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

Host surface:

- Anki Deck Browser WebView is augmented rather than replaced.
- Normal Anki deck navigation remains intact if Anki Alive presentation fails.

Canonical components:

- `AA-MemoryCore`
- `AA-ExpeditionTrack`
- `AA-CheckpointNode`
- shared button, section, empty-state anatomy

Primary task:

- begin or resume one bounded Expedition.

Memory Core policy:

- Phase 1 displays only the current real Anki due queue for the selected study
  context.
- It does not infer memory health, stability, fragility, or other Memory Engine
  meaning that Phase 1 cannot support yet.
- No generated artwork is a structural dependency.

Today's Signals policy:

- the shell is present,
- no Oracle/Rescue/Nemesis/Fragment/Relic counts are fabricated,
- an empty quiet state is shown when no implemented signal exists.

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
- no secondary feature dashboard,
- card remains visually dominant.

Checkpoint feedback is a small non-blocking status cue after a real checkpoint
transition.

### Completion

Completion is moved out of active recall and back to the Deck Browser Today
surface.

Reasons:

- protect recall from a completion overlay appearing over the next question,
- provide real session closure,
- make `Done` visually primary,
- keep `Continue reviewing` explicit and secondary,
- avoid immediately manufacturing another Expedition.

## Expedition visual DNA

Applied identity:

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

The implementation reuses these catalog IDs:

- `AA-FadeRise-01` for normal Today entrance
- `AA-Press-01` for button press
- `AA-ProgressFlow-01` for real progress changes
- `AA-CheckpointActivate-01` for checkpoint state
- `AA-ExpeditionComplete-01` for closure semantics

No new effect ID is introduced.

## Event orchestration

Phase 1 now includes the small central `EventOrchestrator` required by
ADR-021.

At one review boundary:

- ambient/minor presentation may coexist,
- at most one major/closure event is selected,
- `SESSION_CLOSURE` outranks a checkpoint `MAJOR` event.

This specifically prevents the final checkpoint and Expedition completion from
both presenting prominently on the same accepted review.

## Target sizing

Initial implementation policy:

```text
target = min(50, currently available review actions)
```

This remains PROVISIONAL implementation policy, not a newly locked product
formula.

Constraints that remain locked:

- target is positive,
- target is clamped to currently visible work,
- target never silently grows after creation.

## Focus Mode

Focus Mode keeps:

- bounded progress,
- route meaning,
- current numeric progress,
- core actions.

It reduces:

- ambient Memory Core geometry,
- glow,
- expressive transition,
- reviewer strip width and visual weight.

Domain behavior is unchanged.

## Reduced Motion

Both explicit Anki Alive reduced-motion setting and
`prefers-reduced-motion` are respected.

Fallbacks use:

- static state,
- instant progress geometry,
- opacity-only or effectively instant transitions.

No information depends on animation order.

## Accessibility

Implemented in this slice:

- native keyboard-reachable buttons,
- visible `:focus-visible` treatment,
- numeric progress in addition to route geometry,
- `role="progressbar"` and ARIA values,
- non-color checkpoint labels/state,
- `aria-live` checkpoint feedback,
- pointer-transparent reviewer strip.

Real desktop keyboard and screen-reader-adjacent behavior still requires host
validation.

## Performance approach

Reviewer UI updates:

- do not query collection-wide state,
- read compact sidecar Expedition state,
- schedule presentation work onto the Qt event loop after the review event,
- update a tiny existing DOM strip through one JS call,
- use no JavaScript animation loop,
- use transform for reviewer progress,
- use no canvas/WebGL/particle system.

Measured Phase 1 reviewer overhead remains a manual-host validation item.

## Data hygiene

`user_files/anki_alive.sqlite3` is local user state and must not be committed.
The repository ignores local SQLite sidecar files while preserving
`user_files/README.txt`.

## Pre-host UI review

Overall status: NEEDS HOST INSPECTION

No known canonical blocker is intentionally accepted in code.

Still required before visual acceptance:

- real Anki screenshot inspection,
- narrow-window inspection,
- Focus Mode host inspection,
- Reduced Motion host inspection,
- keyboard path host inspection,
- reviewer overlap check against real card layouts,
- performance measurement,
- completion/continue flow validation.

The final Phase 1 handoff must record these results rather than claiming them in
advance.
