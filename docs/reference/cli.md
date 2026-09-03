---
type: "CEP Technical Reference"
id: "cep-reference-cli"
title: "CLI Command Reference"
description: "Precise technical specification for all commands, arguments, options, and exit codes in the cep command-line tool."
status: "Active"
version: "0.1.0"
tags:
  - cep
  - reference
  - cli
timestamp: "2026-06-27T00:00:00Z"
---

# CLI Command Reference

The `cep` executable is the official command-line interface for the Canonical Evaluation Protocol. Implemented in [src/cep/cli.py](../../src/cep/cli.py) using Typer.

---

## Global Options

### `--version`
* **Syntax**: `cep --version`
* **Purpose**: Prints current package version string (`0.1.0`) and exits 0.

### `--help`
* **Syntax**: `cep --help`
* **Purpose**: Displays usage synopsis and available command groups.

---

## Top-Level Commands

### `cep doctor`
* **Purpose**: Runs a lightweight environment check, validating that all registered JSON schemas in `schemas/index.json` conform to the CEP schema profile.
* **Syntax**: `cep doctor`
* **Arguments / Options**: None.
* **Exit Codes**:
  * `0`: Environment sound, all schemas valid.
  * `1`: One or more schemas failed profile validation.
* **Example**:
  ```bash
  uv run cep doctor
  ```

### `cep score-settlement`
* **Purpose**: Scores a `SettlementRecorded`-shaped payload synchronously against expected settlement criteria.
* **Syntax**: `cep score-settlement --input <FILE>`
* **Options**:
  * `--input <FILE>` *(required)*: Path to JSON input document containing `settlement_recorded`, `expected`, and optional `evidence_refs` / `preserved_distinctions`.
* **Exit Codes**:
  * `0`: Document successfully scored.
  * `1`: Input malformed or missing required keys.
* **Output Format**: `<STATUS> <case_id> <answer_id> score=<score>` (and `critical_failures=[...]` if any).
* **Example**:
  ```bash
  uv run cep score-settlement --input tests/fixtures/sample_settlement_recorded.json
  ```

---

## `cep validate` Subcommands

### `cep validate schemas`
* **Purpose**: Validates all registered schemas against the JSON Schema Draft 2020-12 profile in `cep.schema_profile`.
* **Syntax**: `cep validate schemas`
* **Exit Codes**: `0` on success, `1` on error.

### `cep validate reality-gap-corpus`
* **Purpose**: Validates all RealityGapBench corpus artifacts (case files, answer keys, example answers, evidence files, manifest, and fixtures) against their registered schemas.
* **Syntax**: `cep validate reality-gap-corpus`
* **Exit Codes**: `0` on success, `1` on error.

### `cep validate semantic-envelope`
* **Purpose**: Validates Semantic Envelope fixtures or inputs against `cep-semantic-envelope.schema.json`.
* **Syntax**: `cep validate semantic-envelope [PATH] [--stdin]`
* **Options / Arguments**:
  * `[PATH]`: Optional path to a single envelope JSON file.
  * `--stdin`: Optional boolean flag to read one envelope from stdin.
  * *(Omitted arguments)*: Validates all fixtures in `schemas/fixtures/semantic-envelope/` and `semantic-envelope-full/`.
* **Exit Codes**: `0` on success, `1` on error.
* **Example**:
  ```bash
  cat envelope.json | uv run cep validate semantic-envelope --stdin
  ```

### `cep validate all`
* **Purpose**: Chains `validate schemas`, `validate reality-gap-corpus`, and `validate semantic-envelope`.
* **Syntax**: `cep validate all`
* **Exit Codes**: `0` on success, `1` on error.

---

## `cep conformance` Subcommands

### `cep conformance anti-collapse`
* **Purpose**: Evaluates candidate answers with the content-based collapse detector.
* **Syntax**: `cep conformance anti-collapse [--corpus <FILE>]`
* **Options**:
  * `--corpus <FILE>` *(optional)*: Path to an external corpus adhering to `cep/anti-collapse-corpus@1`.
  * *(Omitted flag)*: Evaluates internal RealityGapBench anti-collapse fixtures (`conformance/fixtures/anti-collapse/reality-gap/`) and cross-family example answer invariants.
* **Exit Codes**:
  * `0`: All fixtures/records caught or passed as expected.
  * `1`: Missing expected failures or unexpected collapse.
  * `2`: Malformed external corpus format.
* **Example**:
  ```bash
  uv run cep conformance anti-collapse
  uv run cep conformance anti-collapse --corpus sxr-export.json
  ```

---

## `cep run` Subcommands

### `cep run reality-gap`
* **Purpose**: Scores one candidate answer against a specific RealityGapBench case.
* **Syntax**: `cep run reality-gap --case-dir <DIR> --answer <FILE> [--out <FILE>]`
* **Options**:
  * `--case-dir <DIR>` *(required)*: Path to case directory (e.g. `benchmarks/reality-gap/cases/rg-0001`).
  * `--answer <FILE>` *(required)*: Path to candidate answer JSON file.
  * `--out <FILE>` *(optional)*: Output report destination (defaults to `reports/reality-gap/<case_id>-<answer_id>.result.json`).
* **Exit Codes**: `0` on execution.

### `cep run reality-gap-corpus`
* **Purpose**: Discovers and scores all example answers across all RealityGapBench cases.
* **Syntax**: `cep run reality-gap-corpus`
* **Exit Codes**: `0` if all valid answers pass/partial and all invalid answers do not pass; `1` on regression.

### `cep run authority-corpus`
* **Purpose**: Discovers and scores all example answers across all AuthorityBench cases.
* **Syntax**: `cep run authority-corpus`
* **Exit Codes**: `0` on clean evaluation, `1` on regression.

### `cep run settlement-corpus`
* **Purpose**: Discovers and scores all example answers across all SettlementBench cases.
* **Syntax**: `cep run settlement-corpus`
* **Exit Codes**: `0` on clean evaluation, `1` on regression.

### `cep run capability-corpus`
* **Purpose**: Discovers and scores all example answers across all CapabilityBench cases.
* **Syntax**: `cep run capability-corpus`
* **Exit Codes**: `0` on clean evaluation, `1` on regression.
