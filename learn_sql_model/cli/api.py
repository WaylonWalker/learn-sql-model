import httpx
from rich.console import Console
import typer

from learn_sql_model.cli.common import verbose_callback
from learn_sql_model.config import get_config
from learn_sql_model.optional import _optional_import_

uvicorn = _optional_import_("uvicorn", group="api")
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
    import uvicorn

    uvicorn.run(**get_config().api_server.dict())


@api_app.command()
def status(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    config = get_config()
    url = config.api_client.url

    try:
        r = httpx.get(url + "/docs")
        if r.status_code == 200:
            Console().print(f"[green]API: ([gold1]{url}[green]) is running")
        else:
            Console().print(f"[red]API: ([gold1]{url}[red]) is not running")
    except httpx.ConnectError:
        Console().print(f"[red]API: ([gold1]{url}[red]) is not running")

    try:
        with config.database.engine.connect():
            Console().print(
                f"[green]database: ([gold1]{config.database.engine}[green]) is running"
            )
    except Exception:
        Console().print(
            f"[red]database: ([gold1]{config.database.engine}[red]) is not running"
        )
