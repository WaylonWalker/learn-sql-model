from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select
from sqlmodel.pool import StaticPool
from typer.testing import CliRunner

from learn_sql_model.api.app import app
from learn_sql_model.cli.hero import hero_app
from learn_sql_model.config import get_config, get_session
from learn_sql_model.factories.hero import HeroFactory
from learn_sql_model.models.hero import Hero

runner = CliRunner()
client = TestClient(app)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_api_post(client: TestClient):
    hero = HeroFactory().build(name="Steelman", age=25)
    hero_dict = hero.dict()
    response = client.post("/hero/", json={"hero": hero_dict})
    response_hero = Hero.parse_obj(response.json())

    assert response.status_code == 200
    assert response_hero.name == "Steelman"
    assert response_hero.age == 25


def test_api_read_heroes(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    session.add(hero_1)
    session.add(hero_2)
    session.commit()

    response = client.get("/heros/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == hero_1.name
    assert data[0]["secret_name"] == hero_1.secret_name
    assert data[0]["age"] == hero_1.age
    assert data[0]["id"] == hero_1.id
    assert data[1]["name"] == hero_2.name
    assert data[1]["secret_name"] == hero_2.secret_name
    assert data[1]["age"] == hero_2.age
    assert data[1]["id"] == hero_2.id


def test_api_read_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.get(f"/hero/999")
    assert response.status_code == 404


def test_api_read_hero_404(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.get(f"/hero/{hero_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hero_1.name
    assert data["secret_name"] == hero_1.secret_name
    assert data["age"] == hero_1.age
    assert data["id"] == hero_1.id


def test_api_update_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.patch(
        f"/hero/", json={"hero": {"name": "Deadpuddle", "id": hero_1.id}}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Deadpuddle"
    assert data["secret_name"] == "Dive Wilson"
    assert data["age"] is None
    assert data["id"] == hero_1.id


def test_api_update_hero_404(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.patch(f"/hero/", json={"hero": {"name": "Deadpuddle", "id": 999}})
    assert response.status_code == 404


def test_delete_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.delete(f"/hero/{hero_1.id}")

    hero_in_db = session.get(Hero, hero_1.id)

    assert response.status_code == 200

    assert hero_in_db is None


def test_delete_hero_404(session: Session, client: TestClient):
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.delete(f"/hero/999")
    assert response.status_code == 404


def test_config_memory(mocker):
    mocker.patch(
        "learn_sql_model.config.Database.engine",
        new_callable=lambda: create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        ),
    )
    config = get_config()
    SQLModel.metadata.create_all(config.database.engine)
    hero = HeroFactory().build(name="Steelman", age=25)
    with config.database.session as session:
        session.add(hero)
        session.commit()
        hero = session.get(Hero, hero.id)
        heroes = session.exec(select(Hero)).all()
    assert hero.name == "Steelman"
    assert hero.age == 25
    assert len(heroes) == 1


def test_cli_get(mocker):
    mocker.patch(
        "learn_sql_model.config.Database.engine",
        new_callable=lambda: create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        ),
    )

    config = get_config()
    SQLModel.metadata.create_all(config.database.engine)

    hero = HeroFactory().build(name="Steelman", age=25)
    with config.database.session as session:
        session.add(hero)
        session.commit()
        hero = session.get(Hero, hero.id)
    result = runner.invoke(hero_app, ["get", "--hero-id", "1"])
    assert result.exit_code == 0
    assert f"name='{hero.name}'" in result.stdout
    assert f"secret_name='{hero.secret_name}'" in result.stdout


def test_cli_get_404(mocker):
    mocker.patch(
        "learn_sql_model.config.Database.engine",
        new_callable=lambda: create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        ),
    )

    config = get_config()
    SQLModel.metadata.create_all(config.database.engine)

    hero = HeroFactory().build(name="Steelman", age=25)
    with config.database.session as session:
        session.add(hero)
        session.commit()
        hero = session.get(Hero, hero.id)
    result = runner.invoke(hero_app, ["get", "--hero-id", "999"])
    assert result.exception.status_code == 404
    assert result.exception.detail == "Hero not found"


def test_cli_list(mocker):
    mocker.patch(
        "learn_sql_model.config.Database.engine",
        new_callable=lambda: create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        ),
    )

    config = get_config()
    SQLModel.metadata.create_all(config.database.engine)

    hero_1 = HeroFactory().build(name="Steelman", age=25)
    hero_2 = HeroFactory().build(name="Hunk", age=52)

    with config.database.session as session:
        session.add(hero_1)
        session.add(hero_2)
        session.commit()
        session.refresh(hero_1)
        session.refresh(hero_2)
    result = runner.invoke(hero_app, ["list"])
    assert result.exit_code == 0
    assert f"name='{hero_1.name}'" in result.stdout
    assert f"secret_name='{hero_1.secret_name}'" in result.stdout
    assert f"name='{hero_2.name}'" in result.stdout
    assert f"secret_name='{hero_2.secret_name}'" in result.stdout
