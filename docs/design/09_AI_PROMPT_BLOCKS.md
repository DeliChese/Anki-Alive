# Anki Alive — AI Prompt Blocks

Status: CANONICAL
Pack: 9
Applies to: AI coding agents, design agents, code reviewers, UI auditors, feature implementers, image-generation prompting, handoffs, and fresh-session continuation
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
- `08_UI_REVIEW_CHECKLIST.md`
- `02_DESIGN_SYSTEM.md`
- `01_PRODUCT_PRINCIPLES.md`
- `AGENTS.md`

---

## 1. Purpose

This file contains reusable prompt blocks for AI agents working on Anki Alive.

These prompts exist to reduce dependence on model-specific taste, memory, or conversational context.

A new AI should be able to enter the repository, read the canonical documents, and continue visual work without relying on a previous chat.

These prompts are not substitutes for canonical documentation.

They are entry points into it.

---

# 2. Universal Rule

Every AI prompt for meaningful UI work should contain or imply:

```text
Read canonical docs first.
Do not invent a new visual language.
Preserve recall dominance.
Use semantic tokens.
Use canonical component IDs.
Use canonical effect IDs.
Respect motion ceilings.
Define Focus Mode behavior.
Define Reduced Motion behavior.
Preserve accessibility.
Preserve reviewer performance.
Do not call the work done before UI self-audit.
```

---

# 3. Fresh AI Session Bootstrap

Use this when opening a completely new chat or model.

```text
You are continuing development of Anki Alive.

Before making changes, read:
- AGENTS.md
- PROJECT.md
- docs/01_PRODUCT_PRINCIPLES.md
- docs/02_DESIGN_SYSTEM.md
- docs/03_ARCHITECTURE.md
- docs/04_DATA_MODEL.md
- docs/06_DECISIONS.md
- the current phase spec
- the latest relevant handoff
- all canonical files under docs/design/

Treat these files as the source of truth.

For any UI or visual work:
- follow Arcane Memory Interface,
- preserve Dark Arcane + Modern Minimal,
- use existing semantic tokens,
- use canonical component IDs,
- use approved effect IDs from the Effects Catalog,
- do not silently invent new motion, surface, typography, or feature metaphors,
- preserve Focus Mode and Reduced Motion,
- preserve accessibility,
- keep reviewer UI visually subordinate to the card,
- do not introduce casino, cyberpunk, fantasy-skin, or generic SaaS dashboard drift.

Before implementing meaningful UI, briefly declare:
Feature:
Primary task:
Component IDs:
Surface tier:
Typography roles:
Motion tier:
Effect IDs:
Focus Mode:
Reduced Motion:
Accessibility:
Performance:
Forbidden patterns:

Then implement the smallest coherent change that satisfies the current phase.
```

---

# 4. Low-Touch Owner Prompt

Use when the project owner wants minimal interaction.

```text
Read AGENTS.md, PROJECT.md, the current phase spec, the latest handoff, and all canonical docs under docs/design/.

Continue the current phase autonomously.

Use the existing architecture and visual system.
Run tests and CI where available.
Fix issues you can resolve without asking me.
Update relevant documentation and handoff notes as work progresses.

For visual work:
- follow canonical component IDs,
- follow canonical effect IDs,
- respect motion tiers,
- preserve Focus Mode,
- preserve Reduced Motion,
- preserve accessibility,
- do not invent new visual language without documenting why.

Only ask me when a real Anki manual test or a genuinely non-resolvable product decision is required.
```

---

# 5. Visual Implementation Prompt

Use when building a new screen or meaningful UI surface.

