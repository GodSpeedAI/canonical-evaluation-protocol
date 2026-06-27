from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from cep import __version__
from cep.benchmarks.authority import score_authority
from cep.benchmarks.capability import score_capability
from cep.benchmarks.reality_gap import score_reality_gap
from cep.benchmarks.settlement import score_settlement
from cep.conformance.anti_collapse import run_reality_gap_anti_collapse
from cep.inventory import (
    iter_authority_case_dirs,
    iter_capability_case_dirs,
    iter_reality_gap_case_dirs,
    iter_settlement_case_dirs,
)
from cep.paths import REPORTS_DIR
from cep.reports import write_report
from cep.scoring.common import ScoreRecord
from cep.validation import (
    ValidationResult,
    all_ok,
    validate_all_schemas,
    validate_reality_gap_corpus,
)

app = typer.Typer(help="Canonical Evaluation Protocol CLI.", no_args_is_help=True)
validate_app = typer.Typer(help="Validate CEP artifacts.", no_args_is_help=True)
conformance_app = typer.Typer(help="Run CEP conformance checks.", no_args_is_help=True)
run_app = typer.Typer(help="Run CEP benchmark scorers.", no_args_is_help=True)
console = Console()


def _version_callback(value: bool) -> None:
    if value:
        console.print(__version__)
        raise typer.Exit


VersionOption = Annotated[
    bool,
    typer.Option(
        "--version",
        help="Show the CEP CLI version.",
        callback=_version_callback,
        is_eager=True,
    ),
]


@app.callback(help="Canonical Evaluation Protocol CLI.")
def root(version: VersionOption = False) -> None:
    _ = version


@app.command(help="Run a lightweight environment check.")
def doctor() -> None:
    results = validate_all_schemas()
    if all_ok(results):
        console.print("CEP runtime OK")
        return

    _print_results(results)
    raise typer.Exit(1)


def _print_results(results: list[ValidationResult]) -> None:
    for result in results:
        marker = "PASS" if result.ok else "FAIL"
        console.print(f"{marker} {result.target}")
        for error in result.errors:
            console.print(f"  - {error}")


@validate_app.command("schemas", help="Validate registered JSON schemas.")
def validate_schemas_command() -> None:
    results = validate_all_schemas()
    _print_results(results)
    raise typer.Exit(0 if all_ok(results) else 1)


@validate_app.command("reality-gap-corpus", help="Validate RealityGapBench corpus artifacts.")
def validate_reality_gap_corpus_command() -> None:
    results = validate_reality_gap_corpus()
    _print_results(results)
    raise typer.Exit(0 if all_ok(results) else 1)


@validate_app.command("all", help="Validate schemas and current corpus artifacts.")
def validate_all_command() -> None:
    results = validate_all_schemas() + validate_reality_gap_corpus()
    _print_results(results)
    raise typer.Exit(0 if all_ok(results) else 1)


app.add_typer(validate_app, name="validate")


@conformance_app.command("anti-collapse", help="Run RealityGapBench anti-collapse fixtures.")
def conformance_anti_collapse_command() -> None:
    results = run_reality_gap_anti_collapse()
    ok = True
    for result in results:
        marker = "PASS" if result.ok else "FAIL"
        console.print(f"{marker} {result.fixture_id}: {result.message}")
        if not result.ok:
            ok = False
    raise typer.Exit(0 if ok else 1)


@run_app.command("reality-gap", help="Score one RealityGapBench answer.")
def run_reality_gap_command(
    case_dir: Annotated[Path, typer.Option(exists=True, file_okay=False)],
    answer: Annotated[Path, typer.Option(exists=True, dir_okay=False)],
    out: Annotated[Path | None, typer.Option(dir_okay=False)] = None,
) -> None:
    result = score_reality_gap(case_dir, answer)
    out_path = (
        out or REPORTS_DIR / "reality-gap" / f"{result.case_id}-{result.answer_id}.result.json"
    )
    write_report(result, out_path)
    console.print(
        f"{result.status.upper()} {result.case_id} {result.answer_id} score={result.score}"
    )
    console.print(f"Wrote {out_path}")


@run_app.command("reality-gap-corpus", help="Score all current RealityGapBench example answers.")
def run_reality_gap_corpus_command() -> None:
    failed = _run_corpus(
        case_dirs=iter_reality_gap_case_dirs(),
        scorer=score_reality_gap,
        report_dir=REPORTS_DIR / "reality-gap",
    )
    raise typer.Exit(1 if failed else 0)


def _run_corpus(
    case_dirs: list[Path],
    scorer: Callable[[Path, Path], ScoreRecord],
    report_dir: Path,
) -> bool:
    failed = False
    for case_dir in case_dirs:
        for answer_path in sorted(case_dir.glob("example_*_answer.json")):
            result = scorer(case_dir, answer_path)
            out_path = report_dir / f"{result.case_id}-{result.answer_id}.result.json"
            write_report(result, out_path)
            console.print(
                f"{result.status.upper()} {result.case_id} {result.answer_id} score={result.score}",
            )
            valid_answer_failed = answer_path.name == "example_valid_answer.json" and (
                result.status not in {"pass", "partial"}
            )
            invalid_answer_passed = (
                answer_path.name == "example_invalid_answer.json" and result.status == "pass"
            )
            if valid_answer_failed or invalid_answer_passed:
                failed = True
    return failed


@run_app.command("authority-corpus", help="Score all current AuthorityBench example answers.")
def run_authority_corpus_command() -> None:
    failed = _run_corpus(
        case_dirs=iter_authority_case_dirs(),
        scorer=score_authority,
        report_dir=REPORTS_DIR / "authority",
    )
    raise typer.Exit(1 if failed else 0)


@run_app.command("settlement-corpus", help="Score all current SettlementBench example answers.")
def run_settlement_corpus_command() -> None:
    failed = _run_corpus(
        case_dirs=iter_settlement_case_dirs(),
        scorer=score_settlement,
        report_dir=REPORTS_DIR / "settlement",
    )
    raise typer.Exit(1 if failed else 0)


@run_app.command("capability-corpus", help="Score all current CapabilityBench example answers.")
def run_capability_corpus_command() -> None:
    failed = _run_corpus(
        case_dirs=iter_capability_case_dirs(),
        scorer=score_capability,
        report_dir=REPORTS_DIR / "capability",
    )
    raise typer.Exit(1 if failed else 0)


app.add_typer(conformance_app, name="conformance")
app.add_typer(run_app, name="run")


def main() -> None:
    app()
