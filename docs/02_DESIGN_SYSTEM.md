# 02_DESIGN_SYSTEM.md

# Anki Alive — Design System

## 1. Purpose

This document defines the visual and interaction system for Anki Alive.

It is intended to ensure that:

- the product feels like one coherent system,
- all mechanics share a common visual language,
- reviewer flow remains usable and cognitively respectful,
- new UI added in later phases does not drift stylistically,
- generated assets can be created consistently,
- accessibility and Focus Mode are supported from the start.

This is not just a style guide.

It is a product-level design contract.

---

## 2. Visual Direction

### Working Art Direction Name

**Arcane Memory Interface**

### Core Aesthetic

**Dark Arcane + Modern Minimal**

The interface should feel like:

- a memory observatory,
- an intelligent ritual instrument,
- a premium productivity product with mystery,
- a living archive of cognition.

It should not feel like:

- a children's game,
- a fantasy RPG skin,
- a casino UI,
- a dense cyberpunk dashboard,
- a generic productivity SaaS,
- a cluttered gamer HUD.

### Emotional Tone

Target emotional qualities:

- calm
- focused
- intriguing
- elegant
- precise
- atmospheric
- quietly rewarding

Avoid:

- frantic
- childish
- noisy
- over-celebratory
- manipulative
- overly cute
- aggressive

---

## 3. Design Principles

### DS01 — Recall Comes First

During active recall, the card remains visually dominant.

All supporting UI should be subordinate.

### DS02 — Mystery Without Noise

The product may feel mysterious, but information should remain understandable.

Mystery belongs in sequencing and reveal, not in obscurity.

### DS03 — Meaning Before Decoration

Every major visual element should communicate:

- state,
- progress,
- identity,
- priority,
- stability,
- fragility,
- history,
- event type.

Decoration is allowed only when it supports atmosphere without harming clarity.

### DS04 — Quiet by Default

Most of the time, the UI should be restrained.

Moments of emphasis should feel earned.

### DS05 — One World, Many Signals

Oracle, Rescue, Nemesis, Fragments, Relics, Expedition, and Memory World should all feel distinct while clearly belonging to the same product family.

### DS06 — The Interface Must Age Well

The product should still feel strong after months of use.

Do not rely on novelty-heavy spectacle.

---

## 4. Core Visual Vocabulary

The design system draws from six families of visual metaphor.

### 4.1 Observatory

- orbits
- celestial alignment
- radial markers
- star-map logic
- signal detection

### 4.2 Mineral / Artifact

- obsidian
- glassy crystal
- luminous veins
- fractures
- matte stone
- layered geometric relic forms

### 4.3 Cartographic

- routes
- nodes
- paths
- regions
- checkpoints
- exploration logic

### 4.4 Instrument Panel

- precise labels
- controlled motion
- status readouts
- compact feedback
- measured hierarchy

### 4.5 Archive

- history
- preserved events
- cataloged memory
- old/rare meaning
- chronological identity

### 4.6 Signal

- pulse
- lock
- reveal
- resonance
- instability
- synchronization

---

## 5. Color System

The actual production palette can be adjusted later, but semantic roles should remain stable.

### 5.1 Foundation Roles

```text
bg.canvas
bg.surface
bg.elevated
bg.overlay

text.primary
text.secondary
text.tertiary
text.inverse

line.subtle
line.default
line.strong
```

### 5.2 Semantic State Roles

```text
state.stable
state.fragile
state.warning
state.success
state.inactive
state.active
state.locked
state.mystery
```

### 5.3 Feature Accent Roles

```text
accent.expedition
accent.oracle
accent.rescue
accent.nemesis
accent.fragment
accent.relic
accent.world
```

### 5.4 Suggested Direction

The default palette should lean toward:

- deep blue-black / charcoal-violet surfaces,
- soft cool neutrals for text,
- muted luminous accents,
- limited high-saturation usage.

Recommended emotional color associations:

- **Expedition** → muted gold / path-light / sanded amber
- **Oracle** → pale cyan / moonlit blue / luminous orbit
- **Rescue** → teal / sea-glow / restorative pulse
- **Nemesis** → dark crimson-violet / obsidian red / pressure tone
- **Fragment** → crystalline lavender / cool prism tone
- **Relic** → ancient gold / mineral ivory / soft auric light
- **World** → constellation blue-green / atmospheric slate

### 5.5 Color Usage Rules

- Semantic status must not depend on hue alone.
- Use contrast in value and iconography alongside color.
- Avoid rainbow interfaces.
- Most surfaces should remain low-chroma.
- Bright accents should be rare and meaningful.

