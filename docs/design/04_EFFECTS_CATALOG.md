# Anki Alive — Effects Catalog

Status: CANONICAL
Pack: 4
Applies to: approved UI effects, motion primitives, state transitions, feature reveals, interaction feedback, and AI-authored frontend animation
Art Direction: Arcane Memory Interface
Depends on: `00_VISUAL_CONSTITUTION.md`, `01_COLOR_AND_SURFACE_DNA.md`, `02_TYPOGRAPHY_AND_INFORMATION_HIERARCHY.md`, `03_MOTION_LANGUAGE.md`, `02_DESIGN_SYSTEM.md`

---

## 1. Purpose

This catalog defines approved visual and motion effects for Anki Alive.

Its purpose is to prevent uncontrolled visual invention by contributors and AI agents.

All production UI should reuse approved effect IDs where practical.

If no approved effect fits, an agent should propose a new catalog entry rather than inventing a local animation silently.

---

# 2. Catalog Rules

Every effect must have:

```text
ID
Purpose
Motion tier
Trigger
Duration
Easing
Visual recipe
Allowed contexts
Forbidden contexts
Focus Mode fallback
Reduced Motion fallback
Performance notes
```

Agents should reference IDs directly in implementation plans and feature specs.

Example:

```text
Expedition checkpoint completion
→ AA-Milestone-01
```

---

# 3. Core Utility Effects

## AA-Fade-01

Purpose:

- quiet appearance/disappearance,
- compact state change,
- low-attention transitions.

Motion tier:

```text
M0
```

Trigger:

- visibility change,
- small content replacement.

Duration:

```text
120–180 ms
```

Easing:

```text
AA-Ease-Standard
```

Visual recipe:

```text
opacity 0 → 1
```

Allowed:

- reviewer question state,
- Focus Mode,
- labels,
- small panels,
- status cues.

Forbidden:

- major milestone by itself,
- dramatic event reveal.

Focus Mode:

```text
unchanged
```

Reduced Motion:

```text
instant or 100 ms fade
```

Performance:

- opacity only,
- preferred for hot paths.

---

## AA-FadeRise-01

Purpose:

- default panel/component entrance.

Motion tier:

```text
M1
```

Duration:

```text
180–220 ms
```

Easing:

```text
AA-Ease-Standard
```

Visual recipe:

```text
opacity 0 → 1
translateY 6 px → 0
```

Allowed:

- panels,
- cards,
- dashboard regions,
- signal rows,
- empty states.

Forbidden:

- repeated reviewer motion,
- long staggered lists.

Focus Mode:

```text
reduce translateY to 2 px
```

Reduced Motion:

```text
opacity only
```

Performance:

- transform + opacity only.

---

## AA-Crossfade-01

Purpose:

- state replacement without spatial change.

Motion tier:

```text
M0–M1
```

Duration:

```text
140–220 ms
```

Visual recipe:

```text
old opacity 1 → 0
new opacity 0 → 1
```

Allowed:

- status text,
- tab content,
- number label,
- compact feature state.

Forbidden:

- large page transitions.

Focus Mode:

```text
unchanged
```

Reduced Motion:

```text
instant replacement
```

---

# 4. Interaction Effects

## AA-HoverLift-01

Purpose:

- indicate interactivity on desktop.

Motion tier:

```text
M1
```

Duration:

```text
120–160 ms
```

Visual recipe:

```text
translateY 0 → -2 px
shadow S0/S1 → S1/S2
line.default → line.strong
```

Allowed:

- clickable cards,
- secondary panels,
- navigation tiles.

Forbidden:

- reviewer answer buttons if it distracts,
- passive surfaces,
- every list row.

Focus Mode:

```text
translateY 0 → -1 px
no glow
```

Reduced Motion:

```text
border/value change only
```

---

## AA-Press-01

Purpose:

- tactile button/card press.

Motion tier:

```text
M0
```

Duration:

```text
80–120 ms
```

