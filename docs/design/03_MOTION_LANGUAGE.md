# Anki Alive — Motion Language

Status: CANONICAL
Pack: 3
Applies to: all UI motion, transitions, state changes, event reveals, interaction feedback, animated typography, ambient motion, and AI-authored frontend animation
Art Direction: Arcane Memory Interface
Depends on: `00_VISUAL_CONSTITUTION.md`, `01_COLOR_AND_SURFACE_DNA.md`, `02_TYPOGRAPHY_AND_INFORMATION_HIERARCHY.md`, `02_DESIGN_SYSTEM.md`

---

## 1. Purpose

This document defines the motion language of Anki Alive.

Its purpose is to ensure that motion remains:

- meaningful,
- restrained,
- smooth,
- consistent,
- accessible,
- performant,
- respectful of recall.

Motion is part of the product language.

It is not decorative seasoning.

Anki Alive should never rely on an individual contributor's taste to decide how components move.

AI agents must use the approved motion vocabulary and intensity rules in this document.

---

# 2. Motion North Star

Anki Alive motion should feel like:

> **Quiet instruments resolving into state.**

The product should move with:

```text
clarity
+
precision
+
restraint
+
semantic intent
+
controlled atmosphere
```

Motion should not feel:

- bouncy,
- toy-like,
- springy for its own sake,
- arcade-like,
- flashy,
- chaotic,
- over-choreographed,
- constantly alive.

The interface should feel stable first, animated second.

---

# 3. Core Motion Principles

## M01 — Motion Must Explain Change

Every animation should answer:

> What changed, and why is movement useful here?

Good reasons include:

- reveal,
- transition,
- progress,
- causality,
- completion,
- state resolution,
- spatial continuity.

Bad reason:

> Animation makes it feel premium.

---

## M02 — Recall Has Priority

During active recall:

> motion must become quiet.

The learner should not need to suppress the interface mentally in order to answer.

---

## M03 — Quiet by Default

Most UI elements should be static when nothing meaningful is happening.

Continuous motion must be rare and justified.

---

## M04 — Meaning Earns Spectacle

Stronger motion is reserved for stronger semantic events.

A normal card transition should not move like a Relic formation.

---

## M05 — Motion Must Resolve

An animation should settle into a stable state.

Avoid perpetual movement.

The interface should repeatedly return to calm.

---

## M06 — Motion Must Degrade Gracefully

Every meaningful motion pattern must define:

- reduced-motion fallback,
- Focus Mode behavior,
- no-animation state where practical.

---

# 4. Motion Intensity Tiers

All motion belongs to one of four tiers.

```text
M0 — Quiet
M1 — Functional
M2 — Expressive
M3 — Cinematic
```

AI agents must identify the permitted tier before implementing an animation.

---

# 5. M0 — Quiet

Use during:

- reviewer question state,
- Focus Mode,
- high-attention learning moments,
- subtle status changes.

Allowed motion:

- opacity fade,
- 1–4 px translation,
- tiny progress interpolation,
- subtle line/value transition,
- short crossfade.

Typical duration:

```text
100–180 ms
```

Typical distance:

```text
0–4 px
```

Glow:

```text
G0–G1 only
```

M0 should be nearly invisible as "animation."

---

# 6. M1 — Functional

Use for:

- panel entrance,
- tab change,
- hover/press,
- drawer open,
- list insertion,
- compact navigation,
- layout continuity,
- normal dashboard interaction.

Allowed motion:

- fade + small translation,
- small scale adjustment,
- layout interpolation,
- restrained stagger,
- progress movement,
- crossfade.

Typical duration:

```text
160–260 ms
```

Typical distance:

```text
4–12 px
```

Scale range:

```text
0.98–1.02
```

M1 should feel polished, not theatrical.

---

# 7. M2 — Expressive

Use for:

- checkpoint arrival,
- Oracle resolution,
- Rescue stabilization,
- Fragment progress,
- meaningful milestone,
- feature event reveal.

Allowed motion:

- staged reveal,
- controlled glow pulse,
- border illumination,
- icon resolution,
- short stagger,
- restrained particle accent if explicitly approved.

Typical duration:

```text
260–420 ms
```

Overall event choreography:

```text
up to ~700 ms
```

M2 must have a clear semantic reason.

---

# 8. M3 — Cinematic

Use only for rare major moments.

Examples:

- major Expedition completion,
- Relic formation,
- major Memory World reveal,
- rare Oracle centerpiece.

Allowed:

- multi-stage choreography,
- larger spatial transition,
- richer light change,
- limited atmospheric animation,
- approved shader/canvas effect.

