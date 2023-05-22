import tempfile

from fastapi.testclient import TestClient
import pytest
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
    return config


def test_post_hero(config: Config) -> None:
    config.init()  # required for python api, and no existing db
    hero = HeroFactory().build(name="Batman", age=50, id=1)
    hero = hero.post(config=config)
    db_hero = Hero().get(id=1, config=config)
    assert db_hero.age == 50
    assert db_hero.name == "Batman"


def test_update_hero(config: Config) -> None:
    config.init()  # required for python api, and no existing db
    hero = HeroFactory().build(name="Batman", age=50, id=1)
    hero = hero.post(config=config)
    db_hero = Hero().get(id=1, config=config)
    db_hero.name = "Superman"
    hero = db_hero.post(config=config)
    db_hero = Hero().get(id=1, config=config)
    assert db_hero.age == 50
    assert db_hero.name == "Superman"


def test_cli_create(config):
    result = runner.invoke(
        hero_app,
        [
            "create",
            "--name",
            "Darth Vader",
            "--secret-name",
            "Anakin",
            "--id",
            "2",
            "--age",
            "100",
            "--database-url",
            config.database_url,
        ],
    )
    assert result.exit_code == 0
    db_hero = Hero().get(id=2, config=config)
    assert db_hero.age == 100
    assert db_hero.name == "Darth Vader"


def test_read_main(config):
    config.init()
    hero = HeroFactory().build(name="Ironman", age=25, id=99)
    hero_id = hero.id
    hero = hero.post(config=config)
    response = client.get(f"/hero/{hero_id}")
    assert response.status_code == 200
    reponse_hero = Hero.parse_obj(response.json())
    assert reponse_hero.id == hero_id
    assert reponse_hero.name == "Ironman"
    assert reponse_hero.age == 25
