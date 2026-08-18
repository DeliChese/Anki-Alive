# Anki Alive — Typography & Information Hierarchy

Status: CANONICAL
Pack: 2
Applies to: all UI text, labels, metrics, hierarchy, typography motion, and AI-authored frontend presentation
Art Direction: Arcane Memory Interface
Depends on: `00_VISUAL_CONSTITUTION.md`, `02_DESIGN_SYSTEM.md`

---

## 1. Purpose

This document defines the typography and information hierarchy of Anki Alive.

Its job is to ensure that every screen feels like one coherent product, even when different AI agents or contributors build different features.

Typography in Anki Alive must communicate:

- importance,
- state,
- progression,
- atmosphere,
- precision,
- identity,
- chronology,
- restraint.

Typography must never become decorative noise.

The interface should feel intelligent and atmospheric without sacrificing readability.

---

# 2. Typography North Star

Typography should feel like:

> **A precise archival instrument with a quiet ceremonial edge.**

The system combines:

```text
Modern readability
+
Measured hierarchy
+
Sparse ritual emphasis
+
Data precision
+
Long-term calm
```

The typography must not resemble:

- medieval fantasy UI,
- tarot branding,
- occult poster design,
- cyberpunk terminal dashboards,
- arcade game HUDs,
- generic SaaS typography with no identity.

---

# 3. Core Typography Principles

## T01 — Readability Before Atmosphere

The arcane tone must come primarily from:

- composition,
- spacing,
- geometry,
- motion,
- iconography,
- surfaces.

Body text must remain easy to read.

Do not make text mysterious by making it illegible.

---

## T02 — Hierarchy Before Decoration

Scale, weight, spacing, and placement should establish importance before any decorative effect is added.

Do not rely on:

- glow,
- gradient text,
- colored outlines,
- ornamental framing

to create hierarchy.

---

## T03 — Quiet Majority, Rare Emphasis

Most text should remain visually calm.

Only important moments deserve stronger treatment.

The typography system should make emphasis feel earned.

---

## T04 — Arcane Does Not Mean Fantasy Font

Avoid:

- pseudo-rune fonts,
- medieval serif body copy,
- faux occult display type,
- novelty mystical lettering,
- distressed fantasy fonts.

Anki Alive is a memory instrument, not a fantasy tavern menu.

---

## T05 — Numbers Are Instruments

Numbers, counts, percentages, intervals, dates, and other measurable values should feel precise.

They may use:

- tabular numerals,
- restrained mono-inspired styling,
- aligned metrics,
- measured tracking.

They must not feel like arcade scores.

---

# 4. Typography Role System

All text should belong to one of the following roles.

```text
AA-Type-Display
AA-Type-H1
AA-Type-H2
AA-Type-H3
AA-Type-Body
AA-Type-BodyStrong
AA-Type-Label
AA-Type-Caption
AA-Type-Metric
AA-Type-MetricLarge
AA-Type-Ritual
AA-Type-Mono
AA-Type-Status
```

AI agents should select a semantic role before styling text.

---

# 5. AA-Type-Display

Use sparingly.

Purpose:

- major feature reveal,
- Expedition completion,
- Relic formation,
- major Memory World moment,
- rare Oracle centerpiece.

Characteristics:

- large scale,
- strong contrast,
- controlled tracking,
- limited line length,
- more atmosphere than normal headings.

Rules:

- never use for normal panels,
- never use repeatedly on one screen,
- never use during active recall,
- never animate continuously.

Recommended range:

```text
32–48 px desktop
26–36 px compact surfaces
```

Weight:

```text
500–700
```

Tracking:

```text
0 to +0.04em
```

---

# 6. AA-Type-H1

Primary screen title.

Use for:

- Today screen title,
- Expedition overview,
- Relic Vault,
- Memory World main view.

Recommended range:

```text
24–32 px
```

Weight:

```text
600–700
```

Line height:

```text
1.15–1.25
```

H1 should appear once per major screen.

---

# 7. AA-Type-H2

Section title.

Use for:

- major panel headings,
- grouped feature sections,
- timeline groups,
- secondary screen regions.

Recommended range:

```text
18–22 px
```

Weight:

```text
600
```

Line height:

```text
1.2–1.3
```

---

# 8. AA-Type-H3

Component or card title.

Use for:

- panel titles,
- item titles,
- signal names,
- compact feature modules.

Recommended range:

```text
15–18 px
```

Weight:

```text
550–650
```

---

# 9. AA-Type-Body

Default reading text.

Use for:

- descriptions,
- explanations,
- settings,
- narrative summaries,
- helper text.

Recommended range:

```text
14–16 px
```

Line height:

```text
1.45–1.65
```

