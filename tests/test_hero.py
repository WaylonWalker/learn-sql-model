import tempfile

import pytest

from learn_sql_model.config import Config, get_config
from learn_sql_model.factories.hero import HeroFactory
from learn_sql_model.models.hero import Hero

Hero


@pytest.fixture
def config() -> Config:
    tmp_db = tempfile.NamedTemporaryFile(suffix=".db")
    config = get_config({"database_url": f"sqlite:///{tmp_db.name}"})
    return config


def test_post_hero(config: Config) -> None:
    hero = HeroFactory().build(name="Batman", age=50, id=1)
    hero = hero.post(config=config)
    db_hero = Hero().get(hero.id, config=config)
    assert db_hero == hero


def test_update_hero(config: Config) -> None:
    hero = HeroFactory().build(name="Batman", age=50, id=1)
    hero = hero.post(config=config)
    db_hero = Hero().get(id=hero.id, config=config)
    assert db_hero.dict() == hero.dict()
    db_hero.name = "Superman"
    hero = db_hero.post(config=config)
    db_hero = Hero().get(id=hero.id, config=config)
    assert db_hero.dict() == hero.dict()
