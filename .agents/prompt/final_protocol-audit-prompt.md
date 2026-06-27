You are acting as a **Senior Protocol Verification Architect and Benchmark Evaluation Engineer**.

You are reviewing the fully implemented `canonical-evaluation-protocol` repository.

This is not a normal code review. This is a final assurance audit.

Your job is to determine whether CEP is:

1. internally coherent as a protocol,
2. faithfully implemented in code,
3. executable through its CLI and tests,
4. supported by valid schemas and fixtures,
5. protected against semantic collapse,
6. and whether the benchmark families actually measure the outcomes they claim to measure.

## Source of Truth

Read these first:

```text
AGENTS.md
README.md
index.md
spec/index.md
spec/CEP-*.md
schemas/
benchmarks/
conformance/
src/cep/
tests/
.agents/CURRENT_STATUS.md
.agents/OPEN_QUESTIONS.md
.agents/DEBT.md
.agents/EVIDENCE.md
```

Treat the normative CEP specs as the source of protocol meaning.

Treat schemas, benchmark cases, answer keys, conformance fixtures, scorers, tests, reports, and CLI commands as implementation evidence.

Do not assume the project is correct because tests pass.

## Review Objective

Provide a rigorous final audit answering this question:

```text
Does the implemented CEP repository faithfully preserve the protocol’s intended distinctions and produce benchmark outcomes that actually test RealityGapBench, AuthorityBench, SettlementBench, and CapabilityBench as claimed?
```

## Core Distinctions to Protect

Audit specifically for collapse between:

```text
claim ≠ evidence
completion ≠ settlement
possibility ≠ affordance
authority ≠ capability
score ≠ capability
observation ≠ evidence
representation ≠ reality
declared state ≠ observed state
policy text ≠ authority decision
one-time success ≠ metabolized capability
test pass ≠ production readiness
summary ≠ source
unknown ≠ false
```

Any implementation, schema, test, fixture, benchmark case, scorer, or documentation that blurs these distinctions is a finding.

## Required Work Sequence

### 1. Baseline Execution

Run the project’s normal verification commands.

Prefer the documented command first:

```bash
just all
```

If unavailable, run the equivalent commands manually:

```bash
python tools/validate_okf.py
cep validate all
pytest
cep conformance anti-collapse
cep run reality-gap-corpus
cep run authority-corpus
cep run settlement-corpus
cep run capability-corpus
```

Record exact commands run and results.

Do not claim validation passed unless you ran the command or clearly explain why it could not be run.

---

### 2. Protocol Soundness Audit

Review `spec/CEP-0000` through `spec/CEP-0010`.

Check:

* the derivation ladder is coherent,
* later specs depend correctly on earlier specs,
* definitions do not conflict,
* normative language is clear,
* anti-collapse rules are present where needed,
* conformance requirements are testable,
* Semantic Envelope and benchmark models align with the rest of the protocol,
* the specs do not overclaim implementation maturity.

Output protocol findings separately from code findings.

---

### 3. Schema and Artifact Contract Audit

Review `schemas/` against actual artifacts under:

```text
benchmarks/
conformance/
reports/
examples/
```

Check:

* schemas validate the real artifact shapes,
* schemas are not so loose that invalid artifacts pass,
* schemas are not so strict that legitimate existing artifacts fail,
* required fields correspond to protocol load-bearing meaning,
* schema names and IDs are consistent,
* benchmark result schemas preserve enough evidence to inspect scores,
* conformance reports preserve failure reasons.

Look for missing contracts, duplicate schemas, unused schemas, and schema drift.

---

### 4. Benchmark Validity Audit

Audit each benchmark family separately.

#### RealityGapBench

Determine whether it actually tests:

```text
declared reality vs observed reality
gap detection
gap type classification
evidence grounding
protected distinctions
recommended next action
anti-collapse behavior
```

Check whether valid answers pass for the right reasons and invalid answers fail for the right reasons.

#### AuthorityBench

Determine whether it actually tests:

```text
actor + operation + resource + context + policy
→ allow / deny / escalate
```

Especially check false-allow handling.

AuthorityBench must not allow capability to substitute for authority.

#### SettlementBench

Determine whether it actually tests:

```text
execution/completion claim
vs
reliable consequence registration
```

SettlementBench must penalize premature completion.

#### CapabilityBench

Determine whether it actually tests:

```text
repeated settlement under variation
capability overclaim
affordance delta
metabolization
```

CapabilityBench must not let a score, one-time success, or possibility become capability.

---

### 5. Scoring and Anti-Collapse Audit

Review scorer implementations under `src/cep/`.

Check:

* score thresholds are explicit,
* anti-collapse caps are applied,
* invalid cases cannot silently pass,
* fabricated evidence or missing evidence is handled correctly,
* confidence does not mask wrong answers,
* scoring functions use answer keys correctly,
* valid answers are not hardcoded,
* invalid answers are not merely detected by filename,
* scorer behavior is tested by content, not naming convention.

