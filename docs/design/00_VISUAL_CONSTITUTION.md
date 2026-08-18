# Anki Alive — Visual Constitution

Status: CANONICAL DRAFT — PACK 0

This document is the highest-level visual and aesthetic contract for Anki Alive.

It exists so that visual quality does not depend on the taste, personality, model family, or artistic confidence of the current contributor or AI agent.

It does not replace `docs/02_DESIGN_SYSTEM.md`.

The relationship is:

```text
Product Principles
    ↓
Visual Constitution      ← this document
    ↓
Design System
    ↓
Motion Language / Effects Catalog / Component Canon
    ↓
Feature Specs
    ↓
Implementation
```

If a lower-level visual decision conflicts with this constitution, the lower-level decision changes first.

---

# 1. Visual North Star

The canonical visual identity is:

> **Arcane Memory Interface**

with the core aesthetic:

> **Dark Arcane + Modern Minimal**

Anki Alive should feel like a precise instrument for observing, navigating, preserving, and transforming memory.

The intended impression is not “a game skin placed on Anki.”

It is closer to a quiet memory observatory, a living cognitive archive, and a refined ritual instrument whose mystery comes from the learner’s real memory history.

The interface should feel designed enough to create wonder, but disciplined enough that recall remains sovereign.

---

# 2. Core Aesthetic Equation

Every major visual proposal should satisfy this equation:

```text
CLARITY
+ RESTRAINT
+ ATMOSPHERE
+ MEANING
+ PRECISION
= ANKI ALIVE
```

A proposal that omits one term is incomplete.

Examples:

- atmosphere without clarity becomes decorative fog;
- precision without atmosphere becomes generic enterprise software;
- meaning without restraint becomes noisy gamification;
- restraint without identity becomes anonymous minimalism;
- beauty without recall integrity is failure.

---

# 3. Emotional Target

The default emotional field is:

- calm,
- focused,
- intriguing,
- elegant,
- precise,
- atmospheric,
- quietly rewarding,
- intelligent,
- slightly ceremonial,
- durable over repeated use.

The product may occasionally become:

- tense,
- luminous,
- mysterious,
- monumental,
- restorative,
- ominous,

but only when the underlying learning event deserves that shift.

The product must not become:

- frantic,
- childish,
- noisy,
- candy-like,
- casino-like,
- aggressively futuristic,
- ornamental fantasy,
- permanently celebratory,
- visually needy.

---

# 4. The Primary Visual Law

> **Recall owns the foreground. Everything else earns permission to appear.**

During active recall:

- card content is visually dominant;
- supporting UI recedes;
- atmospheric motion becomes quiet or absent;
- no decorative event may compete for fixation;
- no visual treatment may bias grading behavior;
- no reveal may obscure or delay Anki controls.

The product may become more expressive after the answer is shown or after a grade is accepted, but even then presentation remains bounded.

---

# 5. Quiet by Default, Expressive by Cause

Anki Alive is not continuously spectacular.

Most screens should contain visual tension through composition, depth, typography, material, and controlled luminance rather than constant animation.

A strong Anki Alive screen should still feel intentional when completely static.

Spectacle is event-driven.

```text
No semantic cause → no expressive effect.
```

Acceptable causes include:

- a checkpoint reached,
- an Expedition completed,
- an Oracle resolved,
- a Rescue stabilized,
- a Nemesis materially changed,
- a Fragment assembled,
- a Relic formed, fractured, or restored,
- a significant historical memory milestone.

A generic hover, tab switch, or card load is not a reason for cinematic treatment.

---

# 6. Visual Vocabulary

All feature visuals should draw primarily from the following six metaphor families.

## 6.1 Observatory

Vocabulary:

- orbit,
- alignment,
- lens,
- radial marker,
- celestial disc,
- star-map logic,
- signal detection,
- measured illumination.

Use for:

- Oracle,
- prediction,
- observation,
- uncertainty,
- hidden state becoming known.

## 6.2 Mineral / Artifact

Vocabulary:

- obsidian,
- luminous vein,
- crystal plane,
- matte stone,
- fracture,
- preserved object,
- layered geometric artifact.

Use for:

- Relics,
- Nemesis,
- Fragments,
- durable memory identity.

## 6.3 Cartographic

Vocabulary:

- route,
- node,
- region,
- beacon,
- contour,
- checkpoint,
- discovered territory,
- path-light.

Use for:

- Expedition,
- Memory World,
- session progress,
- navigation.

## 6.4 Instrument Panel

Vocabulary:

- measured readout,
- status signal,
- compact indicator,
- controlled hierarchy,
- precision labeling,
- calibrated state.

Use for:

- reviewer support UI,
- stats,
- health state,
- progress readouts,
- settings.

## 6.5 Archive

Vocabulary:

- preserved history,
- catalogued event,
- chronology,
- old memory,
- record,
- provenance,
- accumulated identity.

Use for:

- history,
- milestones,
- long-term memory identity,
- Vault-like surfaces.

## 6.6 Signal

Vocabulary:

- resonance,
- pulse,
- lock,
- instability,
- synchronization,
- recovery,
- attenuation,
- threshold crossing.

Use for:

- Rescue,
- fragile state,
- Oracle lock,
- nearby events,
- state change feedback.

No feature may invent a completely unrelated visual universe without an explicit design decision.

---

# 7. Aesthetic Vocabulary

When describing desired UI, contributors and AI agents should prefer terms from this list:

```text
restrained
luminous
low-chroma
precise
ceremonial
quiet
layered
matte
mineral
observational
cartographic
archival
atmospheric
measured
intentional
geometric
refined
stable
resonant
mysterious-but-readable
```

These terms are not decoration. They are constraints.

A proposal should be explainable using this vocabulary.

---

# 8. Anti-Vocabulary

The following visual directions are presumptively wrong for Anki Alive unless a canonical decision explicitly overrides this document:

```text
generic RPG HUD
mobile game reward screen
casino rarity reveal
loot box
neon cyberpunk dashboard
rainbow gradient system
toy-like 3D UI
cute mascot interface
medieval fantasy parchment
steampunk control panel
maximal glassmorphism
constant aurora background
confetti celebration system
bouncy social-app motion
glossy skeuomorphic buttons
generic SaaS dashboard
holographic chrome overload
```

An AI must not treat “looks impressive” as evidence that one of these directions belongs in the product.

---

# 9. Material Philosophy

The dominant material language is:

```text
MATTE DARK SURFACE
+ SUBTLE DEPTH
+ CONTROLLED LUMINANCE
+ OCCASIONAL MINERAL / GLASS SIGNAL
```

Preferred material behaviors:

- deep low-chroma surfaces,
- fine borders,
- restrained internal highlights,
- soft luminous edges only when meaningful,
- subtle grain/noise if it improves material depth,
- small value changes before large shadows,
- transparency used with purpose.

Avoid:

- translucent glass on every panel,
- blur as the primary identity,
- glossy reflections everywhere,
- strong outer glow on ordinary components,
- excessive shadow stacks,
- decorative texture that damages text clarity.

The product should feel solid, not slippery.

---

# 10. Luminance Is a Scarce Resource

Brightness is semantic.

High luminance should indicate one or more of:

- current focus,
- active state,
- resolved event,
- nearby milestone,
- rare meaningful reveal,
- important affordance.

If everything glows, nothing is important.

Rules:

1. Ordinary surfaces remain dark and quiet.
2. Accent light is localized.
3. Glow must have a semantic owner.
4. More than one strong glow source in a small region requires justification.
5. Reviewer question state should have almost no decorative luminance competition.

---

# 11. Color Discipline

Color is a signal layer, not wallpaper.

The default composition should be visually coherent even when imagined in grayscale.

Rules:

- most surfaces remain low-chroma;
- feature accents are controlled and semantic;
- status cannot depend on hue alone;
- high saturation is rare;
- gradients must express depth, state, direction, or atmosphere;
- gradients must not be added merely because a surface looks empty;
- feature colors must remain members of one shared world.

