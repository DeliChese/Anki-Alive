# Anki Alive — Color & Surface DNA

Status: CANONICAL
Pack: 1
Applies to: all UI surfaces, color roles, borders, shadows, glow, translucency, gradients, feature accents, and AI-authored frontend presentation
Art Direction: Arcane Memory Interface
Depends on: `00_VISUAL_CONSTITUTION.md`, `02_DESIGN_SYSTEM.md`

---

## 1. Purpose

This document defines the color and surface DNA of Anki Alive.

Its purpose is to prevent visual drift across:

- features,
- phases,
- contributors,
- coding agents,
- design agents,
- generated UI,
- future frontend stacks.

Anki Alive must not rely on individual taste for color, glow, glass, shadow, gradients, borders, or material treatment.

These rules exist so that visually weak agents can still produce coherent work by following a constrained vocabulary.

---

# 2. Surface North Star

Anki Alive surfaces should feel like:

> **Quiet mineral instruments lit from within.**

The product should combine:

```text
Deep matte surfaces
+
Low-chroma structure
+
Rare luminous accents
+
Precise edges
+
Subtle depth
```

The interface must not feel:

- glossy,
- toy-like,
- over-glassed,
- rainbow-lit,
- cyberpunk,
- metallic for decoration alone,
- bright by default.

---

# 3. Foundation Color Philosophy

The visual field should be primarily low-chroma and dark.

Foundation families:

- deep blue-black,
- charcoal,
- charcoal-violet,
- ink slate,
- mineral gray,
- cool neutral text.

Bright color should be reserved for:

- semantic state,
- meaningful feature identity,
- active signal,
- major event,
- rare emphasis.

---

# 4. Canonical Semantic Roles

All colors should map to semantic roles rather than arbitrary local values.

## 4.1 Background Roles

```text
bg.canvas
bg.surface
bg.elevated
bg.overlay
bg.event
```

## 4.2 Text Roles

```text
text.primary
text.secondary
text.tertiary
text.inverse
text.muted
```

## 4.3 Line Roles

```text
line.subtle
line.default
line.strong
line.active
```

## 4.4 State Roles

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

## 4.5 Feature Accent Roles

```text
accent.expedition
accent.oracle
accent.rescue
accent.nemesis
accent.fragment
accent.relic
accent.world
```

AI agents should never invent a new raw color if an existing semantic role fits.

---

# 5. Foundation Palette Direction

Exact production values may evolve, but the relationships must remain stable.

Suggested dark baseline:

```text
bg.canvas
deep blue-black / near-black ink

bg.surface
charcoal-violet

bg.elevated
slightly lighter mineral slate

bg.overlay
dark translucent neutral

bg.event
dark surface with subtle local accent influence
```

Suggested text direction:

```text
text.primary
soft cool near-white

text.secondary
cool light gray

text.tertiary
muted slate gray

text.muted
lower-contrast neutral

text.inverse
deep charcoal on bright special surfaces
```

---

# 6. Chroma Discipline

Most of the interface should remain low-chroma.

Rule:

```text
large area
→ low chroma

small important signal
→ higher chroma allowed
```

Do not fill large panels with saturated feature colors.

Feature accents should usually appear in:

- icons,
- thin borders,
- small markers,
- progress nodes,
- local glow,
- short labels,
- small geometric motifs.

---

# 7. Feature Accent DNA

## 7.1 Expedition

Visual family:

- muted amber,
- antique gold,
- sanded path-light,
- warm mineral brass.

Mood:

- orientation,
- progress,
- grounded movement.

Avoid:

- bright yellow,
- orange arcade UI,
- gold everywhere.

---

## 7.2 Oracle

Visual family:

- pale cyan,
- moonlit blue,
- cool luminous white,
- celestial blue.

Mood:

- observation,
- uncertainty,
- prediction,
- alignment.

Avoid:

- neon cyan,
- hacker-blue,
- electric glow overload.

---

## 7.3 Rescue

Visual family:

- teal,
- sea-glow,
- muted turquoise,
- restorative blue-green.

Mood:

- recovery,
- stabilization,
- care.

Avoid:

- hospital-green,
- emergency red dominance,
- alarm-like flashing.

---

## 7.4 Nemesis

Visual family:

- dark crimson,
- bruised violet,
- obsidian red,
- compressed burgundy.

Mood:

- pressure,
- resistance,
- tension.

Avoid:

- pure red everywhere,
- horror styling,
- aggressive gamer UI.

---

## 7.5 Fragment

Visual family:

- crystalline lavender,
- pale violet,
- spectral lilac,
- cool prism.

Mood:

- incomplete discovery,
- resonance,
- mystery.

Avoid:

- rainbow prism spam,
- candy purple,
- glitter aesthetics.

---

## 7.6 Relic

Visual family:

- ancient gold,
- mineral ivory,
- muted auric light,
- warm stone.

Mood:

- history,
- permanence,
- rarity,
- ownership.

Avoid:

- shiny treasure gold,
- loot rarity colors,
- metallic gradients everywhere.

---

## 7.7 Memory World

Visual family:

- atmospheric blue-green,
- constellation slate,
- muted teal-blue,
- deep topographic cyan-green.

Mood:

- scale,
- continuity,
- legacy.

Avoid:

- bright strategy-game terrain colors,
- saturated map palettes,
- decorative worldbuilding unrelated to memory data.

---

# 8. Surface Tier System

Every major surface should map to one of these tiers.

```text
Tier 0 — Canvas
Tier 1 — Surface
Tier 2 — Elevated
Tier 3 — Overlay
Tier 4 — Event Focus
```

---

# 9. Tier 0 — Canvas

Purpose:

- page background,
- reviewer environment,
- root application field.

Characteristics:

- darkest value,
- lowest visual activity,
- minimal texture,
- no obvious glow.

Canvas must support everything above it without competing.

---

# 10. Tier 1 — Surface

Purpose:

- standard cards,
- panels,
- grouped content.

Characteristics:

- subtle contrast above canvas,
- matte,
- thin line or no border,
- little or no shadow.

This is the default UI surface.

---

# 11. Tier 2 — Elevated

Purpose:

- active panels,
- floating controls,
- emphasized modules,
- dropdown-like structures.

Characteristics:

- slightly brighter surface,
- restrained shadow,
- clearer border separation.

Do not use Tier 2 for every component.

---

# 12. Tier 3 — Overlay

Purpose:

- modal,
- temporary inspection,
- context layer,
- focused secondary interaction.

Characteristics:

- stronger separation,
- background dimming,
- possible controlled translucency.

Overlay must remain easy to dismiss.

---

# 13. Tier 4 — Event Focus

Purpose:

- major reveal,
- Expedition completion,
- Oracle resolution,
- Relic formation,
- rare milestone.

Characteristics:

- strongest surface contrast,
- feature accent allowed,
- local glow allowed,
- richer composition allowed.

Tier 4 is rare.

If many surfaces look like Tier 4, the system has failed.

---

# 14. Matte-First Rule

Default surfaces should feel matte.

Preferred:

- solid low-chroma fill,
- subtle value layering,
- restrained edge definition,
- minimal reflection.

Avoid default use of:

- glossy gradients,
- metallic shine,
- strong specular highlights,
- liquid glass.

---

# 15. Glass Rule

Glass is allowed only when it supports the "instrument" metaphor.

Allowed uses:

- Oracle lens,
- small overlay,
- rare floating control,
- layered instrument surface.

Glass should be:

- subtle,
- low blur,
- low opacity,
- structurally clear.

Avoid:

- full-screen glassmorphism,
- every card translucent,
- heavy blur stacks,
- glossy floating islands everywhere.

---

# 16. Blur Rule

Blur is a scarce resource.

Use for:

- overlay separation,
- Oracle lens effect,
- rare depth transition.

Do not use blur to hide weak layout.

Avoid:

- constant background blur,
- large expensive blur during review,
- stacked blur layers.

---

# 17. Border Philosophy

Borders should feel precise and light.

Preferred:

```text
1 px subtle line
1 px stronger active line
occasional luminous edge
```

Avoid:

- thick borders,
- decorative frames,
- medieval ornament,
- glowing rectangles everywhere.

