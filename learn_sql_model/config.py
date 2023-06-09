from contextvars import ContextVar
from typing import TYPE_CHECKING

from fastapi import Depends
from pydantic import BaseModel, BaseSettings, validator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from learn_sql_model.standard_config import load

if TYPE_CHECKING:
    from sqlalchemy import Engine


class ApiServer(BaseModel):
    app: str = "learn_sql_model.api.app:app"
    port: int = 5000
    reload: bool = True
    log_level: str = "info"
    host: str = "0.0.0.0"
    workers: int = 1


class ApiClient(BaseModel):
    host: str = "learn-sql-model.fly.dev"
    protocol: str = "https"
    url: str = f"{protocol}://{host}"

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
            
        self.db_conf = {}
        if 'sqlite' in self.config.database_url:
            self.db_conf = {
                'connect_args': {"check_same_thread": False},
                'pool_recycle': 3600,
                'pool_pre_ping': True,
            }
        self._engine = create_engine(
                self.config.database_url,
                **self.db_conf
            )

    @property
    def engine(self) -> "Engine":
        return self._engine

    @property
    def session(self) -> "Session":
        return Session(self.engine)


class Config(BaseSettings):
    env: str = "dev"
    database_url: str = "sqlite:///database.db"
    api_server: ApiServer = ApiServer()
    api_client: ApiClient = ApiClient()

    class Config:
        extra = "ignore"
        env_nested_delimiter = "__"
        env_file = ".env", ".env.dev", ".env.qa", ".env.prod"

    @validator("database_url")
    def validate_database_url(cls, v: str) -> str:
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+psycopg2://")
        return v

    @property
    def database(self) -> Database:
        return get_database(config=self)

    def init(self) -> None:
        # SQLModel.metadata.create_all(self.database.engine)
        ...


def get_database(config: Config = None) -> Database:
    if config is None:
        config = get_config()
    return Database(config)


def get_config(overrides: dict = {}) -> Config:
    raw_config = load("learn_sql_model")
    config = Config(**raw_config, **overrides)
    return config


config = get_config()
database = get_database()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database.engine)


def get_session() -> "Session":
    with Session(database.engine) as session:
        yield session


async def reset_db_state(config: Config = None) -> None:
    if config is None:
        config = get_config()
    config.database.db._state._state.set(config.database.db_state_default.copy())
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


config = get_config()
