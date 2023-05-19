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
    import alembic
    # python -m alembic revision --autogenerate -m "New Attribute"
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    alembic.command.revision(
        config=alembic_cfg,
        message=message,
        autogenerate=True,
    )


@model_app.command()
def populate(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    ...
