from __future__ import annotations

from pathlib import Path

from cep.paths import ANTI_COLLAPSE_REALITY_GAP_DIR, REALITY_GAP_CASES_DIR


def iter_reality_gap_case_dirs(root: Path = REALITY_GAP_CASES_DIR) -> list[Path]:
    return sorted(path for path in root.glob("rg-*") if path.is_dir())


def iter_reality_gap_case_files(root: Path = REALITY_GAP_CASES_DIR) -> list[Path]:
    return [case_dir / "case.cep.json" for case_dir in iter_reality_gap_case_dirs(root)]


def iter_reality_gap_answer_keys(root: Path = REALITY_GAP_CASES_DIR) -> list[Path]:
    return [case_dir / "answer_key.json" for case_dir in iter_reality_gap_case_dirs(root)]


def iter_reality_gap_example_answers(root: Path = REALITY_GAP_CASES_DIR) -> list[Path]:
    paths: list[Path] = []
    for case_dir in iter_reality_gap_case_dirs(root):
        paths.extend(sorted(case_dir.glob("example_*_answer.json")))
    return paths


def iter_reality_gap_evidence_files(root: Path = REALITY_GAP_CASES_DIR) -> list[Path]:
    paths: list[Path] = []
    for case_dir in iter_reality_gap_case_dirs(root):
        evidence_dir = case_dir / "evidence"
        if evidence_dir.exists():
            paths.extend(sorted(evidence_dir.glob("*.json")))
    return paths


def iter_reality_gap_anti_collapse_fixtures(
    root: Path = ANTI_COLLAPSE_REALITY_GAP_DIR,
) -> list[Path]:
    return sorted(root.glob("rg-ac-*.json"))


def reality_gap_anti_collapse_manifest(
    root: Path = ANTI_COLLAPSE_REALITY_GAP_DIR,
) -> Path:
    return root / "manifest.json"
