# Anki Alive — UI Review Checklist

Status: CANONICAL
Pack: 8
Applies to: UI implementation review, screenshot review, motion review, feature polish, pre-merge visual QA, and AI self-audit
Art Direction: Arcane Memory Interface
Depends on:
- `00_VISUAL_CONSTITUTION.md`
- `01_COLOR_AND_SURFACE_DNA.md`
- `02_TYPOGRAPHY_AND_INFORMATION_HIERARCHY.md`
- `03_MOTION_LANGUAGE.md`
- `04_EFFECTS_CATALOG.md`
- `05_COMPONENT_CANON.md`
- `06_FEATURE_MOOD_MAPPING.md`
- `07_AI_AESTHETIC_RULES.md`
- `02_DESIGN_SYSTEM.md`
- `01_PRODUCT_PRINCIPLES.md`

---

## 1. Purpose

This document defines the mandatory visual and UX review checklist for Anki Alive.

A feature is not visually complete because:

- it renders,
- it looks polished in one screenshot,
- it uses animation,
- it matches a mockup,
- or an AI says it is done.

A feature is visually complete only when it survives structured review.

The purpose of this checklist is to catch:

- stylistic drift,
- hierarchy failures,
- motion excess,
- reviewer distraction,
- accessibility gaps,
- AI-generated UI clichés,
- feature identity collapse,
- long-term usability problems.

---

# 2. Review Philosophy

Review in this order:

```text
1. Recall integrity
2. Task clarity
3. Information hierarchy
4. Component structure
5. Typography
6. Color and surfaces
7. Feature identity
8. Motion
9. Focus Mode
10. Reduced Motion
11. Accessibility
12. Performance
13. Long-term tastefulness
```

Do not begin by asking:

> Does this look cool?

Begin by asking:

> Does this work as Anki Alive?

---

# 3. Severity Levels

Every review finding should be classified as:

```text
BLOCKER
MAJOR
MINOR
POLISH
```

## BLOCKER

Examples:

- interferes with recall,
- encourages dishonest grading,
- inaccessible core interaction,
- motion cannot be disabled,
- reviewer performance regression,
- casino-like reward behavior,
- feature truth misrepresented visually.

Must be fixed before acceptance.

---

## MAJOR

Examples:

- wrong feature identity,
- incorrect hierarchy,
- major canonical-rule violation,
- overuse of M2/M3 motion,
- Focus Mode broken,
- severe visual clutter.

Should be fixed before merge.

---

## MINOR

Examples:

- inconsistent spacing,
- weak typography role,
- excessive label,
- slightly wrong surface tier,
- redundant border.

Fix during normal polish.

---

## POLISH

Examples:

- small alignment refinement,
- subtle easing improvement,
- minor spacing rhythm,
- tiny icon optical adjustment.

May be deferred if documented.

---

# 4. Pre-Review Context

Before reviewing a screen, identify:

```text
Feature:
Screen:
Primary user task:
Reviewer / non-reviewer:
Semantic state:
Prominence:
Expected component IDs:
Expected surface tier:
Expected motion tier:
Expected effect IDs:
Focus Mode behavior:
Reduced Motion behavior:
```

Review without context can reward the wrong thing.

---

# 5. Recall Integrity Review

For any surface touching review flow, verify:

```text
[ ] Card content remains visually dominant
[ ] No answer information leaks before recall
[ ] No feature pressures a higher grade
[ ] Again is not visually punished
[ ] No event blocks answering
[ ] No animation delays grading
[ ] No decorative motion competes with card content
[ ] No artificial urgency appears during recall
```

Any failure here is a BLOCKER or MAJOR issue.

---

# 6. Primary Task Review

Ask:

1. What should the user do first?
2. Is that action visually obvious?
3. Is another element louder than the primary task?
4. Does the user understand the screen within a few seconds?
5. Is there a clean stopping point?

Checklist:

```text
[ ] One primary task is clear
[ ] One primary visual focal point exists
[ ] Secondary actions are subordinate
[ ] Decorative elements do not compete
[ ] Completion state is understandable
```

---

# 7. Eye-Path Review