Visual recipe:

```text
scale 1 → 0.99
or
translateY 0 → 1 px
```

Allowed:

- buttons,
- compact actionable tiles.

Forbidden:

- decorative elements.

Reduced Motion:

```text
value change only
```

---

## AA-FocusRing-01

Purpose:

- keyboard focus visibility.

Motion tier:

```text
M0
```

Visual recipe:

```text
static high-contrast focus ring
optional 100 ms opacity entrance
```

Allowed:

- all keyboard-focusable controls.

Forbidden:

- hidden focus styling.

Focus Mode:

```text
unchanged
```

Reduced Motion:

```text
static
```

Accessibility:

- mandatory where relevant.

---

# 5. Progress Effects

## AA-ProgressFlow-01

Purpose:

- communicate real progress movement.

Motion tier:

```text
M1
```

Duration:

```text
180–320 ms
```

Visual recipe:

```text
progress geometry interpolates
local active node accent strengthens briefly
```

Allowed:

- Expedition,
- Fragment assembly,
- compact progress bars.

Forbidden:

- fake progress,
- endless looping progress.

Focus Mode:

```text
shorter duration
no glow
```

Reduced Motion:

```text
instant geometry update
```

Performance:

- transform/width only when layout cost is acceptable.

---

## AA-NumberFlow-01

Purpose:

- meaningful metric update.

Motion tier:

```text
M1
```

Duration:

```text
160–260 ms
```

Visual recipe:

```text
brief interpolation or digit crossfade
```

Allowed:

- progress totals,
- meaningful memory metrics,
- session summaries.

Forbidden:

- every numerical update,
- slot-machine style digits.

Focus Mode:

```text
crossfade only
```

Reduced Motion:

```text
instant replacement
```

---

## AA-CheckpointActivate-01

Purpose:

- indicate current or newly reached Expedition checkpoint.

Motion tier:

```text
M1–M2
```

Duration:

```text
220–340 ms
```

Visual recipe:

```text
node value rises slightly
border illumination
path connection resolves
glow G1 briefly
```

Allowed:

- Expedition only.

Forbidden:

- generic progress indicators.

Focus Mode:

```text
static node highlight
```

Reduced Motion:

```text
instant active-state change
```

---

# 6. State Effects

## AA-StatusCrossfade-01

Purpose:

- semantic state transition.

Motion tier:

```text
M0–M1
```

Duration:

```text
140–220 ms
```

Visual recipe:

```text
label crossfade
icon morph/crossfade
semantic color transition
```

Allowed:

- Stable / Fragile / Locked / Restoring / Active.

Forbidden:

- dramatic milestones.

Focus Mode:

```text
unchanged
```

Reduced Motion:

```text
instant label + icon change
```

---

## AA-GlowResolve-01

Purpose:

- brief signal confirmation.

Motion tier:

```text
M1–M2
```

Duration:

```text
240–360 ms
```

Visual recipe:

```text
G0/G1 → G2
hold briefly
G2 → G1/G0
```

Allowed:

- lock,
- stabilize,
- resolve,
- current node activation.

Forbidden:

- continuous loop,
- body text.

Focus Mode:

```text
skip to static state
```

Reduced Motion:

```text
static local highlight
```

---

# 7. Milestone Effects

## AA-Milestone-01

Purpose:

- standard meaningful milestone.

Motion tier:

```text
M2
```

Full choreography:

```text
450–650 ms
```

Stages:

```text
1. edge illumination
2. symbol resolve
3. short label reveal
4. glow decay
```

Allowed:

- checkpoint completion,
- Fragment milestone,
- Rescue completion.

Forbidden:

- every review,
- routine card state changes.

Focus Mode:

```text
static emphasized state + short fade
```

Reduced Motion:

```text
instant resolved state + fade
```

---

## AA-Milestone-02

Purpose:

- stronger session-level milestone.

Motion tier:

```text
M2
```

Full choreography:

