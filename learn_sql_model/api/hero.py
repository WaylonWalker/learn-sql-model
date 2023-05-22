from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import SQLModel

from learn_sql_model.api.user import oauth2_scheme
from learn_sql_model.config import get_config
from learn_sql_model.models.hero import Hero

hero_router = APIRouter()


@hero_router.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(get_config().database.engine)


@hero_router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@hero_router.get("/hero/{id}")
def get_hero(id: int) -> Hero:
    "get one hero"
    return Hero().get(id=id)


@hero_router.post("/hero/")
def post_hero(hero: Hero) -> Hero:
    "read all the heros"
    return hero.post()


@hero_router.get("/heros/")
def get_heros() -> list[Hero]:
    "get all heros"
    return Hero().get()
    # Alternatively
    # with get_config().database.session as session:
    #     statement = select(Hero)
    #     results = session.exec(statement).all()
    # return results
