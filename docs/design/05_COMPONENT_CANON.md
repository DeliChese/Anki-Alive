# Anki Alive — Component Canon

Status: CANONICAL
Pack: 5
Applies to: shared UI components, product-specific modules, feature surfaces, reviewer overlays, navigation modules, event surfaces, and AI-authored frontend layout
Art Direction: Arcane Memory Interface
Depends on:
- `00_VISUAL_CONSTITUTION.md`
- `01_COLOR_AND_SURFACE_DNA.md`
- `02_TYPOGRAPHY_AND_INFORMATION_HIERARCHY.md`
- `03_MOTION_LANGUAGE.md`
- `04_EFFECTS_CATALOG.md`
- `02_DESIGN_SYSTEM.md`

---

## 1. Purpose

This document defines the canonical component language of Anki Alive.

Its purpose is to ensure that UI built by different contributors and AI agents remains structurally coherent.

A feature may have its own identity.

It may not invent a completely separate component system.

The product should feel assembled from one family of instruments.

---

# 2. Component North Star

Anki Alive components should feel like:

> **Precise memory instruments arranged inside a living archive.**

A component should communicate:

- purpose,
- hierarchy,
- state,
- relationship,
- affordance.

It should not exist merely because dashboards usually contain cards.

---

# 3. Core Component Principles

## C01 — Shared Anatomy Before Feature Styling

Similar content should share structure.

Feature identity should be layered through:

- accent,
- geometry,
- symbol,
- motion,
- local material treatment.

Do not create entirely new anatomy for every feature.

---

## C02 — One Primary Purpose Per Component

A component should answer one main question.

Examples:

```text
What should I do?
What changed?
Where am I?
What is this memory state?
What happened?
```

Avoid components that try to be:

- navigation,
- analytics,
- narrative,
- progress,
- settings

all at once.

---

## C03 — Hierarchy Must Survive Without Effects

If glow, motion, gradients, or artwork are removed, the component must still remain understandable.

---

## C04 — Components Must Degrade Gracefully

Every important component should work under:

- Focus Mode,
- Reduced Motion,
- missing optional artwork,
- narrow layouts,
- light/dark semantic themes where supported.

---

## C05 — Reviewer Components Are Special

Components used during active recall must remain much quieter than dashboard or event components.

The card always remains dominant.

---

# 4. Canonical Component Families

Core shared families:

```text
AA-Button
AA-IconButton
AA-Card
AA-Panel
AA-Chip
AA-Badge
AA-Progress
AA-Stat
AA-SignalRow
AA-ListItem
AA-TimelineEntry
AA-EmptyState
AA-Tooltip
AA-Toast
AA-Modal
AA-EventSurface
AA-SectionHeader
AA-Divider
```

Product-specific families:

```text
AA-MemoryCore
AA-ExpeditionTrack
AA-CheckpointNode
AA-OracleSurface
AA-RescueSurface
AA-NemesisSurface
AA-FragmentModule
AA-RelicTile
AA-WorldRegionCard
AA-ReviewProgressStrip
```

---

# 5. AA-Button

Purpose:

- primary or secondary explicit action.

Anatomy:

```text
container
label
optional leading icon
optional trailing icon
focus treatment
```

Variants:

```text
Primary
Secondary
Quiet
Danger
Icon-adjacent
```

Rules:

- text label must remain clear,
- primary CTA should be obvious,
- no more than one dominant primary action per panel,
- do not use decorative gradients by default.

Motion:

```text
AA-Press-01
AA-HoverLift-01 only where appropriate
```

Forbidden:

- bounce,
- neon glow,
- reward-style pulsing,
- giant 3D game buttons.

---

# 6. AA-IconButton

Purpose:

- compact recognized action.

Anatomy:

```text
hit target
icon
focus state
tooltip if meaning is not obvious
```

Rules:

- icon alone is not enough when ambiguity exists,
- hit area must remain accessible,
- use shared symbol language.

Forbidden:

- decorative icon buttons that do nothing,
- tiny inaccessible hit targets.

---

# 7. AA-Card

Purpose:

- group one coherent piece of information or action.

Anatomy:

```text
optional eyebrow / label
title
supporting content
optional semantic visual
optional footer / action
```

Default surface:

```text
Tier 1
G0
S0–S1
line.subtle or none
```

Rules:

- do not create cards inside cards repeatedly,
- cards are not the default answer to every layout problem,
- no KPI-grid sprawl.

Motion:

```text
AA-FadeRise-01
AA-HoverLift-01 only if interactive
```

---