---

# 18. Border Hierarchy

```text
line.subtle
→ passive grouping

line.default
→ standard structural separation

line.strong
→ emphasized boundary

line.active
→ semantically active state
```

AI agents should not invent local border colors unless required by an accepted feature rule.

---

# 19. Glow Philosophy

Glow communicates energy or significance.

Allowed semantic meanings:

- active,
- resonant,
- locked,
- stabilizing,
- revealed,
- significant.

Glow should not exist merely because dark UI "looks cooler" with glow.

---

# 20. Glow Intensity Levels

```text
G0 — none
G1 — ambient edge
G2 — active signal
G3 — major event
```

## G0

Default.

No visible glow.

## G1

Very subtle edge or local halo.

Use for:

- active chip,
- current path node,
- quiet signal.

## G2

Clearly visible but controlled.

Use for:

- Oracle lock,
- Rescue stabilization,
- checkpoint event.

## G3

Rare major emphasis.

Use for:

- Relic formation,
- major Oracle reveal,
- Expedition completion.

G3 should decay quickly after the event.

---

# 21. Glow Budget Rule

A standard screen should contain:

```text
0–2 G1 glows
0–1 G2 glow
0 G3 glow by default
```

A major event may temporarily introduce one G3 glow.

Do not stack multiple strong halos.

---

# 22. Text Glow Rule

Text glow is prohibited by default.

If used:

- display text only,
- major event only,
- extremely subtle,
- brief duration.

Prefer glowing geometry behind text rather than glowing glyphs.

---

# 23. Shadow Philosophy

Shadows indicate depth, not drama.

Preferred shadows:

- soft,
- low opacity,
- short spread,
- subtle vertical separation.

Avoid:

- huge floating shadows,
- black heavy drop shadows,
- layered neon shadows,
- dramatic card lift.

---

# 24. Shadow Tiers

```text
S0 — none
S1 — subtle separation
S2 — elevated control
S3 — overlay/event
```

Most Tier 1 surfaces should use S0 or S1.

---

# 25. Inner Shadow Rule

Inner shadows may be used very sparingly to suggest:

- inset instrument surfaces,
- mineral depth,
- recessed track.

Avoid inner shadows on every card.

---

# 26. Gradient Philosophy

Gradients are allowed only when they support:

- depth,
- atmosphere,
- semantic transition,
- rare feature identity.

They should be:

- low-contrast,
- low-chroma,
- large-scale,
- restrained.

Avoid gradients as default decoration.

---

# 27. Forbidden Gradient Patterns

Avoid:

- rainbow gradients,
- neon cyan-magenta,
- Instagram-style blends,
- bright multi-stop card gradients,
- gradient text,
- gradients on every CTA.

---

# 28. Feature Gradient Rule

A feature may have one approved gradient family.

Example direction:

```text
Oracle
dark blue-black → pale cyan local bloom

Relic
dark mineral → warm auric edge

Nemesis
obsidian violet → compressed crimson
```

These should remain subtle.

---

# 29. Grain & Texture Rule

Very subtle grain may be used to prevent surfaces from feeling sterile.

Allowed:

- extremely low-opacity noise,
- large-scale mineral texture,
- rare artifact texture.

Avoid:

- visible film grain,
- noisy paper texture,
- dirty overlays,
- parchment texture.

Texture should be felt more than noticed.

---

# 30. Pattern Rule

Geometric patterns may be used when tied to feature identity.

Examples:

- Oracle radial guide,
- Expedition path grid,
- Memory World cartographic contour.

Patterns must:

- remain low contrast,
- stay behind content,
- avoid visual clutter.

---

# 31. Active State Rule

Active state may be communicated through:

- accent color,
- stronger line,
- subtle local glow,
- value shift,
- icon change.

Do not rely on color alone.

---

# 32. Hover State Rule

Hover should remain quiet.

Allowed changes:

- slight value lift,
- subtle line increase,
- tiny local glow,
- micro shadow change.

Avoid:

- huge color shift,
- strong scale-up,
- dramatic glow,
- rainbow effects.

---

# 33. Pressed State Rule