```text
Implement this UI using Anki Alive's canonical visual system.

Before writing code, read:
- docs/design/00_VISUAL_CONSTITUTION.md
- docs/design/01_COLOR_AND_SURFACE_DNA.md
- docs/design/02_TYPOGRAPHY_AND_INFORMATION_HIERARCHY.md
- docs/design/03_MOTION_LANGUAGE.md
- docs/design/04_EFFECTS_CATALOG.md
- docs/design/05_COMPONENT_CANON.md
- docs/design/06_FEATURE_MOOD_MAPPING.md
- docs/design/07_AI_AESTHETIC_RULES.md
- docs/design/08_UI_REVIEW_CHECKLIST.md

First provide a compact implementation declaration:

Feature:
Screen:
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
Accessibility:
Performance:
Forbidden patterns:

Then implement.

Constraints:
- reuse existing components before creating new ones,
- reuse semantic tokens,
- do not hard-code arbitrary aesthetic values,
- do not add visual dependencies unless native CSS/WAAPI is clearly insufficient,
- keep one primary visual focal point,
- do not introduce card soup,
- do not raise motion tier without semantic justification,
- do not use unapproved motion when an approved effect exists.

After implementation, run the UI Review Checklist and report remaining visual risks.
```

---

# 6. "Make It Better" Prompt

Use when the UI works but feels visually weak.

```text
Improve this UI without changing product behavior.

Do not interpret "better" as "add more effects."

Prioritize, in order:
1. hierarchy,
2. spacing,
3. alignment,
4. typography,
5. component anatomy,
6. surface coherence,
7. semantic color,
8. state clarity,
9. restrained motion only if needed.

Do not:
- add glow merely for polish,
- add gradients merely for polish,
- add cards merely to organize empty space,
- add motion merely to make the UI feel alive,
- introduce a new visual metaphor,
- change feature identity.

Use canonical tokens, components, and effect IDs.

After refinement, identify:
- what was simplified,
- what was intentionally not animated,
- what existing component/effect was reused,
- any remaining visual debt.
```

---

# 7. Screenshot Audit Prompt

Use when reviewing a screenshot.

```text
Audit this screenshot against Anki Alive's canonical visual system.

Evaluate in this order:
1. primary task clarity,
2. eye path,
3. hierarchy,
4. information density,
5. component canon,
6. typography,
7. surfaces,
8. glow,
9. feature identity,
10. AI-slop patterns,
11. casino/fantasy/cyberpunk drift,
12. Focus Mode implications,
13. accessibility risks.

Use severity labels:
BLOCKER
MAJOR
MINOR
POLISH

Do not redesign the whole screen unless necessary.

For each issue:
- identify the canonical rule being violated,
- explain why it matters,
- propose the smallest correction.

Finish with:
Overall status:
Aesthetic score: __/36
Top 3 corrections:
```

---

# 8. Motion Audit Prompt

Use when reviewing animation or motion code.

```text
Audit this motion against:
- Motion Language
- Effects Catalog
- UI Review Checklist

For every animation identify:
Semantic event:
Motion tier:
Approved effect ID:
Duration:
Easing:
Frequency:
Focus Mode behavior:
Reduced Motion behavior:
Performance implications:

Reject or revise:
- bounce-heavy easing,
- elastic overshoot,
- perpetual pulse,
- excessive stagger,
- random rotation,
- particle spam,
- screen shake,
- large blur animation,
- motion with no semantic cause,
- motion that competes with recall.

Prefer the quietest approved effect that communicates the state.

If no effect is needed, recommend no animation.
```

---

# 9. Reviewer UI Prompt

Use for anything shown during Anki review.

```text
Implement this reviewer UI under strict recall-first constraints.

Rules:
- card content is the visual authority,
- question-state motion ceiling is M0,
- answer-state motion ceiling is M1,
- post-grade M2 is allowed only for one orchestrated meaningful event,
- Tier 1 is the normal reviewer surface ceiling,
- G1 is the normal reviewer glow ceiling,
- ambient motion is off,
- particles are forbidden,
- parallax is forbidden,
- cinematic reveals are forbidden during active recall,
- normal Anki grading controls remain unobscured.

Persistent add-on UI should generally be limited to:
one compact support/progress component
+
one tiny optional state indicator

Use:
AA-ReviewProgressStrip
and existing canonical primitives where possible.

Before implementation, explain how recall dominance is preserved.

After implementation, measure or verify reviewer performance where practical.
```

---

# 10. Focus Mode Prompt

Use when implementing or reviewing Focus Mode.

