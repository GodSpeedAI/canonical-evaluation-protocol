from typer.testing import CliRunner

import cep
from cep.cli import app


def test_imports() -> None:
    assert cep.__version__


def test_doctor_reports_runtime_ok() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["doctor"])

    assert result.exit_code == 0, result.output
    assert "CEP runtime OK" in result.output
