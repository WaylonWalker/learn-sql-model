from rich.console import Console
from sqlmodel import SQLModel, Session
import typer

from learn_sql_model.cli.common import verbose_callback
from learn_sql_model.config import config
from learn_sql_model.models import Hero, Pet

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
def show(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):

    SQLModel.metadata.create_all(config.engine)
    with Session(config.engine) as session:
        heros = session.exec(select(Hero)).all()
    Console().print(heros)


@model_app.command()
def read(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):
    from learn_sql_model.api import read_heroes

    Console().print(read_heroes())


# @model_app.command()
# @expand_pydantic_args(typer=True)
# def create(
#     hero: Hero,
# ):
#     hero.post()

# try:
#     httpx.post("http://localhost:5000/heroes/", json=hero.dict())
# except httpx.ConnectError:
#     console.log("local failover")
#     with Session(config.engine) as session:
#         session.add(hero)
#         session.commit()


@model_app.command()
def populate(
    verbose: bool = typer.Option(
        False,
        callback=verbose_callback,
        help="show the log messages",
    ),
):

    pet_1 = Pet(name="Deadpond-Dog")
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", pets=[pet_1])
    hero_2 = Hero(
        name="Spider-Boy",
        secret_name="Pedro Parqueador",
        pet=Pet(name="Spider-Boy-Dog"),
    )
    hero_3 = Hero(
        name="Rusty-Man",
        secret_name="Tommy Sharp",
        age=48,
        pet=Pet(name="Rusty-Man-Dog"),
    )

    SQLModel.metadata.create_all(config.engine)

    with Session(config.engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()