# 8. AA-Panel

Purpose:

- organize a larger screen region.

Anatomy:

```text
section heading
optional supporting copy
primary content region
optional contextual action
```

Surface:

```text
Tier 1–2
```

Rules:

- panels should have stronger structural purpose than cards,
- do not over-box layouts,
- internal spacing should communicate grouping.

---

# 9. AA-Chip

Purpose:

- compact category, filter, state, or small metadata item.

Anatomy:

```text
optional icon
short label
optional state
```

Typography:

```text
AA-Type-Label
```

Rules:

- 1–4 words preferred,
- do not create chip clouds,
- semantic color must not be the sole meaning.

---

# 10. AA-Badge

Purpose:

- small count or compact semantic marker.

Examples:

```text
3
Locked
New
Fragile
```

Rules:

- badges should remain secondary,
- avoid badge overload,
- do not turn every component into a notification center.

---

# 11. AA-Progress

Purpose:

- represent real bounded progress.

Variants:

```text
Linear
Segmented
Node-based
Radial only when semantically justified
```

Rules:

- progress must represent real state,
- completion boundary should be clear,
- do not use endless fake progress.

Motion:

```text
AA-ProgressFlow-01
```

---

# 12. AA-Stat

Purpose:

- communicate one meaningful metric.

Anatomy:

```text
label
value
optional context
```

Typography:

```text
AA-Type-Metric
or
AA-Type-MetricLarge
```

Rules:

- metric must earn prominence,
- avoid business-dashboard KPI tiles,
- include context when raw value is ambiguous.

---

# 13. AA-SignalRow

Purpose:

- compact feature signal.

Examples:

- Oracle locked,
- Rescue available,
- Nemesis active,
- Relic approaching,
- Fragment resonance.

Anatomy:

```text
feature symbol
title
short state
optional compact value
optional directional affordance
```

Hierarchy:

```text
feature identity
→ state
→ supporting quantity
```

Surface:

```text
usually no card
or
very quiet Tier 1
```

Rules:

- signal rows should scan quickly,
- avoid excessive description.

Motion:

```text
AA-Fade-01
AA-StatusCrossfade-01
```

---

# 14. AA-ListItem

Purpose:

- structured repeated information.

Anatomy:

```text
leading identity
primary label
secondary context
optional trailing action/value
```

Rules:

- keep repeated rows compact,
- avoid card treatment for every list item,
- preserve alignment across rows.

---

# 15. AA-TimelineEntry

Purpose:

- historical event / milestone.

Anatomy:

```text
time marker
event symbol
event title
short meaning
optional related entity
```

Visual metaphor:

```text
Archive
```

Rules:

- chronology must remain clear,
- major events may receive stronger symbol treatment,
- old events should remain readable without becoming visually dominant.

---

# 16. AA-SectionHeader

Purpose:

- establish a major content region.

Anatomy:

```text
title
optional short description
optional single action
```

Rules:

- do not pair every heading with multiple controls,
- section heading should not compete with screen title.

---

# 17. AA-Divider

Purpose:

- separate content only when spacing is insufficient.

Preferred:

- spacing first,
- divider second.

Use:

```text
line.subtle
```

Avoid heavy separators.

---

# 18. AA-EmptyState

Purpose:

- communicate absence without shame.

Anatomy:

```text
optional quiet symbol
clear state title
short explanation
optional next useful action
```

Tone:

- calm,
- intentional,
- slightly aspirational.

Examples:

```text
No active Nemesis
No Rescue signals right now
No Relics have formed yet
```

Forbidden:

- guilt,
- fake urgency,
- oversized illustration dominating the page.

Motion:

```text
AA-FadeRise-01
```

---

# 19. AA-Tooltip

Purpose:

- clarify compact controls or unfamiliar symbols.

Rules:

- concise,
- nonessential to basic operation,
- not used as a substitute for poor labeling.

Motion:

```text
AA-Fade-01
```

---

# 20. AA-Toast

Purpose:

- temporary non-blocking feedback.

Anatomy:

```text
symbol
short message
optional action
```

Rules:

- short,
- dismissible where needed,
- not stacked endlessly,
- no major event content in toast form.

Motion:

```text
AA-FadeRise-01
```

Focus Mode:

- allowed if essential,
- otherwise suppress nonessential toast noise.

---

# 21. AA-Modal

Purpose:

- focused interaction that genuinely requires temporary context isolation.

Use sparingly.

Anatomy:

```text
title
content
primary action
secondary/dismiss action
```

Surface:

```text
Tier 3
```

Rules:

