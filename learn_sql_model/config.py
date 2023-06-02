from contextvars import ContextVar
from typing import TYPE_CHECKING

from fastapi import Depends
from pydantic import BaseModel, BaseSettings
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from learn_sql_model.standard_config import load

if TYPE_CHECKING:
    from sqlalchemy import Engine


class ApiServer(BaseModel):
    app: str = "learn_sql_model.api.app:app"
    port: int = 5000
    reload: bool = True
    log_level: str = "info"
    host: str = "0.0.0.0"


class Database:
    def __init__(self, config: "Config" = None) -> None:
        if config is None:

            self.config = get_config()
        else:
            self.config = config
            self.db_state_default = {
                "closed": None,
                "conn": None,
                "ctx": None,
                "transactions": None,
            }
            self.db_state = ContextVar("db_state", default=self.db_state_default.copy())

    @property
    def engine(self) -> "Engine":
        return create_engine(self.config.database_url)

    @property
    def session(self) -> "Session":
        return Session(self.engine)


class Config(BaseSettings):
    env: str = "dev"
    database_url: str = "sqlite:///database.db"
    api_server: ApiServer = ApiServer()

    class Config:
        extra = "ignore"
        env_nested_delimiter = "__"
        env_file = ".env", ".env.dev", ".env.qa", ".env.prod"

    @property
    def database(self) -> Database:
        return get_database(config=self)

    def init(self) -> None:
        SQLModel.metadata.create_all(self.database.engine)


def get_database(config: Config = None) -> Database:

    if config is None:
        config = get_config()

    return Database(config)


async def reset_db_state(config: Config = None) -> None:
    if config is None:
        config = get_config()
    config.database.db._state._state.set(db_state_default.copy())
    config.database.db._state.reset()


def get_db(config: Config = None, reset_db_state=Depends(reset_db_state)):
    if config is None:
        config = get_config()
    try:
        config.database.db.connect()
        yield
    finally:
        if not config.database.db.is_closed():
            config.database.db.close()


def get_config(overrides: dict = {}) -> Config:
    raw_config = load("learn_sql_model")
    config = Config(**raw_config, **overrides)
    return config