```text
Create the Focus Mode version of this UI.

Preserve:
- task clarity,
- feature identity,
- essential progress,
- semantic state,
- typography hierarchy,
- accessibility.

Reduce or remove:
- M2/M3 flourish,
- ambient motion,
- particles,
- parallax,
- expressive glow,
- nonessential artwork,
- decorative metadata.

Focus Mode should not look disabled, broken, unfinished, or visually punished.

Use M0 plus essential M1 only unless a canonical rule says otherwise.

Report:
What remains:
What is suppressed:
What is replaced:
```

---

# 11. Reduced Motion Prompt

Use when implementing reduced-motion behavior.

```text
Implement Reduced Motion for this UI.

Preserve all semantic meaning.

Preferred replacements:
translation → opacity/static
scale → opacity/value change
parallax → static
particles → static highlight
multi-stage choreography → immediate resolved state + short fade
animated number → instant replacement or short crossfade

No information may depend on motion order or direction.

Do not remove important feedback.

Report each affected effect ID and its fallback.
```

---

# 12. New Component Proposal Prompt

Use only when existing Component Canon is insufficient.

```text
Determine whether this UI truly requires a new canonical component.

First inspect existing Component Canon.

If an existing component can represent the need cleanly, reuse it.

If not, propose:

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
Focus Mode:
Reduced Motion:
Accessibility:
Reuse potential:
Performance implications:

Do not implement the new component until the proposal is coherent.
```

---

# 13. New Effect Proposal Prompt

Use only when Effects Catalog is insufficient.

```text
Determine whether a new Anki Alive effect is truly necessary.

First inspect the existing Effects Catalog.

If an approved effect can communicate the event, reuse it.

If not, propose:

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

Reject the proposal yourself if it exists mainly for novelty.
```

---

# 14. New Visual Token Prompt

Use when a color/surface/spacing token appears missing.

```text
Determine whether a new semantic visual token is required.

Do not add a raw value merely because a component needs a slightly different appearance.

First ask:
- does an existing semantic role fit?
- can hierarchy be solved with spacing/typography instead?
- is the difference reusable?
- is it semantic rather than decorative?

If a new token is still justified, propose:

Token name:
Semantic meaning:
Where used:
Why existing tokens are insufficient:
Dark behavior:
Light behavior if applicable:
Accessibility implications:
Affected components:
```

---

# 15. Expedition Prompt

```text
Design or implement this Expedition UI using canonical Expedition DNA.

Must preserve:
- cartographic path / node geometry,
- bounded nearby progress,
- steady movement,
- clear closure,
- muted amber/path-light accent,
- directional copy,
- low-to-medium density.

Preferred components/effects:
AA-ExpeditionTrack
AA-CheckpointNode
AA-ReviewProgressStrip
AA-ExpeditionAdvance-01
AA-CheckpointActivate-01
AA-ExpeditionComplete-01

Never:
- quest-log framing,
- racing UI,
- speed lines,
- XP,
- moving finish line,
- arcade meters.

During review, remain M0–M1.
```

---

# 16. Oracle Prompt

```text
Design or implement this Oracle UI using canonical Oracle DNA.

Must preserve:
- observational uncertainty,
- radial/orbit/lens geometry,
- cool instrument-glass nuance,
- pale cyan/moonlit accent,
- alignment/lock/reveal motion verbs,
- low visual density.

Preferred components/effects:
AA-OracleSurface
AA-OracleLock-01
AA-OracleReveal-01
AA-OracleReveal-02 only for rare explicitly approved centerpiece moments

Never:
- tarot styling,
- crystal-ball cliché,
- spinning wheel,
- fortune-teller language,
- outcome leakage before review.
```

---

# 17. Rescue Prompt

```text
Design or implement this Rescue UI using canonical Rescue DNA.

Must preserve:
- fragility without shame,
- broken/repaired signal geometry,
- teal restorative accent,
- stabilization/reconnection motion,
- calm recovery copy,
- low visual density.

Preferred components/effects:
AA-RescueSurface
AA-RescueSignal-01
AA-RescueStabilize-01

Never:
- alarm aesthetics,
- punishment,
- red flashing,
- panic pulse,
- failure-shame language.
```

