# Implementation Plan — CEP: Ship the Canonical Schema and a Callable Scoring Surface

**Created:** 2026-07-01

**Source of truth:** `SEA/.agents/reports/syntelligent_infrastructure.md` §4.5
("CEP reference implementation"), §6 Contract and Envelope Audit (Finding
"Canonical candidate", Recommendation), §9 LE-03, LE-06, LE-15, LE-25, §13
WP-2, WP-5. Quote it, don't paraphrase from memory.

**Originating context:** The audit found CEP is *implemented* (a runnable
`typer` CLI, four benchmark scorers, anti-collapse enforcement) but not
*loop-wired* — it evaluates corpora/fixtures, not live settlement events, and
CEP-0008 (its own canonical envelope spec) ships no JSON Schema. This is the
biggest gap in the whole ecosystem's Evaluate/Adapt arc: real evaluation
machinery exists and does nothing at runtime.

**Status of the work today:** `cep/src/cep/` has a working CLI
(`validate`, `conformance`, `run`, `doctor`) and four scorers
(`benchmarks/{authority,settlement,capability,reality_gap}.py`) that already
operate on pydantic answer-key/answer models. What's missing is (a) a shipped
JSON Schema for CEP-0008 so the canon is enforceable, not prose, and (b) a
stable, documented call surface (function or CLI invocation) that
godspeed_agent's plan can call at `SettlementRecorded` without CEP needing to
know anything about godspeed_agent.

---

## 0. How to use this plan (agent operating instructions)

- Task 1 (ship the schema) has no dependency. Task 2 (expose a callable
  scoring surface) depends on Task 1 only insofar as it should conform to
  the same field names; they can be done in either order but Task 1 first is
  recommended.
- **Every task ends with a verification gate.** Do not mark a task done
  until its gate command exits 0.
- **Core principle: CEP defines vocabulary and scores answers — it does not
  reach into other repos.** This plan's job is to make CEP *callable*, not to
  wire CEP into godspeed_agent or SWE_SEED — that wiring is godspeed_agent's
  plan (task 2), which calls into CEP's public surface built here. Do not add
  NATS/event-bus consumption logic to CEP in this plan; keep it a
  library/CLI other repos call synchronously or via CI job.