---

## 6. Typography

Typography should feel contemporary and clear, not decorative-fantasy.

### 6.1 Typeface Roles

```text
Display
Title
Body
Label
Mono / Stat
```

### 6.2 Functional Roles

#### Display

Used sparingly for:

- key screen titles,
- major event reveals,
- major completion moments.

#### Title

Used for:

- section headers,
- panel titles,
- feature names,
- important event labels.

#### Body

Used for:

- descriptions,
- messages,
- explanations,
- settings text.

#### Label

Used for:

- chips,
- micro labels,
- status tags,
- compact metadata.

#### Mono / Stat

Used for:

- score-like readouts,
- progress values,
- percentages,
- time stamps,
- count displays.

### 6.3 Typography Rules

- Favor readability over stylization.
- Do not use faux mystical fonts.
- Use spacing and casing intentionally.
- Allow major events to use slightly wider tracking and stronger scale.
- Avoid dense blocks of micro text in reviewer overlays.

---

## 7. Spacing and Layout

### 7.1 Base Spacing Scale

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

All components should snap to this spacing system where practical.

### 7.2 Radius Scale

```text
8
12
16
20
24
```

Suggested usage:

- chips / pills → 999 or pill radius
- small cards → 12
- panels → 16
- modal/event surfaces → 20
- large hero containers → 24

### 7.3 Stroke / Border Density

The product should favor:

- subtle strokes,
- layered contrast,
- occasional luminous outline,
- minimal hard separators.

### 7.4 Layout Philosophy

Use:

- clear content zones,
- strong visual grouping,
- generous breathing room,
- progressive disclosure,
- consistent alignment.

Avoid:

- dense dashboards,
- five-column analytical grids,
- tiny data labels everywhere,
- hyper-compressed mobile-app styling on desktop.

---

## 8. Elevation and Surface Model

### 8.1 Surface Tiers

```text
Tier 0 — Canvas
Tier 1 — Surface
Tier 2 — Elevated panel
Tier 3 — Overlay
Tier 4 — Event focus surface
```

### 8.2 Surface Behavior

Surfaces should feel layered through:

- subtle value shifts,
- restrained shadow,
- occasional internal glow,
- controlled translucency.

Avoid glassmorphism excess.

The interface should feel solid and intentional, not slippery.

---

## 9. Iconography and Symbol Language

### 9.1 Icon Philosophy

Icons should feel:

- symbolic,
- geometric,
- clean,
- slightly ceremonial,
- legible at small sizes.

Avoid:

- cartoon mascots,
- medieval fantasy ornament,
- skeuomorphic clutter,
- emoji-as-final-design.

### 9.2 Shared Symbol Traits

- line/shape balance
- geometric symmetry
- moderate detail
- distinct silhouette
- meaningful negative space

### 9.3 Feature Symbols

#### Expedition

Path / node / route / marker

#### Oracle

Eye / orbit / lens / celestial disc

#### Rescue

Pulse / arc / stabilizing ring / recovering signal

#### Nemesis

Angular shard / pressure crest / fracture sigil

#### Fragment

Incomplete polygon / crystalline shard / assembling form

#### Relic

Symmetric artifact / rune stone / preserved object

#### Memory World

Constellation / terrain beacon / region network

---

## 10. Component Families

### 10.1 Core Components

- Button
- IconButton
- Card
- Panel
- Tag / Chip
- Progress Bar
- Progress Track
- Badge
- Stat Block
- Toast
- Modal
- Event Reveal Surface
- Signal Row
- Timeline Entry
- List Item
- Toggle
- Slider
- Empty State
- Tooltip

### 10.2 Product-Specific Components

- Memory Core Hero
- Expedition Track
- Checkpoint Node
- Event Queue Marker
- Feature Signal Row
- Oracle Score Readout
- Nemesis Status Block
- Fragment Progress Module
- Relic Tile
- Memory World Region Card

### 10.3 Component Rules

- Components must be composable.
- Feature modules should not invent their own spacing or typography systems.
- Similar content should use shared anatomy even when styling differs.

---

## 11. Reviewer UX Rules

### 11.1 Question State

During active recall:

- the card content dominates,
- only minimal persistent supporting UI is allowed,
- any progress display must remain subtle,
- no large animated event reveal should fire.

Allowed UI examples:

- small Expedition progress header,
- compact signal indicator,
- Focus Mode icon if relevant.

### 11.2 Answer State

When the answer is shown:

- light contextual signals may appear,
- still avoid flooding the screen.

### 11.3 Post-Grade Boundary

This is the preferred reveal point for:

