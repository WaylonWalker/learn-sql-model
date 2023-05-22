from typing import List, Union

from pydantic_typer import expand_pydantic_args
from rich.console import Console
import typer

from learn_sql_model.config import Config
from learn_sql_model.factories.hero import HeroFactory
from learn_sql_model.factories.pet import PetFactory
from learn_sql_model.models.hero import Hero
from learn_sql_model.models.pet import Pet

hero_app = typer.Typer()


@hero_app.callback()
def hero():
    "model cli"


@hero_app.command()
@expand_pydantic_args(typer=True)
def get(
    id: int = None,
    config: Config = None,
) -> Union[Hero, List[Hero]]:
    "get one hero"
    config.init()
    hero = Hero().get(id=id)
    Console().print(hero)
    return hero


@hero_app.command()
@expand_pydantic_args(typer=True)
def create(
    hero: Hero,
    pet: Pet = None,
    config: Config = None,
) -> Hero:
    "read all the heros"
    config.init()
    hero.pet = pet
    hero = hero.post(config=config)
    Console().print(hero)


@hero_app.command()
@expand_pydantic_args(typer=True)
def populate(
    n: int = 10,
    config: Config = None,
) -> Hero:
    "read all the heros"
    config.init()
    if config is None:
        config = Config()
    if config.env == "prod":
        Console().print("populate is not supported in production")
        return

    for hero in HeroFactory().batch(n):
        pet = PetFactory().build()
        hero.pet = pet
        Console().print(hero)
        hero.post(config=config)
