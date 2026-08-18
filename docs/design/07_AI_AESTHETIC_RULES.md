# Anki Alive — AI Aesthetic Rules

Status: CANONICAL
Pack: 7
Applies to: all AI-authored UI, UX, visual design, frontend code, motion, generated-art integration, visual refactors, and design reviews
Art Direction: Arcane Memory Interface
Depends on:
- `00_VISUAL_CONSTITUTION.md`
- `01_COLOR_AND_SURFACE_DNA.md`
- `02_TYPOGRAPHY_AND_INFORMATION_HIERARCHY.md`
- `03_MOTION_LANGUAGE.md`
- `04_EFFECTS_CATALOG.md`
- `05_COMPONENT_CANON.md`
- `06_FEATURE_MOOD_MAPPING.md`
- `02_DESIGN_SYSTEM.md`
- `01_PRODUCT_PRINCIPLES.md`

---

## 1. Purpose

This document defines mandatory aesthetic behavior for AI agents working on Anki Alive.

Its purpose is not to ask AI to "have good taste."

Its purpose is to make good taste operational.

AI agents must treat the canonical design documents as implementation constraints, not optional inspiration.

The goal is:

> **A technically competent but aesthetically weak AI should still produce coherent Anki Alive UI because the design space is constrained.**

---

# 2. Core Rule

Before writing UI code, an AI agent must be able to explain:

```text
What is this screen for?
What is the primary user task?
Which feature identity applies?
Which component canon applies?
Which surface tier applies?
Which typography roles apply?
Which motion tier applies?
Which effect IDs apply?
What happens in Focus Mode?
What happens under Reduced Motion?
What visual elements are forbidden here?
```

If these questions cannot be answered, implementation should not begin.

---

# 3. Canonical Read Order

Before meaningful visual work, AI agents must read:

```text
1. Product Principles
2. Visual Constitution
3. Color & Surface DNA
4. Typography & Information Hierarchy
5. Motion Language
6. Effects Catalog
7. Component Canon
8. Feature Mood Mapping
9. relevant Feature Phase Spec
10. current implementation
```

Do not infer missing rules from general design trends.

Do not replace Anki Alive's visual language with personal preference.

---

# 4. Source-of-Truth Priority

When documents conflict:

```text
Product Principles
↓
Visual Constitution
↓
AI Aesthetic Rules
↓
Feature Mood Mapping
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
Feature Phase Spec
↓
Implementation
```

Higher-level rules win.

If a conflict is meaningful and unresolved, surface it rather than silently choosing a new aesthetic direction.

---

# 5. AI Pre-Implementation Declaration

Before implementing a new visual surface, the agent should record this compact declaration in its working notes, plan, PR description, or design review:

```text
Feature:
Screen / Surface:
Primary user task:
Semantic state:
Prominence:
Component IDs:
Surface tier:
Typography roles:
Feature accent:
Motion tier:
Effect IDs:
Focus Mode:
Reduced Motion:
Accessibility notes:
Performance notes:
Explicitly forbidden patterns:
```

This declaration is mandatory for meaningful new feature UI.

It may be abbreviated for trivial changes.

---

# 6. No Freeform Aesthetic Invention

AI agents must not silently invent:

- new visual themes,
- new color families,
- new motion systems,
- new typography systems,
- new surface materials,
- new feature metaphors,
- new component families,
- major new visual dependencies.

If existing primitives are insufficient:

1. identify the gap,
2. propose the smallest extension,
3. document it,
4. preserve canonical direction.

---

# 7. Default-to-Existing Rule

When a design problem appears, prefer:

```text
existing component
+
existing token
+
existing effect
+
existing feature grammar
```

before creating:

```text
new component
+
new color
+
new animation
+
new visual metaphor
```

Novelty is not a quality metric.

---

# 8. Restraint Default

If multiple valid treatments exist, choose:

```text
less glow
less motion
fewer layers
fewer colors
fewer boxes
fewer labels
shorter animation
clearer hierarchy
```

unless semantic importance explicitly earns stronger treatment.

---

# 9. Recall Integrity Gate

Any visual work touching the reviewer must pass this question:

> **Does this make honest recall easier, unchanged, or harder?**

If harder, redesign.

During active recall:

```text
card content
>
all Anki Alive presentation
```

The reviewer must never become a showcase for feature styling.

---

# 10. Reviewer Hard Limits

During reviewer question state:

```text
Motion ceiling: M0
Surface ceiling: Tier 1
Glow ceiling: G1
Ambient systems: off
Particles: forbidden
Parallax: forbidden
Cinematic reveals: forbidden
Large overlays: forbidden
```

The persistent add-on UI budget should generally be:

```text
one compact progress/support component
+
one tiny optional state indicator
```

Anything more requires explicit justification.

---

# 11. One-Focal-Effect Gate

A normal screen may have:

```text
one primary expressive visual effect
+
small supporting transitions
```

It should not contain several equal visual focal points.

If an AI proposal contains:

- animated background,
- glowing hero,
- shimmer cards,
- floating particles,
- parallax,
- animated borders,

at the same time, revise it.

---

# 12. Effect-ID Requirement

Do not describe implementation as:

```text
"add a nice reveal"
"make it smoother"
"add a cool animation"
```

Use approved language:

```text
AA-FadeRise-01
AA-ProgressFlow-01
AA-OracleReveal-01
AA-Milestone-01
```

If no approved effect fits, propose a new catalog entry.

---

# 13. Component-ID Requirement

Do not design arbitrary anonymous UI structures when a canonical component exists.

Prefer:

```text
AA-SignalRow
AA-EventSurface
AA-ExpeditionTrack
AA-OracleSurface
AA-RelicTile
```

The agent should be able to name the component family being implemented.

---

# 14. Semantic Token Requirement

UI code should express meaning through semantic tokens.

Good:

```text
accent.oracle
state.fragile
bg.elevated
text.secondary
line.active
```

Bad:

```text
#51e7ff
rgba(129, 41, 255, 0.62)
box-shadow: 0 0 31px ...
```

Hard-coded values should be exceptional and justified.

---

# 15. No Template-by-Recoloring

A feature is not considered visually designed if the implementation is:

```text
same card
+
different accent color
```

Each feature must preserve canonical differences in:

- geometry,
- motion verbs,
- material nuance,
- symbol,
- composition,
- copy tone.

---

# 16. Grayscale Identity Test

Before accepting feature UI, ask:

> **Would this feature still be recognizable if all accent color were removed?**

If not, improve:

- geometry,
- anatomy,
- symbol,
- composition,
- material treatment.

---

# 17. No-Motion Identity Test

Ask:

> **Would this feature still be recognizable with all animation disabled?**

If not, motion is carrying too much identity.

Strengthen static design.

---

# 18. No-Artwork Integrity Test

Ask:

> **Does this surface still function correctly if optional generated artwork fails to load?**

If not, artwork has improperly replaced UI structure.

Generated art may support atmosphere.

It must not own interaction or meaning.

---

# 19. AI Slop Gate

Reject or revise output containing several of these:

```text
generic SaaS cards
giant KPI numbers
random gradients
gradient text
glowing body text
excessive glass
excessive blur
neon cyan/magenta
particle spam
shimmer everywhere
too many badges
card-inside-card nesting
decorative charts
random floating icons
motion on every component
huge hero copy with little function
generic "premium" dashboard styling
```

These patterns are not automatically sophisticated.

---

# 20. Casino Gate

Reject immediately if a visual proposal resembles:

- loot-box reveal,
- gacha rarity,
- jackpot,
- slot machine,
- prize chest,
- flashing rarity colors,
- confetti reward spam,
- near-miss reward framing.

Mystery in Anki Alive reveals memory meaning.

It does not imitate gambling.

---

# 21. Fantasy-Skin Gate

Reject or revise:

- parchment panels,
- medieval frames,
- faux runes,
- fantasy serif body text,
- ornate magical borders,
- tarot UI,
- RPG quest windows.

Arcane Memory Interface is not medieval fantasy.

---

# 22. Cyberpunk Gate

Reject or revise:

- neon cyan + magenta baseline palette,
- scanlines,
- glitch,
- terminal overlays,
- dense HUD grids,
- hologram clichés.

