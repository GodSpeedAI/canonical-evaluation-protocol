---
type: "CEP Guide"
id: "cep-docs-running-benchmarks"
title: "Running the Benchmarks"
description: "How to install CEP, run the benchmark families and conformance checks, and interpret the results."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - guide
  - benchmarks
  - usage
timestamp: "2026-06-27T00:00:00Z"
---

# Running the Benchmarks

This guide explains how to run the CEP benchmark families and conformance
checks, and how to read what comes back. It assumes no prior knowledge of the
codebase.

## Prerequisites

CEP uses [`uv`](https://docs.astral.sh/uv/) for a portable, reproducible
Python environment, and [`just`](https://github.com/casey/just) as a command
runner. The project pins its own Python version and dependencies in
`pyproject.toml` / `uv.lock`, so you do not need to manage a virtualenv
yourself.

```bash
# from the repository root
uv sync              # install the locked dependencies
```

Every command below is run from the repository root. The project is fully
portable: it discovers its own root and never relies on absolute paths. If you
ever need to run it from elsewhere, set `CEP_REPO_ROOT` to the checkout path.

## The one command

```bash
just all
```

`just all` runs the complete local proof and is the single command to trust
before committing or releasing. It chains four stages:

| Stage | Command | What it checks |
|-------|---------|----------------|
| validate | `just validate` | OKF Markdown structure, the JSON schema registry, and the RealityGapBench corpus artifacts |
| test | `just test` | the `pytest` suite (unit + CLI + scoring behaviour) |
| conformance | `just conformance` | anti-collapse conformance for **all four** benchmark families |
| smoke | `just smoke` | scores every family's example answers and writes reports |

Run a single stage with `just validate`, `just test`, `just conformance`, or
`just smoke`.

## Running one family at a time

Each family has a corpus runner that scores its bundled valid and invalid
example answers:

```bash
uv run cep run reality-gap-corpus
uv run cep run authority-corpus
uv run cep run settlement-corpus
uv run cep run capability-corpus
```

Typical output:

```text
INVALID rg-0001 ans-rg-0001-invalid-example score=0.0
PASS    rg-0001 ans-rg-0001-valid-example   score=99.0
```

The runner exits non-zero if a valid example fails to pass **or** an invalid
example passes — that is the regression signal you want in CI.

## Scoring a single answer

To score one RealityGapBench answer against a case (for example, output from a
model you are evaluating):

```bash
uv run cep run reality-gap \
  --case-dir benchmarks/reality-gap/cases/rg-0001 \
  --answer path/to/your-answer.json \
  --out reports/reality-gap/my-run.result.json
```

`--out` is optional; without it the report is written under
`reports/reality-gap/`.

## Reading a result

Every run produces a benchmark result record (validated against
[`benchmark-result.schema.json`](../schemas/benchmark-result.schema.json)):

```json
{
  "result_id": "result-rg-0001-ans-...",
  "benchmark_family": "RealityGapBench",
  "score": 99.0,
  "status": "pass",
  "metrics": { "raw_score": 99.0, "evidence_recall": 1.0, ... },
  "critical_failures": [],
  "warnings": []
}
```

### Status and thresholds

`status` is derived from the score **and** whether any critical failure fired:

| Status | Meaning |
|--------|---------|
| `pass` | score ≥ 85 and no critical failure |
| `partial` | score ≥ 60 and no critical failure |
| `fail` | scored above 0 but below the partial bar, or capped by a critical failure |
| `invalid` | a critical failure with a low score — the answer commits a semantic collapse |

A non-empty `critical_failures` list means the answer collapsed a protected
distinction (see the [Anti-Collapse Reference](anti-collapse.md)). **No score is
high enough to override a critical failure** — it caps the result.

### Warnings

`warnings` carry non-fatal signals. The most common is `ungrounded_reasoning`:
a RealityGapBench answer whose `gap_summary` does not reference both the
declared and the observed side. Ungrounded answers cannot reach `pass`, even
with correct labels — this stops label-guessing from scoring well.

### Where reports go

```text
reports/<family>/<case-id>-<answer-id>.result.json
```

The `reports/` directory is git-ignored; rerun `just smoke` (or `just all`) to
regenerate.

## How scoring works, per family

All scorers combine label correctness, recall over the answer key's required
items, and anti-collapse caps. Summary:

* **RealityGapBench** — partial credit for `gap_status`, `gap_type`, and
  `severity` (data-driven from the answer key), plus recall over required
  evidence, constraints, distinctions, and relations, plus a next-action check.
  See [RealityGapBench](../benchmarks/reality-gap/BENCHMARK.md).
* **AuthorityBench** — the `allow`/`deny`/`escalate` decision plus evidence and
  distinction recall; false-allow on a deny case is a critical failure.
  See [AuthorityBench](../benchmarks/authority/BENCHMARK.md).
* **SettlementBench** — settlement status plus recall; calling something settled
  that the case does not consider settled is a critical failure.
  See [SettlementBench](../benchmarks/settlement/BENCHMARK.md).
* **CapabilityBench** — capability status plus recall; claiming capability from a
  score, a one-time success, or mere possibility is a critical failure.
  See [CapabilityBench](../benchmarks/capability/BENCHMARK.md).

## Anti-collapse conformance

```bash
uv run cep conformance anti-collapse
```

This is the protocol's self-defense check. It runs the real detector on each
fixture's submitted answer and on every family's example answers, and confirms
that each known collapse is actually caught. It does **not** trust any fixture's
self-declared verdict. See the [Anti-Collapse Reference](anti-collapse.md) and
[CEP-0010 Conformance](../spec/CEP-0010-conformance.md).

## Troubleshooting

* **`cep: command not found`** — prefix with `uv run` (e.g. `uv run cep ...`) or
  run `uv sync` first.
* **Running outside the repo root** — set `CEP_REPO_ROOT=/path/to/checkout`.
* **A valid example stopped passing after editing a case** — rerun
  `uv run cep validate reality-gap-corpus` to check the artifacts before the
  scorer; schema or evidence-reference errors surface there.