Typical duration:

```text
450–650 ms
```

Full choreography:

```text
up to ~1200 ms
```

M3 must be explicitly allowed by feature specification.

M3 should generally happen outside active recall.

---

# 9. Reviewer Motion Ceiling

## Question State

Maximum:

```text
M0
```

Allowed:

- tiny progress update,
- subtle fade,
- compact status cue.

Forbidden:

- particles,
- large movement,
- pulse loops,
- glow escalation,
- major reveal,
- text choreography.

---

## Answer State

Maximum:

```text
M1
```

Allowed:

- contextual signal,
- compact state update,
- small progress movement.

Do not flood the answer state.

---

## Post-Grade Boundary

Maximum:

```text
M2
```

Only one meaningful orchestrated event may receive M2 treatment.

If multiple events occur:

- merge,
- queue,
- defer,
- downshift.

---

## Session Closure

M2 is normal.

M3 may be allowed for rare, earned closure moments.

---

# 10. Motion Timing Scale

Canonical timing families:

```text
AA-Time-1
120 ms
micro response

AA-Time-2
180 ms
quiet functional transition

AA-Time-3
220 ms
standard functional transition

AA-Time-4
320 ms
meaningful reveal

AA-Time-5
420 ms
expressive transition

AA-Time-6
600 ms
major transition
```

These are reference values, not arbitrary decoration.

---

# 11. Duration Discipline

Shorter is preferred when meaning remains clear.

Avoid:

- 800 ms panel entrances,
- slow hover transitions,
- long modal openings,
- delayed reviewer feedback.

No normal interaction should feel like the interface is asking the user to wait.

---

# 12. Easing Vocabulary

Approved easing families should remain limited.

## AA-Ease-Standard

Use for:

- normal entrance,
- panel transition,
- state change.

Direction:

```text
cubic-bezier(0.2, 0, 0, 1)
```

Feel:

- smooth,
- direct,
- low drama.

---

## AA-Ease-Exit

Use for:

- disappearance,
- dismissal,
- compact exits.

Direction:

```text
cubic-bezier(0.4, 0, 1, 1)
```

Exit should generally be slightly faster than entrance.

---

## AA-Ease-Emphasized

Use for:

- meaningful reveal,
- major state resolve.

Direction:

```text
cubic-bezier(0.2, 0.8, 0.2, 1)
```

Use sparingly.

---

# 13. Easing Prohibitions

Avoid:

- elastic easing,
- back easing with visible overshoot,
- exaggerated bounce,
- playful spring oscillation,
- cartoon physics.

Anki Alive should not wobble.

---

# 14. Spring Rule

Springs are optional, not default.

A spring may be used only if it improves:

- direct manipulation,
- drag settling,
- physical continuity.

Spring behavior should be:

- critically damped or near-critically damped,
- low overshoot,
- short settling time.

Avoid visible oscillation.

---

# 15. Spatial Motion Rules

Movement should preserve spatial meaning.

Preferred directions:

```text
downstream / forward
→ Expedition progress

radial / inward
→ Oracle lock

converging
→ Fragment assembly

stabilizing / centering
→ Rescue

compression / release
→ Nemesis

settling / anchoring
→ Relic
```

Do not move components randomly.

---

# 16. Distance Limits

Normal UI movement:

```text
2–12 px
```

Large panel transitions:

```text
up to ~24 px
```

Major event movement:

```text
up to ~48 px
```

Larger motion requires explicit M3 justification.

---

# 17. Scale Rules

Scale is a subtle tool.

Allowed normal scale ranges:

```text
0.98 → 1.00
1.00 → 1.02
```

Major reveal may use:

```text
0.96 → 1.00
```

Avoid:

- 0.8 → 1.0 pop-ins,
- large zoom effects,
- pulsing scale loops.

---

# 18. Opacity Rules

Opacity is the primary motion companion.

Preferred:

- fade in,
- fade out,
- crossfade,
- glow decay.

Opacity should not make text unreadable during transition.

---

# 19. Blur Motion Rule

Animated blur is allowed rarely.

Use for:

- Oracle reveal,
- atmospheric event focus,
- very rare depth transition.

Avoid blur during reviewer question state.

Reduced Motion fallback:

```text
opacity only
```

---

# 20. Glow Motion Rule

Glow may animate when representing:

- activation,
- lock,
- resonance,
- stabilization,
- completion.

Glow motion should:

- rise quickly,
- peak briefly,
- settle.

Avoid infinite pulse loops.

---

# 21. Pulse Rule

Pulse is allowed only for semantic signal.

Good:

- Rescue signal briefly pulsing when newly active,
- Oracle lock confirmation,
- current Expedition node becoming active.

Bad:

- every icon pulsing forever.

A pulse should usually run:

```text
1–2 cycles maximum
```

---

# 22. Hover Motion

Hover should be M0 or M1.

Approved behavior:

- 1–2 px lift,
- tiny value change,
- subtle border emphasis,
- tiny shadow increase.

Duration:

```text
120–180 ms
```

Avoid:

- large scaling,
- rotating icons,
- glow bursts,
- strong parallax.

---

# 23. Press Motion

Press should feel immediate.

Approved:

```text
scale 1.00 → 0.99
or
translateY 0 → 1 px
```

Duration:

```text
80–120 ms
```

No bounce after release.

---

# 24. Focus Motion

Keyboard focus should not rely on animation.

Use:

- visible focus ring,
- static contrast,
- optional short fade.

Focus clarity is more important than motion.

---

# 25. Entrance Motion

Default entrance recipe:

```text
opacity 0 → 1
translateY 6 px → 0
duration 180–220 ms
AA-Ease-Standard
```

This should become the baseline for many normal surfaces.

Future canonical ID:

```text
AA-FadeRise-01
```

---

# 26. Exit Motion

Default exit recipe:

```text
opacity 1 → 0
translateY 0 → -2 px
duration 120–180 ms
AA-Ease-Exit
```

Exit should not linger.

---

# 27. Crossfade Rule

Use crossfade for:

- compact content replacement,
- status change,
- tab content,
- metric value update.

Avoid crossfading large layouts when spatial continuity would be clearer.

---

# 28. Layout Transition Rule

Layout transitions should preserve orientation.

Use when:

- panel expands,
- list item appears,
- compact section changes size.

Avoid dramatic reflow.

The learner should understand where content moved.

---

# 29. Stagger Rule

Stagger is allowed for grouped reveal.

Normal stagger:

```text
20–45 ms between items
```

Maximum normal group:

```text
4–6 items
```

Avoid cascading 20-item lists.

Stagger should create rhythm, not delay.

---

# 30. Progress Motion

Progress motion should reflect real state change.

Good:

- Expedition path advances,
- checkpoint fills,
- Rescue stabilizes,
- Fragment assembly progresses.

Duration:

```text
180–320 ms
```

Do not fake progress.

Do not interpolate a value that did not actually change.

---

# 31. Number Motion

Numbers may animate only when meaningful.

Allowed:

- short interpolation,
- opacity crossfade,
- digit transition.

Avoid slot-machine behavior.

Future ID:

```text
AA-NumberFlow-01
```

Reduced Motion:

```text
instant replacement
or
short fade
```

---

# 32. Status Transition

Status change should be compact.

Example:

```text
Fragile
→
Stabilizing
→
Stable
```

Use:

- crossfade,
- icon state change,
- small color transition,
- local line/glow change.

Avoid large modal transitions for normal status updates.

---

# 33. Event Choreography Structure

A meaningful event should usually follow:

```text
1. Signal
2. Resolve
3. Confirm
4. Settle
```

Example:

```text
border brightens
→ icon resolves
→ label appears
→ glow decays
```

This structure prevents effect soup.

---

# 34. Milestone Choreography

Canonical milestone rhythm:

```text
Stage 1
edge illumination

Stage 2
symbol resolve

Stage 3
copy reveal

Stage 4
settle into static state
```

Future ID family:

```text
AA-Milestone-01
AA-Milestone-02
```

---

# 35. Expedition Motion DNA

Preferred verbs:

- advance,
- arrive,
- illuminate,
- connect,
- settle.

Preferred motion:

- path progression,
- node activation,
- forward reveal.

Avoid:

- racing,
- speed lines,
- bouncing markers.

---

# 36. Oracle Motion DNA

Preferred verbs:

- align,
- focus,
- lock,
- resolve,
- reveal.

Preferred motion:

- radial convergence,
- iris-like resolution,
- orbit slowdown,
- subtle blur clear.

Avoid:

- magic wheel spin,
- fortune-teller flourish,
- endless rotating rings.

---

# 37. Rescue Motion DNA

Preferred verbs:

- stabilize,
- reconnect,
- calm,
- anchor.

Preferred motion:

- pulse decay,
- broken arc reconnecting,
- waveform settling.

Avoid:

- alarm flashing,
- heartbeat panic animation,
- red shake.

---

# 38. Nemesis Motion DNA

Preferred verbs:

- compress,
- resist,
- fracture,
- weaken,
- release.

Preferred motion:

- controlled tension,
- subtle angular shift,
- fracture line resolving.

