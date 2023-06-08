import sys
from typing import List, Optional, Union

from engorgio import engorgio
from rich.console import Console
import typer

from learn_sql_model.config import Config, get_config
from learn_sql_model.factories.new import newFactory
from learn_sql_model.factories.pet import PetFactory
from learn_sql_model.models.new import (
    new,
    newCreate,
    newDelete,
    newRead,
    newUpdate,
)

new_app = typer.Typer()


@new_app.callback()
def new():
    "model cli"


@new_app.command()
@engorgio(typer=True)
def get(
    id: Optional[int] = typer.Argument(default=None),
    config: Config = None,
) -> Union[new, List[new]]:
    "get one new"
    config.init()
    new = newRead.get(id=id, config=config)
    Console().print(new)
    return new


@new_app.command()
@engorgio(typer=True)
def list(
    where: Optional[str] = None,
    config: Config = None,
    offset: int = 0,
    limit: Optional[int] = None,
) -> Union[new, List[new]]:
    "get one new"
    new = newRead.list(config=config, where=where, offset=offset, limit=limit)
    Console().print(new)
    return new


@new_app.command()
@engorgio(typer=True)
def create(
    new: newCreate,
    config: Config = None,
) -> new:
    "read all the news"
    # config.init()
    new = new.post(config=config)
    Console().print(new)
    return new


@new_app.command()
@engorgio(typer=True)
def update(
    new: newUpdate,
    config: Config = None,
) -> new:
    "read all the news"
    new = new.update(config=config)
    Console().print(new)
    return new


@new_app.command()
@engorgio(typer=True)
def delete(
    new: newDelete,
    config: Config = None,
) -> new:
    "read all the news"
    # config.init()
    new = new.delete(config=config)
    return new


@new_app.command()
@engorgio(typer=True)
def populate(
    new: new,
    n: int = 10,
) -> new:
    "read all the news"
    config = get_config()
    if config.env == "prod":
        Console().print("populate is not supported in production")
        sys.exit(1)

    for new in newFactory().batch(n):
        pet = PetFactory().build()
        new.pet = pet
        Console().print(new)
        new.post(config=config)
