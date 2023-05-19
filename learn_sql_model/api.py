from typing import Union

from fastapi import FastAPI

import httpx
from learn_sql_model.console import console
from learn_sql_model.models import Hero, Pet

models = Union[Hero, Pet]

# from learn_sql_model.config import config
# from learn_sql_model.models import Hero

app = FastAPI()


app.post("/heroes/")


def post(self: models) -> None:

    try:
        httpx.post("http://localhost:5000/heroes/", json=self.dict())
    except httpx.ConnectError:
        console.log("local failover")
        post_local(self)


def post_local(self: models) -> None:
    from learn_sql_model.config import config

    with config.session as session:
        session.add(self)
        session.commit()


def get(self: models, instance: models = None) -> list[models]:
    "read all the heros"
    from learn_sql_model.config import config

    with config.session as session:
        if instance is None:
            heroes = session.exec(select(self)).all()
            return heroes
        else:
            hero = session.exec(select(self).where(self.id == instance.id)).all().one()
            return hero


@app.post("/heroes/")
def create_hero(hero: Hero):
    post(hero)


@app.get("/heroes/")
def read_heroes() -> list[Hero]:
    "read all the heros"
    return get(Hero)


@app.get("/hero/")
def read_heroes(hero: Hero) -> list[Hero]:
    "read all the heros"
    return get(Hero, hero)
