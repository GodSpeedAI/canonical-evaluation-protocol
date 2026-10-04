---
type: "CEP Guide"
id: "cep-getting-started"
title: "Getting Started with CEP"
description: "Quick-start guide for setting up the CEP environment, running local verification, and understanding basic CLI commands."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - getting-started
  - quickstart
timestamp: "2026-06-27T00:00:00Z"
---

# Getting Started with CEP

## 1. Fast Setup

The Canonical Evaluation Protocol uses [`uv`](https://docs.astral.sh/uv/) for Python dependency management and [`just`](https://github.com/casey/just) for execution recipes.

```bash
# 1. Sync dependencies into locked virtualenv
uv sync

# 2. Run the environment doctor check
uv run cep doctor

# 3. Run the complete local proof (validation, tests, conformance, smoke benchmarks)
just all
```

If `just all` outputs green passes across all stages, your environment is fully operational!

---

## 2. Core CLI Commands at a Glance

| Command | Purpose |
|---|---|
| `uv run cep doctor` | Runs a fast schema registry integrity check. |
| `uv run cep validate all` | Validates all schemas, benchmark cases, evidence, and envelopes. |
| `uv run cep conformance anti-collapse` | Runs engine self-defense against semantic collapse fixtures. |
| `uv run cep run reality-gap-corpus` | Evaluates all bundled RealityGapBench example answers. |
| `uv run cep run authority-corpus` | Evaluates all bundled AuthorityBench example answers. |
| `uv run cep run settlement-corpus` | Evaluates all bundled SettlementBench example answers. |
| `uv run cep run capability-corpus` | Evaluates all bundled CapabilityBench example answers. |

---

## 3. Recommended Learning Path

1. **Build Your Mental Model**: Read [System Mental Model](mental-model.md) to understand why CEP evaluates transformations through settlement rather than isolated outputs.
2. **Follow a Tutorial**: Complete [Tutorial: Scoring Your First RealityGap Answer](tutorials/first-reality-gap-evaluation.md) to score real candidate answers.
3. **Explore the Architecture**: Descend into [Canonical Architecture Specification](../architecture.md) for deep component models and source traceability.
4. **Author New Cases**: Consult [Authoring Benchmark Cases](authoring-cases.md) to contribute reviewed cases to the corpus.