The product is dark and luminous, not cyberpunk.

---

# 23. Dead-Minimalism Gate

Minimalism is not permission to remove identity.

Reject or revise interfaces that become:

- plain monochrome SaaS,
- generic gray cards,
- sterile utility screens,
- feature-indistinguishable layouts.

Anki Alive must remain atmospheric and symbolic.

---

# 24. Dashboard Gate

Before adding a metric, card, chart, or widget, ask:

> **Does the learner need this to understand memory or decide what to do?**

If not, omit it.

Desktop space does not need to be filled.

---

# 25. Typography Gate

Before accepting typography, verify:

- one clear primary focal point,
- approved type roles,
- readable body text,
- sparse Ritual typography,
- restrained uppercase,
- no novelty mystical fonts,
- no metric overload,
- no glowing text.

Typography should create hierarchy before visual effects do.

---

# 26. Surface Gate

Before accepting surfaces, verify:

```text
Surface tier is known
Glow level is known
Shadow tier is known
Border role is known
Accent role is known
```

Do not create visual richness by stacking:

```text
glass
+
blur
+
gradient
+
glow
+
shadow
+
noise
```

on every surface.

---

# 27. Motion Gate

Every animation must answer:

```text
What changed?
Why should it move?
What tier is it?
Which approved effect ID applies?
What is the reduced-motion fallback?
```

If "because it looks cool" is the only reason, remove it.

---

# 28. Motion Frequency Gate

An effect that looks beautiful once may become annoying after hundreds of reviews.

Before accepting repeated motion, ask:

> **Will this still feel tasteful after the learner sees it every day for one year?**

If uncertain:

- reduce amplitude,
- reduce frequency,
- downgrade tier,
- reserve it for rarer events.

---

# 29. Focus Mode Gate

Every nontrivial feature surface must define its Focus Mode behavior.

Focus Mode should usually:

- retain essential state,
- retain hierarchy,
- retain feature identity,
- remove expressive motion,
- remove ambient systems,
- reduce glow,
- reduce decoration.

Focus Mode must not look abandoned.

---

# 30. Reduced Motion Gate

Every meaningful animation must define a fallback.

Fallback should preserve:

- state,
- hierarchy,
- causality,
- semantic confirmation.

Reduced Motion must not mean "remove feedback."

---

# 31. Accessibility Gate

Visual work must consider:

- contrast,
- keyboard focus,
- scalable text,
- hit target size,
- non-color-only meaning,
- predictable dismissal,
- motion sensitivity.

Beauty that blocks access is a design failure.

---

# 32. Performance Gate

The reviewer hot path is sacred.

AI agents must avoid:

- expensive blur animation,
- unnecessary JS loops,
- high particle counts,
- layout thrashing,
- large DOM churn,
- canvas/WebGL inside active recall,
- per-card heavy rendering.

Prefer:

- opacity,
- transform,
- semantic CSS states,
- native CSS/WAAPI where sufficient.

---

# 33. Dependency Gate

A visual dependency may be introduced only when:

1. native primitives are insufficient,
2. repeated real use cases exist,
3. runtime cost is acceptable,
4. Anki WebView compatibility is acceptable,
5. maintenance risk is acceptable,
6. reduced-motion behavior is supported.

Do not import an animation library for one fancy transition.

---

# 34. Reference-Library Rule

External UI libraries and effect galleries may be studied for:

- timing,
- geometry,
- interaction patterns,
- motion principles.

They must not become style authority over canonical Anki Alive docs.

Do not copy an effect merely because it is impressive.

---

# 35. Generated-Art Gate

Before inserting generated art, verify:

```text
Does it reinforce feature identity?
Does it respect accent family?
Does it preserve text legibility?
Does UI remain functional without it?
Is it restrained enough for repeated use?
```

Generated artwork must be color-graded and composed into the product, not dropped in raw.

---

# 36. Copy Gate

Feature copy must match canonical mood.

Avoid:

- overdramatic fantasy prose,
- hype language,
- excessive exclamation marks,
- game reward language,
- shame,
- artificial urgency.