- Oracle resolution,
- Rescue result,
- Nemesis reaction,
- Fragment progression,
- subtle milestone feedback.

### 11.4 Interruption Budget

At most one prominent reveal per review boundary.

If multiple events occur:

- orchestrate,
- queue,
- merge,
- defer,
- or downshift to ambient signals.

### 11.5 Escape Hatch

The user should never feel trapped by an event reveal.

Where dismissal is needed:

- keep it lightweight,
- support keyboard operation,
- avoid long animations before dismissal.

---

## 12. Today Screen

The Today screen is the primary home surface.

### 12.1 Main Goals

- establish today's state,
- create curiosity,
- present a clear entry point,
- avoid information overload,
- anchor the emotional tone of the product.

### 12.2 Primary Anatomy

Recommended structure:

1. temporal header
2. memory state summary
3. Memory Core hero visual
4. expedition entry CTA
5. Today's Signals list
6. optional secondary history snapshot

### 12.3 Memory Core

The Memory Core is the primary home-screen visual anchor.

It should feel like a living memory instrument.

It may change through:

- stability,
- due load,
- historical growth,
- active feature state,
- long-term collection maturity.

It should not become a noisy animated toy.

### 12.4 Today's Signals

Each signal row should communicate:

- mechanic
- status
- quantity or state
- curiosity hook

Example types:

- Oracle: number locked
- Rescue: fragile memories count
- Nemesis: active / present
- Relic: approaching / formed
- Fragment: signal strength

---

## 13. Expedition Visual System

### 13.1 Role

Expedition is the central session UI structure.

### 13.2 Anatomy

- title
- numeric progress
- path track
- checkpoint nodes
- current position
- next signal hint
- completion state

### 13.3 Checkpoints

Checkpoints should feel meaningful but not flashy.

Possible checkpoint states:

- unreached
- nearby
- reached
- hidden special
- completion

### 13.4 Completion

Completion should feel satisfying and conclusive.

Avoid immediately replacing one completion with another obligation.

---

## 14. Feature Visual Grammar

This is the core of cross-feature stylistic consistency.

### 14.1 Expedition

**Geometry:** linear path, nodes, route marks  
**Material feel:** refined HUD / path marker  
**Motion:** forward movement, subtle progression  
**Mood:** movement, completion, orientation

### 14.2 Oracle

**Geometry:** circle, iris, orbit, eclipse  
**Material feel:** luminous glass / celestial instrument  
**Motion:** reveal, rotate, lock, align  
**Mood:** foresight, tension, mind-game

### 14.3 Rescue

**Geometry:** pulse ring, broken curve repaired, wave stabilization  
**Material feel:** softened energy / signal restoration  
**Motion:** pulse, calm repair, re-anchoring  
**Mood:** urgency without panic, recovery

### 14.4 Nemesis

**Geometry:** angular shard, crest, split forms, compressed silhouettes  
**Material feel:** obsidian pressure, fault-line artifact  
**Motion:** tense compression, cracking, weakening  
**Mood:** challenge, resistance, earned victory

### 14.5 Fragment

**Geometry:** incomplete polygon, shard network, suspended facets  
**Material feel:** crystal fragment / encoded object  
**Motion:** assemble, resonate, unlock  
**Mood:** discovery, mystery, progress toward reveal

### 14.6 Relic

**Geometry:** symmetry, artifact silhouette, preserved structure  
**Material feel:** stone + luminous mineral vein + ancient precision  
**Motion:** awaken, stabilize, fracture slowly, restore  
**Mood:** permanence, rarity, ownership, history

### 14.7 Memory World

**Geometry:** map, constellation, terrain markers, region clusters  
**Material feel:** atmospheric archive / living topography  
**Motion:** ambient drift, subtle beacon pulse  
**Mood:** scope, continuity, legacy

---

## 15. Motion System

### 15.1 Motion Principles

- Motion should clarify state change.
- Motion should never delay learning unnecessarily.
- Motion should feel deliberate rather than playful.
- Major reveals should be short and readable.
- Motion must degrade cleanly under reduced-motion settings.

### 15.2 Suggested Timing Scale

```text
120ms  micro response
200ms  subtle transition
350ms  standard reveal
600ms  major completion / hero transition
```

### 15.3 Motion Categories

#### Micro

- button press
- chip update
- small progress shift

#### Standard

- panel entrance
- signal reveal
- small event transition

#### Major

- Oracle reveal
- checkpoint completion
- Relic formation
- expedition completion

### 15.4 Motion Avoidances

Avoid:

- bounce-heavy easing,
- long celebratory loops,
- flashing,
- confetti bursts,
- exaggerated particle effects,
- movement during active recall.

