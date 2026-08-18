# 01_PRODUCT_PRINCIPLES.md

# Anki Alive — Product Principles

This document defines product rules that should remain stable across features and development phases.

These principles are stronger than individual feature ideas.

If a proposed feature conflicts with a principle, the feature should change first.

---

## P01 — The Game Is the Memory

Progress must primarily come from real memory behavior.

Preferred sources include:

- recall outcomes,
- stability,
- difficulty,
- retrievability,
- review history,
- lapse history,
- card age,
- interval growth,
- long-term survival,
- meaningful session completion.

Avoid creating progress systems that could function equally well without Anki data.

If a mechanic could be copied into any generic timer app without losing meaning, it should be questioned.

---

## P02 — Recall Is the Center of the Experience

Nothing should become more important than answering the card.

During the recall moment:

- the card content has priority,
- motivational UI should remain quiet,
- animations should not compete for attention,
- prediction systems must not leak hints,
- events should generally reveal after the response.

The system surrounds recall.

It does not replace recall.

---

## P03 — Honest Failure Is Valuable

Pressing `Again` is a correct action when the learner does not remember.

Therefore:

- `Again` must never reduce an artificial score,
- `Again` must never destroy a reward,
- `Again` must never shame the learner,
- `Again` must never make progression obviously worse than lying with `Good`.

A failed recall may:

- create a Rescue,
- strengthen Nemesis status,
- fracture a Relic,
- change future predictions,
- generate a recovery opportunity.

But the user should never feel punished for telling the truth.

---

## P04 — Never Reward Dishonest Grading

No important reward should be obtainable merely by repeatedly pressing `Good` or `Easy`.

Where possible, progression should use signals such as:

- later successful recalls,
- stability growth,
- difficulty,
- lapse history,
- historical performance,
- session consistency,
- scheduler-backed outcomes.

If a system creates pressure to choose a higher grade than deserved, redesign it.

---

## P05 — Completion Must Be Real

Anki Alive may use unfinished-task tension, nearby checkpoints, and visible progress.

However:

> The finish line must not constantly move.

When the learner completes an Expedition:

- acknowledge completion,
- preserve closure,
- do not immediately manufacture another mandatory objective,
- allow the learner to stop cleanly.

"One more" prompts may point to a nearby existing closure point.

They must not create an infinite chain.

---

## P06 — Use Curiosity, Not Deception

Mystery is allowed.

Dishonesty is not.

The system may hide:

- which card is an Oracle target,
- which event lies ahead,
- what a Fragment will reveal.

But it must not fake:

- probabilities,
- randomness,
- rarity,
- predictions,
- progress,
- memory state.

If the system says a prediction was locked before the answer, it must actually have been locked before the answer.

---

## P07 — Rewards Must Remain Memory-Centered

Preferred rewards include:

- discovering an old memory,
- stabilizing a fragile card,
- forming a Relic,
- defeating a Nemesis,
- revealing personal history,
- unlocking a meaningful visualization,
- completing an Expedition,
- seeing long-term progress.

Avoid defaulting to:

- coins,
- gems,
- generic XP,
- purchasable cosmetics,
- arbitrary treasure,
- unrelated collectibles.

If collectibles exist, they should represent real memory history.

---

## P08 — Difficult Cards Deserve More Meaning, Not More Avoidance

Hard material should become more interesting to engage with.

The system may elevate difficult cards into:

- Nemeses,
- Rescue events,
- restoration stories,
- high-value memory milestones.

Do not design systems where the easiest cards produce the best rewards.

---

## P09 — Failure Should Create Recovery Paths

Anki Alive should prefer:

**failure → new learning state → recovery opportunity**

over:

**failure → punishment**

Examples:

- forgotten Relic → Fractured Relic → restoration,
- weak card → Rescue opportunity,
- repeated lapses → Nemesis,
- missed Oracle prediction → future rematch.

This gives failure narrative consequence without making honesty painful.

---

## P10 — Motivation Must Exist at Multiple Time Scales

The product should balance three loops.

### Micro Loop

Seconds to minutes.

Examples:

- Oracle reveal,
- Rescue result,
- progress signal.

### Session Loop

Minutes to tens of minutes.

Examples:

- Expedition,
- checkpoints,
- Fragment recovery,
- Nemesis encounter,
- completion.

### Long-Term Loop

Days to years.

Examples:

- Relics,
- history,
- Memory World,
- old memories,
- persistent mastery.

Do not rely on a single motivational loop.

Novelty fades.

---

## P11 — Progress Should Feel Nearby

Large review queues can feel psychologically distant.

Prefer:

- short checkpoints,
- visible next milestones,
- clear local progress,
- bounded sessions.

Avoid presenting only:

> 0 / 300

when a more useful structure might show several meaningful nearby steps.

The learner should frequently understand what "finished with this part" means.

---

## P12 — Do Not Exploit Loss Aversion

Loss can be meaningful, but it must remain recoverable.

Allowed examples:

- a Relic becomes fractured,
- a memory becomes fragile,
- a Nemesis regains strength.

Avoid:

- permanent deletion of earned history,
- losing rewards because the user missed a day,
- streak resets used as pressure,
- artificial expiry timers,
- punishment for leaving Anki.

Loss should represent memory change, not obedience to the product.

---

## P13 — No Streak Dependency

