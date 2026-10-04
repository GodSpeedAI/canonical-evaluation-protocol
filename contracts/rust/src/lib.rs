//! GodSpeed CEP-0008 profile validation.
//!
//! The schemas and the conformance corpus live in the `cep` repository; this
//! crate embeds the schema files directly (`include_str!`), so there is no
//! second copy to drift. Beyond schema validation it performs the checks a
//! schema cannot: recomputing the DomainForge identity digest, keeping a
//! lineage in one pinned world, and rejecting a transition that goes nowhere.
//!
//! The `world_ref` grammar is defined by DomainForge. This crate never parses
//! it; it compares strings and the digest suffix only.

use jsonschema::{Registry, Resource, Validator};
use serde_json::Value;
use sha2::{Digest, Sha256};
use std::collections::BTreeMap;

const BASE_ID: &str = "https://cep.dev/schemas/cep-semantic-envelope.schema.json";
const BASE: &str = include_str!("../../../schemas/cep-semantic-envelope.schema.json");
const TRANSITION: &str =
    include_str!("../../../schemas/profiles/godspeed/world-transition.v1.schema.json");
const IDENTITY_NS: &str = "domainforge.identity";

#[derive(Debug, thiserror::Error)]
pub enum ContractError {
    #[error("embedded schema is invalid: {0}")]
    Schema(String),
}

/// The six initial GodSpeed profiles.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Profile {
    SemanticSnapshot,
    AuthorityRequest,
    AuthorityDecision,
    ExecutionTrace,
    EvidencePacket,
    SettlementPacket,
}

impl Profile {
    pub const ALL: [Profile; 6] = [
        Profile::SemanticSnapshot,
        Profile::AuthorityRequest,
        Profile::AuthorityDecision,
        Profile::ExecutionTrace,
        Profile::EvidencePacket,
        Profile::SettlementPacket,
    ];

    /// The CEP-0008 `envelope_kind` this profile constrains.
    pub fn kind(self) -> &'static str {
        match self {
            Profile::SemanticSnapshot => "semantic_snapshot",
            Profile::AuthorityRequest => "authority_request",
            Profile::AuthorityDecision => "authority_decision",
            Profile::ExecutionTrace => "execution_trace",
            Profile::EvidencePacket => "evidence_packet",
            Profile::SettlementPacket => "settlement_packet",
        }
    }

    pub fn profile_id(self) -> String {
        format!("godspeed.{}", self.kind())
    }

    pub fn from_kind(kind: &str) -> Option<Profile> {
        Profile::ALL.into_iter().find(|p| p.kind() == kind)
    }

    fn schema_text(self) -> &'static str {
        match self {
            Profile::SemanticSnapshot => {
                include_str!("../../../schemas/profiles/godspeed/semantic_snapshot.v1.schema.json")
            }
            Profile::AuthorityRequest => {
                include_str!("../../../schemas/profiles/godspeed/authority_request.v1.schema.json")
            }
            Profile::AuthorityDecision => {
                include_str!("../../../schemas/profiles/godspeed/authority_decision.v1.schema.json")
            }
            Profile::ExecutionTrace => {
                include_str!("../../../schemas/profiles/godspeed/execution_trace.v1.schema.json")
            }
            Profile::EvidencePacket => {
                include_str!("../../../schemas/profiles/godspeed/evidence_packet.v1.schema.json")
            }
            Profile::SettlementPacket => {
                include_str!("../../../schemas/profiles/godspeed/settlement_packet.v1.schema.json")
            }
        }
    }
}

/// Authority disposition. Never a boolean: only [`Decision::Allow`] is an
/// unrestricted allow.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Decision {
    Allow,
    Deny,
    Escalate,
    Unknown,
    ConstrainedAllow,
    Boundary,
    Degraded,
}

impl Decision {
    pub fn parse(text: &str) -> Option<Decision> {
        Some(match text {
            "allow" => Decision::Allow,
            "deny" => Decision::Deny,
            "escalate" => Decision::Escalate,
            "unknown" => Decision::Unknown,
            "constrained_allow" => Decision::ConstrainedAllow,
            "boundary" => Decision::Boundary,
            "degraded" => Decision::Degraded,
            _ => return None,
        })
    }

    /// True only for an unrestricted allow. A boundary, degraded or
    /// constrained decision permits nothing beyond its constraints.
    pub fn is_unrestricted_allow(self) -> bool {
        self == Decision::Allow
    }

    /// Dispositions that must carry constraints and a policy basis.
    pub fn requires_constraints(self) -> bool {
        matches!(
            self,
            Decision::ConstrainedAllow | Decision::Boundary | Decision::Degraded
        )
    }
}

/// Read the typed disposition from an `authority_decision` envelope.
pub fn decision_of(envelope: &Value) -> Option<Decision> {
    envelope
        .pointer("/extensions/godspeed.authority_decision/decision")
        .and_then(Value::as_str)
        .and_then(Decision::parse)
}

/// The pinned `world_ref` string of an envelope (`scope.world_ref`).
pub fn world_ref_of(envelope: &Value) -> Option<&str> {
    envelope.pointer("/scope/world_ref").and_then(Value::as_str)
}

fn canonical_json(value: &Value) -> String {
    // serde_json's default map is ordered by key and `to_string` is compact,
    // which is DomainForge's canonical JSON for string-only identities.
    value.to_string()
}

/// sha256 over canonical JSON of a DomainModelIdentity, as `sha256:<hex>`.
pub fn identity_digest(identity: &Value) -> String {
    let digest = Sha256::digest(canonical_json(identity).as_bytes());
    format!("sha256:{digest:x}")
}

/// Compiled profile validators.
pub struct Contract {
    validators: BTreeMap<Profile, Validator>,
    transition: Validator,
}

