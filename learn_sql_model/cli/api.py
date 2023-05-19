import typer
import uvicorn

from learn_sql_model.cli.common import verbose_callback
from learn_sql_model.config import config

api_app = typer.Typer()


@api_app.callback()
def api(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    "model cli"


@api_app.command()
def run(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    uvicorn.run("learn_sql_model.api.app:app", port=config.port, log_level="info")