Preferred line length:

```text
45–75 characters
```

Body text must prioritize comfort over visual novelty.

---

# 10. AA-Type-BodyStrong

Use for:

- short emphasized phrases,
- key explanations,
- important state descriptions.

Do not replace entire paragraphs with strong text.

Use weight before color when possible.

---

# 11. AA-Type-Label

Use for:

- chips,
- compact category names,
- controls,
- metadata keys,
- small section markers.

Recommended range:

```text
11–13 px
```

Weight:

```text
500–650
```

Optional tracking:

```text
+0.02em to +0.08em
```

Uppercase may be used sparingly for short labels only.

Never uppercase long text.

---

# 12. AA-Type-Caption

Use for:

- secondary metadata,
- timestamps,
- quiet explanations,
- history details.

Recommended range:

```text
11–13 px
```

Weight:

```text
400–500
```

Caption text must remain legible and should not drop below accessible contrast thresholds.

---

# 13. AA-Type-Metric

Use for:

- progress numbers,
- percentages,
- intervals,
- counts,
- summary statistics.

Recommended range:

```text
14–20 px
```

Properties:

- tabular numerals when available,
- compact line height,
- stable width where possible,
- restrained contrast.

Metrics should feel measured, not competitive.

---

# 14. AA-Type-MetricLarge

Use only for genuinely important values.

Examples:

- Expedition completion progress,
- major memory-age milestone,
- meaningful stability summary.

Recommended range:

```text
24–40 px
```

Use sparingly.

Do not turn every dashboard value into a KPI hero.

---

# 15. AA-Type-Ritual

This is a special role.

Use for rare ceremonial or atmospheric labels.

Examples:

- ORACLE LOCKED
- RELIC RESTORED
- EXPEDITION COMPLETE
- MEMORY SIGNAL RESOLVED

Characteristics:

- short,
- high tracking,
- restrained uppercase,
- low frequency,
- never paragraph length.

Recommended range:

```text
10–13 px
```

Tracking:

```text
+0.08em to +0.16em
```

Weight:

```text
550–700
```

Never use Ritual typography for normal navigation.

---

# 16. AA-Type-Mono

Use for:

- IDs,
- timestamps,
- technical diagnostics,
- data readouts,
- compact statistical values.

Mono styling must not dominate the product.

Anki Alive is not a terminal interface.

---

# 17. AA-Type-Status

Use for short semantic states.

Examples:

```text
Stable
Fragile
Locked
Restoring
Active
Dormant
Resolved
```

Status text must always be understandable without color.

Use:

- text,
- icon,
- shape,
- structural placement

alongside color.

---

# 18. Font Family Strategy

The final production font stack may evolve, but all future selections must preserve these roles.

## Primary UI Family

Required qualities:

- modern,
- highly readable,
- neutral but refined,
- excellent small-size rendering,
- broad weight coverage.

Suitable direction:

```text
Inter
IBM Plex Sans
Source Sans 3
Manrope
Geist-like modern grotesk families
system UI fallback
```

Licensing must be verified before distribution.

---

## Display Family

Optional.

Only introduce a separate display face if it clearly improves identity without harming coherence.

Required qualities:

- elegant,
- restrained,
- slightly distinctive,
- not faux-historical,
- not fantasy-coded.

A separate display font is not mandatory.

---

## Metric / Mono Family

Optional.

Suitable direction:

```text
IBM Plex Mono
JetBrains Mono
Source Code Pro
system monospace fallback
```

Use only where precision benefits from monospacing.

---

# 19. Font Dependency Rule

Do not add a font dependency casually.

A new bundled font must justify:

1. identity benefit,
2. readability,
3. license compatibility,
4. file size,
5. rendering quality in Anki WebView,
6. Windows/macOS/Linux behavior,
7. fallback behavior.

System fonts are preferred when the aesthetic difference is small.

---

# 20. Weight Discipline

Avoid using too many font weights.

Preferred functional set:

```text
400 — normal reading
500 — subtle emphasis
600 — headings / strong labels
700 — rare major emphasis
```

Do not create hierarchy using five near-identical weights.

---

# 21. Text Color Hierarchy

Typography color should map to semantic roles.

```text
text.primary
text.secondary
text.tertiary
text.inverse
```

General usage:

```text
Primary
→ important reading / primary heading

Secondary
→ supporting copy / metadata

Tertiary
→ quiet context / inactive metadata

Inverse
→ text on bright or special surfaces
```

Do not invent arbitrary grays per component.

---

# 22. Accent Text Rule

Accent color may be used for:

- semantic state,
- important feature identity,
- rare interactive emphasis.

Avoid coloring whole paragraphs.

Accent text should usually be short.

