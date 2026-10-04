// GodSpeed CEP-0008 profile validation (TypeScript).
//
// Schemas and the conformance corpus live in the cep repository; this module reads
// the schema files directly, so there is no second copy to drift. Beyond schema
// validation it performs checks a schema cannot make. The world_ref grammar is
// defined by DomainForge: this module never parses it, it compares strings and the
// digest suffix only.
import Ajv2020 from "ajv/dist/2020.js";
import type { ValidateFunction } from "ajv/dist/2020.js";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export type {
  SemanticEnvelope,
  SemanticSnapshotEnvelope,
  AuthorityRequestEnvelope,
  AuthorityDecisionEnvelope,
  ExecutionTraceEnvelope,
  EvidencePacketEnvelope,
  SettlementPacketEnvelope,
  WorldTransition,
} from "./generated/envelope-types.js";

export const PROFILES = [
  "semantic_snapshot",
  "authority_request",
  "authority_decision",
  "execution_trace",
  "evidence_packet",
  "settlement_packet",
] as const;
export type Profile = (typeof PROFILES)[number];

/** Authority disposition. Never a boolean: only "allow" is an unrestricted allow. */
export const DECISIONS = [
  "allow",
  "deny",
  "escalate",
  "unknown",
  "constrained_allow",
  "boundary",
  "degraded",
] as const;
export type Decision = (typeof DECISIONS)[number];

const BASE_ID = "https://cep.dev/schemas/cep-semantic-envelope.schema.json";
const IDENTITY_NS = "domainforge.identity";
const schemasDir = resolve(dirname(fileURLToPath(import.meta.url)), "../../../schemas");

type Json = null | boolean | number | string | Json[] | { [key: string]: Json };
type JsonObject = { [key: string]: Json };

const read = (...parts: string[]): JsonObject =>
  JSON.parse(readFileSync(join(schemasDir, ...parts), "utf8")) as JsonObject;

const isObject = (v: unknown): v is JsonObject =>
  typeof v === "object" && v !== null && !Array.isArray(v);

export const profileId = (profile: Profile): string => `godspeed.${profile}`;

export const profileFromKind = (kind: unknown): Profile | undefined =>
  PROFILES.find((p) => p === kind);

export const isDecision = (value: unknown): value is Decision =>
  typeof value === "string" && (DECISIONS as readonly string[]).includes(value);

export const isUnrestrictedAllow = (d: Decision): boolean => d === "allow";

export const decisionRequiresConstraints = (d: Decision): boolean =>
  d === "constrained_allow" || d === "boundary" || d === "degraded";

/** Typed disposition of an authority_decision envelope, or undefined if absent/unrecognised. */
export function decisionOf(envelope: unknown): Decision | undefined {
  if (!isObject(envelope)) return undefined;
  const ext = envelope["extensions"];
  const block = isObject(ext) ? ext["godspeed.authority_decision"] : undefined;
  const value = isObject(block) ? block["decision"] : undefined;
  return isDecision(value) ? value : undefined;
}

/** The pinned world_ref string of an envelope (scope.world_ref). */
export function worldRefOf(envelope: unknown): string | undefined {
  if (!isObject(envelope)) return undefined;
  const scope = envelope["scope"];
  const value = isObject(scope) ? scope["world_ref"] : undefined;
  return typeof value === "string" ? value : undefined;
}

/** Canonical JSON: UTF-8, recursively sorted keys, no whitespace. */
export function canonicalJson(value: unknown): string {
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  if (isObject(value)) {
    return `{${Object.keys(value)
      .sort()
      .map((k) => `${JSON.stringify(k)}:${canonicalJson(value[k])}`)
      .join(",")}}`;
  }
  return JSON.stringify(value);
}

/** sha256 over canonical JSON of a DomainModelIdentity, as `sha256:<hex>`. */
export function identityDigest(identity: unknown): string {
  return `sha256:${createHash("sha256").update(canonicalJson(identity), "utf8").digest("hex")}`;
}

export class Contract {
  private readonly validators = new Map<Profile, ValidateFunction>();
  private readonly transition: ValidateFunction;

  constructor() {
    const ajv = new Ajv2020({ allErrors: true, strict: false });
    ajv.addSchema(read("cep-semantic-envelope.schema.json"), BASE_ID);
    for (const profile of PROFILES) {
      this.validators.set(
        profile,
        ajv.compile(read("profiles", "godspeed", `${profile}.v1.schema.json`)),
      );
    }
    this.transition = ajv.compile(read("profiles", "godspeed", "world-transition.v1.schema.json"));
  }

