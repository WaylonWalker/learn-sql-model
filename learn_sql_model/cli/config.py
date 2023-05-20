from rich.console import Console
import typer

from learn_sql_model.cli.common import verbose_callback
from learn_sql_model.config import get_config

config_app = typer.Typer()


@config_app.callback()
def config(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    "configuration cli"


@config_app.command()
def show(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    Console().print(get_config())