---

# 18. Nemesis Prompt

```text
Design or implement this Nemesis UI using canonical Nemesis DNA.

Must preserve:
- persistent resistance,
- angular/compressed geometry,
- obsidian/crimson-violet material,
- weaken/release motion,
- data-grounded difficulty,
- low-to-medium density.

Preferred components/effects:
AA-NemesisSurface
AA-NemesisPressure-01
AA-NemesisWeaken-01
AA-NemesisDefeat-01

Never:
- monster/boss framing,
- health bars,
- screen shake,
- combat effects,
- violent learner-directed language.
```

---

# 19. Fragments Prompt

```text
Design or implement this Fragment UI using canonical Fragment DNA.

Must preserve:
- incomplete geometry,
- crystalline assembly,
- lavender/spectral accent,
- resonance/convergence motion,
- discovery without gambling language,
- low visual density.

Preferred components/effects:
AA-FragmentModule
AA-FragmentResonate-01
AA-FragmentAssemble-01
AA-FragmentReveal-01

Never:
- loot-box framing,
- rarity stars,
- prize drops,
- sparkle spam,
- slot-machine timing.
```

---

# 20. Relics Prompt

```text
Design or implement this Relic UI using canonical Relic DNA.

Must preserve:
- durable historical identity,
- symmetric artifact geometry,
- mineral/auric material,
- restrained prestige,
- real memory history,
- formation/fracture/restoration states.

Preferred components/effects:
AA-RelicTile
AA-RelicAwaken-01
AA-RelicFracture-01
AA-RelicRestore-01

Never:
- collectible-card framing,
- loot rarity,
- item-spin animation,
- treasure drop,
- shiny gold overload.
```

---

# 21. Memory World Prompt

```text
Design or implement this Memory World UI using canonical Memory World DNA.

Must preserve:
- data-grounded cartography,
- regions/constellations/topography,
- atmospheric blue-green/slate accent,
- spatial continuity,
- reflective long-term history,
- medium density maximum.

Preferred components/effects:
AA-WorldRegionCard
AA-WorldBeacon-01
AA-WorldRegionReveal-01
AA-WorldTransition-01
AA-AmbientDrift-01 outside recall only

Never:
- fantasy kingdoms,
- strategy-game territory UI,
- arbitrary biomes,
- noisy map markers,
- constant camera motion.
```

---

# 22. Today Screen Prompt

```text
Design or implement the Today screen as the neutral meeting place of Anki Alive.

Primary goals:
- establish today's memory state,
- give a clear entry into Expedition,
- create light curiosity,
- avoid information overload.

Preferred structure:
1. temporal header
2. memory-state summary
3. AA-MemoryCore hero
4. Expedition entry CTA
5. AA-SignalRow list
6. optional quiet history snapshot

Rules:
- one hero only,
- no dashboard wall,
- no KPI tile grid,
- feature signals remain secondary to the main action,
- atmosphere remains quiet.
```

---

# 23. Generated Art Direction Prompt

Use when generating visual assets for Anki Alive.

```text
Create artwork for Anki Alive under the Arcane Memory Interface art direction.

Core visual language:
Dark Arcane + Modern Minimal
living memory observatory
mineral artifacts
cartographic discovery
luminous signals
precise geometry
quiet atmosphere

Requirements:
- low-chroma base,
- restrained luminous accents,
- premium but not glossy,
- atmospheric but not noisy,
- no readable UI text baked into the artwork unless explicitly requested,
- no casino aesthetics,
- no fantasy RPG skin,
- no cyberpunk neon overload,
- no cartoon reward language,
- no generic sci-fi HUD.

The asset must support UI rather than replace controls or hierarchy.

Feature:
[FEATURE]

Feature DNA:
[PASTE RELEVANT FEATURE MOOD BLOCK]

Composition:
[DESCRIBE ROLE, NOT UI LOGIC]

Leave sufficient negative space for UI integration.
```

---

# 24. Generated Art Review Prompt

