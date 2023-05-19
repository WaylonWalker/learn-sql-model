from typing import TYPE_CHECKING

from pydantic import BaseSettings
from sqlmodel import SQLModel, Session, create_engine

from learn_sql_model.models import Hero, Pet
from learn_sql_model.standard_config import load

models = [Hero, Pet]

if TYPE_CHECKING:
    from sqlalchemy import Engine


class Config(BaseSettings):
    database_url: str = "sqlite:///database.db"

    class Config:
        env_prefix = "LEARN_SQL_MODEL_"

    @property
    def engine(self) -> "Engine":
        return create_engine(self.database_url)

    @property
    def session(self) -> "Session":
        return Session(self.engine)

    def create_db_and_tables(self) -> None:
        SQLModel.metadata.create_all(self.engine)

    # def create_endpoints(self) -> None:
    # for model in models:
    # app.post("/heroes/")(Hero.post_local)
    # app.get("/heroes/")(Hero.read_heroes)


raw_config = load("learn_sql_model")
config = Config(**raw_config)
config.create_db_and_tables()
