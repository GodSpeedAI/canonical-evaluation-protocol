---
type: "CEP Guide"
id: "cep-agent-operating-guide"
title: "Agent Operating Guide"
description: "Repository-level instructions for agents working on the Canonical Evaluation Protocol project."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - agents
  - guide
  - project-memory
timestamp: "2026-06-27T00:00:00Z"
---

# AGENTS.md

Goal:

```
Preserve protocol fidelity.
Produce evidence-backed progress.
Leave the repo easier for the next agent to understand.
```

Treat this as a standards/protocol project. The primary risk is **semantic drift**: changing CEP meaning, collapsing protected distinctions, or producing documentation that looks complete but is not evidence-backed.

---

## 1. Project Purpose

CEP (Canonical Evaluation Protocol) evaluates represented transformations through questions, evidence, settlement, conformance, and capability/affordance implications.

The protocol exists to preserve these distinctions:

```
claim ≠ evidence
completion ≠ settlement
possibility ≠ affordance
authority ≠ capability
score ≠ capability
observation ≠ evidence
representation ≠ reality
declared state ≠ observed state
```

---

## 2. Operating Principle

A task is done only when:

- the intended outcome is clear
- changed files match that outcome
- relevant validation passes
- evidence is recorded
- handoff state is updated

Prefer small, verifiable changes over broad rewrites. When uncertain, choose the next move that is small, reversible, evidence-producing, protocol-preserving, and useful to the next agent. Do not optimize for looking complete.

---

## 3. Local Agent Memory: `.agents/`

Create if missing:

```
.agents/
├── CURRENT_STATUS.md
├── OPEN_QUESTIONS.md
├── DEBT.md
└── lessons/
```

These are the handoff substrate for future agents. They are not decorative.

---

## 4. Read Order

Before making changes, read these files if they exist:

```
AGENTS.md
README.md
SPEC_INDEX.md
spec/index.md
.agents/CURRENT_STATUS.md
.agents/OPEN_QUESTIONS.md
.agents/DEBT.md
```

Then inspect files directly relevant to the assigned task. Treat prior agent summaries as navigation aids, not source of truth.

---

## 5. Source of Truth Order

When documents conflict:

1. Explicit user instruction in the current task
2. `AGENTS.md`
3. Normative specs under `spec/CEP-*.md`
4. Schemas and fixtures
5. Benchmark family specs
6. `README` / `SPEC_INDEX` / directory indexes
7. `.agents/CURRENT_STATUS.md`
8. `.agents/lessons/`
9. `.agents/DEBT.md`
10. Agent summaries or prior informal notes

Conflicts that affect protocol meaning must be recorded in `.agents/OPEN_QUESTIONS.md`. Do not silently resolve them.

---

## 6. Protected Distinctions

Preserve these in all documentation, schemas, tests, fixtures, examples, and code:

```
representation / reality
representation / state
state / transformation
action / transformation
prompt / question
question / answer
data / evidence
observation / evidence
claim / evidence
evidence / settlement
completion / settlement
settlement / success
settlement / approval
settlement / benefit
possibility / affordance
authority / capability
score / capability
signature / truth
summary / source
redaction / absence
unknown / false
```

If a change risks collapsing any of these, stop. Repair the change or record the issue in `.agents/OPEN_QUESTIONS.md`.

---

## 7. Work Loop

1. Identify the requested outcome.
2. Inspect current repo state.
3. Identify affected files.
4. Make the smallest coherent change.
5. Run relevant validation.
6. Record evidence.
7. Update `.agents/CURRENT_STATUS.md`.
8. Record debt, questions, or lessons if needed.

---

## 8. `.agents/CURRENT_STATUS.md`

The handoff state for the next agent. Update after every meaningful task.

Required fields:

- **Last Updated** — date and agent name
- **Current Outcome Being Pursued** — concrete outcome, not the activity ("Make the CEP spec set OKF-compatible" not "Working on docs")
- **Last Completed Work** — changes made, files modified, validation performed
- **Current Repo State** — what is now true
- **Next Affordable Move** — smallest useful next step
- **Why This Next Move Matters** — how it reduces error, improves conformance, or unlocks later work
- **Validation / Evidence** — link to `EVIDENCE.md` entry if one exists
- **Files Recently Modified**
- **Cautions for Next Agent**

Keep it current. Move older detail into `EVIDENCE.md`, `.agents/DEBT.md`, or `.agents/lessons/`.

---

## 9. `.agents/OPEN_QUESTIONS.md`

For load-bearing questions requiring human judgment. Use when:

- a protocol decision is ambiguous
- metadata cannot be confidently inferred
- two sources conflict
- a naming, schema, or benchmark decision affects public structure or scoring meaning
- a license or governance decision is unclear

Do not use for questions answerable by reading the repo.

Required fields per entry: ID, title, date, raised by, context, question, recommendation, options, impact if unresolved, default used if any, status.