Feature accents may differentiate mechanics, but they must not create a rainbow dashboard.

---

# 12. Typography Is Modern, Not Fantasy

Typography carries most of the product’s perceived refinement.

Rules:

- body text prioritizes legibility;
- display treatment is used sparingly;
- ceremonial feeling comes from scale, spacing, rhythm, casing, and composition before decorative typefaces;
- faux-rune fonts are prohibited for functional text;
- “mystical” typography must never reduce reading speed;
- stats and compact readouts should feel instrument-like rather than arcade-like.

If an interface requires a novelty font to feel like Anki Alive, the interface has failed.

---

# 13. Composition Before Effects

Every screen must first work through:

1. hierarchy,
2. grouping,
3. alignment,
4. spacing,
5. typography,
6. surface depth,
7. semantic color,
8. only then motion and effects.

An AI must not compensate for weak composition by adding glow, particles, gradients, blur, 3D tilt, or animation.

A static screenshot should communicate the intended hierarchy without explanation.

---

# 14. Information Density

The product should feel information-rich without feeling dashboard-dense.

Prefer:

- one primary visual anchor,
- a clear first read,
- progressive disclosure,
- generous negative space,
- compact secondary signals,
- meaningful grouping.

Avoid:

- many equally weighted cards,
- five-column analytical grids,
- micro-labels everywhere,
- repeated status badges,
- simultaneous competing graphs,
- visualizing data simply because it exists.

The learner should know where to look within one glance.

---

# 15. One Primary Anchor per Surface

Every major screen or state should have one dominant visual anchor.

Examples:

- Today → Memory Core,
- Expedition → path / current checkpoint,
- Oracle → locked/resolved celestial instrument,
- Relic detail → artifact itself,
- Memory World → map / region field.

Secondary modules support the anchor.

They do not compete with it.

If a screen contains three hero treatments, it contains no hero treatment.

---

# 16. Feature Distinction Without Fragmentation

Features may differ in geometry, material emphasis, and motion grammar.

They may not differ in foundational design logic.

Shared across all features:

- spacing scale,
- typography roles,
- surface hierarchy,
- interaction quality,
- focus treatment,
- restrained luminance,
- accessibility,
- motion discipline,
- semantic data grounding.

Feature identity should come from a controlled subset of:

- geometry,
- accent family,
- symbol,
- event choreography,
- material metaphor.

Do not create a separate visual design system per mechanic.

---

# 17. Feature Emotional Profiles

These profiles constrain later detailed feature packs.

## Expedition

```text
orientation
forward movement
measured progress
nearby closure
path-light
```

Never frantic adventure-game UI.

## Oracle

```text
foresight
alignment
uncertainty
rare luminosity
measured tension
```

Never fortune-teller kitsch or casino prediction theatrics.

## Rescue

```text
fragility
restoration
stabilization
care without sentimentality
```

Never alarm-red panic UI or shame.

## Nemesis

```text
resistance
pressure
difficulty
earned weakening
durable challenge
```

Never demonic fantasy boss UI or aggressive taunting.

## Fragment

```text
discovery
partial information
assembly
encoded history
```

Never randomized loot-crate language.

## Relic

```text
preservation
age
rarity through history
material permanence
restoration
```

Never collectible-card rarity spam.

## Memory World

```text
scope
continuity
cartography
legacy
quiet wonder
```

Never a decorative virtual pet world detached from learning data.

---

# 18. Spectacle Budget

Visual spectacle is governed by a budget.

Each screen or review boundary has a finite amount of attention it may spend.

A practical model:

```text
S0 — Silent
S1 — Functional emphasis
S2 — Expressive reveal
S3 — Cinematic milestone
```

Rules:

- active recall: S0 by default;
- reviewer support UI: at most S1;
- ordinary navigation: S0–S1;
- meaningful post-grade event: up to S2;
- major session closure: may reach S2;
- S3 is exceptional and requires explicit canonical permission;
- two S2/S3 effects must not compete simultaneously;
- one prominent event per review boundary remains mandatory.

