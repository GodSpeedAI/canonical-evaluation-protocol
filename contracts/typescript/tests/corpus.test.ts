// The TypeScript validator must reach the same verdicts as the Python and Rust
// validators on the shared corpus in schemas/fixtures/godspeed.
import { describe, expect, test } from "bun:test";
import { readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import {
  Contract,
  DECISIONS,
  checkWorldConsistency,
  decisionOf,
  decisionRequiresConstraints,
  identityDigest,
  isUnrestrictedAllow,
  profileFromKind,
  type Profile,
} from "../src/index.js";

const repo = resolve(dirname(fileURLToPath(import.meta.url)), "../../..");
const json = (...p: string[]) => JSON.parse(readFileSync(join(repo, ...p), "utf8"));
const corpus = (name: string) => json("schemas", "fixtures", "godspeed", name);
const manifest = corpus("manifest.json");
const contract = new Contract();

describe("shared corpus", () => {
  test("corpus is non-trivial", () => expect(manifest.cases.length).toBeGreaterThanOrEqual(30));

  for (const c of manifest.cases as any[]) {
    test(`schema verdict: ${c.file}`, () => {
      const errors = contract.validate(c.profile as Profile, corpus(c.file));
      if (c.schema === "valid") expect(errors).toEqual([]);
      else expect(errors.length).toBeGreaterThan(0);
    });
    if (c.schema === "valid") {
      test(`semantic verdict: ${c.file}`, () => {
        const errors = contract.verifySemantics(c.profile as Profile, corpus(c.file));
        if (c.semantic === "ok") expect(errors).toEqual([]);
        else {
          expect(errors.length).toBeGreaterThan(0);
          if (c.semantic_error_contains) {
            expect(errors.some((e) => e.includes(c.semantic_error_contains))).toBe(true);
          }
        }
      });
    }
  }

  for (const chain of manifest.chains as any[]) {
    test(`lineage world: ${chain.case}`, () => {
      const envs = chain.files.map((name: string) => {
        const env = corpus(name);
        const override = chain.override?.[name];
        if (override) env.scope.world_ref = override;
        return env;
      });
      const ok = checkWorldConsistency(envs).length === 0;
      expect(ok).toBe(chain.expect === "consistent");
    });
  }

  test("validateDeclared routes by envelope_kind", () => {
    for (const c of manifest.cases.filter((x: any) => x.schema === "valid")) {
      const r = contract.validateDeclared(corpus(c.file));
      expect(r.errors).toEqual([]);
      expect(r.profile).toBe(c.profile);
    }
    const unknown = corpus("valid/authority_request.json");
    unknown.envelope_kind = "composite";
    expect(contract.validateDeclared(unknown).errors.length).toBeGreaterThan(0);
    expect(profileFromKind("composite")).toBeUndefined();
  });
});

describe("DomainForge identity", () => {
  test("digest matches the vendored golden vectors", () => {
    const vectors = json("schemas", "vendored", "world_ref", "golden-vectors.json");
    for (const c of vectors.valid) expect(identityDigest(c.identity)).toBe(c.canonical_digest);
  });
});

describe("authority dispositions", () => {
  test("typed, never boolean; only allow is unrestricted", () => {
    for (const d of DECISIONS) {
      const env = corpus(`valid/authority_decision-${d}.json`);
      expect(decisionOf(env)).toBe(d);
      expect(isUnrestrictedAllow(d)).toBe(d === "allow");
      expect(decisionRequiresConstraints(d)).toBe(
        d === "constrained_allow" || d === "boundary" || d === "degraded",
      );
    }
    expect(decisionOf(corpus("invalid/authority_decision-boolean-flattened.json"))).toBeUndefined();
    expect(decisionOf(corpus("invalid/authority_decision-unrecognised-disposition.json"))).toBeUndefined();
  });
});

describe("world transition", () => {
  const a = manifest.worlds.A.world_ref;
  const b = manifest.worlds.B.world_ref;
  const good = {
    source_world_ref: a,
    target_world_ref: b,
    transition_kind: "semantic_change",
    reason: "corporate policy model gained a Pump entity",
    compatibility: "backward_compatible",
    semantic_closure_equal: false,
  };
  test("explicit and must move", () => {
    expect(contract.validateWorldTransition(good)).toEqual([]);
    expect(contract.validateWorldTransition({ ...good, target_world_ref: a }).length).toBeGreaterThan(0);
    expect(contract.validateWorldTransition({ ...good, target_world_ref: "world:corporate" }).length).toBeGreaterThan(0);
    const { reason: _r, ...missing } = good;
    expect(contract.validateWorldTransition(missing).length).toBeGreaterThan(0);
  });
});
