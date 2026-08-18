# START_PHASE.md

# Anki Alive — Start Phase Prompt

Use this prompt at the beginning of a new phase chat or agent workstream.

---

## Short Version

```text
Continue the Anki Alive project for Phase [X]: [PHASE NAME].

Before making changes:
1. inspect PROJECT.md and AGENTS.md,
2. inspect all canonical docs relevant to this phase,
3. inspect the latest handoff,
4. inspect the current repository state and tests.

Treat accepted ADRs as constraints.
Do not rely on previous chat history when repository documentation exists.

For this phase:
- restate the exact scope,
- identify dependencies and open questions,
- identify architecture/data/UI/testing/performance/accessibility impact,
- implement only the current phase,
- place out-of-scope ideas in backlog,
- run meaningful tests,
- measure reviewer-path performance if affected,
- update canonical docs,
- create the phase handoff before declaring completion.

Preserve:
- honest recall,
- no punishment for Again,
- no reward for arbitrary Good/Easy,
- Anki scheduler authority,
- Focus Mode,
- one prominent event reveal per review boundary,
- Arcane Memory Interface design language.

The game is the memory itself.
```

---

## Full Phase Startup Procedure

### Step 1 — Establish Context

Read:

```text
PROJECT.md
AGENTS.md
docs/00_PRODUCT_VISION.md
docs/01_PRODUCT_PRINCIPLES.md
docs/02_DESIGN_SYSTEM.md
docs/03_ARCHITECTURE.md
docs/04_DATA_MODEL.md
docs/05_ROADMAP.md
docs/06_DECISIONS.md
docs/07_BACKLOG.md
docs/08_TESTING.md
docs/09_ACCESSIBILITY.md
docs/10_PERFORMANCE.md
```

Then read:

- the current phase specification,
- the latest handoff,
- relevant source files,
- relevant tests,
- migration state.

---

### Step 2 — Confirm Current Reality

Do not trust stale documentation blindly.

Compare docs against repository state.

Identify:

- what already exists,
- what is incomplete,
- what differs from the handoff,
- what tests currently pass/fail,
- what migrations exist.

---

### Step 3 — State Phase Contract

Before implementing, summarize:

```text
Phase:
Goal:
In scope:
Out of scope:
Critical invariant:
Dependencies:
Open questions:
Expected durable data changes:
Expected UI surfaces:
Expected test obligations:
Expected performance-sensitive paths:
```

This summary should be concise.

---

### Step 4 — Resolve Blocking Uncertainty

Only investigate uncertainty that materially blocks safe implementation.

Examples:

- exact Anki hook behavior,
- data availability,
- undo semantics,
- current compatibility behavior.

Do not research unrelated future features.

---

### Step 5 — Implement Vertical Slices

Prefer:

```text
domain model
    ↓
persistence/interface
    ↓
service/use case
    ↓
integration
    ↓
minimal UI
    ↓
tests
    ↓
polish
```

Do not build the full UI before proving the state model.

---

### Step 6 — Keep Scope Clean

If a new idea appears:

- capture it in backlog,
- do not expand current phase unless dependency-critical.

---

### Step 7 — Validate

Run:

- relevant unit tests,
- persistence/migration tests,
- integration tests,
- manual Anki checks,
- accessibility checks,
- performance checks.

Record what was actually run.

---

### Step 8 — Update Project Memory

Before closing the phase:

- update roadmap status,
- add accepted ADRs,
- update backlog,
- update architecture/data model if changed,
- write phase handoff.

---

## Phase Completion Phrase

Do not say:

> Phase complete.

until the phase handoff exists and required quality gates are satisfied.

Prefer:

> Phase [X] is complete according to the current Definition of Done. The handoff records tests, known issues, performance findings, and next-phase dependencies.

If incomplete:

> Phase [X] is partial. The handoff records the last safe state and remaining work.

---

# Startup North Star

> **Read the project before changing the project.**