Later Motion Language documents may refine timing and effect IDs, but cannot loosen this hierarchy silently.

---

# 19. Motion Ceiling

Until a dedicated Motion Language defines approved primitives, all motion follows these ceilings:

```text
M0 — quiet micro-feedback
M1 — functional transition
M2 — expressive semantic reveal
M3 — cinematic event
```

Default permissions:

| Context | Maximum |
|---|---:|
| Reviewer question state | M0 |
| Reviewer answer state | M0–M1 |
| Post-grade minor event | M1 |
| Post-grade major event | M2 |
| Today / dashboard | M1 |
| Expedition navigation | M1 |
| Expedition completion | M2 |
| Focus Mode | M0 |
| Reduced Motion | M0 or static equivalent |
| M3 | Explicit spec only |

An AI may not increase the motion tier because a stronger animation “looks cooler.”

---

# 20. Motion Character

When motion is allowed, it should feel:

- deliberate,
- damped,
- short,
- legible,
- physically coherent,
- slightly ceremonial at major moments.

Prefer:

- fades,
- small translations,
- controlled scale settling,
- progressive reveal,
- subtle alignment,
- path progression,
- restrained luminous decay.

Avoid:

- bounce-heavy easing,
- rubber-band motion,
- perpetual floating,
- slot-machine number reels,
- shake-as-default-error,
- repeated pulsing on ordinary content,
- movement solely to make a screen feel alive.

“Alive” comes from meaningful state change, not constant movement.

---

# 21. Reviewer Constitution

The reviewer is a protected visual zone.

During question state:

- the card dominates;
- persistent Anki Alive UI is compact;
- no decorative particles;
- no hero art;
- no ambient parallax;
- no large glowing containers;
- no animated text reveal unrelated to card content;
- no pre-grade reward framing;
- no visual pressure toward any answer button.

During answer state:

- small contextual signals may emerge;
- grade controls remain visually clear;
- supporting UI still stays subordinate.

After grade:

- one semantic reveal may become prominent;
- it must be dismissible or naturally brief;
- it must never block continuation unnecessarily.

Any effect that would be acceptable on Today may still be unacceptable in Reviewer.

---

# 22. Focus Mode Constitution

Focus Mode is not “the ugly mode.”

It is a premium quiet presentation.

Focus Mode preserves:

- hierarchy,
- spacing,
- typography,
- semantic state,
- useful progress,
- visual dignity.

Focus Mode suppresses or reduces:

- ambient motion,
- decorative particles,
- nonessential glow,
- expressive reveals,
- repeated interruption,
- atmosphere that competes with recall.

A component that becomes visually broken under Focus Mode is not complete.

---

# 23. Reduced Motion Constitution

Every approved motion primitive must eventually define a reduced-motion fallback.

Fallback order:

1. preserve state communication,
2. remove spatial travel,
3. remove repeated motion,
4. replace choreography with immediate or opacity-only transition,
5. preserve focus and reading order.

Reduced Motion must not hide information or remove completion feedback.

---

# 24. Accessibility Is Part of Aesthetic Quality

Anki Alive does not treat accessibility as a separate utilitarian layer beneath visual design.

A visually sophisticated component that fails keyboard navigation, focus visibility, contrast, scalable text, or non-color status communication is aesthetically incomplete.

Rules:

- focus states must be intentionally designed;
- semantic state cannot rely on hue alone;
- text remains readable over atmospheric surfaces;
- ornamental layers cannot intercept controls;
- motion cannot be required to understand state;
- icon-only controls require accessible labels;
- generated art cannot contain essential text or controls.

---

# 25. Generated Art Constitution

Generated artwork may support:

- atmosphere,
- feature identity,
- major empty states,
- historical objects,
- Relics,
- background fields,
- selective hero moments.

Generated artwork may not replace:

- buttons,
- navigation,
- progress semantics,
- labels,
- charts,
- input controls,
- critical instructional text.

Artwork must integrate with UI rather than forcing the UI to adapt around an image.

The interface should remain functional if decorative art fails to load.

---

