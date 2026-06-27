from __future__ import annotations

from typing import Annotated

import typer
from rich.console import Console

from cep import __version__
from cep.validation import (
    ValidationResult,
    all_ok,
    validate_all_schemas,
    validate_reality_gap_corpus,
)

app = typer.Typer(help="Canonical Evaluation Protocol CLI.", no_args_is_help=True)
validate_app = typer.Typer(help="Validate CEP artifacts.", no_args_is_help=True)
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


def main() -> None:
    app()
