from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from cep import __version__
from cep.benchmarks.authority import score_authority
from cep.benchmarks.capability import score_capability
from cep.benchmarks.reality_gap import score_reality_gap
from cep.benchmarks.settlement import (
    ScoreSettlementInput,
    SettlementAnswerKey,
    from_settlement_recorded,
    score_settlement,
    score_settlement_answer,
)
from cep.conformance.anti_collapse import run_reality_gap_anti_collapse
from cep.conformance.benchmark_invariants import run_benchmark_anti_collapse
from cep.conformance.corpus import (
    CorpusError,
    evaluate_corpus,
)
from cep.inventory import (
    iter_authority_case_dirs,
    iter_capability_case_dirs,
    iter_reality_gap_case_dirs,
    iter_settlement_case_dirs,
)
from cep.io import load_json
from cep.paths import REPORTS_DIR, SCHEMAS_DIR
from cep.reports import write_report
from cep.schema_profile import as_object
from cep.scoring.common import ScoreRecord
from cep.validation import (
    ValidationResult,
    all_ok,
    validate_all_schemas,
    validate_instance,
    validate_instance_json,
    validate_reality_gap_corpus,
    validate_semantic_envelope_corpus,
    validate_semantic_envelope_full_corpus,
    validate_semantic_envelope_invalid_corpus,
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


@validate_app.command(
    "semantic-envelope",
    help="Validate Semantic Envelope fixtures against the CEP-0008 schema profile.",
)
def validate_semantic_envelope_command(
    path: Annotated[Path | None, typer.Argument(dir_okay=False)] = None,
    stdin: Annotated[
        bool,
        typer.Option("--stdin", help="Read one envelope from standard input."),
    ] = False,
) -> None:
    if path is not None:
        result = validate_instance(
            path,
            SCHEMAS_DIR / "cep-semantic-envelope.schema.json",
        )
        _print_results([result])
        raise typer.Exit(0 if result.ok else 1)

    if stdin:
        content = sys.stdin.read()
        result = validate_instance_json(
            content,
            SCHEMAS_DIR / "cep-semantic-envelope.schema.json",
            target="stdin",
        )
        _print_results([result])
        raise typer.Exit(0 if result.ok else 1)

    results = (
        validate_semantic_envelope_corpus()
        + validate_semantic_envelope_full_corpus()
        + validate_semantic_envelope_invalid_corpus()
    )
    _print_results(results)
    raise typer.Exit(0 if all_ok(results) else 1)


@validate_app.command("all", help="Validate schemas and current corpus artifacts.")
def validate_all_command() -> None:
    results = (
        validate_all_schemas()
        + validate_reality_gap_corpus()
        + validate_semantic_envelope_corpus()
        + validate_semantic_envelope_full_corpus()
        + validate_semantic_envelope_invalid_corpus()
    )
    _print_results(results)
    raise typer.Exit(0 if all_ok(results) else 1)


app.add_typer(validate_app, name="validate")


@conformance_app.command("anti-collapse", help="Run anti-collapse conformance for all families.")
def conformance_anti_collapse_command(
    corpus: Annotated[Path | None, typer.Option(exists=True, dir_okay=False)] = None,
) -> None:
    """Run CEP anti-collapse conformance.

    Without `--corpus`: evaluate CEP's own reality-gap fixtures and the
    cross-family example-answer invariants (historical behavior).

    With `--corpus <path>`: evaluate an externally supplied corpus (e.g. an
    `sxr`-exported record set) through the same anti-collapse evaluator. The
    gate passes only if every record commits no anti-collapse violation.
    """
    if corpus is not None:
        try:
            results = evaluate_corpus(corpus)
        except CorpusError as exc:
            console.print(f"ERROR {exc.reason}")
            raise typer.Exit(2) from exc
        failed = 0
        for result in results:
            marker = "PASS" if result.ok else "FAIL"
            console.print(f"{marker} {result.record_id}: {result.message}")
            if not result.ok:
                failed += 1
        console.print(f"corpus: {len(results) - failed}/{len(results)} passed")
        raise typer.Exit(0 if failed == 0 else 1)

    ok = True
    for result in run_reality_gap_anti_collapse():
        marker = "PASS" if result.ok else "FAIL"
        console.print(f"{marker} {result.fixture_id}: {result.message}")
        ok = ok and result.ok
    for invariant in run_benchmark_anti_collapse():
        marker = "PASS" if invariant.ok else "FAIL"
        console.print(f"{marker} {invariant.family} {invariant.case_id}: {invariant.message}")
        ok = ok and invariant.ok
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


@app.command(
    "score-settlement",
    help="Score a SettlementRecorded-shaped payload against expected settlement criteria.",
)
def score_settlement_command(
    input_path: Annotated[Path, typer.Option("--input", exists=True, dir_okay=False)],
) -> None:
    document = ScoreSettlementInput.model_validate(load_json(input_path))
    payload = as_object(document.settlement_recorded.get("payload"))
    if payload is None:
        console.print("error: settlement_recorded.payload must be an object")
        raise typer.Exit(1)
    answer_key = SettlementAnswerKey.model_validate(
        {"case_ref": payload.get("work_request_id"), **document.expected},
    )
    answer = from_settlement_recorded(
        payload,
        evidence_refs=document.evidence_refs,
        preserved_distinctions=document.preserved_distinctions,
    )
    result = score_settlement_answer(answer_key, answer)
    console.print(
        f"{result.status.upper()} {result.case_id} {result.answer_id} score={result.score}",
    )
    if result.critical_failures:
        console.print(f"critical_failures={result.critical_failures}")


app.add_typer(conformance_app, name="conformance")
app.add_typer(run_app, name="run")


def main() -> None:
    app()