Inspect the visual reading order.

Expected pattern:

```text
primary meaning
↓
current state/action
↓
supporting context
↓
metadata
↓
atmosphere
```

Checklist:

```text
[ ] Eye lands on the correct element first
[ ] Secondary hierarchy is clear
[ ] There are not multiple competing heroes
[ ] Metadata does not dominate
[ ] Decorative contrast is lower than semantic contrast
```

---

# 8. Information Density Review

Ask:

> Could 20% of visible UI be removed without losing meaning?

If yes, remove or demote it.

Checklist:

```text
[ ] Screen is not filled merely because space exists
[ ] No unnecessary KPI cards
[ ] No redundant labels
[ ] No repeated explanations
[ ] No excessive badges
[ ] Progressive disclosure is used where appropriate
```

---

# 9. Component Canon Review

For each component:

```text
[ ] Canonical component ID is identifiable
[ ] Component has one main purpose
[ ] Anatomy matches Component Canon
[ ] Shared primitives are reused
[ ] Nested card soup is avoided
[ ] Surface tier matches role
[ ] Motion tier matches role
[ ] Empty/loading/error states exist where needed
```

If a component cannot be named, ask whether it should exist.

---

# 10. Card-Soup Detection

Reject or revise if the screen contains:

- cards inside cards,
- many equally styled boxes,
- excessive panel boundaries,
- repeated bordered containers,
- every content group elevated.

Preferred:

```text
space
+
alignment
+
hierarchy
```

before adding another box.

---

# 11. Typography Review

Verify:

```text
[ ] One strongest typographic focal point
[ ] Approved type roles are used
[ ] Body text is comfortably readable
[ ] Ritual typography is rare
[ ] Uppercase is restrained
[ ] Metrics are not over-prominent
[ ] Labels are necessary
[ ] Line length is reasonable
[ ] Paragraph rhythm is clear
[ ] Text contrast is adequate
```

Reject:

- fantasy fonts,
- glowing body text,
- gradient text,
- oversized KPI typography,
- micro text used for style.

---

# 12. Copy Review

Check feature copy for:

```text
[ ] concise language
[ ] no hype
[ ] no shame
[ ] no artificial urgency
[ ] no casino terminology
[ ] no generic game language
[ ] feature-specific tone is preserved
[ ] technical state remains explainable
```

Avoid excessive exclamation marks.

---

# 13. Color Review

Checklist:

```text
[ ] Large areas remain low-chroma
[ ] Bright color is semantically justified
[ ] Feature accent is local, not flooding the screen
[ ] Semantic tokens are used
[ ] No arbitrary local palette appears
[ ] Status is not communicated by color alone
[ ] Saturation matches importance
```

---

# 14. Surface Review

Verify:

```text
[ ] Surface tier is appropriate
[ ] Material family is coherent
[ ] Matte-first principle is preserved
[ ] Glass is rare
[ ] Blur is rare
[ ] Borders are restrained
[ ] Shadows communicate depth rather than drama
[ ] Texture is subtle
```

Reject effect stacks such as:

```text
glass
+ blur
+ gradient
+ glow
+ heavy shadow
+ grain
```

without strong semantic need.

---

# 15. Glow Review

Ask:

> What does each glow mean?

Checklist:

```text
[ ] Every glow has semantic purpose
[ ] Default surfaces remain G0/G1
[ ] G2 is rare
[ ] G3 appears only for major events
[ ] Text glow is absent or explicitly justified
[ ] Glow settles after emphasis
```

If the answer is "it looks premium," remove it.

---

# 16. Feature Identity Review

For the active feature, verify canonical DNA.

## Expedition

```text
[ ] path / node geometry
[ ] directional progress
[ ] bounded closure
[ ] no quest/racing aesthetic
```

## Oracle

```text
[ ] radial / orbit geometry
[ ] observational tone
[ ] uncertainty resolves only after outcome
[ ] no fortune-teller styling
```

## Rescue

```text
[ ] broken/repaired signal language
[ ] restorative tone
[ ] no panic or punishment
```

## Nemesis

