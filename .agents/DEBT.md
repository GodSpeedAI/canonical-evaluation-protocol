> **Remediation banner (2026-06-27):** DEBT-0002 through DEBT-0008 (the Final
> Protocol Audit findings) are **RESOLVED**. Fixes verified by `just all`, `ruff`,
> and `basedpyright` (0 errors); see the Remediation Log in
> `.agents/reports/final_protocol_audit.md`. The per-entry "Status: Open" lines
> below are superseded by this banner and each entry's "Resolved" note.

## DEBT-0001 — OKF Validator Warned On Example Links In AGENTS.md

- **ID**: DEBT-0001
- **Title**: OKF validator warns on example links in `AGENTS.md`
- **Date**: 2026-06-27
- **Found By**: Codex
- **Area**: OKF validation
- **Description**: `uv run python tools/validate_okf.py` previously exited successfully but warned that example links like `./CEP-0000-derivation-ladder.md` in `AGENTS.md` did not resolve from the repo root.
- **Why It Matters**: Non-fatal warning noise could hide future link warnings that do matter.
- **Recommended Repair**: Teach `tools/validate_okf.py` to ignore links inside fenced code blocks, or rewrite the example navigation block so its example links are not parsed as real repo links.
- **Priority**: Low
- **Scope Note**: Out of scope for phases 0-3 because validation exits zero and the warnings come from instructional examples, not public spec navigation.
- **Status**: Closed — fixed by ignoring fenced code blocks and making broken concept-document links fail in `tools/validate_okf.py`.

## DEBT-0002 — Anti-collapse conformance does not run the engine

- **ID**: DEBT-0002
- **Title**: Anti-collapse conformance suite is self-referential
- **Date**: 2026-06-27
- **Found By**: Final Protocol Audit (see `.agents/reports/final_protocol_audit.md` F-01)
- **Area**: `src/cep/conformance/anti_collapse.py`
- **Description**: `check_fixture` reads `observed = fixture.expected_validation.errors` and never runs a scorer/validator on `submitted_answer`. It verifies the fixture's self-declared errors ⊇ manifest, not that the engine detects collapse. Proven: the real RealityGap scorer cannot emit `declared_observed_collapse`.
- **Why It Matters**: CEP-0010 requires behavioral anti-collapse enforcement; `cep conformance anti-collapse` 10/10 PASS is not evidence of detection.
- **Recommended Repair**: Drive each fixture `submitted_answer` through the real scorer/validator; compare observed failures to the manifest.
- **Priority**: Critical (blocks public anti-collapse claims).
- **Status**: Resolved (2026-06-27) — see Remediation Log in `.agents/reports/final_protocol_audit.md`.

## DEBT-0003 — RealityGap declared failure caps mostly unreachable

- **ID**: DEBT-0003
- **Date**: 2026-06-27
- **Found By**: Final Protocol Audit (F-02)
- **Area**: `src/cep/benchmarks/reality_gap.py`
- **Description**: 10 of 14 `CRITICAL_FAILURE_CAPS` are never assigned by `_detected_failures` (declared_observed_collapse, unknown_as_false, ci_approval_collapse, possibility_affordance_collapse, authority_capability_collapse, summary_source_collapse, score_capability_collapse, fabricated_evidence, readiness_claim_as_evidence, missing_evidence_as_failure_proof).
- **Recommended Repair**: Implement load-bearing detectors or delete dead caps.
- **Priority**: High.
- **Status**: Resolved (2026-06-27) — see Remediation Log in `.agents/reports/final_protocol_audit.md`.

## DEBT-0004 — RealityGap scoring is reasoning-blind

- **ID**: DEBT-0004
- **Date**: 2026-06-27
- **Found By**: Final Protocol Audit (F-03)
- **Area**: `src/cep/benchmarks/reality_gap.py`
- **Description**: `gap_summary` is ignored except a `"completed"` substring check. A correct-label answer with a garbage explanation scores 99.0/PASS.
- **Recommended Repair**: Require reasoning grounded in accepted evidence/distinctions.
- **Priority**: High.
- **Status**: Resolved (2026-06-27) — see Remediation Log in `.agents/reports/final_protocol_audit.md`.

## DEBT-0005 — SettlementBench hardcodes "settled = collapse"

- **ID**: DEBT-0005
- **Date**: 2026-06-27
- **Found By**: Final Protocol Audit (F-04)
- **Area**: `src/cep/benchmarks/settlement.py`
- **Description**: `_detected_failures` flags any `settled`/claim-accepted answer regardless of `expected_settlement_status`, so the family cannot score a genuinely-settled case.
- **Recommended Repair**: Only flag when `expected_settlement_status != "settled"`.
- **Priority**: High (blocks adding any settled-positive case).
- **Status**: Resolved (2026-06-27) — see Remediation Log in `.agents/reports/final_protocol_audit.md`.

## DEBT-0006 — Non-RG report metrics hardcode recall=1.0

- **ID**: DEBT-0006
- **Date**: 2026-06-27
- **Found By**: Final Protocol Audit (F-06)
- **Area**: `authority.py`, `settlement.py`, `capability.py`
- **Description**: `constraint_recall` and `relation_recall` are literal `1.0` in `ScoreMetrics`, misrepresenting what was measured.
- **Recommended Repair**: Compute real values or omit/null them.
- **Priority**: Medium.
- **Status**: Resolved (2026-06-27) — see Remediation Log in `.agents/reports/final_protocol_audit.md`.

## DEBT-0007 — Anti-collapse fixtures only for RealityGapBench

- **ID**: DEBT-0007
- **Date**: 2026-06-27
- **Found By**: Final Protocol Audit (F-07)
- **Area**: `conformance/fixtures/`
- **Description**: No anti-collapse fixtures/runner for AuthorityBench, SettlementBench, CapabilityBench.
- **Recommended Repair**: Add fixtures + runner per family.
- **Priority**: Medium.
- **Status**: Resolved (2026-06-27) — see Remediation Log in `.agents/reports/final_protocol_audit.md`.

## DEBT-0008 — Stray report artifact

- **ID**: DEBT-0008
- **Date**: 2026-06-27
- **Found By**: Final Protocol Audit (F-10)
- **Area**: `reports/test-rg-0001-valid.result.json`
- **Description**: Stray non-conforming report at reports root.
- **Recommended Repair**: Delete.
- **Priority**: Low.
- **Status**: Resolved (2026-06-27) — see Remediation Log in `.agents/reports/final_protocol_audit.md`.
