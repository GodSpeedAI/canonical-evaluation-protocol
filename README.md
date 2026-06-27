---
type: "CEP Guide"
id: "cep-readme"
title: "Canonical Evaluation Protocol"
description: "Vendor-neutral protocol for evaluating represented transformations."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - guide
  - readme
timestamp: "2026-06-26T14:13:47Z"
---

# Canonical Evaluation Protocol

**Canonical Evaluation Protocol (CEP)** is a vendor-neutral protocol for evaluating represented transformations: what changed, what evidence supports the change, whether the result settled, and whether repeated settled performance can support a capability claim.

CEP exists because most evaluation systems collapse too much.

They treat an output as proof.
They treat task completion as settlement.
They treat tool access as capability.
They treat policy text as authority.
They treat a benchmark score as operational readiness.

CEP keeps those distinctions separate.

This repository is the public home for the CEP specifications, schemas, benchmark family definitions, conformance fixtures, examples, and reference implementation material.

---

## What CEP Is

CEP is a protocol for evaluating stateful work across AI systems, agents, tools, organizations, and human-machine workflows.

It provides a shared vocabulary and structure for answering questions like:

* What state was declared?
* What state was observed?
* What transformation was attempted?
* What evidence supports the claim?
* What consequences actually registered?
* Has the transformation settled?
* Is this a one-time success or repeatable capability?
* What affordances became reachable after settlement?
* Where did declared reality diverge from observed reality?

CEP is not a leaderboard, prompt format, agent framework, or governance dashboard.

It is the evaluation substrate beneath those things.

---

## Core Idea

CEP evaluates transformations through evidence-backed settlement.

```text
Declared State
  ↓
Transformation
  ↓
Observed State
  ↓
Question
  ↓
Evidence
  ↓
Settlement
  ↓
Capability / Affordance Update
```

A system does not get credit merely because it produced an answer.

It gets credit when it preserves the right distinctions, cites the right evidence, avoids semantic collapse, and produces a result that can be inspected, scored, and reused.

---

## The Derivation Ladder

CEP uses a derived ontology where each layer depends on the prior layer.

```text
0. Indeterminate Field
1. Constraint
2. Distinction
3. Relation
4. Representation
5. State
6. Transformation
7. Observation
8. Question
9. Evidence
10. Settlement
```

### 0. Indeterminate Field

The pre-representational condition. Outside formal protocol scope, but acknowledged as the condition before distinctions are made.

### 1. Constraint

Any condition that limits, enables, or shapes possibility.

### 2. Distinction

A constraint made differentiable. A marked difference.

### 3. Relation

A preserved connection between distinctions.

### 4. Representation

A structure that preserves distinctions and relations.

### 5. State

A representation situated in subject, scope, time, and identity context.

### 6. Transformation

A represented change in constraints, distinctions, relations, or state under identity continuity.

### 7. Observation

A perspective-bound registration of something relevant to a transformation or state.

### 8. Question

A constraint over attention, relevance, answer shape, and evidence selection.

### 9. Evidence

A representation that changes confidence in a claim relative to a question.

### 10. Settlement

Reliable consequence registration that can support state update, correction, repetition, or capability evaluation.

---

## Why This Matters

CEP prevents common evaluation failures:

```text
output ≠ evidence
claim ≠ proof
completion ≠ settlement
test pass ≠ capability
policy text ≠ authority decision
tool access ≠ operational competence
possibility ≠ affordance
benchmark score ≠ production readiness
```

These distinctions matter when AI systems start acting in real environments: writing files, calling APIs, modifying infrastructure, opening pull requests, changing workflows, escalating decisions, or claiming work is complete.

A prompt is not an authority boundary.
A summary is not evidence.
A completed task is not automatically a settled transformation.

CEP gives systems a way to prove what happened.

---

## Repository Structure

```text
.
├── spec/
│   └── Normative CEP specifications
│
├── schemas/
│   └── JSON schemas for cases, evidence, answers, results, and reports
│
├── benchmarks/
│   └── Benchmark family definitions and benchmark cases
│
├── conformance/
│   └── Anti-collapse fixtures and conformance requirements
│
├── src/cep/
│   └── Reference implementation: CLI, validators, scorers, detector
│
├── tests/
│   └── Unit, CLI, and scoring-behaviour tests
│
├── reports/
│   └── Generated benchmark result records (git-ignored)
│
├── rfc/
│   └── Proposed and accepted protocol changes
│
└── docs/
    └── Usage guides and reference material
```

---

## Specifications

The initial CEP specification set includes:

* `CEP-0000` — Derivation Ladder and First Principles
* `CEP-0001` — Ontology
* `CEP-0002` — Representation Model
* `CEP-0003` — State Model
* `CEP-0004` — Transformation Model
* `CEP-0005` — Question Model
* `CEP-0006` — Evidence Model
* `CEP-0007` — Settlement Model
* `CEP-0008` — Semantic Envelope
* `CEP-0009` — Benchmark Model
* `CEP-0010` — Conformance

Start here:

* [`spec/`](spec/index.md)

---