```text
Audit this generated asset for Anki Alive.

Check:
- visual constitution fit,
- feature identity,
- palette fit,
- surface/material fit,
- saturation,
- visual noise,
- negative space,
- repeat-use durability,
- casino/fantasy/cyberpunk drift,
- whether the asset competes with UI hierarchy.

Result:
PASS
PASS WITH NOTES
REVISE
REJECT

Provide the smallest edits needed.
```

---

# 25. Visual Refactor Prompt

Use when cleaning existing frontend code.

```text
Refactor this UI toward the canonical Anki Alive design system without changing product behavior.

Goals:
- replace hard-coded visual values with semantic tokens,
- map anonymous UI to canonical component IDs,
- replace custom animations with approved effect IDs,
- reduce card soup,
- reduce effect soup,
- preserve feature identity,
- preserve accessibility,
- preserve Focus Mode,
- preserve Reduced Motion,
- preserve reviewer performance.

Do not introduce a new framework or visual dependency unless absolutely necessary.

Report:
Reused canonical primitives:
Removed one-off styling:
Remaining visual debt:
```

---

# 26. Visual Dependency Evaluation Prompt

```text
Evaluate whether this visual/motion dependency should be added to Anki Alive.

Assess:
1. exact repeated need,
2. whether CSS/WAAPI can solve it,
3. bundle/runtime cost,
4. Anki WebView compatibility,
5. maintenance risk,
6. accessibility,
7. Reduced Motion support,
8. reviewer performance risk,
9. whether the library would pull the product away from canonical styling.

Recommendation:
ADD
DO NOT ADD
DEFER

If ADD, define the narrow permitted use.
```

---

# 27. Pre-Merge Visual Audit Prompt

```text
Run a pre-merge visual audit for this change.

Read:
- all canonical docs under docs/design/
- relevant Product Principles
- relevant feature spec

Check:
- recall integrity,
- primary task,
- hierarchy,
- component canon,
- typography,
- surfaces,
- feature identity,
- motion/effect IDs,
- Focus Mode,
- Reduced Motion,
- accessibility,
- performance,
- AI-slop drift,
- casino/fantasy/cyberpunk drift.

Return:

Overall status:
PASS / PASS WITH NOTES / REVISE / BLOCKED

Blockers:
Major:
Minor:
Polish:

Aesthetic score:
__/36

Canonical drift:
NONE / DOCUMENTED / NEEDS DECISION

Do not claim PASS if required tests or host checks were not actually performed.
```

---

# 28. UI Self-Audit Prompt

Use immediately before saying visual work is done.

```text
Before declaring this UI done, perform a self-audit.

Report:

Primary visual decision:
Primary user task:
Feature identity:
Component IDs used:
Effect IDs used:
Motion tier:
Surface tier:
What was intentionally restrained:
What was intentionally not animated:
Focus Mode result:
Reduced Motion result:
Accessibility result:
Performance result:
Remaining aesthetic risk:
Visual debt:
Aesthetic score: __/36

If any BLOCKER or unresolved MAJOR issue exists, do not call the UI done.
```

---

# 29. Handoff Prompt

```text
Create/update the visual handoff for this work.

Include:

Completed visual scope:
Canonical components used:
Canonical effects used:
New tokens/components/effects introduced:
Feature identity decisions:
Focus Mode status:
Reduced Motion status:
Accessibility status:
Performance status:
Known visual compromises:
Deferred polish:
Screens requiring manual visual verification:
Relevant screenshots/assets:
Next-agent instructions:

The next AI should not need the current chat to understand the visual state.
```

---

# 30. Fresh Model Continuation Prompt

Use when changing from one model/provider to another.

```text
You are taking over Anki Alive from another AI.

Do not assume the previous model's taste or hidden context.

The repository is authoritative.

Read:
- AGENTS.md
- PROJECT.md
- Product Principles
- Architecture
- Data Model
- Decisions
- current phase spec
- latest handoff
- every canonical file under docs/design/

Preserve all accepted decisions.

For UI work, do not redesign from personal taste.
Use:
- canonical components,
- semantic tokens,
- canonical feature geometry,
- canonical motion verbs,
- approved effect IDs,
- defined Focus Mode behavior,
- defined Reduced Motion behavior.

Before changing UI, produce a compact visual implementation declaration.

After changing UI, run the canonical UI Review Checklist.

If the existing implementation appears to conflict with canonical docs, report the conflict before normalizing it.
```

