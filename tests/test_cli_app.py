from typer.testing import CliRunner

from learn_sql_model.cli.app import app

runner = CliRunner()


def test_cli_app_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