## Benchmark Families

CEP benchmark families evaluate different kinds of represented transformations.
Four families are executable today, each with a scorer, example answers, and
anti-collapse protection:

* [`RealityGapBench`](benchmarks/reality-gap/BENCHMARK.md) — does declared reality diverge from observed reality? (detect, classify, evidence, explain)
* [`AuthorityBench`](benchmarks/authority/BENCHMARK.md) — given actor, operation, resource, context, and policy, is the decision `allow` / `deny` / `escalate`? (no capability standing in for authority)
* [`SettlementBench`](benchmarks/settlement/BENCHMARK.md) — did a completion claim actually settle as a reliable consequence? (no premature completion)
* [`CapabilityBench`](benchmarks/capability/BENCHMARK.md) — does repeated settlement under variation support a capability claim? (no score or one-time success standing in for capability)

Initial RealityGapBench case types include authority drift, process drift,
evidence gap, settlement gap, semantic drift, affordance gap, and capability gap.

The current corpus is a **smoke corpus** (one to three reviewed cases per
family) — enough to prove the engine end to end. Growing it is the main roadmap
item; see [Authoring Benchmark Cases](docs/authoring-cases.md).

---

## Conformance

CEP conformance checks whether an implementation preserves protocol semantics.

A CEP-compatible system must not merely parse CEP-shaped files. It must preserve the distinctions that make CEP useful.

Conformance fixtures live in:

* [`conformance/`](conformance/index.md)

`cep conformance anti-collapse` runs a real content-based detector against every
fixture's submitted answer **and** every family's example answers — it never
trusts a fixture's self-declared verdict. Initial anti-collapse fixtures test
failures such as:

* declared state collapsed into observed state
* claim treated as evidence
* unknown treated as false
* completion treated as settlement
* CI pass treated as peer approval
* possibility treated as affordance
* authority treated as capability
* score treated as capability

See the [Anti-Collapse Reference](docs/anti-collapse.md) for the full list of
detector codes and how detection works.

---

## Semantic Envelope

The Semantic Envelope is CEP’s canonical transport object.

It carries the context required to evaluate a transformation across tools, agents, systems, benchmarks, and organizations.

A Semantic Envelope may include:

* representations
* states
* transformations
* observations
* questions
* claims
* evidence
* settlements
* authority context
* benchmark results
* conformance reports
* omissions
* uncertainty
* contradictions
* provenance

The envelope is not the truth.

It is the portable structure that lets a system inspect what was claimed, what was observed, what evidence was provided, and what settled.

---

## Current Status

CEP is at an early but **executable** stage. The specification set, JSON
schemas, four benchmark families, scorers, an engine-backed anti-collapse
detector, and a CLI all run locally and are verified by `just all`. The corpus
is a smoke corpus (one to three reviewed cases per family); broader corpus
breadth is the main roadmap item.

The settlement target met for this stage:

```text
Validate the corpus artifacts,
score a RealityGapBench case,
produce a benchmark result record,
and confirm anti-collapse conformance across all four families.
```

## Minimal Executable Proof

Install dependencies, then run the full local proof:

```bash
uv sync
just all
```

`just all` validates OKF Markdown structure, the schema registry, and the
RealityGapBench corpus; runs the test suite; runs four-family anti-collapse
conformance; and scores every family's example answers, writing reports under
`reports/<family>/`.

To run a single family or score one answer, see
[Running the Benchmarks](docs/running-benchmarks.md).

---

## Documentation

* [Running the Benchmarks](docs/running-benchmarks.md) — install, run, and interpret results.
* [Authoring Benchmark Cases](docs/authoring-cases.md) — add human-reviewed cases to grow the corpus.
* [Anti-Collapse Reference](docs/anti-collapse.md) — the collapses CEP detects and how.

---

## Design Principles

CEP follows these principles:

1. **Preserve distinctions.** Do not collapse claims, evidence, settlement, authority, capability, or affordance.
2. **Bind answers to questions.** Evidence only matters relative to a question.
3. **Require provenance.** Evaluation artifacts must show where they came from.
4. **Treat outcomes as settlement events.** Outcomes matter because they produce consequence and feedback.
5. **Separate success from settlement.** A result can be successful, harmful, authorized, unauthorized, settled, or unsettled.
6. **Treat capability as repeated settlement under variation.** One good result is not capability.
7. **Make uncertainty explicit.** Unknown is not false. Missing evidence is not proof.
8. **Make conformance testable.** Protocol compatibility must be validated, not asserted.

---

## Who This Is For

CEP is intended for:

* AI evaluation researchers
* agent framework builders
* governance and assurance teams
* benchmark designers
* AI safety and reliability engineers
* enterprise architecture teams
* compliance and audit teams
* human-AI workflow designers
* organizations building governed agentic systems

---

## Short Description

Canonical Evaluation Protocol for evidence-backed AI and organizational capability benchmarks.

---

## License

License information will be defined in the repository root.

---

## Project Status

Draft protocol. Expect breaking changes until the v0.1 specification set, schemas, fixtures, and reference runner are settled.
