import sys
from typing import List, Optional, Union

from engorgio import engorgio
import httpx
from rich.console import Console
import typer

from learn_sql_model.config import Config, get_config
from learn_sql_model.factories.hero import HeroFactory
from learn_sql_model.factories.pet import PetFactory
from learn_sql_model.models.hero import (
    Hero,
    HeroCreate,
    HeroDelete,
    HeroRead,
    HeroUpdate,
)

hero_app = typer.Typer()


@hero_app.callback()
def hero():
    "model cli"


@hero_app.command()
@engorgio(typer=True)
def get(
    id: Optional[int] = typer.Argument(default=None),
    config: Config = None,
) -> Union[Hero, List[Hero]]:
    "get one hero"
    config.init()
    hero = HeroRead.get(id=id, config=config)
    Console().print(hero)
    return hero


@hero_app.command()
@engorgio(typer=True)
def list(
    where: Optional[str] = None,
    config: Config = None,
    offset: int = 0,
    limit: Optional[int] = None,
) -> Union[Hero, List[Hero]]:
    "get one hero"
    hero = HeroRead.list(config=config, where=where, offset=offset, limit=limit)
    Console().print(hero)
    return hero


@hero_app.command()
@engorgio(typer=True)
def create(
    hero: HeroCreate,
    config: Config = None,
) -> Hero:
    "read all the heros"

    r = httpx.post(
        f"{config.api_client.url}/hero/",
        json=hero.dict(),
    )
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code}:\n {r.text}")

    # hero = hero.post(config=config)
    # Console().print(hero)
    # return hero


@hero_app.command()
@engorgio(typer=True)
def update(
    hero: HeroUpdate,
    config: Config = None,
) -> Hero:
    "read all the heros"
    r = httpx.patch(
        f"{config.api_client.url}/hero/",
        json=hero.dict(),
    )
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code}:\n {r.text}")


@hero_app.command()
@engorgio(typer=True)
def delete(
    hero: HeroDelete,
    config: Config = None,
) -> Hero:
    "read all the heros"
    r = httpx.delete(
        f"{config.api_client.url}/hero/{hero.id}",
    )
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code}:\n {r.text}")


@hero_app.command()
@engorgio(typer=True)
def populate(
    hero: Hero,
    n: int = 10,
) -> Hero:
    "read all the heros"
    config = get_config()
    if config.env == "prod":
        Console().print("populate is not supported in production")
        sys.exit(1)

    for hero in HeroFactory().batch(n):
        pet = PetFactory().build()
        hero.pet = pet
        Console().print(hero)
        hero.post(config=config)
