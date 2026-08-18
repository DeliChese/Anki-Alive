# 09_ACCESSIBILITY.md

# Anki Alive — Accessibility and Sensory Design

## 1. Purpose

This document defines accessibility and sensory-load requirements for Anki Alive.

Accessibility is not an afterthought.

Because Anki Alive introduces additional presentation layers beyond plain reviewing, it has an increased responsibility to avoid:

- visual overload,
- motion discomfort,
- color-only meaning,
- keyboard traps,
- focus confusion,
- low-contrast interfaces,
- attention hijacking.

The goal is not just compliance.

The goal is inclusive, sustainable studying.

---

## 2. Accessibility Goals

Anki Alive should be usable by learners who may need:

- reduced motion,
- strong contrast,
- keyboard-first navigation,
- lower sensory load,
- clear focus indication,
- screen magnification,
- non-color state distinction,
- minimal interruption.

The add-on should remain a support layer, not an obstacle.

---

## 3. Product-Level Accessibility Principles

### A11Y01 — Studying Must Remain Possible Without Extra Stimulus

The user must be able to review effectively even if:

- motion is reduced,
- non-essential reveals are suppressed,
- decorative visuals are minimized,
- sound is disabled.

### A11Y02 — Focus Mode Is Accessibility-Relevant

Focus Mode is not only a productivity preference.

For some users, it is the primary accessible mode.

### A11Y03 — State Must Not Depend on Color Alone

Any state difference that matters must also be represented by:

- labels,
- shapes,
- icons,
- patterns,
- position,
- clear wording.

### A11Y04 — Motion Must Be Optional

Any major or repeated motion should be reducible or removable.

### A11Y05 — Keyboard Support Is Essential

Users should not need the mouse for core interactions.

### A11Y06 — Interruption Must Be Controlled

Event reveals should not trap users or break their flow.

---

## 4. Focus Mode Requirements

Focus Mode must support:

- minimal event presentation
- reduced motion
- simpler overlays
- lower ambient decoration
- clean reviewer view
- stable layout

Focus Mode should be available without hunting through deep settings.

It should be easy to toggle and easy to understand.

### Focus Mode should not:

- disable essential study information,
- alter scheduling,
- hide grading controls,
- break session tracking,
- create a degraded-feeling product.

---

## 5. Motion Accessibility

### 5.1 Motion Categories

#### Essential motion

Motion that clarifies state change and is difficult to remove entirely without confusion.

Example:

- short progress transition,
- subtle reveal state change.

#### Optional motion

Motion that can be reduced or removed.

Example:

- ambient pulsing,
- decorative drift,
- major reveal flourish.

### 5.2 Reduced Motion Behavior

When reduced motion is enabled:

- transitions should shorten or disappear,
- pulsing should stop,
- parallax should be disabled,
- repeated ambient animation should stop,
- major reveals should become mostly static,
- large movement should become simple fade or instant state change.

### 5.3 Motion Constraints

Avoid:

- rapid flashing,
- repeated shimmer on important surfaces,
- bounce or elastic movement,
- forced long transitions,
- looping visual effects competing with card reading.

---

## 6. Contrast and Readability

### 6.1 Contrast Philosophy

Dark interfaces can easily become low-contrast.

Anki Alive must preserve sufficient contrast between:

- text and background,
- controls and surfaces,
- focus indicators and surroundings,
- semantic state markers and neutral UI.

### 6.2 Contrast Guidelines

- primary text should be clearly readable on all major surfaces,
- secondary text should remain readable, not decorative haze,
- subtle borders should not be the only separation mechanism,
- low-contrast atmospheric surfaces should never hold critical text.

### 6.3 Readability Rules

- avoid long thin all-caps paragraphs,
- avoid tiny metadata in critical workflows,
- use line spacing appropriate for body copy,
- keep important stat blocks readable at a glance.

---

## 7. Color-Independence

Examples of required non-color cues:

- Oracle vs Rescue vs Nemesis should differ in iconography, not only accent color.
- Fragile vs stable memory should differ in wording and symbol, not only hue.
- Hidden vs ready Fragment states should differ in progress shape and label.

Possible supporting differences:

- solid vs outlined forms,
- distinct geometry,
- label text,
- status patterns,
- strength of stroke,
- card ordering,
- icon family.

---

## 8. Keyboard Navigation

### 8.1 Principles

All core workflows should be keyboard-friendly.

### 8.2 Required Support Areas

- starting an Expedition
- dismissing reveals
- navigating settings
- toggling Focus Mode
- moving through major panels
- operating buttons and toggles

### 8.3 Focus Behavior

Keyboard focus must be:

- visible,
- predictable,
- never lost invisibly,
- restored sensibly after overlays close.

### 8.4 Focus Indicator

A clear visible focus style is required.

Do not rely on browser-default behavior alone if it is too subtle in the dark theme.

---

## 9. Screen Density and Cognitive Load

Not every accessibility issue is about impairment labels.

Dense, noisy UI harms many users.

Therefore:

- reviewer overlays must remain sparse,
- dashboards must avoid metric spam,
- event text must stay short,
- there should be only one main action at a time,
- multiple simultaneous events should be orchestrated.

This is especially important for learners with ADHD, fatigue, or exam stress.

---

## 10. Event Reveal Accessibility

Event reveals should:

- appear after the answer, not during recall,
- be short and understandable,
- be dismissible quickly,
- support keyboard dismissal,
- avoid blocking future review for long,
- avoid forcing the user through multiple stacked reveals.

If multiple events are queued, prefer summarization or deferral.

---

## 11. Sensory Load by Screen

### 11.1 Reviewer

Most sensitive context.

Must be the quietest screen.

### 11.2 Today

May contain atmosphere and a hero visual, but should remain readable and uncluttered.

