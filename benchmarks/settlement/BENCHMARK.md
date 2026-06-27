---
type: "CEP Benchmark"
id: "settlementbench"
title: "SettlementBench"
description: "Benchmark family for evaluating completion versus settlement preservation."
status: "Draft"
version: "0.1.0"
tags:
  - cep
  - benchmark
  - settlement
timestamp: "2026-06-27T00:00:00Z"
---

# SettlementBench

SettlementBench evaluates whether a system distinguishes task execution from reliable consequence registration.

Protected distinctions:

```text
completion != settlement
execution != reliable consequence registration
```

An action can complete mechanically while the represented transformation remains unsettled.