```text
550–800 ms
```

Visual recipe:

```text
surface emphasis
feature symbol resolve
short supporting copy
controlled local glow
settle
```

Allowed:

- Expedition major checkpoint,
- significant long-term event.

Forbidden:

- reviewer question state.

Focus Mode:

```text
AA-Milestone-01 fallback
```

Reduced Motion:

```text
static event surface
```

---

# 8. Expedition Effects

## AA-ExpeditionAdvance-01

Purpose:

- visual movement along Expedition path.

Motion tier:

```text
M1
```

Duration:

```text
180–300 ms
```

Visual recipe:

```text
path segment illuminates forward
current marker advances or state switches
previous segment settles
```

Allowed:

- Expedition progress only.

Forbidden:

- racing effects,
- speed lines.

Focus Mode:

```text
instant path state + 120 ms fade
```

Reduced Motion:

```text
instant
```

---

## AA-ExpeditionComplete-01

Purpose:

- Expedition closure.

Motion tier:

```text
M2
```

Full choreography:

```text
600–900 ms
```

Stages:

```text
final path resolves
completion node illuminates
title/status appears
surface settles into calm completed state
```

Allowed:

- Expedition completion.

Forbidden:

- immediate mandatory next-task prompt.

Focus Mode:

```text
static completion surface + short fade
```

Reduced Motion:

```text
instant completed state
```

---

# 9. Oracle Effects

## AA-OracleLock-01

Purpose:

- indicate prediction commitment.

Motion tier:

```text
M1
```

Duration:

```text
220–320 ms
```

Visual recipe:

```text
radial marks align
ring contrast increases
small lock/status label resolves
G1 brief local glow
```

Allowed:

- Oracle pre-commit UI outside distracting recall context.

Forbidden:

- hinting card outcome,
- dramatic prediction reveal before answer.

Focus Mode:

```text
static locked icon/state
```

Reduced Motion:

```text
instant lock state
```

---

## AA-OracleReveal-01

Purpose:

- reveal committed Oracle result.

Motion tier:

```text
M2
```

Duration:

```text
300–420 ms
```

Full choreography:

```text
blur/value resolves
radial geometry focuses
result appears
halo decays
```

Allowed:

- post-grade Oracle resolution.

Forbidden:

- active recall,
- repeated loop.

Focus Mode:

```text
AA-StatusCrossfade-01 + static symbol
```

Reduced Motion:

```text
opacity reveal only
```

---

## AA-OracleReveal-02

Purpose:

- rare centerpiece Oracle reveal.

Motion tier:

```text
M3
```

Full choreography:

```text
700–1100 ms
```

Allowed only if:

- feature spec explicitly allows,
- outside active recall,
- event is genuinely rare.

Visual recipe:

```text
radial field aligns
central result resolves
local light expands subtly
copy appears
all motion settles
```

Focus Mode:

```text
AA-OracleReveal-01
```

Reduced Motion:

```text
static result surface
```

---

# 10. Rescue Effects

## AA-RescueSignal-01

Purpose:

- indicate fragile memory needing recovery.

Motion tier:

```text
M1
```

Duration:

```text
220–320 ms
```

Visual recipe:

```text
broken arc becomes visible
one short soft pulse
signal settles
```

Allowed:

- Rescue state entry.

Forbidden:

- panic flashing,
- repeated heartbeat loop.

Focus Mode:

```text
static fragile marker
```

Reduced Motion:

```text
static
```

---

## AA-RescueStabilize-01

Purpose:

- communicate memory recovery.

Motion tier:

```text
M2
```

Duration:

```text
320–460 ms
```

Visual recipe:

```text
pulse amplitude decreases
broken arc reconnects
teal signal settles
local glow decays
```

Allowed:

- successful Rescue resolution.

Forbidden:

- reward spam.

Focus Mode:

```text
status change + static repaired arc
```

Reduced Motion:

```text
instant stable state
```

---