Create adversarial mutations where useful.

Examples:

```text
valid answer with wrong gap_type
invalid answer renamed as valid
answer with missing evidence_refs
answer with fabricated evidence_refs
answer with correct label but wrong explanation
answer with high confidence and wrong conclusion
answer that claims capability from score alone
answer that treats approval as settlement
answer that treats policy text as runtime authority
```

If these pass incorrectly, record findings.

---

### 6. Test Quality Audit

Review `tests/`.

Check:

* tests verify behavior, not just existence,
* tests fail when protocol distinctions are violated,
* tests cover valid and invalid cases,
* tests cover anti-collapse fixtures,
* tests cover CLI commands,
* tests cover report generation,
* tests cover schema validation,
* tests are not brittle to harmless formatting changes,
* tests are not too shallow to catch semantic regressions.

Recommend missing tests.

---

### 7. Documentation and Agent Memory Audit

Review:

```text
README.md
AGENTS.md
.agents/CURRENT_STATUS.md
.agents/OPEN_QUESTIONS.md
.agents/DEBT.md
.agents/EVIDENCE.md
.agents/lessons/
```

Check:

* README reflects the actual executable state,
* AGENTS.md gives correct operating instructions,
* CURRENT_STATUS.md is current,
* OPEN_QUESTIONS.md contains real human decisions only,
* DEBT.md contains out-of-scope issues,
* EVIDENCE.md records actual verification evidence,
* no file claims completion without proof.

---

## Required Output

Create a final audit report at:

```text
.agents/reports/final_protocol_audit.md
```

If `.agents/reports/` does not exist, create it.

The report must use this structure:

```markdown
# Final Protocol Audit — Canonical Evaluation Protocol

## Executive Verdict

Choose one:

- PASS — Protocol and benchmarks are sound enough for current local proof.
- PASS WITH CONDITIONS — Core loop works, but specific issues must be fixed before public release.
- FAIL — Protocol or benchmark implementation has load-bearing gaps.

## Commands Run

List exact commands, exit status, and relevant output.

## Scope Reviewed

List files and directories reviewed.

## Protocol Soundness Findings

Findings related to CEP definitions, derivation ladder, specs, conformance model, and semantic coherence.

## Benchmark Validity Findings

Separate sections for:

- RealityGapBench
- AuthorityBench
- SettlementBench
- CapabilityBench

For each, answer:

1. What outcome does this benchmark claim to test?
2. Does the current implementation actually test that outcome?
3. What evidence supports that conclusion?
4. What gaps remain?

## Implementation Findings

Findings related to code, schemas, CLI, reports, tests, fixtures, and CI.

## Anti-Collapse Findings

List every semantic collapse risk found.

For each:

- collapse type
- location
- why it matters
- current protection
- missing protection
- recommended fix

## Adversarial / Falsification Tests

List any mutations or adversarial checks performed.

For each:

- mutation attempted
- expected failure
- actual result
- conclusion

## Severity-Ranked Findings

Use this severity model:

- Critical — protocol meaning is wrong, benchmark outcome is invalid, or false pass is possible.
- High — implementation can pass while missing a load-bearing distinction.
- Medium — ambiguity, under-tested behavior, weak schema, incomplete report, or brittle test.
- Low — cleanup, naming, docs, ergonomics, or non-blocking polish.

Each finding must include:

- ID
- severity
- affected files
- issue
- evidence
- recommended fix
- whether the fix should block release

## Recommended Fix Plan

Provide a sequenced repair plan:

1. first fix
2. second fix
3. third fix

Each fix must be small, testable, and tied to a finding.

## Release Readiness

State whether the repo is ready for:

- private continued development
- public GitHub visibility
- external benchmark users
- versioned `v0.1.0` release

Do not overclaim.

## Final Answer

Answer directly:

> Is CEP executable and do the benchmarks provide the intended outcomes?

Use plain language and cite the strongest evidence from the audit.
```

## Rules

Do not rewrite specs unless explicitly asked.

Do not make broad refactors during the audit.

You may propose patches, but the primary deliverable is the audit report.

If you find a critical issue that invalidates benchmark results, stop expansion work and document the blocker.

Update:

```text
.agents/CURRENT_STATUS.md
.agents/DEBT.md
.agents/OPEN_QUESTIONS.md, if human decisions are needed
.agents/EVIDENCE.md
```

Only add `.agents/lessons/` entries for durable, generalizable lessons.

## Completion Criteria

This audit is complete only when:

* verification commands were run or failure to run was documented,
* `.agents/reports/final_protocol_audit.md` exists,
* findings are severity-ranked,
* benchmark validity is assessed family by family,
* anti-collapse risks are explicitly reviewed,
* adversarial/falsification tests are documented,
* release readiness is stated,
* `.agents/CURRENT_STATUS.md` is updated,
* `.agents/EVIDENCE.md` records the audit.

Place the final report in `.agents/reports/final_protocol_audit.md` and submit it for review.