Good:

```text
Oracle locked
3 checkpoints remaining
Relic restored
```

Bad:

an entire explanatory paragraph rendered cyan because it belongs to Oracle.

---

# 23. Gradient Text Rule

Gradient text is prohibited by default.

It may be considered only for extremely rare, high-significance display moments.

Never use gradient text for:

- body,
- labels,
- navigation,
- buttons,
- metrics,
- normal headings.

---

# 24. Text Glow Rule

Text glow is prohibited by default.

If used at all:

- major display text only,
- very low intensity,
- brief event state,
- no readability loss.

Glow should usually belong to surrounding geometry, not glyphs.

---

# 25. Information Hierarchy Ladder

All screen information should fit roughly into:

```text
Level 0 — Recall
Level 1 — Primary task
Level 2 — Current progress / core state
Level 3 — Important feature signal
Level 4 — Supporting explanation
Level 5 — Metadata
Level 6 — Atmosphere
```

The visual hierarchy must mirror this order.

---

# 26. One Primary Message Rule

Every panel should answer:

> What is the most important thing here?

One component should not contain three equally loud messages.

Use progressive disclosure for secondary information.

---

# 27. Metric Hierarchy Rule

A metric must earn prominence.

Before displaying a number prominently, ask:

1. Does the learner need it now?
2. Does it change a decision?
3. Does it explain memory state?
4. Does it support closure?
5. Does it deserve attention over card content?

If not, reduce its prominence.

---

# 28. No KPI Dashboard Rule

Avoid screens dominated by:

- giant numbers,
- percentage tiles,
- analytics cards,
- metric grids.

Anki Alive is not business intelligence software.

Metrics support memory understanding.

They are not the product identity.

---

# 29. Label Economy

Use labels only when they improve understanding.

Avoid:

```text
STATUS
STATE
TYPE
LEVEL
PROGRESS
CURRENT
```

when the surrounding context already makes the meaning obvious.

Prefer fewer, stronger labels.

---

# 30. Microcopy Density Rule

Reviewer overlays should contain very little text.

During review:

- short status,
- compact progress,
- small event cue.

Long explanations should be deferred outside the recall moment.

---

# 31. Line Length Rules

Recommended maximum reading widths:

```text
Body prose
45–75 characters

Dense settings/help
up to ~85 characters

Event reveal copy
25–55 characters

Labels
1–5 words
```

Avoid wide paragraphs spanning large desktop surfaces.

---

# 32. Paragraph Rhythm

Use:

- short paragraphs,
- clear grouping,
- meaningful spacing.

Avoid:

- walls of text,
- excessive dividers,
- repeated heading levels,
- tiny explanatory footnotes everywhere.

---

# 33. Vertical Rhythm

Typography spacing should use the shared spacing scale.

Preferred relationships:

```text
Label → value
4–8 px

Heading → supporting copy
8–12 px

Paragraph → paragraph
12–16 px

Section → section
24–32 px

Major region → major region
32–48 px
```

Spacing should create hierarchy before additional decoration is introduced.

---

# 34. Heading Density

Avoid stacking headings unnecessarily.

Bad:

```text
MEMORY
Memory Status
Current Memory Status
Today
```

Good:

```text
Memory State
Supporting explanation
```

One meaningful heading is stronger than several redundant ones.

---

# 35. Capitalization Rules

Default:

```text
Sentence case
```

Use title case only when product naming requires it.

Use uppercase only for:

- short Ritual labels,
- very small technical labels,
- rare category markers.

Do not uppercase body copy.

---

# 36. Tracking Rules

Normal body:

```text
0 to +0.01em
```

Headings:

```text
-0.02em to +0.02em
```

Labels:

```text
+0.02em to +0.08em
```

Ritual labels:

```text
+0.08em to +0.16em
```

Excessive tracking is not inherently arcane.

---

# 37. Numeral Rules

Where available, use:

- tabular numerals for aligned metrics,
- proportional numerals for normal prose.

Do not use decorative numerals.

Numbers should remain immediately legible.

---

# 38. Date & Time Presentation

History and archival interfaces should prefer human-readable time.

Examples:

```text
18 Aug 2026
3 days ago
First learned 2 years ago
```

Raw technical timestamps belong only in diagnostics or advanced detail.

---

# 39. Progress Copy

Prefer language that reinforces bounded progress.

Good:

```text
Checkpoint 2 of 4
12 reviews to the next checkpoint
Expedition complete
```

Avoid psychologically distant raw counts when local structure exists.

Bad:

```text
67 / 438
```

without context.

---

# 40. Failure Language

Failure-related states must remain neutral and restorative.

Preferred:

```text
Memory weakened
Signal unstable
Relic fractured
Rescue available
```