# 11. Nemesis Effects

## AA-NemesisPressure-01

Purpose:

- show active resistance/challenge without aggression.

Motion tier:

```text
M1
```

Duration:

```text
220–320 ms
```

Visual recipe:

```text
angular form compresses slightly
line contrast strengthens
no shake
```

Allowed:

- Nemesis presence/status.

Forbidden:

- screen shake,
- red flashing.

Focus Mode:

```text
static stronger silhouette
```

Reduced Motion:

```text
static
```

---

## AA-NemesisWeaken-01

Purpose:

- show meaningful improvement against Nemesis.

Motion tier:

```text
M2
```

Duration:

```text
320–460 ms
```

Visual recipe:

```text
compressed shape releases slightly
fracture line softens
crimson/violet pressure decreases
```

Allowed:

- real improvement event.

Forbidden:

- every successful review.

Focus Mode:

```text
static state shift
```

Reduced Motion:

```text
instant state shift
```

---

## AA-NemesisDefeat-01

Purpose:

- major Nemesis resolution.

Motion tier:

```text
M2–M3
```

Full choreography:

```text
600–1000 ms
```

Visual recipe:

```text
tension releases
fracture geometry resolves
symbol settles into historical state
copy appears
```

Forbidden:

- explosive boss-death visuals,
- confetti,
- screen shake.

Focus Mode:

```text
AA-Milestone-01
```

Reduced Motion:

```text
static resolved state
```

---

# 12. Fragment Effects

## AA-FragmentResonate-01

Purpose:

- indicate meaningful Fragment progress.

Motion tier:

```text
M1
```

Duration:

```text
200–320 ms
```

Visual recipe:

```text
one shard brightens
neighboring geometry responds subtly
```

Allowed:

- incremental Fragment progress.

Forbidden:

- sparkle spam.

Focus Mode:

```text
static highlight
```

Reduced Motion:

```text
static
```

---

## AA-FragmentAssemble-01

Purpose:

- Fragment assembly milestone.

Motion tier:

```text
M2
```

Duration:

```text
360–520 ms
```

Visual recipe:

```text
2–4 fragments converge
alignment resolves
local prism accent appears
settle
```

Forbidden:

- random particle shower,
- loot-box framing.

Focus Mode:

```text
instant assembled geometry + fade
```

Reduced Motion:

```text
static assembled state
```

---

## AA-FragmentReveal-01

Purpose:

- completed Fragment discovery.

Motion tier:

```text
M2–M3
```

Full choreography:

```text
550–900 ms
```

Visual recipe:

```text
assembly completes
encoded form becomes legible
short discovery copy appears
light decays
```

Allowed:

- rare discovery.

Focus Mode:

```text
AA-Milestone-01
```

Reduced Motion:

```text
static reveal surface
```

---

# 13. Relic Effects

## AA-RelicAwaken-01

Purpose:

- Relic formation or activation.

Motion tier:

```text
M3
```

Full choreography:

```text
700–1100 ms
```

Visual recipe:

```text
artifact silhouette resolves
mineral vein light appears
central form stabilizes
ritual label appears
all glow settles
```

Allowed:

- rare Relic formation.

Forbidden:

- spinning item,
- rarity burst,
- treasure drop.

Focus Mode:

```text
AA-Milestone-02
```

Reduced Motion:

```text
static formed Relic + short fade
```

---

## AA-RelicFracture-01

Purpose:

- communicate real memory fracture without punishment.

Motion tier:

```text
M2
```

Duration:

```text
320–480 ms
```

Visual recipe:

```text
one controlled fracture line appears
light continuity breaks
state settles
```

Forbidden:

- violent shatter,
- red damage explosion.

Focus Mode:

```text
static fracture state
```

Reduced Motion:

```text
instant fracture state
```

---

## AA-RelicRestore-01

Purpose:

- restoration milestone.

Motion tier:

```text
M2–M3
```

Full choreography:

```text
500–850 ms
```

