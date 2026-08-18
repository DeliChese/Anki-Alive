# Anki Alive

> **Your memory is alive. Keep it alive.**

Anki Alive is an Anki add-on that turns genuine memory progress into an evolving learning experience.

The project is designed around a simple belief:

> The add-on should not reward the user for merely opening Anki or pressing buttons. It should make real recall, memory stability, and meaningful session completion feel satisfying enough that users want to keep learning.

Anki Alive does **not** aim to turn Anki into a generic game with XP, coins, streak pressure, loot boxes, or arbitrary achievements. Instead, it gives narrative, visual meaning, and progression to the memory data Anki already contains.

## Core Experience

The core loop is:

**Open → Expedition → Recall → Event → Closure → Long-term memory history**

A study session should feel like an unfolding journey rather than a queue of anonymous cards.

Core mechanics planned for the product include:

- **Expedition** — the primary session structure and progress loop
- **Oracle** — hidden predictions about cards the learner may forget
- **Rescue** — fragile memories that can be stabilized through genuine recall
- **Nemesis** — unusually difficult cards that become persistent challenges
- **Fragments** — mystery events unlocked through meaningful study progress
- **Relics** — long-lived, highly stable memories with persistent history
- **Memory World** — a long-term visual representation of the learner's evolving knowledge

## Product Philosophy

Anki Alive must always reinforce good learning behavior.

That means:

- Honest failure is useful.
- Pressing **Again** must never be punished.
- The add-on must not encourage fake **Good** or **Easy** answers.
- Rewards should reflect genuine recall, memory stability, difficulty, or meaningful completion.
- Users must always be able to study normally without being trapped inside gamification.
- Visual effects must support recall rather than interrupt it.
- Long-term progression should come from the learner's own memory history, not artificial currencies.

## Project Structure

The repository will gradually grow into the following structure:

```text
anki-alive/
├─ README.md
├─ PROJECT.md
├─ AGENTS.md
├─ docs/
├─ handoffs/
├─ prompts/
├─ src/
├─ tests/
└─ assets/
```

Canonical project documentation will live in `docs/`.

Important product and architectural decisions must be written into the repository rather than left only inside chat history.

## Development Strategy

Anki Alive is developed phase by phase.

Each phase should be completed as a coherent vertical slice:

1. Specification
2. UX and visual design
3. Architecture impact review
4. Implementation
5. Testing
6. Performance review
7. UX and recall-integrity review
8. Documentation update
9. Handoff

A phase is not considered complete merely because the feature works.

**Quality, visual polish, and learning integrity are part of the Definition of Done.**

## Planned Roadmap

The current product direction is:

```text
FOUNDATION
    ↓
EXPEDITION
    ↓
ORACLE
    ↓
RESCUE
    ↓
NEMESIS
    ↓
FRAGMENTS
    ↓
RELICS
    ↓
MEMORY WORLD
    ↓
POLISH + PUBLIC RELEASE
```

The exact implementation may evolve as the project matures, but major changes to this direction should be deliberate and documented.

## Status

Anki Alive is currently in **pre-implementation product definition**.

The repository is being prepared so future development can continue across multiple chats, contributors, or coding agents without losing product intent.

See:

- [`PROJECT.md`](PROJECT.md) for the compact project briefing
- [`AGENTS.md`](AGENTS.md) for mandatory working rules for AI and coding agents