---

# 31. Technical AI Guardrail Prompt

Use specifically for an AI that is strong technically but weak visually.

```text
Treat visual design as a constrained engineering system.

Do not make aesthetic choices from intuition.

For every UI decision, derive it from:
- semantic purpose,
- canonical component,
- semantic token,
- feature mood mapping,
- motion tier,
- approved effect ID.

If you are unsure what looks better:
- choose less motion,
- choose less glow,
- choose fewer containers,
- choose clearer typography,
- choose more whitespace,
- choose the existing canonical primitive.

Do not improvise.

When the canon does not contain an answer, propose an extension instead of styling ad hoc.
```

---

# 32. High-Creativity AI Guardrail Prompt

Use for a model likely to over-design.

```text
You may be visually creative only inside the canonical Anki Alive design space.

Creativity is welcome in:
- composition,
- geometry refinement,
- meaningful feature symbolism,
- data-grounded visual identity,
- carefully proposed reusable primitives.

Creativity is not permission to:
- increase motion tier,
- add more glow,
- add more gradients,
- add new visual themes,
- add spectacle,
- add decorative UI,
- change feature metaphors.

Before introducing any novel visual treatment, explain:
What semantic gap does this solve?
Why can existing canon not solve it?
How will it degrade in Focus Mode and Reduced Motion?
Why will it remain tasteful after repeated daily use?
```

---

# 33. "Do Not Touch the Design" Prompt

Use for purely technical changes.

```text
This task is technical only.

Do not alter:
- layout,
- spacing,
- typography,
- color,
- surfaces,
- component anatomy,
- motion,
- feature visual identity

unless required to fix a concrete bug.

If a visual change becomes necessary, identify it explicitly before making it.

Preserve current canonical UI behavior.
```

---

# 34. "Audit, Don't Rewrite" Prompt

```text
Audit the current implementation against canonical Anki Alive docs.

Do not rewrite large sections merely for stylistic preference.

Identify:
- actual canonical violations,
- architecture drift,
- component drift,
- token drift,
- motion/effect drift,
- accessibility gaps,
- Focus Mode gaps,
- Reduced Motion gaps,
- performance risks.

For each issue, propose the smallest correction.

Preserve working code that already satisfies the canon.
```

---

# 35. Manual Anki Test Prompt

Use when the AI needs the owner to test locally.

```text
Prepare the smallest manual Anki validation request.

Do not ask the owner to inspect technical internals unnecessarily.

Tell them only:
1. what to Pull/Sync,
2. whether Anki should be restarted,
3. exactly what screen/action to open,
4. exactly what to observe,
5. what screenshot/log to send back if needed.

Keep the test short.

Separate:
- automated evidence already passed,
- manual evidence still needed.
```

---

# 36. Visual Bug Report Prompt

```text
Analyze this visual bug using canonical Anki Alive rules.

Identify:
Expected canonical behavior:
Observed behavior:
Affected component:
Affected effect:
Likely layer:
- token
- component
- layout
- motion
- integration
- host compatibility

Propose the smallest fix.

Do not redesign unrelated UI.
```

---

# 37. Phase Visual Planning Prompt

Use before a new development phase begins.

```text
Create the visual plan for this phase before implementation.

Read:
- current phase spec,
- Product Principles,
- all canonical docs under docs/design/,
- latest handoff.

Identify:

Screens/surfaces:
Primary tasks:
Canonical components:
New components potentially required:
Surface tiers:
Typography roles:
Feature DNA:
Motion ceilings:
Approved effects:
New effects potentially required:
Focus Mode states:
Reduced Motion states:
Accessibility concerns:
Reviewer performance concerns:
Manual visual tests needed:

Do not implement speculative polish outside phase scope.
```

---