Visual recipe:

```text
fracture seam illuminates
two sides reconnect visually
auric light settles
status becomes restored
```

Focus Mode:

```text
AA-Milestone-01
```

Reduced Motion:

```text
static restored state
```

---

# 14. Memory World Effects

## AA-WorldBeacon-01

Purpose:

- quiet active location signal.

Motion tier:

```text
M0–M1
```

Visual recipe:

```text
one subtle luminance pulse
long pause
```

Loop:

```text
maximum low-frequency loop if truly needed
```

Allowed:

- non-review Memory World.

Forbidden:

- multiple beacons pulsing simultaneously.

Focus Mode:

```text
static beacon
```

Reduced Motion:

```text
static
```

---

## AA-WorldRegionReveal-01

Purpose:

- reveal newly meaningful region.

Motion tier:

```text
M2
```

Duration:

```text
360–520 ms
```

Visual recipe:

```text
region opacity/value resolves
boundary appears
one beacon activates
```

Allowed:

- Memory World progression.

Forbidden:

- dramatic camera flythrough by default.

Focus Mode:

```text
static reveal
```

Reduced Motion:

```text
instant
```

---

## AA-WorldTransition-01

Purpose:

- move between map regions while preserving orientation.

Motion tier:

```text
M1–M2
```

Duration:

```text
260–420 ms
```

Visual recipe:

```text
small pan/scale transition
stable anchor remains visible
```

Forbidden:

- exaggerated 3D camera motion,
- motion sickness-inducing travel.

Focus Mode:

```text
crossfade
```

Reduced Motion:

```text
crossfade or instant
```

---

# 15. Ambient Effects

## AA-AmbientDrift-01

Purpose:

- very subtle atmospheric life outside recall.

Motion tier:

```text
M0
```

Behavior:

```text
slow low-amplitude drift
```

Allowed:

- Today screen,
- Memory World,
- rare hero backgrounds.

Forbidden:

- reviewer question state,
- multiple simultaneous ambient systems.

Focus Mode:

```text
off
```

Reduced Motion:

```text
off
```

Performance:

- must remain cheap and composited.

---

## AA-AmbientGlow-01

Purpose:

- low-frequency local breathing light.

Motion tier:

```text
M0
```

Behavior:

```text
small luminance variation
very slow
```

Allowed:

- rare dormant/active signal outside recall.

Forbidden:

- entire screen,
- text,
- every card.

Focus Mode:

```text
off
```

Reduced Motion:

```text
static
```

---

# 16. Loading Effects

## AA-LoadingLine-01

Purpose:

- quiet known/unknown wait state.

Motion tier:

```text
M0
```

Allowed:

- non-blocking loading.

Visual recipe:

```text
thin progress/sweep line
low contrast
```

Forbidden:

- fake percentage,
- flashy branded loader.

Focus Mode:

```text
unchanged
```

Reduced Motion:

```text
static progress indicator where possible
```

---

## AA-SkeletonFade-01

Purpose:

- temporary content placeholder.

Motion tier:

```text
M0
```

Visual recipe:

```text
static skeleton
optional very low opacity fade
```

Forbidden:

- strong shimmer loop.

Focus Mode:

```text
static
```

Reduced Motion:

```text
static
```

---

# 17. Error and Warning Effects

## AA-WarningEmphasis-01

Purpose:

- draw attention to non-critical warning.

Motion tier:

```text
M0
```

Visual recipe:

```text
border/state color change
optional short fade
```

Forbidden:

- flashing,
- shaking,
- alarm red unless truly critical.

---

## AA-ErrorEmphasis-01

Purpose:

- clear technical error presentation.

Motion tier:

```text
M0–M1
```

Visual recipe:

```text
static high-contrast error state
optional tiny 2 px emphasis
```

Forbidden:

- screen shake,
- repeated pulse.

Reduced Motion:

```text
static
```

---

# 18. Event Selection Rules