Pressed states should feel tactile but restrained.

Allowed:

- slight compression,
- darker value,
- reduced glow,
- subtle inset feel.

Avoid:

- exaggerated bounce,
- arcade button depression.

---

# 34. Disabled State Rule

Disabled does not mean invisible.

Use:

- lower contrast,
- reduced accent,
- stable geometry.

Maintain readability.

Do not make disabled controls look broken.

---

# 35. Locked State Rule

Locked should feel:

- dormant,
- quiet,
- intentional.

Use:

- low contrast,
- restrained iconography,
- subtle structural cue.

Avoid:

- giant padlocks,
- punishment visuals,
- grayed-out mystery spam.

---

# 36. Stable State Rule

Stable should feel:

- calm,
- anchored,
- resolved.

Use:

- controlled cool or neutral-positive accent,
- no urgent pulse,
- low motion.

Do not use celebratory green everywhere.

---

# 37. Fragile State Rule

Fragile should feel:

- delicate,
- recoverable,
- informative.

Use:

- muted warning family,
- broken arc or signal language,
- subtle contrast increase.

Avoid:

- blinking red,
- emergency framing,
- punitive color language.

---

# 38. Success State Rule

Success should feel:

- resolved,
- complete,
- calm.

Use:

- modest positive color,
- strong shape/state confirmation,
- brief local glow if meaningful.

Avoid:

- confetti,
- green floods,
- giant checkmarks everywhere.

---

# 39. Warning State Rule

Warnings should be visible but not alarming unless there is a real technical risk.

Use:

- amber / muted warm accent,
- icon + text,
- clear hierarchy.

Do not use dramatic red for routine warning states.

---

# 40. Error State Rule

Technical errors may use stronger contrast.

Even then:

- preserve readable hierarchy,
- avoid flashing,
- avoid panic aesthetics.

Critical errors should be clear, not theatrical.

---

# 41. Feature Surface Identity

Feature identity should come from:

- accent,
- geometry,
- local material treatment,
- iconography,
- motion.

Not from fully recoloring every surface.

A feature should still look like Anki Alive first.

---

# 42. Reviewer Surface Ceiling

During active recall:

Allowed:

- Tier 0 canvas,
- Tier 1 quiet surface,
- minimal G0/G1 glow,
- minimal S0/S1 shadow.

Avoid:

- heavy blur,
- Tier 4 event surfaces,
- G2/G3 glow,
- bright gradients,
- visually dense overlays.

---

# 43. Focus Mode Surface Rules

Focus Mode should reduce:

- glow intensity,
- translucency,
- decorative patterns,
- ambient gradients,
- visual depth.

Focus Mode should preserve:

- hierarchy,
- semantic color,
- readable surfaces,
- essential state distinction.

---

# 44. Reduced Sensory Mode

Where future settings allow deeper sensory reduction, prefer:

- flatter surfaces,
- no continuous glow,
- no animated gradient,
- minimal texture,
- minimal blur.

The interface should remain beautiful in a quieter form.

---

# 45. Light Theme Principle

If a light theme exists, it should preserve:

- hierarchy,
- low-chroma structure,
- feature accents,
- restrained material identity.

Do not invert dark colors mechanically.

Light mode should feel like:

> pale mineral paper + precise instrument glass

not generic white SaaS.

---

# 46. White Usage Rule

Pure white should be rare.

Prefer soft cool near-white for text.

Pure white may be used for:

- rare high-contrast highlight,
- tiny critical signal,
- special luminous core.

---

# 47. Black Usage Rule

Pure black should be used sparingly.

Near-black surfaces generally produce richer hierarchy.

Avoid flattening the entire product into `#000000`.

---

# 48. Saturation Rule

Saturation must correlate with importance.

```text
ambient
→ low saturation

active
→ moderate saturation

major event
→ locally higher saturation
```

Never make the baseline UI highly saturated.

---

# 49. Opacity Rule

Do not use opacity as the sole method of hierarchy when it harms readability.

Text below essential contrast should not be accepted merely because it "looks subtle."

Subtle does not mean faint.

---

# 50. Surface Recipe Format

Future approved surface recipes should use IDs.