Avoid:

- screen shake,
- violent impact,
- boss battle effects.

---

# 39. Fragment Motion DNA

Preferred verbs:

- resonate,
- assemble,
- converge,
- unlock.

Preferred motion:

- shard alignment,
- geometric assembly,
- restrained light convergence.

Avoid:

- loot-box opening,
- random sparkle shower.

---

# 40. Relic Motion DNA

Preferred verbs:

- awaken,
- stabilize,
- fracture,
- restore,
- preserve.

Preferred motion:

- slow light emergence,
- mineral vein illumination,
- fracture seam resolve.

Avoid:

- treasure-item spin,
- rarity burst,
- floating collectible bounce.

---

# 41. Memory World Motion DNA

Preferred verbs:

- drift,
- reveal,
- pan,
- settle,
- beacon.

Preferred motion:

- slow atmospheric parallax outside recall,
- map region transition,
- beacon pulse.

Avoid:

- constant camera movement,
- strategy-game map animation,
- decorative cloud loops everywhere.

---

# 42. Ambient Motion Rule

Ambient motion must be:

- slow,
- low amplitude,
- nonessential,
- suppressible.

Allowed examples:

- faint star drift,
- subtle map atmosphere,
- very slow luminous breathing.

Ambient motion must never run during active recall unless nearly imperceptible.

---

# 43. Ambient Motion Budget

A normal screen should have:

```text
0–1 ambient motion system
```

Do not layer multiple continuous systems.

---

# 44. Particle Rule

Particles are not a default design primitive.

Allowed only for:

- rare M2/M3 event,
- low count,
- short duration,
- semantic purpose.

Forbidden:

- persistent particles during review,
- confetti,
- reward showers,
- random sparkles.

---

# 45. Parallax Rule

Parallax is allowed only outside active recall.

Use:

- subtle,
- low depth,
- slow movement,
- optional.

Avoid exaggerated depth.

Reduced Motion:

```text
static composition
```

---

# 46. Loop Rule

Continuous loops are discouraged.

A loop may exist only if:

1. it communicates ongoing state,
2. it is low intensity,
3. it can be suppressed,
4. it does not compete with reading.

Examples:

- very subtle Oracle waiting indicator,
- dormant beacon.

Avoid decorative loops.

---

# 47. Loading Motion

Loading indicators should remain quiet.

Preferred:

- subtle progress line,
- small spinner,
- soft skeleton fade.

Avoid:

- flashy branded loaders,
- full-screen animation,
- long blocking sequences.

Loading must never pretend progress if none is known.

---

# 48. Empty State Motion

Empty states should usually remain static.

Optional:

- single subtle entrance,
- tiny ambient illustration movement outside recall.

Do not make empty states perform.

---

# 49. Error Motion

Errors should be clear, not dramatic.

Allowed:

- short emphasis,
- border/state change,
- optional tiny horizontal shift if necessary.

Avoid screen shake.

---

# 50. Motion & Sound

If sound is ever added:

- motion and sound should resolve together,
- sound must remain optional,
- no arcade reward synchronization.

Motion must stand on its own without audio.

---

# 51. Focus Mode Motion Rules

Focus Mode defaults to:

```text
M0
+
essential M1
```

Focus Mode should suppress:

- M2 flourish,
- M3 cinematic events,
- ambient loops,
- decorative particles,
- parallax,
- repeated pulses.

Meaningful events may be represented through:

- static highlight,
- short fade,
- compact label.

---

# 52. Reduced Motion Rules

When `prefers-reduced-motion` or equivalent is active:

Replace:

```text
translation
→ opacity

scale
→ opacity/value change

parallax
→ static

particle reveal
→ static highlight

multi-stage choreography
→ immediate resolved state + short fade
```

The state change must remain understandable.

---

# 53. No-Motion Integrity Rule

Every interaction should still make sense with motion disabled.

No core meaning may depend on:

- direction of movement,
- animation order,
- timing alone.

Motion enhances understanding.

It does not own understanding.

---

# 54. Performance Rule

The reviewer hot path is sacred.

Avoid:

- expensive layout thrashing,
- large blur animations,
- unnecessary JavaScript animation loops,
- high particle counts,
- canvas/WebGL during review,
- frequent large DOM reflow.

Prefer:

- transform,
- opacity,
- composited properties,
- native CSS/WAAPI where sufficient.

---

# 55. Dependency Rule

Do not add a motion library merely for one animation.

Before adding a dependency, verify:

1. native CSS/WAAPI is insufficient,
2. the library solves repeated real needs,
3. bundle/runtime cost is acceptable,
4. Anki WebView compatibility is acceptable,
5. reduced-motion support is possible,
6. maintenance risk is acceptable.

