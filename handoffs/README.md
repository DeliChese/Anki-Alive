# Handoffs

# Anki Alive — Phase Handoff Standard

## 1. Purpose

A handoff allows a new chat, agent, or contributor to continue the project without needing the previous conversation.

A phase is not complete until its handoff exists.

The handoff should contain enough information to answer:

- What was built?
- What changed?
- What remains?
- What assumptions were made?
- What should the next phase know before touching the code?

---

## 2. File Naming

Recommended format:

```text
handoffs/
├─ PHASE_0_FOUNDATION_HANDOFF.md
├─ PHASE_1_EXPEDITION_HANDOFF.md
├─ PHASE_2_ORACLE_HANDOFF.md
└─ ...
```

If a phase has multiple major internal milestones, optional interim handoffs may use:

```text
PHASE_1_M1_HANDOFF.md
```

Do not create excessive handoff files for tiny tasks.

---

## 3. Required Sections

Every phase handoff should include:

1. phase status
2. completed scope
3. implementation summary
4. architecture changes
5. data/schema changes
6. UI/UX changes
7. tests run
8. performance findings
9. accessibility findings
10. files changed
11. accepted decisions
12. known issues
13. technical debt
14. deferred ideas
15. next-phase dependencies
16. startup instructions for the next agent

---

## 4. Handoff Template

```text
# Phase X — [Name] Handoff

## Status

COMPLETE / PARTIAL / BLOCKED

Completed on:
Add-on version:
Schema version:
Target Anki versions tested:

---

## 1. Scope Completed

- ...
- ...

## 2. Scope Not Completed

- ...
- ...

## 3. Implementation Summary

Describe the major implementation.

Focus on architecture and behavior, not every line of code.

## 4. Architecture Changes

List:

- new modules
- changed boundaries
- new services
- new event types
- compatibility changes

If none:

No architecture changes.

## 5. Data / Schema Changes

Include:

- schema version
- migrations added
- tables added/changed
- settings changes
- migration risks

If none:

No data/schema changes.

## 6. UI / UX Changes

Describe:

- screens
- reviewer elements
- animations
- Focus Mode behavior
- reduced-motion behavior

## 7. Tests Run

### Automated

Command:
Result:

### Manual

Scenarios:
Result:

### Not Tested

Explicitly list gaps.

## 8. Performance Findings

Include measured values where possible.

Examples:

- reviewer hook P50
- reviewer hook P95
- database write timing
- Today load
- known slow paths

## 9. Accessibility Findings

Include:

- keyboard behavior
- reduced motion
- focus states
- non-color cues
- known accessibility gaps

## 10. Files Changed

- `path/to/file`
- `path/to/file`

## 11. Decisions Accepted

- ADR-XXX
- ADR-YYY

## 12. Known Issues

### KI-001 — Title

Severity:
Impact:
Workaround:

## 13. Technical Debt

### TD-001 — Title

Why deferred:
Recommended future action:

## 14. Deferred Ideas

- BL-XXX
- BL-YYY

## 15. Next Phase Dependencies

Before Phase X+1 begins:

- ...
- ...

## 16. Next Agent Startup

Read, in order:

1. `PROJECT.md`
2. `docs/01_PRODUCT_PRINCIPLES.md`
3. `docs/03_ARCHITECTURE.md`
4. `docs/04_DATA_MODEL.md`
5. `docs/02_DESIGN_SYSTEM.md`
6. `docs/05_ROADMAP.md`
7. latest decisions
8. this handoff
9. next phase spec

Then inspect:

- relevant source modules
- tests
- migration state
- open known issues

Do not begin feature implementation before verifying the current repository state.
```

---

## 5. Test Evidence Rules

Do not write:

> All tests pass.

unless the test commands were actually executed.

Prefer:

```text
Automated:
pytest tests/domain -q
Result: 148 passed

Manual:
Anki 25.x — Expedition start/resume/complete
Result: passed
```

If something was not tested, say so.

---

## 6. Performance Evidence Rules

Do not describe performance as:

> fast

Prefer actual evidence:

```text
Reviewer answer-hook overhead:
P50: 2.8 ms
P95: 6.9 ms
n = 500 reviews
```

If no benchmark was run:

> Not measured in this phase.

---

## 7. Known Issue Severity

Suggested levels:

```text
CRITICAL
HIGH
MEDIUM
LOW
COSMETIC
```

### CRITICAL

Data loss, corrupted review flow, unsafe migrations.

### HIGH

Major feature failure or serious performance issue.

### MEDIUM

Important edge case or degraded UX.

### LOW

Minor inconsistency.

### COSMETIC

Visual issue without behavioral impact.

---

## 8. Technical Debt Rules

Technical debt is not:

> code I dislike.

It should describe a real deferred cost.

Include:

- reason for deferral,
- future risk,
- recommended correction.

---

## 9. Handoff Integrity

Before finalizing a handoff:

- verify filenames,
- verify schema version,
- verify test commands,
- verify decisions,
- verify known issues,
- verify roadmap status.

A handoff with incorrect facts is worse than a short handoff.

---

## 10. Partial Phase Handoff

If a phase ends incomplete due to an interruption:

create a handoff anyway.

Use:

```text
Status: PARTIAL
```

Clearly identify:

- last known working state,
- incomplete code paths,
- uncommitted assumptions,
- tests not run,
- safest next action.

Never pretend the phase is complete.

---

## 11. Cross-Chat Continuity

The repository is the source of truth.

The next chat should not rely on phrases such as:

> "as we discussed earlier"

unless the relevant decision is also present in canonical docs or the handoff.

If context matters, write it down.

---

## 12. Handoff Review Checklist

Before closing a phase:

- [ ] scope status is accurate
- [ ] docs are updated
- [ ] ADRs are recorded
- [ ] backlog is updated
- [ ] migration state is documented
- [ ] tests are listed honestly
- [ ] performance results are documented
- [ ] accessibility review is included
- [ ] known issues are explicit
- [ ] next dependencies are clear
- [ ] next-agent startup instructions are usable

---

# Handoff North Star

> **A new agent should be able to continue safely without reading the old chat.**