- easy dismissal,
- keyboard support,
- do not use modal for every reveal,
- major events should often use EventSurface instead.

Motion:

```text
AA-Fade-01
or
small AA-FadeRise-01
```

---

# 22. AA-EventSurface

Purpose:

- meaningful feature event or milestone.

Surface:

```text
Tier 4
```

Anatomy:

```text
feature identity
ritual/state label
primary visual
primary event statement
short supporting copy
optional next action
```

Rules:

- one primary event,
- strong but restrained,
- may use M2,
- rare M3 only if explicitly approved,
- must settle into calm.

Typical effects:

```text
AA-Milestone-01
AA-Milestone-02
feature-specific effect
```

---

# 23. AA-MemoryCore

Purpose:

- primary Today-screen visual anchor.

Role:

- living summary of memory state,
- product identity anchor,
- high-level signal surface.

Anatomy:

```text
core visual
primary memory state
supporting status
optional tiny trend/context
```

Rules:

- should feel like an instrument,
- should evolve from real data,
- must not behave like a virtual pet,
- should not constantly animate.

Surface:

```text
Tier 2–4 depending context
```

Ambient motion:

```text
AA-AmbientGlow-01 or equivalent
outside recall only
```

---

# 24. AA-ReviewProgressStrip

Purpose:

- show compact Expedition progress during review.

This is one of the most constrained components in the product.

Anatomy:

```text
minimal progress indicator
optional current checkpoint marker
optional tiny compact status
```

Surface:

```text
Tier 0–1
```

Motion ceiling:

```text
M0 during question
M1 after answer if needed
```

Allowed effects:

```text
AA-Fade-01
AA-ProgressFlow-01 with quiet settings
```

Forbidden:

- large labels,
- animated particles,
- strong glow,
- moving illustrations,
- secondary feature dashboards.

The card remains dominant.

---

# 25. AA-ExpeditionTrack

Purpose:

- central visual structure for session progress.

Anatomy:

```text
start marker
path
checkpoint nodes
current position
future checkpoints
completion marker
optional event hint markers
```

Geometry:

```text
cartographic / path-based
```

Rules:

- clear direction,
- nearby progress emphasized,
- future distance should not feel psychologically overwhelming,
- track must remain readable without motion.

Effects:

```text
AA-ExpeditionAdvance-01
AA-CheckpointActivate-01
AA-ExpeditionComplete-01
```

---

# 26. AA-CheckpointNode

States:

```text
Unreached
Nearby
Current
Reached
Hidden Special
Completion
```

Anatomy:

```text
node geometry
state indicator
optional label
optional short context
```

Rules:

- current and completion states may be stronger,
- hidden special nodes must not become manipulative loot cues.

---

# 27. AA-OracleSurface

Purpose:

- contain Oracle state, commitment, or result.

Visual metaphor:

```text
Observatory
```

Anatomy:

```text
radial/orbit symbol
state label
prediction/result content
short explanation
optional confidence/context
```

Surface:

```text
Tier 2–4
```

Rules:

- pre-answer state must not leak outcome,
- locked state should feel committed but quiet,
- result may use stronger reveal post-grade.

Effects:

```text
AA-OracleLock-01
AA-OracleReveal-01
AA-OracleReveal-02 only when explicitly allowed
```

---

# 28. AA-RescueSurface

Purpose:

- communicate fragile memory and recovery path.

Visual metaphor:

```text
Signal / stabilization
```

Anatomy:

```text
memory identity reference
fragility/stability state
recovery signal
short meaning
```

Surface:

```text
Tier 1–3
```

Rules:

- no punishment tone,
- no emergency aesthetic,
- recovery should feel humane.

Effects:

```text
AA-RescueSignal-01
AA-RescueStabilize-01
```

---

# 29. AA-NemesisSurface

Purpose:

- communicate persistent meaningful difficulty.

Visual metaphor:

```text
compressed mineral resistance
```

Anatomy:

```text
Nemesis identity
status
historical context
current meaning
optional progression toward resolution
```

Rules:

- avoid boss-bar clichés,
- no cartoon villain framing,
- challenge should feel data-grounded.

Effects:

```text
AA-NemesisPressure-01
AA-NemesisWeaken-01
AA-NemesisDefeat-01
```

---

# 30. AA-FragmentModule

Purpose:

- communicate partial discovery.

Visual metaphor:

```text
incomplete crystalline form
```

Anatomy:

```text
fragment geometry
assembly state
short signal
optional discovery hint
```

Rules:

- mystery without casino mechanics,
- progress must reflect real state.