# 38. Prompt for Choosing Between Two Designs

```text
Compare Design A and Design B using Anki Alive's canonical rules.

Do not choose based on novelty.

Score each on:
- recall clarity,
- primary task clarity,
- hierarchy,
- feature identity,
- cross-feature cohesion,
- typography,
- surface restraint,
- motion semantics,
- accessibility,
- Focus Mode,
- Reduced Motion,
- long-term tastefulness.

Prefer the design that is:
clearer,
quieter,
more semantic,
more reusable,
less distracting,
more durable.

If they are otherwise equal, choose the one with fewer effects.
```

---

# 39. Prompt for Rejecting Bad Design Direction

```text
Evaluate whether this design direction conflicts with Anki Alive.

Check for:
- casino behavior,
- fantasy skinning,
- cyberpunk drift,
- generic SaaS drift,
- dead minimalism,
- reviewer distraction,
- over-animation,
- feature identity conflict,
- product-principle conflict.

If it conflicts:
- state the exact conflict,
- do not soften the assessment merely because the design is visually attractive,
- preserve any useful underlying idea,
- translate that idea back into canonical Anki Alive language.
```

---

# 40. Prompt for Adding "More Life"

```text
Make this surface feel more alive without increasing distraction.

Interpret "alive" as:
- state evolution,
- meaningful data-driven visual change,
- stronger feature identity,
- clearer progress,
- subtle material depth,
- one restrained ambient system outside recall if justified.

Do not make everything move.

Use canonical effects only.

The product is alive because memory changes.
```

---

# 41. Prompt for Adding "More Arcane"

```text
Make this surface feel more Arcane Memory Interface without using fantasy clichés.

Prefer:
- radial/precise geometry,
- cartographic or archival structure,
- mineral materials,
- sparse ceremonial labels,
- controlled local light,
- mystery through reveal sequencing.

Do not add:
- runes for decoration,
- tarot motifs,
- parchment,
- faux occult fonts,
- generic purple glow,
- ornate fantasy borders.
```

---

# 42. Prompt for Adding "More Premium"

```text
Make this UI feel more premium through craft, not effect quantity.

Improve:
- spacing,
- alignment,
- typographic rhythm,
- proportion,
- surface hierarchy,
- icon consistency,
- motion timing,
- state clarity.

Do not automatically add:
- glass,
- blur,
- gradients,
- gold,
- giant shadows,
- more animation.

Premium quality should come from restraint and precision.
```

---

# 43. Minimal Visual Decision Record

Use when a small but meaningful new visual rule is accepted.

```text
Visual decision:
Status:
Context:
Decision:
Reason:
Affected components/features:
Focus Mode impact:
Reduced Motion impact:
Performance impact:
Alternatives considered:
```

Important visual decisions should live in the repository.

---

# 44. Prompt Block Composition Rule

Do not paste every prompt in this file into every task.

Choose the smallest combination that matches the job.

Typical combinations:

```text
Fresh implementation
→ Fresh AI Session Bootstrap
+ Visual Implementation Prompt
+ Feature-specific prompt
+ UI Self-Audit Prompt
```

```text
Reviewer feature
→ Visual Implementation Prompt
+ Reviewer UI Prompt
+ relevant feature prompt
+ Pre-Merge Visual Audit Prompt
```

```text
Visual polish
→ Make It Better Prompt
+ Screenshot Audit Prompt
```

```text
New effect
→ New Effect Proposal Prompt
+ Motion Audit Prompt
```

---

# 45. Model-Agnostic Rule

These prompts must not depend on a specific provider.

They should work with:

- general chat models,
- coding agents,
- repository agents,
- design-review agents,
- future AI systems.

The repository carries the visual memory.

The model is replaceable.

---

# 46. Final Prompt Contract

When giving an AI visual authority over Anki Alive, the owner should be able to say:

> Read the canonical design docs. Use the approved components and effects. Do not improvise outside the visual system. Audit yourself before calling it done.

That should be enough to place the AI on the correct track.

---

# AI Prompt North Star

> **The repository remembers the taste so the model does not have to.**
