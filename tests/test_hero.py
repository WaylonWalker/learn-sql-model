import tempfile

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from typer.testing import CliRunner

from learn_sql_model.api.app import app
from learn_sql_model.cli.hero import hero_app
from learn_sql_model.config import Config, get_config
from learn_sql_model.factories.hero import HeroFactory
from learn_sql_model.models.hero import Hero

runner = CliRunner()
client = TestClient(app)


@pytest.fixture
def config() -> Config:
    tmp_db = tempfile.NamedTemporaryFile(suffix=".db")
    config = get_config({"database_url": f"sqlite:///{tmp_db.name}"})

    engine = create_engine(
        config.database_url, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # breakpoint()
    SQLModel.metadata.create_all(config.database.engine)

    # def override_get_db():
    #     try:
    #         db = TestingSessionLocal()
    #         yield db
    #     finally:
    #         db.close()
    def override_get_config():
        return config

    app.dependency_overrides[get_config] = override_get_config

    yield config
    # tmp_db automatically deletes here


def test_post_hero(config: Config) -> None:
    hero = HeroFactory().build(name="Batman", age=50, id=1)
    hero = hero.post(config=config)
    db_hero = Hero().get(id=1, config=config)
    assert db_hero.age == 50
    assert db_hero.name == "Batman"


def test_update_hero(config: Config) -> None:
    hero = HeroFactory().build(name="Batman", age=50, id=1)
    hero = hero.post(config=config)
    db_hero = Hero().get(id=1, config=config)
    db_hero.name = "Superbman"
    hero = db_hero.post(config=config)
    db_hero = Hero().get(id=1, config=config)
    assert db_hero.age == 50
    assert db_hero.name == "Superbman"


def test_cli_get(config):
    hero = HeroFactory().build(name="Steelman", age=25, id=99)
    hero.post(config=config)
    result = runner.invoke(
        hero_app,
        ["get", "--id", 99, "--database-url", config.database_url],
    )
    assert result.exit_code == 0
    db_hero = Hero().get(id=99, config=config)
    assert db_hero.age == 25
    assert db_hero.name == "Steelman"


def test_cli_create(config):
    hero = HeroFactory().build(name="Steelman", age=25, id=99)
    result = runner.invoke(
        hero_app,
        [
            "create",
            *hero.flags(config=config),
            "--database-url",
            config.database_url,
        ],
    )
    assert result.exit_code == 0
    db_hero = Hero().get(id=99, config=config)
    assert db_hero.age == 25
    assert db_hero.name == "Steelman"


def test_cli_populate(config):
    result = runner.invoke(
        hero_app,
        [
            "populate",
            "--n",
            10,
            "--database-url",
            config.database_url,
        ],
    )
    assert result.exit_code == 0
    db_hero = Hero().get(config=config)
    assert len(db_hero) == 10


def test_cli_populate_fails_prod(config):
    result = runner.invoke(
        hero_app,
        ["populate", "--n", 10, "--database-url", config.database_url, "--env", "prod"],
    )
    assert result.exit_code == 1
    assert result.output.strip() == "populate is not supported in production"


def test_api_read(config):
    hero = HeroFactory().build(name="Steelman", age=25, id=99)
    hero_id = hero.id
    hero = hero.post(config=config)
    response = client.get(f"/hero/{hero_id}")
    assert response.status_code == 200
    reponse_hero = Hero.parse_obj(response.json())
    assert reponse_hero.id == hero_id
    assert reponse_hero.name == "Steelman"
    assert reponse_hero.age == 25


def test_api_post(config):
    hero = HeroFactory().build(name="Steelman", age=25)
    hero_dict = hero.dict()
    response = client.post("/hero/", json={"hero": hero_dict})
    assert response.status_code == 200

    response_hero = Hero.parse_obj(response.json())
    db_hero = Hero().get(id=response_hero.id, config=config)

    assert db_hero.name == "Steelman"
    assert db_hero.age == 25


def test_api_read_all(config):
    hero = HeroFactory().build(name="Mothman", age=25, id=99)
    hero_id = hero.id
    hero = hero.post(config=config)
    response = client.get("/heros/")
    assert response.status_code == 200
    heros = response.json()
    response_hero_json = [hero for hero in heros if hero["id"] == hero_id][0]
    response_hero = Hero.parse_obj(response_hero_json)
    assert response_hero.id == hero_id
    assert response_hero.name == "Mothman"
    assert response_hero.age == 25