Anki Alive may display historical consistency if useful.

It must not make streak preservation the central motivation.

Avoid:

- "study today or lose everything",
- escalating streak pressure,
- streak-protected premium mechanics,
- shame around missed days.

The learner should be able to return after a break without feeling that the product has invalidated prior progress.

---

## P14 — No Casino Design

Variable discovery can be useful for curiosity.

Casino mechanics are not.

Avoid:

- loot-box framing,
- purchasable random rewards,
- flashing rarity theatrics,
- artificial scarcity,
- gambling language,
- near-miss manipulation,
- monetized randomness.

Mystery should reveal the learner's own memory story.

---

## P15 — Focus Mode Is a First-Class Experience

The learner must be able to reduce stimulation.

Focus Mode should support:

- minimal animation,
- reduced event interruption,
- clean review presentation,
- optional progress visibility,
- unchanged scheduling behavior.

Focus Mode is not an accessibility afterthought.

It is part of the core product.

---

## P16 — Respect Attention

Animations and events should have a reason.

Use motion for:

- reveal,
- completion,
- state transition,
- progress,
- meaningful feedback.

Avoid:

- constant movement,
- decorative particles during recall,
- delays before answering,
- forced celebrations,
- repeated interruption.

A beautiful interface can still be quiet.

---

## P17 — Respect Accessibility and Sensory Preferences

The design system should eventually support:

- reduced motion,
- keyboard navigation,
- clear focus states,
- readable contrast,
- scalable text,
- non-color-only status indicators,
- light/dark compatibility where practical.

Gamification must not make the product harder to use.

---

## P18 — Preserve Anki's Core Workflow

The add-on must coexist with Anki rather than fight it.

Users should always be able to:

- review normally,
- use familiar grading controls,
- stop studying,
- resume later,
- disable optional presentation features.

Avoid architecture that requires replacing Anki behavior unnecessarily.

---

## P19 — Prefer Transparent Meaning

Users do not need every algorithmic detail during review.

But important states should be explainable.

For example:

- why a card became a Nemesis,
- why a memory entered Rescue,
- what caused a Relic to fracture,
- what an Oracle probability represents.

Do not build "magic" that cannot be explained.

Mystery belongs in discovery, not in system trust.

---

## P20 — Behavioral Design Must End in Closure

Anki Alive may intentionally create tension.

Examples:

- unfinished progress,
- nearby checkpoints,
- hidden events,
- unresolved predictions.

But every tension loop must have an attainable closure state.

The product should create:

> "I want to finish this."

Not:

> "I can never be finished."

---

## P21 — Long-Term Identity Comes From History

The strongest rewards should become more meaningful with time.

The learner's history should accumulate:

- first-learned dates,
- old memories,
- difficult victories,
- repaired failures,
- long-lived Relics,
- significant review events.

The product should become more personal after months and years of use.

---

## P22 — Avoid Artificial Urgency

Urgency should reflect real memory state.

Good urgency:

> "This memory is becoming fragile."

Bad urgency:

> "Open this reward before midnight or lose it."

Time pressure may be used only when it has a genuine learning reason.

---

## P23 — The Product Must Be Useful Without Novelty

Novelty will fade.

After the surprise wears off, the system should still provide value through:

- clearer progress,
- meaningful memory status,
- stronger session structure,
- useful historical context,
- genuine learning feedback.

Do not rely on constant introduction of new spectacle.

---

## P24 — Visual Identity Must Serve Meaning

The working visual direction is:

**Dark Arcane + Modern Minimal**

Visual symbolism is welcome, but every component must remain readable and functional.

The interface should avoid becoming:

- fantasy decoration without information,
- noisy HUD clutter,
- excessive glow,
- cartoonish reward spam,
- disconnected visual themes per feature.

Oracle, Rescue, Nemesis, Fragments, Relics, and Expedition should feel like parts of one system.

---

## P25 — Product Metrics Must Not Corrupt the Product

Metrics are tools, not goals.

Do not optimize blindly for:

- longest session,
- most daily opens,
- most clicks,
- highest notification response,
- maximum streak length.

Prefer metrics that indicate:

- meaningful session completion,
- honest review behavior,
- willingness to engage difficult material,
- long-term retention,
- healthy return behavior,
- successful use of Focus Mode.

If a metric improves while learning quality worsens, the metric is wrong.

---

## P26 — Every Feature Must Pass the Recall Integrity Test

Before accepting a feature, ask:

1. Does it preserve honest recall?
2. Could it pressure the user to grade dishonestly?
3. Does the reward reflect real learning?
4. Does it interrupt concentration?
5. Does it create a clean closure point?
6. Can the user ignore or disable it and still study normally?
7. Does it remain meaningful after novelty fades?

If several answers are unfavorable, redesign the feature.

---

# Product Decision Filter

A new mechanic should ideally satisfy most of the following:

- grounded in real Anki data,
- strengthens recall,
- increases willingness to engage difficult cards,
- creates curiosity without deception,
- supports nearby completion,
- contributes to long-term personal history,
- works without currency,
- works without streak pressure,
- respects Focus Mode,
- has a clear stopping point.

---

# Final Principle

When uncertain, return to this question:

> **Are we making remembering more compelling, or merely making interaction more addictive?**

Anki Alive should always choose the first.
