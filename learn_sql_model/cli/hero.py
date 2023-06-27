import sys
from typing import List, Optional, Union

from engorgio import engorgio
from rich.console import Console
import typer

from learn_sql_model.config import get_config
from learn_sql_model.models.hero import (
    Hero,
    HeroCreate,
    HeroDelete,
    HeroRead,
    HeroUpdate,
    Heros,
)
from learn_sql_model.optional import _optional_import_

HeroFactory = _optional_import_(
    "learn_sql_model.factories.hero",
    "HeroFactory",
    group="api",
)

hero_app = typer.Typer()

config = get_config()


@hero_app.callback()
def hero():
    "model cli"


@hero_app.command()
def get(
    hero_id: Optional[int] = typer.Argument(),
) -> Union[Hero, List[Hero]]:
    "get one hero"
    hero = HeroRead.get(id=hero_id)
    Console().print(hero)
    return hero


@hero_app.command()
def list() -> Union[Hero, List[Hero]]:
    "list many heros"
    heros = Heros.list()
    Console().print(heros)
    return heros


@hero_app.command()
def clear() -> Union[Hero, List[Hero]]:
    "list many heros"
    heros = Heros.list()
    for hero in heros.__root__:
        HeroDelete.delete(id=hero.id)
    return hero


@hero_app.command()
@engorgio(typer=True)
def create(
    hero: HeroCreate,
) -> Hero:
    "create one hero"
    hero.post()


@hero_app.command()
@engorgio(typer=True)
def update(
    hero: HeroUpdate,
) -> Hero:
    "update one hero"
    hero.update()


@hero_app.command()
@engorgio(typer=True)
def delete(
    hero_id: Optional[int] = typer.Argument(),
) -> Hero:
    "delete a hero by id"
    hero = HeroDelete.delete(id=hero_id)
    Console().print(hero)
    return hero


@hero_app.command()
def populate(
    n: int = 10,
) -> Hero:
    "Create n number of heros"
    if config.env == "prod":
        Console().print("populate is not supported in production")
        sys.exit(1)

    for hero in HeroFactory().batch(n):
        hero = HeroCreate(**hero.dict())
        hero.post()