Preferred:

- concise,
- precise,
- atmospheric,
- humane,
- explainable.

---

# 37. Feature-Specific Mandatory Checks

## Expedition

Must preserve:

```text
path / node / bounded progress
```

Never become:

```text
quest log / racing UI
```

## Oracle

Must preserve:

```text
orbit / alignment / locked uncertainty
```

Never become:

```text
fortune teller / roulette
```

## Rescue

Must preserve:

```text
fragility / stabilization / recovery
```

Never become:

```text
alarm / punishment
```

## Nemesis

Must preserve:

```text
persistent resistance / compressed geometry
```

Never become:

```text
boss battle
```

## Fragments

Must preserve:

```text
incomplete assembly / discovery
```

Never become:

```text
loot drop
```

## Relics

Must preserve:

```text
history / durable artifact
```

Never become:

```text
collectible rarity economy
```

## Memory World

Must preserve:

```text
data-grounded map / long-term history
```

Never become:

```text
decorative fantasy world
```

---

# 38. Visual Change Classification

AI agents should classify visual changes as:

```text
LEVEL A — Token adjustment
LEVEL B — Component refinement
LEVEL C — New component or effect
LEVEL D — Feature visual-system change
LEVEL E — Product art-direction change
```

Permissions:

```text
A
normally safe

B
safe if canonical rules are preserved

C
requires documentation

D
requires explicit design review / decision

E
requires intentional canonical decision
```

Do not disguise Level D/E changes as "polish."

---

# 39. Aesthetic Stop Conditions

An AI agent should stop and surface the issue if:

- canonical docs conflict,
- new visual metaphor is required,
- a new M3 effect is needed,
- a major visual dependency is proposed,
- reviewer hierarchy would change,
- a feature cannot fit existing component grammar,
- accessibility conflicts with intended art direction,
- performance budget appears at risk.

Stopping is preferable to silently drifting.

---

# 40. Implementation Plan Template

For meaningful UI work, use:

```text
## Visual implementation plan

Primary task:
Feature:
Canonical component(s):
Surface tier:
Typography roles:
Accent:
Motion tier:
Effects:
Focus Mode:
Reduced Motion:
Accessibility:
Performance:
Forbidden patterns:
```

This should remain compact.

---

# 41. Visual Code Review Template

Reviewers or AI agents should verify:

```text
[ ] Product purpose is clear
[ ] Recall hierarchy is preserved
[ ] Canonical feature grammar is used
[ ] Shared components are reused
[ ] Semantic tokens are used
[ ] Typography roles are correct
[ ] Surface tier is appropriate
[ ] Glow is restrained
[ ] Motion tier is appropriate
[ ] Approved effect IDs are used
[ ] Focus Mode is defined
[ ] Reduced Motion is defined
[ ] Accessibility is considered
[ ] Performance is acceptable
[ ] No casino/fantasy/cyberpunk drift
[ ] No generic AI dashboard drift
```

---

# 42. Aesthetic Quality Score

For major feature UI, AI agents may self-check with this rubric.

Score each category:

```text
0 = fails
1 = weak
2 = acceptable
3 = strong
```

Categories:

```text
Recall clarity
Hierarchy
Feature identity
Cross-feature cohesion
Typography
Surface restraint
Motion semantics
Accessibility
Focus Mode
Reduced Motion
Performance discipline
Long-term tastefulness
```

Maximum:

```text
36
```

Guidance:

```text
32–36
strong

27–31
acceptable but review weak areas

22–26
revise before considering done

below 22
visual direction is not ready
```

A score does not override canonical rules.

One severe violation may still block acceptance.

---

# 43. Critical-Failure Overrides

Regardless of score, reject UI if it:

- interferes with recall,
- encourages dishonest grading,
- creates casino reward behavior,
- cannot support Reduced Motion,
- is inaccessible in core interaction,
- introduces major visual architecture silently,
- creates unacceptable reviewer cost.

---

# 44. AI Self-Critique Requirement

Before declaring major UI "done," the implementing AI should identify at least:

```text
1 thing intentionally restrained
1 thing it chose not to animate
1 thing reused from the existing canon
1 potential aesthetic risk checked
1 accessibility/reduced-motion consideration
```