Avoid:

```text
FAILED
BAD JOB
LOSS
PENALTY
YOU BROKE YOUR STREAK
```

Typography tone must support honest recall.

---

# 41. Success Language

Success should feel meaningful without reward spam.

Preferred:

```text
Stabilized
Checkpoint reached
Relic restored
Expedition complete
```

Avoid:

```text
AMAZING!!!
EPIC WIN!!!
+500 XP
LEGENDARY!
```

No excessive punctuation.

---

# 42. Typography Motion Rules

Text motion exists only to support:

- reveal,
- state transition,
- number change,
- hierarchy change,
- meaningful completion.

Approved future categories may include:

```text
AA-TextFade-01
AA-TextReveal-01
AA-NumberFlow-01
AA-StatusCrossfade-01
```

Avoid:

- letter-by-letter animation for normal UI,
- typewriter effects,
- bouncing text,
- rotating words,
- perpetual text shimmer.

---

# 43. Number Animation Rule

Number animation may be used when:

- the change is meaningful,
- the animation is brief,
- the value remains readable,
- it does not resemble a slot machine.

Do not animate every counter update.

Reduced Motion:

```text
instant value replacement
or
short opacity crossfade
```

---

# 44. Ritual Copy Rule

Ritual language should be rare.

Use short phrases that preserve clarity.

Good:

```text
SIGNAL LOCKED
RELIC RESTORED
EXPEDITION COMPLETE
ORACLE RESOLVED
```

Avoid excessive mystical prose.

Bad:

```text
THE ASTRAL VESSEL OF THY MEMORY HAS AWAKENED
```

Anki Alive is atmospheric, not theatrical fantasy.

---

# 45. Feature Typography Nuance

Feature identity may adjust typography subtly.

## Expedition

- structured,
- directional,
- practical,
- measured.

## Oracle

- slightly wider tracking,
- quiet ceremonial labels,
- circular alignment motifs.

## Rescue

- calm,
- human,
- restorative,
- never alarming.

## Nemesis

- tighter,
- stronger,
- controlled tension.

## Fragment

- sparse,
- mysterious,
- incomplete labels where meaningful.

## Relic

- archival,
- durable,
- quiet prestige.

## Memory World

- cartographic,
- geographic,
- atmospheric,
- strong region naming.

These are nuances, not separate typography systems.

---

# 46. Focus Mode Typography

Focus Mode should retain the same type hierarchy.

It may reduce:

- ritual labels,
- decorative tracking,
- expressive typography motion,
- secondary metadata.

It must not:

- shrink important text,
- lower contrast,
- hide essential progress,
- feel visually broken.

---

# 47. Reduced Motion Typography

All animated text must remain understandable without motion.

Fallbacks:

- static text,
- opacity-only transition,
- instant replacement.

No information may depend on animation order alone.

---

# 48. Accessibility Rules

Typography must support:

- scalable text,
- strong contrast,
- keyboard navigation context,
- readable small text,
- clear focus labels,
- non-color-only state communication.

Avoid important text below:

```text
11 px
```

except for tightly controlled diagnostic contexts.

---

# 49. AI Typography Checklist

Before shipping a screen, an AI agent must verify:

1. What is the primary message?
2. Is there exactly one strongest typographic focal point?
3. Are role names mapped to approved type roles?
4. Is body copy readable?
5. Are metrics appropriately prominent?
6. Are labels necessary?
7. Is uppercase restrained?
8. Is Ritual typography rare?
9. Is accent text semantically justified?
10. Is any glow/gradient text present without approval?
11. Does Focus Mode remain elegant?
12. Does reduced motion preserve all information?

---

# 50. AI Typography Failure Patterns

Reject or revise typography that shows:

- giant KPI numbers everywhere,
- too many heading sizes,
- random font families,
- excessive uppercase,
- pseudo-occult fonts,
- gradient text,
- glowing body copy,
- microscopic metadata,
- arcade score styling,
- overly wide paragraphs,
- excessive bold,
- every label looking equally important.

---

# 51. Canonical Conflict Resolution

When typography decisions conflict:

```text
Product Principles
↓
Visual Constitution
↓
Typography & Information Hierarchy
↓
Design System
↓
Feature Spec
↓
Component implementation
```

The higher-level rule wins.

---

# 52. Final Typography Principle

When uncertain, ask:

> **Can the learner understand the hierarchy before noticing the styling?**

If yes, typography is doing its job.

And when two treatments are equally readable:

> **Choose the one that feels quieter, more precise, and more durable over time.**

---

# Typography North Star

> **Modern clarity with a restrained ceremonial edge: readable first, atmospheric second, memorable always.**
