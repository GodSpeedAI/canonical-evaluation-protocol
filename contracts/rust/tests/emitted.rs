//! A snapshot emitted by the real DomainForge binary must pass this validator.
//! Gated on CEP_TEST_DOMAINFORGE_BIN (a build with `--world-name`); skipped otherwise.

use cep_godspeed_contract::{world_ref_of, Contract, Profile};
use serde_json::Value;
use std::process::Command;

const HEADER: &str = "@namespace \"auth\"\n@version \"1.0.0\"\n\n";
const VALID: &str = "Entity \"User\" in auth\nEntity \"Role\" in auth\n";

fn emit(source: &str, flags: &[&str]) -> Option<(Option<i32>, Value)> {
    let bin = std::env::var("CEP_TEST_DOMAINFORGE_BIN").ok()?;
    let dir = std::env::temp_dir().join(format!(
        "cep-emitted-{}-{}",
        std::process::id(),
        flags.len()
    ));
    std::fs::create_dir_all(&dir).unwrap();
    let path = dir.join("model.sea");
    std::fs::write(&path, source).unwrap();
    let out = Command::new(bin)
        .args(["envelope", "--emit", "cep"])
        .args(flags)
        .arg(&path)
        .output()
        .expect("domainforge runs");
    let _ = std::fs::remove_dir_all(&dir);
    Some((
        out.status.code(),
        serde_json::from_slice(&out.stdout).expect("JSON envelope"),
    ))
}

#[test]
fn valid_world_snapshot_conforms_and_verifies() {
    let Some((code, env)) = emit(
        &format!("{HEADER}{VALID}"),
        &[
            "--world-name",
            "godspeed-corporate",
            "--world-alias",
            "world:corporate",
        ],
    ) else {
        eprintln!("skipped: CEP_TEST_DOMAINFORGE_BIN not set");
        return;
    };
    let contract = Contract::new().unwrap();
    assert_eq!(code, Some(0));
    contract
        .validate(Profile::SemanticSnapshot, &env)
        .expect("schema");
    contract
        .verify_semantics(Profile::SemanticSnapshot, &env)
        .expect("semantics");
    assert!(world_ref_of(&env).is_some());
}

#[test]
fn invalid_world_is_flagged_not_pinned_and_conforms() {
    let Some((code, env)) = emit("this is not sea", &["--world-name", "godspeed-corporate"]) else {
        eprintln!("skipped: CEP_TEST_DOMAINFORGE_BIN not set");
        return;
    };
    let contract = Contract::new().unwrap();
    assert_ne!(code, Some(0));
    assert!(world_ref_of(&env).is_none());
    contract
        .validate(Profile::SemanticSnapshot, &env)
        .expect("schema");
    contract
        .verify_semantics(Profile::SemanticSnapshot, &env)
        .expect("semantics");
}

#[test]
fn snapshot_without_world_name_does_not_claim_the_profile() {
    let Some((_, env)) = emit(&format!("{HEADER}{VALID}"), &[]) else {
        eprintln!("skipped: CEP_TEST_DOMAINFORGE_BIN not set");
        return;
    };
    assert!(Contract::new()
        .unwrap()
        .validate(Profile::SemanticSnapshot, &env)
        .is_err());
}
