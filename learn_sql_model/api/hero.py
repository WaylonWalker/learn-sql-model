from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import SQLModel

from learn_sql_model.api.user import oauth2_scheme
from learn_sql_model.api.websocket_connection_manager import manager
from learn_sql_model.config import Config, get_config
from learn_sql_model.models.hero import (
    Hero,
    HeroCreate,
    HeroDelete,
    HeroRead,
    HeroUpdate,
)

hero_router = APIRouter()


@hero_router.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(get_config().database.engine)


@hero_router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@hero_router.get("/hero/{id}")
async def get_hero(id: int, config: Config = Depends(get_config)) -> Hero:
    "get one hero"
    return Hero().get(id=id, config=config)


@hero_router.get("/h/{id}")
async def get_h(id: int, config: Config = Depends(get_config)) -> Hero:
    "get one hero"
    return Hero().get(id=id, config=config)


@hero_router.post("/hero/")
async def post_hero(hero: HeroCreate) -> HeroRead:
    "read all the heros"
    config = get_config()
    hero = hero.post(config=config)
    await manager.broadcast({hero.json()}, id=1)
    return hero


@hero_router.patch("/hero/")
async def patch_hero(hero: HeroUpdate) -> HeroRead:
    "read all the heros"
    config = get_config()
    hero = hero.update(config=config)
    await manager.broadcast({hero.json()}, id=1)
    return hero


@hero_router.delete("/hero/{hero_id}")
async def delete_hero(hero_id: int):
    "read all the heros"
    hero = HeroDelete(id=hero_id)
    config = get_config()
    hero = hero.delete(config=config)
    await manager.broadcast(f"deleted hero {hero_id}", id=1)
    return hero


@hero_router.get("/heros/")
async def get_heros(config: Config = Depends(get_config)) -> list[Hero]:
    "get all heros"
    return Hero().get(config=config)