fn compile(registry: &Registry<'_>, text: &str) -> Result<Validator, ContractError> {
    let schema: Value =
        serde_json::from_str(text).map_err(|e| ContractError::Schema(e.to_string()))?;
    jsonschema::options()
        .with_registry(registry)
        .build(&schema)
        .map_err(|e| ContractError::Schema(e.to_string()))
}

impl Contract {
    pub fn new() -> Result<Self, ContractError> {
        let base: Value =
            serde_json::from_str(BASE).map_err(|e| ContractError::Schema(e.to_string()))?;
        let registry = Registry::new()
            .add(BASE_ID, Resource::from_contents(base))
            .map_err(|e| ContractError::Schema(e.to_string()))?
            .prepare()
            .map_err(|e| ContractError::Schema(e.to_string()))?;
        let mut validators = BTreeMap::new();
        for profile in Profile::ALL {
            validators.insert(profile, compile(&registry, profile.schema_text())?);
        }
        Ok(Self {
            validators,
            transition: compile(&registry, TRANSITION)?,
        })
    }

    /// Schema errors for one profile (empty `Ok` means valid).
    pub fn validate(&self, profile: Profile, envelope: &Value) -> Result<(), Vec<String>> {
        errors(&self.validators[&profile], envelope)
    }

    /// Validate against the profile named by the envelope's own kind.
    pub fn validate_declared(&self, envelope: &Value) -> Result<Profile, Vec<String>> {
        let kind = envelope
            .get("envelope_kind")
            .and_then(Value::as_str)
            .unwrap_or_default();
        let profile = Profile::from_kind(kind)
            .ok_or_else(|| vec![format!("no GodSpeed profile for envelope_kind {kind:?}")])?;
        self.validate(profile, envelope).map(|()| profile)
    }

    /// Checks a schema cannot make; empty `Ok` means the envelope's claims hold.
    pub fn verify_semantics(&self, profile: Profile, envelope: &Value) -> Result<(), Vec<String>> {
        let mut problems = Vec::new();
        let declared = envelope
            .pointer("/extensions/cep.profile/profile_id")
            .and_then(Value::as_str);
        if declared != Some(profile.profile_id().as_str()) {
            problems.push(format!(
                "declared profile {declared:?} does not match {:?}",
                profile.profile_id()
            ));
        }
        if profile == Profile::SemanticSnapshot {
            problems.extend(verify_snapshot(envelope));
        }
        into_result(problems)
    }

    pub fn validate_world_transition(&self, record: &Value) -> Result<(), Vec<String>> {
        errors(&self.transition, record)?;
        if record.get("source_world_ref") == record.get("target_world_ref") {
            return Err(vec![
                "source_world_ref and target_world_ref must differ".to_string()
            ]);
        }
        Ok(())
    }
}

fn errors(validator: &Validator, instance: &Value) -> Result<(), Vec<String>> {
    let problems: Vec<String> = validator
        .iter_errors(instance)
        .map(|e| format!("{} at {}", e, e.instance_path()))
        .collect();
    into_result(problems)
}

fn into_result(problems: Vec<String>) -> Result<(), Vec<String>> {
    if problems.is_empty() {
        Ok(())
    } else {
        Err(problems)
    }
}

fn verify_snapshot(envelope: &Value) -> Vec<String> {
    let world_ref = world_ref_of(envelope);
    if envelope.get("completeness_status").and_then(Value::as_str) == Some("invalid") {
        return match world_ref {
            Some(_) => vec!["an invalid semantic world must not carry a world_ref".to_string()],
            None => vec![],
        };
    }
    let Some(world_ref) = world_ref else {
        return vec!["a valid semantic snapshot must pin a world_ref".to_string()];
    };
    let Some(block) = envelope.pointer(&format!("/extensions/{IDENTITY_NS}")) else {
        return vec![format!("missing extensions[{IDENTITY_NS:?}]")];
    };
    let Some(identity) = block.get("domain_model_identity") else {
        return vec!["missing domain_model_identity".to_string()];
    };

    let mut problems = Vec::new();
    let recomputed = identity_digest(identity);
    if !world_ref.ends_with(&format!("@{recomputed}")) {
        problems.push(format!(
            "world_ref digest does not match the recomputed identity digest {recomputed}"
        ));
    }
    let closure = identity.get("semantic_closure_hash");
    if block.get("semantic_closure_hash") != closure {
        problems.push(
            "semantic_closure_hash differs from domain_model_identity.semantic_closure_hash"
                .to_string(),
        );
    }
    if let Some(integrity) = envelope.get("integrity") {
        if integrity.get("semantic_hash") != closure {
            problems.push(
                "integrity.semantic_hash differs from domain_model_identity.semantic_closure_hash"
                    .to_string(),
            );
        }
    }
    problems
}

/// A lineage must stay in one pinned world; moving worlds needs an explicit
/// transition record.
pub fn check_world_consistency(envelopes: &[Value]) -> Result<(), Vec<String>> {
    let mut pinned = Vec::new();
    for env in envelopes {
        let id = env
            .get("envelope_id")
            .and_then(Value::as_str)
            .unwrap_or("<no id>");
        match world_ref_of(env) {
            Some(world) => pinned.push((id, world)),
            None => return Err(vec![format!("envelope {id:?} pins no world_ref")]),
        }
    }
    let distinct: std::collections::BTreeSet<&str> = pinned.iter().map(|(_, w)| *w).collect();
    if distinct.len() > 1 {
        let detail: Vec<String> = pinned.iter().map(|(i, w)| format!("{i}={w}")).collect();
        return Err(vec![format!(
            "lineage spans more than one world without an explicit transition: {}",
            detail.join(", ")
        )]);
    }
    Ok(())
}
