from pathlib import Path

import alembic
from alembic.config import Config
import copier
import typer

from learn_sql_model.cli.common import verbose_callback

model_app = typer.Typer()


@model_app.callback()
def model(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    "model cli"


@model_app.command()
def create(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    template = Path("templates/model")
    copier.copy(str(template), ".")


@model_app.command()
def create_revision(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
    message: str = typer.Option(
        prompt=True,
    ),
):
    alembic_cfg = Config("alembic.ini")
    alembic.command.revision(
        config=alembic_cfg,
        message=message,
        autogenerate=True,
    )
    alembic.command.upgrade(config=alembic_cfg, revision="head")


@model_app.command()
def checkout(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
    revision: str = typer.Option("head"),
):
    alembic_cfg = Config("alembic.ini")
    alembic.command.upgrade(config=alembic_cfg, revision="head")


@model_app.command()
def populate(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    ...