Use the lowest effect intensity that communicates the event.

Preferred order:

```text
AA-Fade-01
↓
AA-FadeRise-01
↓
AA-StatusCrossfade-01
↓
feature-specific M1 effect
↓
AA-Milestone-01
↓
feature-specific M2 effect
↓
M3 only if explicitly earned
```

---

# 19. Effect Composition Rules

Approved composition:

```text
one primary effect
+
0–2 subtle supporting effects
```

Example:

```text
AA-Milestone-01
+
AA-GlowResolve-01
```

Bad composition:

```text
AA-FadeRise-01
+
AA-HoverLift-01
+
AA-GlowResolve-01
+
AA-AmbientGlow-01
+
particle system
+
parallax
```

all competing at once.

---

# 20. AI Effect Selection Rule

Before using an effect, an AI agent must state:

```text
Semantic event:
Prominence:
Motion tier:
Effect ID:
Why this effect:
Focus Mode fallback:
Reduced Motion fallback:
Performance notes:
```

This may live in implementation notes rather than user-facing UI.

---

# 21. New Effect Proposal Template

If a new effect is necessary:

```text
Proposed ID:
Purpose:
Feature:
Semantic trigger:
Motion tier:
Why existing effects are insufficient:
Visual recipe:
Duration:
Easing:
Allowed contexts:
Forbidden contexts:
Focus Mode fallback:
Reduced Motion fallback:
Performance cost:
Reuse potential:
```

Do not implement first and document later.

---

# 22. Effect Rejection Criteria

Reject a proposed effect if it:

- exists only for novelty,
- duplicates an existing effect,
- increases motion during recall,
- relies on bounce/elastic behavior,
- introduces heavy blur for no semantic reason,
- uses particle spam,
- resembles casino reward design,
- cannot degrade under reduced motion,
- creates significant reviewer cost,
- does not settle into a stable state.

---

# 23. Canonical Conflict Resolution

When effect rules conflict:

```text
Product Principles
↓
Visual Constitution
↓
Motion Language
↓
Effects Catalog
↓
Feature Spec
↓
Component implementation
```

The higher-level rule wins.

---

# 24. Initial Approved Effect Index

```text
CORE
AA-Fade-01
AA-FadeRise-01
AA-Crossfade-01

INTERACTION
AA-HoverLift-01
AA-Press-01
AA-FocusRing-01

PROGRESS
AA-ProgressFlow-01
AA-NumberFlow-01
AA-CheckpointActivate-01

STATE
AA-StatusCrossfade-01
AA-GlowResolve-01

MILESTONE
AA-Milestone-01
AA-Milestone-02

EXPEDITION
AA-ExpeditionAdvance-01
AA-ExpeditionComplete-01

ORACLE
AA-OracleLock-01
AA-OracleReveal-01
AA-OracleReveal-02

RESCUE
AA-RescueSignal-01
AA-RescueStabilize-01

NEMESIS
AA-NemesisPressure-01
AA-NemesisWeaken-01
AA-NemesisDefeat-01

FRAGMENT
AA-FragmentResonate-01
AA-FragmentAssemble-01
AA-FragmentReveal-01

RELIC
AA-RelicAwaken-01
AA-RelicFracture-01
AA-RelicRestore-01

MEMORY WORLD
AA-WorldBeacon-01
AA-WorldRegionReveal-01
AA-WorldTransition-01

AMBIENT
AA-AmbientDrift-01
AA-AmbientGlow-01

LOADING
AA-LoadingLine-01
AA-SkeletonFade-01

WARNING / ERROR
AA-WarningEmphasis-01
AA-ErrorEmphasis-01
```

---

# 25. Final Effects Principle

When uncertain, ask:

> **Which approved effect communicates this event with the least spectacle?**

Use that one.

If no effect is needed:

> **Use none.**

---

# Effects Catalog North Star

> **Every effect has a name, a meaning, a ceiling, and a reason to exist.**
