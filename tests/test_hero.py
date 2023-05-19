import tempfile

import pytest
from sqlmodel import Session

from learn_sql_model.config import Config, get_config
from learn_sql_model.factories.hero import HeroFactory
from learn_sql_model.models.hero import Hero

Hero


@pytest.fixture
def config() -> Session:
    tmp_db = tempfile.NamedTemporaryFile(suffix=".db")
    config = get_config({"database_url": f"sqlite:///{tmp_db.name}"})
    config.create_db_and_tables()
    return config


def test_post_hero(config: Config) -> None:
    hero = HeroFactory().build(name="Batman", age=50)
    hero.post(config=config)
    assert hero.get(hero.id) == hero
    breakpoint()
