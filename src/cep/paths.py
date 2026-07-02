import os
from pathlib import Path


def _looks_like_repo_root(path: Path) -> bool:
    return (path / "schemas" / "index.json").is_file() and (path / "benchmarks").is_dir()


def _discover_repo_root() -> Path:
    configured = os.environ.get("CEP_REPO_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()

    for candidate in (Path.cwd(), *Path(__file__).resolve().parents):
        if _looks_like_repo_root(candidate):
            return candidate

    return Path.cwd().resolve()


REPO_ROOT = _discover_repo_root()
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"
REALITY_GAP_DIR = BENCHMARKS_DIR / "reality-gap"
REALITY_GAP_CASES_DIR = REALITY_GAP_DIR / "cases"
AUTHORITY_DIR = BENCHMARKS_DIR / "authority"
AUTHORITY_CASES_DIR = AUTHORITY_DIR / "cases"
SETTLEMENT_DIR = BENCHMARKS_DIR / "settlement"
SETTLEMENT_CASES_DIR = SETTLEMENT_DIR / "cases"
CAPABILITY_DIR = BENCHMARKS_DIR / "capability"
CAPABILITY_CASES_DIR = CAPABILITY_DIR / "cases"
CONFORMANCE_DIR = REPO_ROOT / "conformance"
ANTI_COLLAPSE_REALITY_GAP_DIR = CONFORMANCE_DIR / "fixtures" / "anti-collapse" / "reality-gap"
SCHEMAS_DIR = REPO_ROOT / "schemas"
SEMANTIC_ENVELOPE_FIXTURES_DIR = SCHEMAS_DIR / "fixtures" / "semantic-envelope"
REPORTS_DIR = REPO_ROOT / "reports"
