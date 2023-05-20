from typing import TYPE_CHECKING

from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from learn_sql_model.standard_config import load

if TYPE_CHECKING:
    from sqlalchemy import Engine


class Database:
    def __init__(self, config: "Config" = None) -> None:
        if config is None:

            self.config = get_config()
        else:
            self.config = config
        self.create_db_and_tables()

    @property
    def engine(self) -> "Engine":
        return create_engine(self.config.database_url)

    def session(self) -> "Session":
        return Session(self.engine)

    def create_db_and_tables(self) -> None:
        from learn_sql_model.models.hero import Hero
        from learn_sql_model.models.pet import Pet

        __all__ = [Hero, Pet]

        SQLModel.metadata.create_all(self.engine)


class Config(BaseSettings):
    database_url: str = "sqlite:///database.db"
    port: int = 5000

    class Config:
        env_prefix = "LEARN_SQL_MODEL_"

    @property
    def database(self) -> Database:
        return get_database(config=self)


def get_database(config: Config = None) -> Database:

    if config is None:
        config = get_config()

    return Database(config)


def get_config(overrides: dict = {}) -> Config:
    raw_config = load("learn_sql_model")
    config = Config(**raw_config, **overrides)
    return config
