from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import SQLModel

from learn_sql_model.api.user import oauth2_scheme
from learn_sql_model.config import Config, get_config
from learn_sql_model.models.new import new

new_router = APIRouter()


@new_router.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(get_config().database.engine)


@new_router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@new_router.get("/new/{id}")
def get_new(id: int, config: Config = Depends(get_config)) -> new:
    "get one new"
    return new().get(id=id, config=config)


@new_router.get("/h/{id}")
def get_h(id: int, config: Config = Depends(get_config)) -> new:
    "get one new"
    return new().get(id=id, config=config)


@new_router.post("/new/")
def post_new(new: new, config: Config = Depends(get_config)) -> new:
    "read all the news"
    new.post(config=config)
    return new


@new_router.get("/news/")
def get_news(config: Config = Depends(get_config)) -> list[new]:
    "get all news"
    return new().get(config=config)
