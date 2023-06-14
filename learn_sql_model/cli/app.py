from trogon import Trogon
import typer
from typer.main import get_group

from learn_sql_model.cli.api import api_app
from learn_sql_model.cli.config import config_app
from learn_sql_model.cli.hero import hero_app
from learn_sql_model.cli.model import model_app
from learn_sql_model.game.game import game_app

app = typer.Typer(
    name="learn_sql_model",
    help="learn-sql-model cli for managing the project",
)
app.add_typer(config_app, name="config")
# app.add_typer(tui_app, name="tui")
app.add_typer(model_app, name="model")
app.add_typer(api_app, name="api")
app.add_typer(hero_app, name="hero")
app.add_typer(game_app, name="game")


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
        False,
        callback=version_callback,
        help="show the version of the learn-sql-model package.",
    ),
):
    "configuration cli"


@app.command()
def tui(ctx: typer.Context) -> None:
    Trogon(get_group(app), click_context=ctx).run()


if __name__ == "__main__":
    typer.run(main)