Effects:

```text
AA-FragmentResonate-01
AA-FragmentAssemble-01
AA-FragmentReveal-01
```

---

# 31. AA-RelicTile

Purpose:

- represent a durable long-term memory artifact.

Anatomy:

```text
artifact identity visual
name/title
state
age/history marker
optional short milestone context
```

States may include:

```text
Active
Fractured
Restoring
Restored
Dormant where explicitly defined
```

Surface:

```text
Tier 2–4
```

Rules:

- should feel precious through restraint,
- do not use rarity stars,
- no collectible-card-game framing.

Effects:

```text
AA-RelicAwaken-01
AA-RelicFracture-01
AA-RelicRestore-01
```

---

# 32. AA-WorldRegionCard

Purpose:

- summarize a Memory World region.

Anatomy:

```text
region identity
region visual/map fragment
memory summary
meaningful signal
optional navigation affordance
```

Rules:

- should feel cartographic,
- not like a strategy-game territory card,
- data must explain visual significance.

Effects:

```text
AA-WorldRegionReveal-01
AA-WorldTransition-01
```

---

# 33. Component Surface Mapping

Default guidance:

```text
AA-Button
Tier 1–2

AA-Card
Tier 1

AA-Panel
Tier 1–2

AA-SignalRow
Tier 0–1

AA-Modal
Tier 3

AA-EventSurface
Tier 4

AA-ReviewProgressStrip
Tier 0–1

AA-OracleSurface
Tier 2–4

AA-RelicTile
Tier 2–4
```

Do not raise surface tier merely to make a feature feel special.

---

# 34. Component Motion Mapping

Default guidance:

```text
Button
M0

Card entrance
M1

SignalRow
M0–M1

Panel
M1

Reviewer strip
M0

EventSurface
M2

Rare major EventSurface
M3 by explicit permission only
```

---

# 35. Component Radius Rules

Use shared radius scale:

```text
8
12
16
20
24
999
```

Guidance:

```text
small controls
8–12

cards
12–16

panels
16–20

event surfaces
20–24

chips
999
```

Feature modules must not invent arbitrary radius systems.

---

# 36. Component Spacing Rules

Use shared spacing scale:

```text
4
8
12
16
24
32
48
64
96
```

Typical component internals:

```text
small compact control
8–12 px

card
16–24 px

panel
24–32 px

event surface
24–48 px depending scale
```

---

# 37. Component Border Rules

Default:

```text
line.subtle
```

Active:

```text
line.default or line.active
```

Major event:

```text
line.strong
with optional semantic glow
```

Avoid decorative border framing.

---

# 38. Component Icon Rules

Icons should:

- use shared geometry language,
- have consistent stroke/shape density,
- remain recognizable at small sizes,
- pair with text when ambiguity exists.

Feature symbols should remain stable.

Do not substitute emoji in production UI.

---

# 39. Component Artwork Rule

Artwork may exist inside:

- MemoryCore,
- RelicTile,
- FragmentModule,
- WorldRegionCard,
- EventSurface.

Artwork must not:

- replace essential labels,
- control layout logic,
- obscure actions,
- force the component to depend on asset loading.

---

# 40. Card-vs-Panel Decision Rule

Use a Card when:

- content is relatively self-contained,
- it may be repeated,
- it may be interactive.

Use a Panel when:

- it organizes a screen region,
- it contains several related internal components.

Do not nest Cards inside Cards without clear semantic necessity.

---

# 41. Modal-vs-EventSurface Decision Rule

Use Modal when:

- user must make a focused decision,
- the action is temporary,
- background interaction should pause.

Use EventSurface when:

- the system is presenting meaningful state,
- the learner is receiving a milestone or reveal,
- interaction need not feel like a dialog box.

---

# 42. Component Density Rule

A screen should prefer:

```text
few strong components
```

over:

```text
many tiny widgets
```

Avoid:

- card grids by default,
- endless status boxes,
- analytics tile walls.

---

# 43. One Hero Rule

A major screen may have one hero component.

Examples:

```text
Today
→ AA-MemoryCore

Expedition
→ AA-ExpeditionTrack

Relic Vault
→ featured AA-RelicTile or archive composition

Memory World
→ map/world surface
```

Do not create several competing heroes.

---

# 44. Reviewer Component Budget

During active recall, persistent add-on UI should generally be limited to:

```text
one compact progress/support component
+
tiny optional status indicator
```

Anything more requires strong justification.

---

# 45. Focus Mode Component Rules

Focus Mode should:

- retain component anatomy,
- reduce accent,
- remove ambient artwork where nonessential,
- reduce motion,
- reduce Tier 4 treatment,
- suppress decorative modules.

Focus Mode should not create a second unrelated component design system.

---

# 46. Reduced Motion Component Rules

Component structure must remain identical enough that state is understandable without animation.

Motion fallback should not cause layout jumps that make the interface harder to follow.

---

# 47. Empty and Loading Anatomy Requirement

Every feature screen should intentionally define:

```text
loading
empty
normal
error
```

where applicable.

AI agents must not consider only the "happy populated" state.

---

# 48. Error State Anatomy

Errors should use shared component structure.

Preferred:

```text
clear title
short explanation
recoverable action if available
diagnostic detail only when useful
```

Do not create dramatic feature-specific error art.

---

# 49. Responsive Adaptation

When width decreases:

Prefer:

- stack regions,
- simplify secondary metadata,
- preserve primary action,
- preserve semantic order.

Avoid:

- shrinking everything,
- micro text,
- cramped horizontal controls.

---

# 50. Component API Philosophy

Implementation APIs should expose semantic variants.

Good:

```text
variant="oracle"
state="locked"
prominence="minor"
```

Bad:

```text
glowColor="#82f4ff"
borderWidth="1.3"
shadowBlur="17"
```

Consumers should express meaning, not arbitrary styling.

---

# 51. Component Token Rule

Components should consume semantic tokens for:

- color,
- spacing,
- radius,
- line,
- elevation,
- motion,
- typography.

Avoid hard-coded one-off values unless explicitly justified.

---

# 52. Component Composition Rule

A feature should compose shared primitives before creating new custom structures.

Example:

```text
AA-OracleSurface
=
AA-Panel
+ feature symbol
+ AA-Type-Ritual
+ AA-StatusCrossfade-01
+ Oracle-specific geometry
```

This preserves coherence.

---

# 53. New Component Admission Rule

A new component family should only be introduced if:

1. existing anatomy cannot represent the content cleanly,
2. the need is semantically distinct,
3. reuse is likely or the feature importance justifies uniqueness,
4. accessibility is defined,
5. Focus Mode behavior is defined,
6. motion behavior is defined,
7. surface tier is defined.

---

# 54. New Component Proposal Template

```text
Proposed ID:
Purpose:
Feature:
Why existing components are insufficient:
Anatomy:
Surface tier:
Typography roles:
Motion tier:
Approved effects:
States:
Focus Mode behavior:
Reduced Motion behavior:
Accessibility:
Reuse potential:
```

---

# 55. AI Component Implementation Rule

Before building a UI component, an AI agent must identify:

```text
1. Component ID
2. Primary purpose
3. Anatomy
4. Semantic state
5. Surface tier
6. Typography roles
7. Motion tier
8. Approved effect IDs
9. Focus Mode behavior
10. Reduced Motion behavior
11. Accessibility requirements
12. Empty/loading/error states where applicable
```

---

# 56. AI Component Failure Patterns

Reject or revise a component that shows:

- unclear primary purpose,
- too many equally prominent sections,
- nested card soup,
- arbitrary local colors,
- arbitrary local spacing,
- feature-specific typography system,
- excessive glow,
- unnecessary motion,
- inaccessible icon-only actions,
- mobile-game reward framing,
- missing empty/error states.

---

# 57. Component Review Checklist

Before a component is accepted, verify:

1. Is its primary purpose obvious?
2. Does it use approved anatomy?
3. Does it reuse shared primitives?
4. Is its surface tier appropriate?
5. Does typography follow canonical roles?
6. Does motion follow approved IDs?
7. Is glow restrained?
8. Is the component still clear without motion?
9. Does Focus Mode remain coherent?
10. Does it have necessary empty/loading/error states?
11. Is accessibility considered?
12. Does it look like Anki Alive rather than a generic UI kit?

---

# 58. Canonical Conflict Resolution

When component rules conflict:

```text
Product Principles
↓
Visual Constitution
↓
Color & Surface DNA
↓
Typography & Information Hierarchy
↓
Motion Language
↓
Effects Catalog
↓
Component Canon
↓
Feature Spec
↓
Implementation
```

The higher-level rule wins.

---

# 59. Final Component Principle

When uncertain, ask:

> **What is this component for, and can that purpose be understood before noticing its styling?**

If not, simplify.

And when two structures are equally functional:

> **Choose the one with fewer boxes, clearer hierarchy, and stronger semantic identity.**

---

# Component North Star

> **One product, one family of instruments, many memory stories.**
