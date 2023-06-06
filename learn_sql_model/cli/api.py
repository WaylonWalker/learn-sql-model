from rich.console import Console
import typer
import uvicorn

from learn_sql_model.cli.common import verbose_callback
from learn_sql_model.config import get_config

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
    uvicorn.run(**get_config().api_server.dict())


@api_app.command()
def status(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    import httpx

    config = get_config()
    host = config.api_server.host
    port = config.api_server.port
    url = f"http://{host}:{port}/docs"

    try:
        r = httpx.get(url)
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
    except Exception as e:
        Console().print(
            f"[red]database: ([gold1]{config.database.engine}[red]) is not running"
        )
