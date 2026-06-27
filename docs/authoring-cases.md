---
type: "CEP Guide"
id: "cep-docs-authoring-cases"
title: "Authoring Benchmark Cases"
description: "How to add human-reviewed benchmark cases to grow the CEP corpus beyond the smoke set."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - guide
  - benchmarks
  - authoring
  - corpus
timestamp: "2026-06-27T00:00:00Z"
---

# Authoring Benchmark Cases

The `v0.1.0` corpus is a **smoke corpus**: one to three cases per family, enough
to prove the engine works end to end. Growing it is the one remaining
non-blocking item from the protocol audit (tracked as **F-09**). This guide is
the workflow for adding cases.

## Human review is required

Every benchmark case must be reviewed by a human before it enters the corpus.
This is a deliberate protocol decision recorded in
[Open Questions OQ-0005](../.agents/OPEN_QUESTIONS.md): a benchmark is only as
trustworthy as the cases in it, so machine-generated cases are a starting draft,
never the final artifact. A case is "in the corpus" when a reviewer has
confirmed:

1. the declared and observed states are realistic and genuinely diverge (or
   genuinely do not);
2. the answer key's accepted answers are correct and its critical-failure
   conditions are the right ones for the case;
3. the `example_valid_answer` earns a `pass`/`partial` for the **right reasons**,
   not by gaming labels;
4. the `example_invalid_answer` commits a real, named semantic collapse;
5. no protected distinction is blurred (see the
   [Anti-Collapse Reference](anti-collapse.md)).

Until those five hold, the case is a draft. Keep drafts out of the `cases/`
directories that the runners auto-discover.

## How cases are discovered

The corpus runners glob case directories by family prefix:

| Family | Directory | Prefix |
|--------|-----------|--------|
| RealityGapBench | `benchmarks/reality-gap/cases/` | `rg-*` |
| AuthorityBench | `benchmarks/authority/cases/` | `auth-*` |
| SettlementBench | `benchmarks/settlement/cases/` | `set-*` |
| CapabilityBench | `benchmarks/capability/cases/` | `cap-*` |

Adding a correctly named, correctly shaped directory is all it takes for it to
be picked up — no registry edit required.

## RealityGapBench case layout

A RealityGapBench case is the richest. The directory name **is** the case id and
must match the `case_ref` field inside every file.

```text
benchmarks/reality-gap/cases/rg-0004/
├── case.cep.json              # the case: declared/observed states, constraints, question
├── declared.md                # human-readable declared state narrative
├── observed.jsonl             # observed events, one JSON object per line
├── evidence/
│   ├── ev-rg-0004-001.json    # evidence records; ids must match the case's evidence_requirements
│   └── ev-rg-0004-002.json
├── answer_key.json            # accepted answers, partial-credit rules, critical-failure conditions
├── example_valid_answer.json  # a model answer that should score pass/partial
├── example_invalid_answer.json# a model answer that commits a collapse
└── README.md                  # case summary (concept doc; needs OKF frontmatter)
```

Key answer-key fields (see the existing `rg-0001` case for a complete example):

* `accepted_gap_statuses`, `accepted_gap_types`, `accepted_severity_range`
* `required_evidence_refs`, `optional_evidence_refs`
* `required_affected_constraints` / `_distinctions` / `_relations`
* `accepted_next_actions`
* `partial_credit_rules` — the points awarded per `gap_status` / `gap_type` /
  `severity` value (this is how scoring stays data-driven, not hardcoded)
* `critical_failure_conditions` — the collapse codes that invalidate an answer

Every evidence id referenced under the case's `evidence_requirements` must have a
matching file in `evidence/`, or validation fails.

## Other families' case layout

AuthorityBench, SettlementBench, and CapabilityBench cases are simpler:

```text
benchmarks/<family>/cases/<id>/
├── case.cep.json
├── answer_key.json
├── example_valid_answer.json
└── example_invalid_answer.json
```

The `answer_key.json` expected fields per family:

| Family | Decisive field | Plus |
|--------|----------------|------|
| AuthorityBench | `expected_decision` (`allow`/`deny`/`escalate`) | `required_evidence_refs`, `required_distinctions` |
| SettlementBench | `expected_settlement_status` | `required_evidence_refs`, `required_distinctions` |
| CapabilityBench | `expected_capability_status` | `required_evidence_refs`, `required_distinctions` |

All answer keys also carry `case_ref`.

## Validate, then score

After writing a case, run the loop:

```bash
# 1. structural validation (schemas, evidence references, case_ref matching)
uv run cep validate reality-gap-corpus      # RealityGapBench
uv run cep validate all                      # schemas + RealityGap corpus

# 2. score the example answers
uv run cep run reality-gap-corpus            # or authority-/settlement-/capability-corpus

# 3. confirm anti-collapse behaviour holds for every family
uv run cep conformance anti-collapse

# 4. the full proof
just all
```

A new case is ready when:

* validation passes,
* its `example_valid_answer` scores `pass`/`partial` with no critical failures,
* its `example_invalid_answer` scores `invalid`/`fail` **and** lists the intended
  collapse in `critical_failures`,
* `just all` is green.

The cross-family conformance check
(`src/cep/conformance/benchmark_invariants.py`) enforces points two and three
automatically, so a case whose examples do not behave correctly will fail the
suite.

## Adding a RealityGap anti-collapse fixture

To add a dedicated anti-collapse fixture (the strongest form of regression test):

1. Create `conformance/fixtures/anti-collapse/reality-gap/rg-ac-00NN-<name>.json`
   with a `target_case_ref`, a `submitted_answer` that commits the collapse, and
   an `expected_validation` block describing why it is invalid.
2. Register it in that directory's `manifest.json` with the `expected_errors` the
   detector must report.
3. Run `uv run cep conformance anti-collapse`.

The harness scores your `submitted_answer` with the real detector and confirms
the expected collapse codes actually fire — it never trusts the fixture's own
declaration. If the detector cannot yet name the collapse you are testing, that
is a signal to extend `src/cep/detect.py` (and a finding worth recording).

## Roadmap

Corpus breadth (more reviewed cases across every declared gap and decision type)
is the path from "executable proof" to "credible benchmark." See the
[Roadmap](../ROADMAP.md).