Always include a recommendation. Do not dump uncertainty without helping the human decide. When a question is resolved, mark it closed and preserve the answer.

---

## 10. `.agents/DEBT.md`

Tracks issues noticed outside current task scope: broken links, inconsistent naming, missing tests, weak validation, duplicated content, schema drift, fixture gaps, documentation and technical debt, repo hygiene.

Do not use for in-scope issues. Fix those directly.

Required fields per entry: ID, title, date, found by, area, description, why it matters, recommended repair, priority, scope note, status.

Priority guide:

```
Critical  — breaks protocol meaning, validation, or public trust
High      — likely to cause wrong implementation or benchmark result
Medium    — slows future work or creates ambiguity
Low       — cleanup or polish
```

---

## 11. `.agents/lessons/`

Durable, generalizable lessons that help future agents avoid mistakes across multiple tasks. Do not create lessons for one-off issues.

One file per lesson: `0001-short-title.md`

Required fields: ID, title, date, applies to, lesson, why it matters, use this when, do not use this when, example, candidate for AGENTS.md (Yes/No), status.

Lessons must be generalizable and concise. If a lesson becomes foundational, mark `Candidate for AGENTS.md: Yes`.

---

## 12. Evidence Requirements

If the repo has `EVIDENCE.md`, update it after every meaningful task.

Required fields per entry: ID, date, agent, task, outcome, files changed, validation commands, validation result, fidelity notes, remaining gaps, status.

Do not claim validation passed if no command was run. Record why if validation could not be run.

---

## 13. Documentation Rules

CEP documentation must be precise, navigable, and standards-like.

- Use Markdown.
- Use OKF-compatible YAML frontmatter where the repo has adopted it. Reserved OKF filenames (`index.md`, `log.md`) are excluded.
- Use stable headings and relative links.
- Use fenced code blocks for schemas, JSON, YAML, and examples.
- Do not rewrite normative language casually.
- Do not summarize complete specs into shorter replacements.
- Do not remove anti-collapse rules, limitations, or uncertainty notes.
- Do not overclaim maturity.

---

## 14. Cross-Linking Rules

- Link canonical concepts to their defining specs.
- Link dependency, anti-collapse, and conformance/benchmark references.
- Do not link every repeated word.
- Do not link inside code fences.
- Use relative links only.

Every `spec/CEP-*.md` should include a navigation block:

```markdown
## Navigation

**Depends on:** [CEP-0000](./CEP-0000-derivation-ladder.md)
**Defines:** Evidence, Evidence Requirement
**Used by:** [CEP-0007](./CEP-0007-settlement-model.md), [CEP-0009](./CEP-0009-benchmark-model.md)
```

---

## 15. Schema and Fixture Rules

Schemas and fixtures are protocol artifacts.

When modifying them:

- Preserve IDs and required fields unless explicitly changing the contract.
- Update examples and validation if the schema changes.
- Record breaking changes and unresolved compatibility questions.

Benchmark fixtures must preserve anti-collapse intent. A fixture designed to fail must still fail for the intended reason.

---

## 16. Validation

Before finishing, run the most relevant validation available. Look for commands in `README.md`, `package.json`, `pyproject.toml`, `Makefile`, `justfile`, `Taskfile.yml`, or `tools/`.

Common categories: Markdown link validation, YAML frontmatter, JSON schema, schema/example consistency, fixture validation, test suite, formatting, typecheck.

If a task creates a recurring validation need and no validator exists, consider adding a lightweight one under `tools/`. Do not build heavy infrastructure for small documentation tasks.

---

## 17. Git Discipline

- Do not mix unrelated refactors.
- Do not reformat entire files unless formatting is the task.
- Do not rename public files without clear reason.
- Do not delete content unless explicitly obsolete.
- Do not invent missing specs.
- Do not silently resolve protocol conflicts.
- Do not commit secrets.

Inspect the diff before finalizing:

```bash
git status --short
git diff --stat
git diff
```

---

## 18. When to Stop and Ask

Stop and record an open question when:

- the task requires deciding CEP semantics not defined in the repo
- two specs conflict
- a change would alter benchmark scoring meaning
- a schema change would break existing fixtures
- a public naming choice is unclear
- a license or governance claim is ambiguous
- a validation failure cannot be resolved without changing intended behavior

Do not stop for minor implementation choices that can be safely resolved and recorded.

---

## 19. Handoff Requirements

At the end of every task, update:

```
.agents/CURRENT_STATUS.md     — always
EVIDENCE.md                   — if present or relevant
.agents/OPEN_QUESTIONS.md     — if human judgment is needed
.agents/DEBT.md               — if out-of-scope issues were found
.agents/lessons/              — if a durable lesson was learned
```

The next agent must be able to answer: what was being pursued, what changed and why, what validated it, what remains, what should happen next.