Examples:

```text
AA-Surface-Canvas-01
AA-Surface-Panel-01
AA-Surface-Elevated-01
AA-Surface-OracleLens-01
AA-Surface-Relic-01
AA-Surface-Event-01
```

Each recipe should define:

- background role,
- border role,
- shadow tier,
- glow tier,
- translucency,
- allowed gradient,
- allowed texture,
- Focus Mode fallback.

---

# 51. AI Color Implementation Rule

Before implementing color or surface styling, an AI agent must identify:

```text
1. Semantic role
2. Surface tier
3. Feature accent role
4. Glow level
5. Shadow level
6. Border role
7. Gradient permission
8. Texture permission
9. Focus Mode behavior
10. Accessibility implications
```

If these are unknown, the agent should not invent them silently.

---

# 52. AI Surface Failure Patterns

Reject or revise UI that contains:

- many unrelated surface colors,
- excessive glass,
- excessive blur,
- glow on every card,
- thick decorative borders,
- rainbow feature colors,
- metallic gradients everywhere,
- bright saturated backgrounds,
- random local shadows,
- hard-coded arbitrary colors instead of semantic tokens.

---

# 53. One-Material-Family Rule

A standard screen should feel like one material family.

Allowed:

```text
matte mineral surfaces
+
one local glass element
```

Bad:

```text
glass
+
chrome
+
paper
+
metal
+
glossy plastic
+
stone
```

all in one screen.

---

# 54. Surface Economy Rule

Do not create a new surface style merely because a new feature exists.

Reuse shared surface recipes whenever possible.

Feature identity should be layered onto the common system rather than replacing it.

---

# 55. Visual Contrast Budget

Use strongest contrast for:

1. recall content,
2. primary action,
3. major state,
4. key feature signal.

Do not spend maximum contrast on decorative elements.

---

# 56. Background Atmosphere Rule

Background atmosphere may include:

- extremely subtle gradient,
- low-contrast constellation,
- muted topographic field,
- faint mineral texture.

It must remain subordinate to content.

Avoid animated background effects during recall.

---

# 57. Event Surface Rule

Major events may temporarily use:

- Tier 4 surface,
- one G3 glow,
- approved feature gradient,
- stronger border,
- richer atmosphere.

After completion, the visual state should settle back into the normal surface hierarchy.

Spectacle must resolve into calm.

---

# 58. Long-Term Wear & History

Persistent objects such as Relics may visually encode history through:

- fracture lines,
- softened edges,
- mineral veining,
- restored seams,
- subtle patina.

Avoid arbitrary damage textures.

Visual aging must correspond to real memory history.

---

# 59. Generated Art Integration Rule

Generated art should be color-graded to the product palette.

Do not place a highly saturated generated asset into a restrained UI without adaptation.

Generated visuals should respect:

- feature accent family,
- surface value,
- local contrast,
- text legibility.

---

# 60. AI Color Review Checklist

Before shipping UI, verify:

1. Is the screen mostly low-chroma?
2. Are bright accents semantically justified?
3. Is there one coherent material family?
4. Is glow rare?
5. Is glass rare?
6. Are borders subtle?
7. Are shadows supporting depth rather than drama?
8. Are feature colors used locally rather than flooding surfaces?
9. Does Focus Mode remain visually coherent?
10. Does the UI avoid casino, cyberpunk, and generic SaaS drift?
11. Are semantic roles used instead of arbitrary colors?
12. Would this still feel tasteful after daily use for one year?

---

# 61. Canonical Conflict Resolution

When color or surface rules conflict:

```text
Product Principles
↓
Visual Constitution
↓
Color & Surface DNA
↓
Design System
↓
Feature Spec
↓
Component implementation
```

The higher-level rule wins.

---

# 62. Final Surface Principle

When uncertain, ask:

> **Does this surface communicate state and hierarchy, or is it merely trying to look expensive?**

Choose the treatment that preserves meaning.

And when two treatments are equally functional:

> **Choose the darker, quieter, more restrained material language.**

---

# Color & Surface North Star

> **Deep mineral calm, precise luminous signals, and rare light used only where meaning earns it.**