  /** Schema errors for one profile; an empty array means valid. */
  validate(profile: Profile, envelope: unknown): string[] {
    return collect(this.validators.get(profile)!, envelope);
  }

  /** Validate against the profile named by the envelope's own kind. */
  validateDeclared(envelope: unknown): { profile?: Profile; errors: string[] } {
    const kind = isObject(envelope) ? envelope["envelope_kind"] : undefined;
    const profile = profileFromKind(kind);
    if (!profile) return { errors: [`no GodSpeed profile for envelope_kind ${JSON.stringify(kind)}`] };
    const errors = this.validate(profile, envelope);
    return errors.length ? { errors } : { profile, errors };
  }

  /** Checks a schema cannot make; an empty array means the envelope's claims hold. */
  verifySemantics(profile: Profile, envelope: unknown): string[] {
    const problems: string[] = [];
    const ext = isObject(envelope) ? envelope["extensions"] : undefined;
    const decl = isObject(ext) ? ext["cep.profile"] : undefined;
    const declared = isObject(decl) ? decl["profile_id"] : undefined;
    if (declared !== profileId(profile)) {
      problems.push(
        `declared profile ${JSON.stringify(declared)} does not match ${JSON.stringify(profileId(profile))}`,
      );
    }
    if (profile === "semantic_snapshot") problems.push(...verifySnapshot(envelope));
    return problems;
  }

  validateWorldTransition(record: unknown): string[] {
    const errors = collect(this.transition, record);
    if (
      errors.length === 0 &&
      isObject(record) &&
      record["source_world_ref"] === record["target_world_ref"]
    ) {
      return ["source_world_ref and target_world_ref must differ"];
    }
    return errors;
  }
}

function collect(validate: ValidateFunction, instance: unknown): string[] {
  return validate(instance)
    ? []
    : (validate.errors ?? []).map((e) => `${e.instancePath || "$"} ${e.message ?? "invalid"}`);
}

function verifySnapshot(envelope: unknown): string[] {
  if (!isObject(envelope)) return ["envelope is not an object"];
  const worldRef = worldRefOf(envelope);
  if (envelope["completeness_status"] === "invalid") {
    return worldRef === undefined ? [] : ["an invalid semantic world must not carry a world_ref"];
  }
  if (worldRef === undefined) return ["a valid semantic snapshot must pin a world_ref"];

  const ext = envelope["extensions"];
  const block = isObject(ext) ? ext[IDENTITY_NS] : undefined;
  if (!isObject(block)) return [`missing extensions[${JSON.stringify(IDENTITY_NS)}]`];
  const identity = block["domain_model_identity"];
  if (!isObject(identity)) return ["missing domain_model_identity"];

  const problems: string[] = [];
  const recomputed = identityDigest(identity);
  if (!worldRef.endsWith(`@${recomputed}`)) {
    problems.push(`world_ref digest does not match the recomputed identity digest ${recomputed}`);
  }
  const closure = identity["semantic_closure_hash"];
  if (block["semantic_closure_hash"] !== closure) {
    problems.push("semantic_closure_hash differs from domain_model_identity.semantic_closure_hash");
  }
  const integrity = envelope["integrity"];
  if (isObject(integrity) && integrity["semantic_hash"] !== closure) {
    problems.push("integrity.semantic_hash differs from domain_model_identity.semantic_closure_hash");
  }
  return problems;
}

/** A lineage must stay in one pinned world; moving worlds needs an explicit transition record. */
export function checkWorldConsistency(envelopes: unknown[]): string[] {
  const pinned: Array<[string, string]> = [];
  for (const env of envelopes) {
    const id = isObject(env) && typeof env["envelope_id"] === "string" ? env["envelope_id"] : "<no id>";
    const world = worldRefOf(env);
    if (world === undefined) return [`envelope ${JSON.stringify(id)} pins no world_ref`];
    pinned.push([id, world]);
  }
  if (new Set(pinned.map(([, w]) => w)).size > 1) {
    const detail = pinned.map(([i, w]) => `${i}=${w}`).join(", ");
    return [`lineage spans more than one world without an explicit transition: ${detail}`];
  }
  return [];
}