```text
[ ] compressed/angular resistance
[ ] difficulty grounded in memory
[ ] no boss-fight styling
```

## Fragments

```text
[ ] incomplete/assembly geometry
[ ] discovery tone
[ ] no loot-box framing
```

## Relics

```text
[ ] durable artifact identity
[ ] history visible
[ ] no rarity economy
```

## Memory World

```text
[ ] cartographic/data-grounded meaning
[ ] spatial continuity
[ ] no decorative fantasy world
```

---

# 17. Grayscale Test

Temporarily imagine or inspect the UI without feature accent colors.

Ask:

```text
Can I still identify the feature?
Can I still understand state?
Can I still understand hierarchy?
```

Checklist:

```text
[ ] Geometry carries identity
[ ] Symbol carries identity
[ ] Typography/composition carries identity
[ ] Color is supportive, not essential
```

---

# 18. No-Motion Test

Imagine all animation disabled.

Verify:

```text
[ ] Feature identity remains
[ ] State remains understandable
[ ] Completion remains clear
[ ] Interaction remains usable
[ ] No information depends on choreography
```

---

# 19. No-Artwork Test

Imagine all optional generated images fail to load.

Verify:

```text
[ ] Core controls remain present
[ ] State remains understandable
[ ] Layout remains coherent
[ ] Feature remains usable
[ ] Text contrast remains correct
```

Generated art may enrich.

It must not be structural dependency.

---

# 20. Motion Review

For every visible animation:

```text
[ ] Semantic reason exists
[ ] Motion tier is correct
[ ] Approved effect ID exists
[ ] Duration is appropriate
[ ] Easing is restrained
[ ] Motion resolves fully
[ ] No excessive overshoot
[ ] No unnecessary loop
[ ] No competing simultaneous motion
```

---

# 21. Reviewer Motion Review

During question state:

```text
[ ] M0 ceiling respected
[ ] no particle system
[ ] no parallax
[ ] no expressive glow
[ ] no cinematic transition
[ ] no animated background competing with recall
```

During answer state:

```text
[ ] M1 ceiling generally respected
[ ] feedback remains compact
```

Post-grade:

```text
[ ] at most one M2 event is prominent
```

---

# 22. Motion Frequency Review

Ask:

> How often will the learner see this?

Classification:

```text
every card
every few cards
every session
every few sessions
rare long-term event
```

The more frequent the event:

```text
lower amplitude
shorter duration
lower tier
less atmosphere
```

---

# 23. Repetition Test

Ask:

> Would this still feel tasteful after 500 repetitions?

If no:

- reduce duration,
- reduce scale,
- reduce glow,
- reduce frequency,
- downgrade the effect.

---

# 24. Focus Mode Review

Activate or mentally simulate Focus Mode.

Checklist:

```text
[ ] Core task remains obvious
[ ] Feature identity remains
[ ] Essential progress remains
[ ] Ambient motion is removed
[ ] M2/M3 flourish is removed or deferred
[ ] Glow is reduced
[ ] Decorative artwork is reduced where appropriate
[ ] UI does not look broken or disabled
```

---

# 25. Reduced Motion Review

Verify every animated effect has a fallback.

Checklist:

```text
[ ] translation can become opacity/static
[ ] scale can become value/opacity
[ ] parallax can become static
[ ] particle reveal can become static highlight
[ ] multi-stage event can become resolved state
[ ] meaning remains intact
```

---

# 26. Accessibility Review

Checklist:

```text
[ ] keyboard focus is visible
[ ] essential controls are keyboard reachable
[ ] status is not color-only
[ ] text remains readable
[ ] hit targets are adequate
[ ] dismiss actions are predictable
[ ] important icons have understandable meaning
[ ] motion sensitivity is respected
[ ] contrast is sufficient
[ ] empty/error states remain understandable
```

---

# 27. Interaction Review

For every interactive component:

```text
[ ] hover state exists where appropriate
[ ] press state is immediate
[ ] focus state is visible
[ ] disabled state remains readable
[ ] locked state is understandable
[ ] action affordance is clear
```

Avoid decorative controls that appear interactive but are not.

---