This encourages explicit constraint awareness.

---

# 45. Screenshot Review Questions

When reviewing a screenshot, ask:

1. Where does the eye go first?
2. Is that where it should go?
3. Is there more than one visual hero?
4. Is feature identity visible without reading labels?
5. Is any glow competing with text?
6. Are there too many containers?
7. Does anything look like generic AI dashboard styling?
8. Does anything look fantasy, cyberpunk, or casino-like?
9. Could 20% of the decoration be removed without losing meaning?
10. Would the UI improve if that 20% were removed?

If yes, remove it.

---

# 46. Motion Review Questions

When reviewing motion, ask:

1. What semantic state changed?
2. Is movement helping explain it?
3. Is the tier too high?
4. Is the duration too long?
5. Does it settle fully?
6. Does it repeat too often?
7. Does Focus Mode suppress it appropriately?
8. Does Reduced Motion remain clear?
9. Will it remain pleasant after hundreds of repetitions?
10. Is there a quieter approved effect that works?

---

# 47. "Make It More Beautiful" Interpretation Rule

If given a vague instruction such as:

```text
make this more beautiful
make this premium
make this more alive
make this more polished
```

AI agents must NOT interpret it as permission to add more effects.

Interpret it first as:

```text
improve hierarchy
improve spacing
improve typography
improve alignment
improve proportion
improve state clarity
improve material coherence
remove noise
```

Only then consider additional visual effects.

---

# 48. "Make It More Game-Like" Interpretation Rule

Do not automatically add:

- XP,
- rewards,
- badges,
- bounce,
- bright colors,
- loot framing.

In Anki Alive, game-like meaning should come from:

- memory state,
- progression,
- discovery,
- identity,
- history,
- challenge,
- closure.

---

# 49. "Make It More Arcane" Interpretation Rule

Do not automatically add:

- runes,
- occult fonts,
- magic circles,
- purple glow,
- fantasy ornament.

Prefer:

- precise radial geometry,
- controlled light,
- mystery through sequencing,
- mineral materials,
- sparse ceremonial labels,
- observatory logic.

---

# 50. "Make It More Premium" Interpretation Rule

Do not automatically add:

- glass,
- gradients,
- giant shadows,
- gold,
- blur.

Premium quality should come from:

- spacing,
- typography,
- proportion,
- restraint,
- consistent details,
- smooth but quiet interaction,
- meaningful material hierarchy.

---

# 51. "Make It More Alive" Interpretation Rule

Do not make everything move.

Prefer:

- meaningful state evolution,
- data-driven visual change,
- one ambient system where appropriate,
- rare motion tied to actual memory events.

The product is alive because memory changes.

Not because the background never stops moving.

---

# 52. Visual Debt Rule

If implementation temporarily diverges from canon due to technical limitation:

- document the divergence,
- explain why,
- mark follow-up,
- do not silently normalize it as new style.

Visual debt is still debt.

---

# 53. Handoff Rule

When handing UI work to another AI, include:

```text
Implemented component IDs
Implemented effect IDs
New tokens if any
Known visual compromises
Focus Mode status
Reduced Motion status
Accessibility status
Screens requiring visual review
```

Do not rely on chat history alone.

---

# 54. AI Aesthetic Contract

Every AI working on Anki Alive should operate under this contract:

> I do not redesign the product merely because I can.
>
> I preserve recall dominance.
>
> I reuse the canon before inventing.
>
> I use meaning before decoration.
>
> I use motion only when state earns movement.
>
> I treat accessibility, Focus Mode, and Reduced Motion as design states.
>
> I surface conflicts instead of silently changing direction.
>
> I optimize for an interface that remains beautiful after years of repeated use.

---

# 55. Final Decision Rule

When uncertain between two visually valid implementations:

Choose the one that is:

```text
clearer
quieter
more semantic
more reusable
less distracting
more durable
```

If still equal:

> **Choose the one with fewer effects.**

---

# AI Aesthetic North Star

> **Do not ask the AI to have taste. Build the rules so taste emerges from compliance.**
