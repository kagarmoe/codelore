from typer.testing import CliRunner

from codelore.cli import app


def test_cli_version() -> None:
    result = CliRunner().invoke(app, ["--version"])

    assert result.exit_code == 0
    assert "codelore 0.1.0" in result.output


def test_cli_lists_scaffolded_commands() -> None:
    result = CliRunner().invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "build-window" in result.output
    assert "export-evidence-pack" in result.output
