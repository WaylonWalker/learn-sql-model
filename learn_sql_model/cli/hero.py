from typing import List, Union

from pydantic_typer import expand_pydantic_args
from rich.console import Console
import typer

from learn_sql_model.models.hero import Hero

hero_app = typer.Typer()


@hero_app.callback()
def hero():
    "model cli"


@hero_app.command()
def get(id: int = None) -> Union[Hero, List[Hero]]:
    "get one hero"
    hero = Hero().get(item_id=id)
    Console().print(hero)
    return hero


@hero_app.command()
@expand_pydantic_args(typer=True)
def create(hero: Hero) -> Hero:
    "read all the heros"
    hero = hero.post()
    Console().print(hero)