### 11.3 History / Vault / World

Can tolerate more richness because they are exploratory screens rather than active recall surfaces.

Even so, they should remain navigable and not overwhelm.

---

## 12. Audio Accessibility

If sounds exist in the future:

- sounds must be optional,
- default volume should be restrained,
- there should be separate control for sound enablement,
- critical state must not depend on sound,
- avoid sharp or startling sounds.

---

## 13. Reduced Information Mode

In addition to Focus Mode, some interfaces may benefit from simplified content tiers.

For example:

- compact signal rows,
- fewer visible secondary stats,
- reduced lore-like text,
- static event summaries instead of animated reveals.

This should be considered during implementation if the standard UI becomes too dense.

---

## 14. Text Content Accessibility

### 14.1 Copy Style

Prefer:

- clear verbs,
- short phrases,
- direct meaning.

Examples:

- "Memory stabilized."
- "Oracle revealed."
- "Nemesis weakening."
- "Expedition complete."

Avoid:

- vague poetic filler,
- sarcasm,
- shame language,
- dense explanatory paragraphs during review.

### 14.2 Localization Readiness

Copy should be structurally simple enough that future localization is possible.

Avoid excessively culture-specific reward slang.

---

## 15. Empty States and Emotional Accessibility

Empty states should not imply failure.

Examples:

Good:
- "No active Nemesis."
- "No fragile memories detected."
- "No Relics yet."

Bad:
- "You haven't earned anything."
- "Nothing impressive here."
- "Come back when you're serious."

Emotional tone matters for accessibility too.

---

## 16. Error States

Errors should be:

- understandable,
- recoverable,
- non-blaming.

Example qualities:

- explain what failed,
- explain what still works,
- explain what the user can do next.

The add-on should never make a user fear that their studying is ruined because a cosmetic or narrative feature failed.

---

## 17. Reading Order and Structure

When building screens:

- preserve logical heading order,
- group related content,
- maintain predictable layout hierarchy,
- avoid using decoration to imply meaning without textual structure.

If web content is used, semantic markup should be preferred where practical.

---

## 18. Magnification and Resizing

The UI should remain usable under enlarged text and window resizing.

Avoid:

- fixed-height text containers clipping content,
- tiny badges carrying critical meaning,
- layouts that collapse into unusable clutter.

Plan for desktop scaling and varied display sizes.

---

## 19. Pointer Targets

Controls should be comfortably targetable.

Important controls should not rely on tiny icons alone.

If an icon-only button is used, it should have:

- sufficient hit area,
- visible hover/focus states,
- accessible labeling.

---

## 20. Feature-Specific Accessibility Notes

### 20.1 Expedition

- Progress must be readable numerically and visually.
- Checkpoints should have labels or tooltips.
- Completion should not require animation to understand.

### 20.2 Oracle

- Reveal should be understandable even with motion disabled.
- Prediction outcome must not rely on a color swap only.
- Score display should remain readable at a glance.

### 20.3 Rescue

- Fragility should be communicated by label and symbol.
- Stabilization feedback should remain clear in reduced-motion mode.

### 20.4 Nemesis

- Encounter surfaces should not become visually aggressive to the point of distraction.
- "Challenge" should not become a stress spike.

### 20.5 Fragments

- Hidden/ready/revealed states must be distinguishable by more than glow.
- Progress should be numerically or structurally visible.

### 20.6 Relics

- Formation/fracture states should remain clear without animation.
- Vault browsing should support keyboard navigation.

### 20.7 Memory World

- World exploration should have a simplified information path.
- Atmospheric visuals must not hide labels and interactive regions.

---

## 21. Accessibility QA Checklist

Before shipping a feature, validate:

- Can the feature be used with keyboard only?
- Is focus visible at every interaction point?
- Can the feature be understood with reduced motion?
- Is critical meaning preserved without color?
- Is the text readable in the default dark theme?
- Does the feature avoid interrupting recall?
- Can the user dismiss or bypass non-essential reveals?
- Does Focus Mode remain coherent?
- Are empty and error states respectful?
- Does the UI remain understandable under larger text or tighter window sizes?

---

## 22. Accessibility Tiers by Phase

### Phase 1 — Expedition
Minimum:
- visible focus states
- keyboard support for session controls
- readable progress
- reduced-motion-safe checkpoint reveal

### Phase 2 — Oracle
Minimum:
- non-color result distinction
- keyboard dismiss
- short reveal duration
- reduced-motion fallback

### Phase 3 — Rescue
Minimum:
- clear fragile/stabilized wording
- no panic framing
- quiet reveal behavior

### Phase 4 — Nemesis
Minimum:
- no over-aggressive motion
- readable challenge state
- keyboard-safe encounter UI

### Phase 5 — Fragments
Minimum:
- clear progress readability
- hidden/ready/revealed distinction without color only

### Phase 6 — Relics
Minimum:
- vault navigation accessibility
- clear fracture/restoration states

### Phase 7 — Memory World
Minimum:
- simplified navigation path
- readable region/state labeling
- lower-sensory view option

---

## 23. Known Accessibility Risks to Watch

Common risks for this product direction:

- too much low-contrast glow on dark surfaces,
- event reveals stacking up,
- over-reliance on ambient animation,
- mystery states becoming vague,
- tiny labels in analytics/history screens,
- feature-specific iconography becoming too abstract,
- Focus Mode being implemented too late.

These risks should be reviewed repeatedly, not once.

---

## 24. Accessibility as Product Quality

Accessibility here is not separate from product quality.

If the UI is calmer, clearer, easier to dismiss, keyboard-friendly, and respectful of attention, it becomes better for nearly all learners.

That is especially important because the product deals directly with concentration and memory.

---

# Accessibility North Star

> **Anki Alive should make studying more engaging without making studying harder.**