---

## 16. Sound and Haptics Philosophy

Sound, if ever used, must be optional and restrained.

Potential categories:

- progress tick
- event resonance
- completion tone
- warning soft cue

No loud arcade effects.

No dopamine-casino soundscape.

---

## 17. Focus Mode Visual Rules

Focus Mode is not a stripped broken mode.

It is a valid visual presentation.

### Focus Mode should:

- reduce event interruption,
- reduce motion,
- lower ambient visuals,
- retain useful progress information,
- preserve hierarchy and beauty.

### Focus Mode should not:

- hide essential controls,
- remove legibility,
- break layout,
- look "disabled" or inferior.

---

## 18. Empty States

Empty states are opportunities to reinforce tone.

Examples:

- no active Nemesis
- no pending Rescue
- no Relics yet
- no history yet

Empty states should feel:

- intentional,
- calm,
- slightly aspirational.

Avoid shame language.

---

## 19. Copy Tone

Copy should feel:

- concise
- clear
- lightly dramatic
- never cringe
- never childish
- never manipulative
- never overly verbose during review

Preferred style:

- "Memory stabilized."
- "Oracle revealed."
- "Nemesis weakening."
- "Fragment recovered."
- "Relic fractured."
- "Expedition complete."

Avoid:

- "OMG!! Epic win!!"
- "Don't break your streak!"
- "Claim your loot now!"
- "You failed badly."
- "Hurry before it's gone."

---

## 20. Generated Asset Direction

Generated assets should support the product, not dominate it.

### 20.1 Good Use Cases

- feature sigils
- Memory Core variants
- Relic family concepts
- Fragment shards
- subtle background textures
- empty-state illustrations
- Memory World landmark concepts
- atmospheric hero art

### 20.2 Poor Use Cases

- core buttons
- typography
- tiny icons requiring precision
- full layouts
- primary interaction controls
- small reviewer HUD elements

### 20.3 Asset Style Rules

Generated assets should generally favor:

- matte obsidian surfaces
- translucent crystalline structures
- restrained volumetric light
- clean geometric composition
- mineral or astronomical motifs
- low clutter
- subtle luminous accents
- premium, non-cartoon rendering

### 20.4 Avoid in Asset Generation

- fantasy characters
- monsters
- weapons
- ornate medieval filigree
- casino sparkles
- glossy toy materials
- kawaii mascots
- UI text embedded in images
- bright rainbow palettes
- chaotic particle overload

### 20.5 Asset Prompt Framework

Every generated asset request should define:

1. feature identity
2. geometry family
3. material language
4. color role
5. lighting behavior
6. mood
7. complexity level
8. intended placement
9. whether it is ambient or focal

Example skeleton:

```text
Create a [asset type] for Anki Alive.
Style: Arcane Memory Interface, dark arcane + modern minimal.
Feature: [Oracle / Rescue / Nemesis / Fragment / Relic / World].
Geometry: [...]
Materials: [...]
Lighting: [...]
Mood: [...]
Use: [...]
Avoid text. Avoid characters. Avoid casino or fantasy-game styling.
```

---

## 21. Do / Don't Summary

### Do

- keep layouts breathable
- keep reviewer minimal
- use semantic visual distinction
- let major moments feel special
- use quiet atmospheric art
- make history feel precious
- create consistent feature identities
- let Focus Mode feel intentional

### Don't

- overlay everything with decoration
- animate during recall
- use juvenile reward visuals
- use bright colors everywhere
- make every event a modal
- make every feature invent its own design language
- rely on image assets for critical UI
- confuse mystery with ambiguity

---

## 22. Initial Screen Targets by Phase

### Phase 1 — Expedition

- Today screen shell
- reviewer expedition header
- checkpoint reveal
- completion surface

### Phase 2 — Oracle

- Oracle reveal surface
- Oracle summary component

### Phase 3 — Rescue

- Rescue signal component
- Rescue post-grade reveal

### Phase 4 — Nemesis

- Nemesis encounter and weakening visuals

### Phase 5 — Fragments

- Fragment progress module
- reveal surface

### Phase 6 — Relics

- Relic formation reveal
- Relic Vault foundation

### Phase 7 — Memory World

- World landing view
- region cards
- long-term ambient visualization

---

## 23. Future Deliverables

This design-system document should later inform:

- token files
- component inventory
- CSS variables / QSS strategy
- icon set
- asset prompt bible
- UI mockups
- animation spec
- implementation-ready component specs

---

# Design North Star

> **Make memory feel alive through clarity, atmosphere, and meaning — never through noise.**
