from typing import Annotated

from fastapi import APIRouter, Depends

from learn_sql_model.api.user import oauth2_scheme
from learn_sql_model.models import Hero

hero_router = APIRouter()


@hero_router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@hero_router.get("/hero/{id}")
def get_hero(id: int) -> Hero:
    "get one hero"
    return Hero.get(item_id=id)


@hero_router.post("/hero/")
def post_hero(hero: Hero) -> Hero:
    "read all the heros"
    return hero.post()


@hero_router.get("/heros/")
def get_heros() -> list[Hero]:
    "get all heros"
    return Hero.get()
