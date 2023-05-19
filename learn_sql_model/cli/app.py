import typer

from learn_sql_model.cli.api import api_app
from learn_sql_model.cli.common import verbose_callback
from learn_sql_model.cli.config import config_app
from learn_sql_model.cli.hero import hero_app
from learn_sql_model.cli.model_app import model_app
from learn_sql_model.cli.tui import tui_app

app = typer.Typer(
    name="learn_sql_model",
    help="A rich terminal report for coveragepy.",
)
app.add_typer(config_app)
app.add_typer(tui_app)
app.add_typer(model_app)
app.add_typer(api_app)
app.add_typer(hero_app, name="hero")


def version_callback(value: bool) -> None:
    """Callback function to print the version of the learn-sql-model package.

    Args:
        value (bool): Boolean value to determine if the version should be printed.

    Raises:
        typer.Exit: If the value is True, the version will be printed and the program will exit.

    Example:
        version_callback(True)
    """
    if value:
        from learn_sql_model.__about__ import __version__

        typer.echo(f"{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
    ),
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
) -> None:
    return


if __name__ == "__main__":
    typer.run(main)
