// A snapshot emitted by the real DomainForge binary must pass this validator.
// Gated on CEP_TEST_DOMAINFORGE_BIN (a build with --world-name); skipped otherwise.
import { describe, expect, test } from "bun:test";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { Contract, worldRefOf } from "../src/index.js";

const BIN = process.env["CEP_TEST_DOMAINFORGE_BIN"];
const HEADER = '@namespace "auth"\n@version "1.0.0"\n\n';
const VALID = 'Entity "User" in auth\nEntity "Role" in auth\n';

function emit(source: string, flags: string[]) {
  const dir = mkdtempSync(join(tmpdir(), "cep-emitted-"));
  try {
    const path = join(dir, "model.sea");
    writeFileSync(path, source);
    const proc = Bun.spawnSync([BIN!, "envelope", "--emit", "cep", ...flags, path]);
    return { code: proc.exitCode, env: JSON.parse(proc.stdout.toString()) };
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

describe.skipIf(!BIN)("real DomainForge emission", () => {
  const contract = new Contract();

  test("valid world snapshot conforms and verifies", () => {
    const { code, env } = emit(HEADER + VALID, ["--world-name", "godspeed-corporate", "--world-alias", "world:corporate"]);
    expect(code).toBe(0);
    expect(contract.validate("semantic_snapshot", env)).toEqual([]);
    expect(contract.verifySemantics("semantic_snapshot", env)).toEqual([]);
    expect(worldRefOf(env)).toBeDefined();
  });

  test("invalid world is flagged, not pinned, and conforms", () => {
    const { code, env } = emit("this is not sea", ["--world-name", "godspeed-corporate"]);
    expect(code).not.toBe(0);
    expect(worldRefOf(env)).toBeUndefined();
    expect(contract.validate("semantic_snapshot", env)).toEqual([]);
    expect(contract.verifySemantics("semantic_snapshot", env)).toEqual([]);
  });

  test("a snapshot without --world-name does not claim the profile", () => {
    const { env } = emit(HEADER + VALID, []);
    expect(contract.validate("semantic_snapshot", env).length).toBeGreaterThan(0);
  });
});
