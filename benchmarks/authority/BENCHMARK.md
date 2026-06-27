---
type: "CEP Benchmark"
id: "authoritybench"
title: "AuthorityBench"
description: "Benchmark family for evaluating pre-action authority preservation."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - benchmark
  - authority
timestamp: "2026-06-27T00:00:00Z"
---

# AuthorityBench

AuthorityBench evaluates whether a system can decide whether an actor may perform an operation on a resource in a given context.

Core decision shape:

```text
actor + operation + resource + context + policy
  -> allow | deny | escalate
  -> evidence
```

Primary protected distinction:

```text
authority != capability
```

Capability to execute an operation is not authority to execute it. A system must preserve policy, context, and evidence requirements before recommending an action.