- Match surrounding code style: `cep/src/cep/benchmarks/*.py` (pydantic
  models + scoring functions), `cep/src/cep/scoring/common.py` (`recall`,
  `status_from_score` — reuse these, don't reinvent).
- The `benchmarks/*.py` fixtures/answer-keys are the spec for what "correct"
  means per scorer — change them deliberately, in the same commit as any
  scoring-logic change that justifies it.

### Global verification gates (must stay green after EVERY task)

```bash
cd /home/sprime01/projects/cep
just ci-test     # or: pytest — check justfile for the exact CI target name
cep validate all
cep conformance anti-collapse
```

No rebuild/codegen step in this repo.

---

## Key facts already discovered (do not re-derive)

| Thing | Location |
|---|---|
| CEP-0008 spec (conceptual canon, prose only, no schema today) | `cep/spec/CEP-0008-semantic-envelope.md` — explicitly states "does not define final JSON Schema" (§2) |
| CLI entry point | `cep/src/cep/cli.py` (typer): `validate`, `conformance`, `run`, `doctor` |
| Four benchmark scorers | `cep/src/cep/benchmarks/{authority,settlement,capability,reality_gap}.py` |
| Shared scoring utilities | `cep/src/cep/scoring/common.py` — `recall`, `status_from_score` |
| Anti-collapse enforcement (CEP's core thesis, executable) | `cep/src/cep/conformance/anti_collapse.py`, `CRITICAL_FAILURE_CAPS` (e.g. `completion_settlement_collapse` caps score at 30.0) |
| Settlement scorer's model, which mirrors the loop's real `SettlementRecorded` event shape | `cep/src/cep/benchmarks/settlement.py` — fields `expected_settlement_status`, `required_evidence_refs`, `required_distinctions`, `completion_claim_accepted` |
| Existing schema directory (where the new JSON Schema belongs) | `cep/schemas/*.json` (already holds `benchmark-result.schema.json` — follow its style) |
| v1 flat envelope this schema must be provable-compatible with | `hassos-addon-agent-memory-ledger/agent_memory_ledger/rootfs/usr/share/agent_memory_ledger/contracts/sea.agent.event.v1.json` (see plan 00-INDEX.md cross-cutting facts) — required: `schema_version`(`"v1"`), `event_id`, `source_agent`, `occurred_at`, `payload`; optional `idempotency_key`, `source`, `event_type`, `correlation_id`, `causation_id`, `trace_id`, `provenance{origin,chain}`, `metadata`; `additionalProperties: false` |
| The real `SettlementRecorded` payload shape produced at runtime, which the new call surface (Task 2) must accept | `godspeed_agent/agentic_capability_loop/adapters.py` `handle_evidence_recorded()` — emits `usable`/`partial`/`unusable` classification (see godspeed_agent plan for exact field names before writing Task 2's adapter function signature) |
| PET's unrelated "Prompt Judge" naming collision to flag (not fix in code, just disambiguate in docs) | `SEA/libs/pet/ports/src/prompt-judge.port.ts`, `llm-prompt-judge.adapter.ts` — a different product, evaluates human-written prompts, not CEP's domain |

---

## Task 1 — Ship `cep/schemas/semantic-envelope.schema.json` and prove v1 is a conformant profile

**Goal:** CEP-0008's canon is enforceable, not prose: a JSON Schema exists
under `cep/schemas/`, and a test in this repo proves a real v1 envelope
instance (from agent-memory-ledger's contract) validates as a conformant
profile of it.

**Why this shape:** LE-03's exact framing: "canon is prose, not enforceable."
The audit's recommendation (§6) is explicit: adopt CEP-0008 as the canonical
*semantic model*, and "define one JSON Schema profile of it that equals the
flat v1 contract (family C is the closest to a real schema and is already
enforced at the durable boundary)." This is not "replace v1" — it's "prove
v1 already satisfies CEP-0008's distinctions, formally."

### Steps

1. Read `cep/spec/CEP-0008-semantic-envelope.md` in full for the exact
   distinctions it names (state, transformation, question, evidence,
   settlement, authority, capability, provenance, uncertainty, omissions).
2. Author `cep/schemas/semantic-envelope.schema.json` (JSON Schema draft
   2020-12, matching the style of the existing
   `cep/schemas/benchmark-result.schema.json`) encoding those distinctions as
   schema properties, with the v1 flat contract's field names
   (`payload`, `provenance`, `event_type`, `source_agent`) mapped onto them
   via a documented `$comment` or adjacent mapping doc — do not invent new
   field names that don't correspond to anything real.
3. Add 2-3 fixture instances under `cep/schemas/fixtures/` (or wherever
   existing schema fixtures live) built from real v1 envelope shapes (copy
   the required/optional fields from the `sea.agent.event.v1.json` contract
   listed in Key Facts above).
4. Add a `cep validate` subcommand path (or extend the existing `validate`
   command) that validates a v1-shaped instance against
   `semantic-envelope.schema.json` and reports pass/fail per CEP-0008
   distinction.

### Gate

```bash
cd /home/sprime01/projects/cep
cep validate semantic-envelope
pytest -k "semantic_envelope or cep_0008" -v
```

**Done when:** the validate command passes on the v1-shaped fixtures, and
fails with a specific, named-distinction error if a fixture is mutated to
drop a CEP-0008-required concept (e.g. remove `provenance`) — proving the
schema actually encodes CEP-0008's distinctions rather than being a
pass-through `{"type": "object"}`.

**Redesign trigger:** if encoding CEP-0008's full distinction set turns out
to require fields the v1 contract cannot represent under
`additionalProperties: false`, do not silently drop those distinctions from
the schema to make the test pass — document the gap explicitly as an open
question in this file and flag it back for a cross-repo decision (do not
resolve unilaterally in this plan).

---

## Task 2 — Expose a stable, documented settlement-scoring call surface for producers

**Goal:** A function or CLI invocation exists that any producer repo (today:
godspeed_agent) can call synchronously at settlement time, passing a
`SettlementRecorded`-shaped payload, and get back a CEP score/status —
without CEP needing any knowledge of godspeed_agent, NATS, or the live loop.

**Why this shape:** LE-06's framing: "Evaluate/Adapt arc has an engine but no
live feed — wiring, not building." The wiring itself belongs in the
*producer's* plan (a producer calls CEP, CEP doesn't reach out and subscribe
to anything) — this repo's job is only to make that call surface exist,
stable, and documented, so godspeed_agent's plan can consume it with zero
CEP-internals knowledge.

### Steps

1. In `cep/src/cep/benchmarks/settlement.py`, confirm/add a top-level
   function (e.g. `score_settlement(answer: SettlementAnswer) -> ScoreResult`)
   that wraps the existing scorer logic — reuse `scoring/common.py`'s
   `recall`/`status_from_score`, do not duplicate.
2. Define (or confirm existing) the exact pydantic input model's field names
   — these must match what a real `SettlementRecorded` payload can supply:
   `expected_settlement_status`, `required_evidence_refs`,
   `required_distinctions`, `completion_claim_accepted` (per Key Facts table
   above). If godspeed_agent's actual payload uses different field names,
   add a thin adapter function in this repo (`from_settlement_recorded(payload: dict) -> SettlementAnswer`)
   rather than asking godspeed_agent to reshape its event — CEP owns the
   vocabulary translation since it owns the vocabulary.
3. Add a CLI passthrough (`cep score-settlement --input <json-file>` or
   similar under `cli.py`) so the same function is callable from a shell
   step, not only as a Python import, for repos that don't want a Python
   dependency on CEP.
4. Document the call contract (input shape, output shape, exit codes for
   CLI) in a short README section or docstring — this is the exact text
   godspeed_agent's plan (task 2) needs to wire against without opening this
   repo's source.

### Gate

```bash
cd /home/sprime01/projects/cep
pytest -k "score_settlement or settlement_answer" -v
cep score-settlement --input tests/fixtures/sample_settlement_recorded.json
```

**Done when:** the CLI and the Python function both accept a realistic
`SettlementRecorded`-shaped fixture and return a score/status; deliberately
passing a fixture that violates `completion_settlement_collapse` (per
`CRITICAL_FAILURE_CAPS`) must cap the score at 30.0, proving the call surface
actually routes through the real anti-collapse scorer and isn't a stub.

**Redesign trigger:** none plausible — this wraps existing, tested scoring
logic behind a new entry point; no scoring logic itself changes.

---

## Task 3 — Disambiguate CEP's "scorer" vocabulary from PET's "Prompt Judge" (LE-25)

**Goal:** A short, discoverable note exists (README or module docstring)
stating CEP's benchmark scorers are unrelated to `libs/pet`'s "Prompt Judge"
concept in the SEA repo, so a future code-searcher doesn't conflate them.

**Why this shape:** LE-25's exact framing: "at least three unrelated things
called some variant of 'Judge' or 'scorer'... A reader skimming code search
results for 'judge' or 'score' across this stack will hit all three and
could easily conflate them. No functional defect — a documentation/naming
clarity item."

### Steps

1. Add a short paragraph to `cep/README.md` (or `cep/src/cep/benchmarks/__init__.py`
   docstring) stating explicitly: "CEP's scorers evaluate *agent transformations*
   against evidence/settlement/authority/capability distinctions. They are
   unrelated to SEA's PET (`libs/pet`) 'Prompt Judge', which evaluates
   *human-written prompts* in a gamified training app — different product,
   different domain, coincidental name overlap."

### Gate

```bash
grep -n "Prompt Judge" /home/sprime01/projects/cep/README.md
```

**Done when:** the disambiguation text is present and greppable — this is a
documentation task, its "gate" is presence-verification, not a test.

**Redesign trigger:** none plausible.

---

## Final acceptance checklist (whole plan)

- [ ] `cep/schemas/semantic-envelope.schema.json` exists and validates real
      v1-shaped fixtures, with a teeth-check (mutated fixture fails on a
      named distinction). *(Task 1)*
- [ ] A stable `score_settlement` function + CLI command exists, documented,
      callable by another repo without reading CEP's source; a
      collapse-triggering fixture correctly caps at 30.0. *(Task 2)*
- [ ] CEP/PET naming disambiguation text is present in the README. *(Task 3)*
- [ ] All global gates green (`cep validate all`, `cep conformance
      anti-collapse`, test suite).
- [ ] No scoring logic in `benchmarks/*.py` was changed — only new entry
      points added around it.

## Guardrails (do not violate)

- Do not add NATS/event-bus subscription logic to CEP — it stays a
  library/CLI other repos call, per the audit's own framing ("CEP → rest:
  none yet... define producer at settlement" — the producer is
  godspeed_agent, not CEP itself).
- Do not modify `CRITICAL_FAILURE_CAPS` or any existing scorer's pass/fail
  logic while building the new call surface — Task 2 wraps, it doesn't
  change scoring behavior.
- Do not resolve a CEP-0008/v1 field-set mismatch unilaterally if one is
  found in Task 1 — escalate, don't invent a compromise schema.
- Commit hygiene: keep Task 3 (a two-line doc change) in its own commit,
  separate from the schema/scoring work in Tasks 1-2.