# 26. Effect Stacking Rules

The following effects are individually valid in some contexts:

- blur,
- transparency,
- glow,
- gradient,
- grain,
- shadow,
- border illumination,
- particles,
- parallax,
- 3D transform.

They are not permission to stack all of them.

Default rule:

> **One dominant atmospheric device per component.**

A component using luminous border treatment should usually reduce outer glow.

A component using rich artwork should simplify its surrounding surface.

A modal with blur should not also require heavy glass reflection, particles, and 3D tilt.

If an AI proposes three or more decorative effect families on one ordinary component, it must justify each one semantically.

---

# 27. Forbidden Combination Patterns

The following combinations are strong indicators of aesthetic drift:

```text
aurora + particles + glass + neon border
3D tilt + glare + glow + floating loop
rainbow gradient + animated border + shimmer
confetti + rarity color + reward modal
red shake + warning glow + countdown pressure
fantasy rune font + parchment + ornamental frame
```

These combinations are prohibited by default.

---

# 28. Anti-Slop Test

Before accepting a visual implementation, ask:

1. Would this still look strong if all animation stopped?
2. Does the first glance reveal a clear hierarchy?
3. Is every strong accent attached to meaning?
4. Is there one primary visual anchor?
5. Could any decorative layer be removed without losing meaning?
6. Does it resemble a generic AI-generated dashboard?
7. Does it resemble a game reward screen more than a memory instrument?
8. Is glass/glow/gradient being used because the component lacks composition?
9. Does the feature still belong to the same world as the rest of Anki Alive?
10. Would repeated daily use make this exhausting?

If questions 6–10 produce concern, revise before adding more polish.

---

# 29. Generic AI Dashboard Warning Signs

A screen is likely drifting into generic AI-generated UI when it contains several of these at once:

- every statistic in its own rounded card,
- arbitrary gradient text,
- large icon in a glowing square for every section,
- identical card anatomy repeated everywhere,
- decorative glass panels with no depth hierarchy,
- tiny pill badges attached to all labels,
- floating abstract blobs,
- meaningless sparkles,
- saturated purple/blue gradient as default brand identity,
- excessive center alignment,
- overuse of “hero” sections,
- animation on every component entrance.

Anki Alive should be recognizable from structure and material behavior, not only from accent color.

---

# 30. Restraint Escalation Rule

When uncertain between two treatments, choose the quieter one first.

Then add intensity only if:

- hierarchy remains too weak,
- semantic meaning is not clear,
- the event deserves stronger emphasis,
- Focus Mode and Reduced Motion behavior remain coherent,
- reviewer attention is unaffected.

This is the inverse of “add effects until it feels premium.”

---

# 31. Visual Novelty Rule

Novelty is not a renewable design resource.

Do not create a new visual trick for every phase.

Prefer deepening a shared vocabulary:

- one stronger checkpoint language,
- one stronger artifact language,
- one stronger signal language,
- one stronger reveal language.

A mature Anki Alive should feel more coherent over time, not more eclectic.

---

# 32. AI Implementation Contract

Any AI or contributor implementing UI must follow this order:

```text
1. Identify user state and semantic purpose.
2. Identify the primary visual anchor.
3. Choose existing component family.
4. Apply canonical spacing / typography / surface hierarchy.
5. Choose feature accent and metaphor family.
6. Determine spectacle tier.
7. Determine motion ceiling.
8. Define Focus Mode behavior.
9. Define Reduced Motion behavior.
10. Check reviewer restrictions if relevant.
11. Implement static hierarchy first.
12. Add approved motion/effects only after static hierarchy works.
13. Run the Visual Compliance Review.
```

Skipping directly to “make it beautiful” is not an acceptable implementation process.

---

# 33. Mandatory Design Citation Rule for AI Work

For meaningful UI work, an AI should state which canonical rules it is applying.

At minimum:

```text
Visual Constitution sections:
Design System sections:
Feature visual grammar:
Spectacle tier:
Motion ceiling:
Focus Mode behavior:
Reduced Motion behavior:
```