# 28. Empty State Review

Checklist:

```text
[ ] absence is explained
[ ] tone is calm
[ ] no shame
[ ] optional next action is useful
[ ] no oversized decorative empty-state art
```

---

# 29. Loading State Review

Checklist:

```text
[ ] loading is truthful
[ ] fake percentages are absent
[ ] animation is quiet
[ ] blocking is minimized
[ ] loading state does not mimic failure
```

---

# 30. Error State Review

Checklist:

```text
[ ] error is clearly named
[ ] explanation is useful
[ ] recovery path exists where possible
[ ] normal review remains usable if optional feature fails
[ ] no dramatic error animation
```

---

# 31. Responsive Layout Review

At narrower widths, verify:

```text
[ ] semantic order is preserved
[ ] primary action remains visible
[ ] content stacks rather than shrinks excessively
[ ] text does not become microscopic
[ ] controls remain usable
[ ] artwork does not crowd content
```

---

# 32. Light/Dark Compatibility Review

Where both themes are supported:

```text
[ ] semantic roles remain correct
[ ] contrast remains readable
[ ] feature accents remain coherent
[ ] surfaces preserve hierarchy
[ ] light mode is not mechanical color inversion
```

---

# 33. Performance Review

Especially for reviewer UI:

```text
[ ] no collection-wide rendering work
[ ] no unnecessary DOM churn
[ ] no large blur animation
[ ] no expensive continuous JS loop
[ ] no high particle count
[ ] no WebGL/canvas dependency during recall
[ ] transform/opacity preferred for motion
[ ] repeated effects remain cheap
```

Any uncertain reviewer cost should be measured.

---

# 34. Dependency Review

If visual work adds a dependency:

```text
[ ] native CSS/WAAPI is insufficient
[ ] repeated need exists
[ ] runtime cost is understood
[ ] Anki WebView compatibility is known
[ ] maintenance risk is acceptable
[ ] Reduced Motion can be supported
[ ] library styling does not override Anki Alive canon
```

---

# 35. AI Slop Review

Reject or revise if several are present:

```text
[ ] random gradient
[ ] giant KPI metric
[ ] generic SaaS card
[ ] excessive glass
[ ] excessive blur
[ ] gradient text
[ ] glowing body text
[ ] icon soup
[ ] badge soup
[ ] card soup
[ ] chart without decision value
[ ] random particles
[ ] shimmer everywhere
[ ] neon cyan/magenta
[ ] overlarge hero copy
```

---

# 36. Casino Review

Immediate rejection if the design introduces:

- loot-box framing,
- prize chest,
- rarity explosion,
- slot-machine motion,
- near-miss animation,
- reward confetti,
- artificial scarcity,
- flashing rarity colors.

---

# 37. Fantasy Drift Review

Reject or revise:

- parchment,
- rune spam,
- fantasy body fonts,
- medieval frames,
- tarot layouts,
- ornamental magic circles without semantic role.

---

# 38. Cyberpunk Drift Review

Reject or revise:

- neon magenta/cyan baseline,
- scanlines,
- glitch,
- terminal UI,
- hologram clichés,
- dense HUD overlays.

---

# 39. Dead Minimalism Review

Ask:

> Did restraint erase identity?

Reject or revise if the feature becomes:

- generic gray utility UI,
- visually indistinguishable from other features,
- sterile,
- devoid of symbolic meaning.

Minimal should remain atmospheric.

---

# 40. Screenshot Review Protocol

For a static screenshot:

## Pass 1 — Squint Test

Blur/squint mentally.

Ask:

- what dominates?
- are major regions clear?
- is visual weight balanced?

## Pass 2 — Hierarchy

Inspect:

- title,
- primary action,
- state,
- supporting info.

## Pass 3 — Noise

Count:

- borders,
- glows,
- badges,
- cards,
- accent colors,
- visible competing effects.

## Pass 4 — Identity

Ask:

- which feature is this?
- can you tell without the title?

## Pass 5 — Removal

Ask:

> What can be removed?

---

# 41. Motion Recording Review Protocol

When reviewing video/GIF motion:

1. Watch once normally.
2. Watch again focusing only on motion.
3. Identify all simultaneously moving elements.
4. Classify each by tier.
5. Remove motion with no semantic purpose.
6. Check repetition burden.
7. Check Focus Mode fallback.
8. Check Reduced Motion fallback.

---

# 42. Before/After Review Rule

When polishing existing UI:

Do not ask only:

> Is the after prettier?

Ask:

```text
Is hierarchy clearer?
Is state more understandable?
Is motion quieter?
Is density lower?
Is feature identity stronger?
Is accessibility equal or better?
Is performance equal or better?
```

A prettier regression is still a regression.

---

# 43. Visual Regression Review

When implementation changes:

```text
[ ] core hierarchy unchanged unless intentional
[ ] feature geometry preserved
[ ] semantic colors preserved
[ ] motion tier did not silently increase
[ ] Focus Mode still works
[ ] Reduced Motion still works
[ ] reviewer remains quiet
```

---

# 44. Pre-Merge UI Gate

Before merge, meaningful UI work should have:

```text
[ ] visual implementation plan recorded
[ ] component IDs identified
[ ] effect IDs identified
[ ] screenshot or host inspection where practical
[ ] Focus Mode checked
[ ] Reduced Motion checked
[ ] accessibility checked
[ ] performance checked
[ ] canonical docs updated if new primitive introduced
```

---

# 45. AI Self-Audit Requirement

Before an AI says "UI is done," it should report:

```text
Primary visual decision:
What was intentionally restrained:
What was intentionally not animated:
Canonical component reused:
Canonical effect reused:
Focus Mode result:
Reduced Motion result:
Accessibility check:
Performance check:
Remaining visual risk:
```

The report may be concise.

---

# 46. Aesthetic Quality Rubric

Score each category:

```text
0 = failing
1 = weak
2 = acceptable
3 = strong
```

Categories:

```text
Recall integrity
Task clarity
Hierarchy
Typography
Surface coherence
Feature identity
Motion semantics
Focus Mode
Reduced Motion
Accessibility
Performance discipline
Long-term tastefulness
```

Maximum:

```text
36
```

Interpretation:

```text
33–36
excellent

29–32
strong

25–28
acceptable with polish

21–24
needs revision

20 or below
not visually ready
```

A BLOCKER overrides the score.

---

# 47. Review Result Template

```text
## UI Review Result

Feature:
Screen:
Overall status: PASS / PASS WITH NOTES / REVISE / BLOCKED

Blockers:
- none

Major:
- ...

Minor:
- ...

Polish:
- ...

Aesthetic score:
__/36

Focus Mode:
PASS / FAIL / NOT APPLICABLE

Reduced Motion:
PASS / FAIL / NOT APPLICABLE

Accessibility:
PASS / NEEDS WORK

Performance:
PASS / NEEDS MEASUREMENT / FAIL

Canonical drift:
NONE / DOCUMENTED / NEEDS DECISION
```

---

# 48. Pass Criteria

A UI may be considered visually accepted when:

```text
No BLOCKER issues remain
No unresolved MAJOR canonical drift remains
Recall integrity passes
Focus Mode is coherent
Reduced Motion preserves meaning
Accessibility is acceptable
Performance is acceptable
Feature identity is clear
Screen remains tasteful under repetition
```

---

# 49. Definition of Visual Done

Visual work is done when:

- hierarchy is clear,
- component structure is canonical,
- typography is coherent,
- surface use is restrained,
- feature identity is distinct,
- motion is semantic,
- Focus Mode is valid,
- Reduced Motion is valid,
- accessibility is considered,
- performance is acceptable,
- visual debt is documented,
- the interface still feels like Anki Alive.

---

# 50. Final Review Question

At the very end, ask:

> **If all novelty disappeared tomorrow, would this still be a clear, elegant, meaningful interface for learning?**

If yes, the design has durability.

Then ask:

> **Does it make memory feel more alive without making the interface itself demand attention?**

If yes, it belongs in Anki Alive.

---

# UI Review North Star

> **Do not review whether the interface performs beautifully. Review whether meaning survives the performance.**
