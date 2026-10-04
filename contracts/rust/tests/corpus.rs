//! The Rust validator must reach the same verdicts as the Python reference on
//! the shared corpus in `schemas/fixtures/godspeed`.

use cep_godspeed_contract::{
    check_world_consistency, decision_of, identity_digest, Contract, Decision, Profile,
};
use serde_json::Value;
use std::path::PathBuf;

fn repo(path: &str) -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../")
        .join(path)
}

fn read(path: PathBuf) -> Value {
    serde_json::from_str(
        &std::fs::read_to_string(&path).unwrap_or_else(|e| panic!("{path:?}: {e}")),
    )
    .unwrap()
}

fn corpus(name: &str) -> Value {
    read(repo(&format!("schemas/fixtures/godspeed/{name}")))
}

fn manifest() -> Value {
    corpus("manifest.json")
}

fn contract() -> Contract {
    Contract::new().expect("embedded schemas compile")
}

#[test]
fn schema_verdicts_match_the_manifest() {
    let contract = contract();
    let manifest = manifest();
    let cases = manifest["cases"].as_array().unwrap();
    assert!(cases.len() >= 30, "corpus unexpectedly small");
    for case in cases {
        let file = case["file"].as_str().unwrap();
        let profile = Profile::from_kind(case["profile"].as_str().unwrap()).unwrap();
        let result = contract.validate(profile, &corpus(file));
        match case["schema"].as_str().unwrap() {
            "valid" => assert!(result.is_ok(), "{file} should be valid: {result:?}"),
            _ => assert!(result.is_err(), "{file} should be rejected"),
        }
    }
}

#[test]
fn semantic_verdicts_match_the_manifest() {
    let contract = contract();
    let manifest = manifest();
    for case in manifest["cases"].as_array().unwrap() {
        if case["schema"] != "valid" {
            continue;
        }
        let file = case["file"].as_str().unwrap();
        let profile = Profile::from_kind(case["profile"].as_str().unwrap()).unwrap();
        let result = contract.verify_semantics(profile, &corpus(file));
        match case["semantic"].as_str().unwrap() {
            "ok" => assert!(result.is_ok(), "{file}: {result:?}"),
            _ => {
                let errs = result.expect_err(file);
                if let Some(needle) = case["semantic_error_contains"].as_str() {
                    assert!(errs.iter().any(|e| e.contains(needle)), "{file}: {errs:?}");
                }
            }
        }
    }
}

#[test]
fn lineage_must_stay_in_one_world() {
    let manifest = manifest();
    for chain in manifest["chains"].as_array().unwrap() {
        let mut envelopes = Vec::new();
        for name in chain["files"].as_array().unwrap() {
            let name = name.as_str().unwrap();
            let mut env = corpus(name);
            if let Some(world) = chain["override"].get(name).and_then(Value::as_str) {
                env["scope"]["world_ref"] = Value::String(world.to_string());
            }
            envelopes.push(env);
        }
        let ok = check_world_consistency(&envelopes).is_ok();
        assert_eq!(ok, chain["expect"] == "consistent", "{}", chain["case"]);
    }
}

#[test]
fn identity_digest_matches_the_vendored_domainforge_vectors() {
    let vectors = read(repo("schemas/vendored/world_ref/golden-vectors.json"));
    for case in vectors["valid"].as_array().unwrap() {
        assert_eq!(
            identity_digest(&case["identity"]),
            case["canonical_digest"].as_str().unwrap(),
            "{}",
            case["case"]
        );
    }
}

#[test]
fn authority_dispositions_are_typed_and_never_boolean() {
    for (name, expect) in [
        ("allow", Decision::Allow),
        ("deny", Decision::Deny),
        ("escalate", Decision::Escalate),
        ("unknown", Decision::Unknown),
        ("constrained_allow", Decision::ConstrainedAllow),
        ("boundary", Decision::Boundary),
        ("degraded", Decision::Degraded),
    ] {
        let env = corpus(&format!("valid/authority_decision-{name}.json"));
        let decision = decision_of(&env).expect(name);
        assert_eq!(decision, expect);
        assert_eq!(decision.is_unrestricted_allow(), name == "allow", "{name}");
        assert_eq!(
            decision.requires_constraints(),
            matches!(name, "constrained_allow" | "boundary" | "degraded")
        );
    }
    let flattened = corpus("invalid/authority_decision-boolean-flattened.json");
    assert_eq!(decision_of(&flattened), None);
    let junk = corpus("invalid/authority_decision-unrecognised-disposition.json");
    assert_eq!(decision_of(&junk), None);
}

#[test]
fn validate_declared_routes_by_envelope_kind() {
    let contract = contract();
    for case in manifest()["cases"].as_array().unwrap() {
        if case["schema"] != "valid" {
            continue;
        }
        let env = corpus(case["file"].as_str().unwrap());
        let profile = contract
            .validate_declared(&env)
            .expect("valid fixture routes");
        assert_eq!(profile.kind(), case["profile"].as_str().unwrap());
    }
    let mut unknown = corpus("valid/authority_request.json");
    unknown["envelope_kind"] = Value::String("composite".into());
    assert!(contract.validate_declared(&unknown).is_err());
}

#[test]
fn world_transition_is_explicit_and_must_move() {
    let contract = contract();
    let m = manifest();
    let a = m["worlds"]["A"]["world_ref"].clone();
    let b = m["worlds"]["B"]["world_ref"].clone();
    let good = serde_json::json!({
        "source_world_ref": a, "target_world_ref": b,
        "transition_kind": "semantic_change",
        "reason": "corporate policy model gained a Pump entity",
        "compatibility": "backward_compatible",
        "semantic_closure_equal": false
    });
    assert!(contract.validate_world_transition(&good).is_ok());
    let mut same = good.clone();
    same["target_world_ref"] = a.clone();
    assert!(contract.validate_world_transition(&same).is_err());
    let mut alias = good.clone();
    alias["target_world_ref"] = Value::String("world:corporate".into());
    assert!(contract.validate_world_transition(&alias).is_err());
    let mut missing = good.clone();
    missing.as_object_mut().unwrap().remove("reason");
    assert!(contract.validate_world_transition(&missing).is_err());
}