Later effect/component packs may replace free-form descriptions with effect IDs and component IDs.

An AI that cannot identify the rules governing its UI proposal has not demonstrated compliance.

---

# 34. Visual Compliance Review

A meaningful UI change is not done until it passes all relevant checks below.

## Identity

- [ ] Clearly belongs to Arcane Memory Interface.
- [ ] Does not resemble a generic RPG, casino, cyberpunk HUD, or SaaS dashboard.
- [ ] Uses canonical metaphor families.

## Hierarchy

- [ ] One clear primary anchor exists.
- [ ] First-glance reading order is obvious.
- [ ] Supporting information is visibly subordinate.
- [ ] Negative space is intentional.

## Material / Color

- [ ] Surfaces are predominantly low-chroma.
- [ ] Luminance is semantic.
- [ ] Glow is restrained.
- [ ] No unjustified effect stacking.
- [ ] Feature accent remains part of the shared product world.

## Motion

- [ ] Motion tier is within the allowed ceiling.
- [ ] Motion communicates state or hierarchy.
- [ ] No unnecessary repeated movement.
- [ ] Reduced Motion behavior is defined.

## Reviewer / Attention

- [ ] Recall remains visually dominant where relevant.
- [ ] Anki controls remain unobscured.
- [ ] No grade-biasing treatment exists.
- [ ] Interruption budget is respected.

## Focus Mode

- [ ] Component remains coherent in Focus Mode.
- [ ] Essential information survives suppression.
- [ ] Focus Mode does not look broken or punitive.

## Accessibility

- [ ] Focus state is visible.
- [ ] Status does not depend on color alone.
- [ ] Text remains readable.
- [ ] Motion is not required to understand the state.

## Longevity

- [ ] Treatment can survive daily repeated use.
- [ ] It does not rely primarily on novelty.
- [ ] It does not create pressure to add stronger spectacle later.

---

# 35. Visual Quality Score

For design reviews, score each dimension from 0–2:

```text
0 = fails
1 = acceptable / needs refinement
2 = strong
```

Dimensions:

- Recall Respect
- Hierarchy
- Product Identity
- Restraint
- Semantic Meaning
- Material Coherence
- Typography
- Motion Discipline
- Accessibility
- Repeated-Use Durability

Maximum: 20.

Guidance:

- 18–20: strong canonical fit
- 15–17: acceptable with targeted polish
- 12–14: substantial design revision required
- below 12: reject direction

Any score of `0` in Recall Respect, Accessibility, or Product Identity blocks acceptance regardless of total score.

The score is a review aid, not a substitute for judgment.

---

# 36. Exception Protocol

This constitution may be intentionally exceeded only when:

1. a feature has a strong semantic reason,
2. the deviation is documented,
3. reviewer/recall integrity is preserved,
4. Focus Mode and accessibility remain supported,
5. the decision is recorded in a feature spec or ADR,
6. the exception does not silently become the new default.

“Because the library demo looked cool” is not an exception rationale.

---

# 37. Relationship to Future Design Packs

The following packs should refine this constitution without contradicting it:

```text
Pack 1 — Color & Surface DNA
Pack 2 — Typography & Information Hierarchy
Pack 3 — Motion Language
Pack 4 — Effects Catalog
Pack 5 — Component Canon
Pack 6 — Feature Mood Mapping
Pack 7 — AI Aesthetic Rules / Execution Playbook
Pack 8 — UI Review & Anti-Drift Checklist
Pack 9 — Prompt Blocks / Agent Bootstrap
```

Future packs may introduce exact tokens, effect IDs, timings, spring values, component anatomy, reference implementations, and approved inspiration sources.

They may not weaken the product principles of recall, restraint, honest grading, accessibility, Focus Mode, or closure.

---

# 38. Constitution North Star

When an AI is uncertain whether a visual idea belongs in Anki Alive, ask:

> **Does this make memory feel meaningful without making the interface demand attention for itself?**

If yes, refine it.

If no, remove it.

And when two beautiful options remain:

> **Choose the one that will still feel beautiful on the 500th review session.**