---

# 56. Reference Libraries

External libraries may be studied for patterns, not copied blindly.

Useful reference families may include:

- Motion,
- Anime.js,
- AutoAnimate,
- Motion Primitives,
- Codrops experiments.

Anki Alive should extract principles and approved patterns rather than import an effect zoo.

---

# 57. Canonical Motion Primitive IDs

Future Effects Catalog should define stable IDs.

Initial expected families:

```text
AA-FadeRise-01
AA-Fade-01
AA-Crossfade-01
AA-HoverLift-01
AA-Press-01
AA-ProgressFlow-01
AA-NumberFlow-01
AA-StatusCrossfade-01
AA-GlowResolve-01
AA-Milestone-01
AA-OracleReveal-01
AA-RescueStabilize-01
AA-FragmentAssemble-01
AA-RelicAwaken-01
```

Agents should reuse these instead of inventing local animations.

---

# 58. Motion Primitive Documentation Format

Every approved primitive must define:

```text
ID
Purpose
Motion tier
Trigger
Duration
Easing
Transform
Opacity
Glow behavior
Allowed contexts
Forbidden contexts
Focus Mode fallback
Reduced Motion fallback
Performance notes
```

---

# 59. AI Motion Implementation Rule

Before implementing motion, an AI agent must identify:

```text
1. Semantic event
2. Motion tier
3. Approved primitive ID
4. Trigger
5. Duration
6. Easing
7. Spatial meaning
8. Focus Mode behavior
9. Reduced Motion fallback
10. Performance implications
```

If no approved primitive fits, the agent should propose a new primitive rather than silently invent one.

---

# 60. AI Motion Failure Patterns

Reject or revise motion containing:

- bounce-heavy easing,
- elastic overshoot,
- permanent pulses,
- screen shake,
- large zooms,
- excessive stagger,
- random rotation,
- particle spam,
- long blocking sequences,
- motion during active recall,
- multiple competing animations,
- animation with no semantic reason.

---

# 61. One-Motion-Story Rule

A component should generally tell one motion story.

Good:

```text
fade + rise
```

Good:

```text
border illuminate + symbol resolve
```

Bad:

```text
fade
+ scale
+ rotate
+ blur
+ glow
+ bounce
```

unless explicitly designed as rare M3 choreography.

---

# 62. Motion Density Rule

A screen should not contain many simultaneously animated components.

Default:

```text
one primary motion focus
+
small supporting transitions
```

The learner should always know where to look.

---

# 63. Motion Sequencing Rule

If multiple transitions are required:

1. prioritize semantic order,
2. shorten the sequence,
3. avoid unnecessary waiting,
4. settle quickly.

Do not animate because choreography is visually impressive.

---

# 64. Event Interruption Rule

No animation may prevent the learner from:

- answering,
- dismissing,
- continuing,
- stopping study.

If an event must block interaction, the reason must be explicit and rare.

---

# 65. Completion Rule

Completion motion should:

```text
rise
→ resolve
→ settle
```

Not:

```text
explode
→ loop
→ prompt another task
```

Celebration should end in calm.

---

# 66. Long-Term Familiarity Rule

Ask:

> Will this motion still feel tasteful after the user sees it hundreds of times?

If not:

- reduce frequency,
- reduce amplitude,
- downgrade tier,
- reserve it for rarer states.

---

# 67. AI Motion Review Checklist

Before shipping a motion-enabled UI, verify:

1. Does each animation communicate meaning?
2. Is the motion tier appropriate?
3. Does recall remain visually dominant?
4. Is there only one primary motion focus?
5. Does the animation resolve into calm?
6. Is the duration short enough?
7. Is easing restrained?
8. Is any loop truly necessary?
9. Does Focus Mode reduce the motion correctly?
10. Does Reduced Motion preserve meaning?
11. Is the reviewer hot path safe?
12. Would this still feel tasteful after daily use for one year?

---

# 68. Canonical Conflict Resolution

When motion rules conflict:

```text
Product Principles
↓
Visual Constitution
↓
Motion Language
↓
Design System
↓
Feature Spec
↓
Effects Catalog
↓
Component implementation
```

The higher-level rule wins.

---

# 69. Final Motion Principle

When uncertain, ask:

> **Does this movement make the state easier to understand, or is the interface merely performing?**

Choose the motion that supports understanding.

And when two valid motions exist:

> **Choose the shorter, quieter, better-settled one.**

---

# Motion North Star

> **Meaning moves. Everything else stays still.**
