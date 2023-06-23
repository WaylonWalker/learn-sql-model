from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from sqlmodel.pool import StaticPool
from typer.testing import CliRunner

from learn_sql_model.api.app import app
from learn_sql_model.cli.hero import hero_app
from learn_sql_model.config import get_session
from learn_sql_model.factories.hero import HeroFactory
from learn_sql_model.models import hero as hero_models
from learn_sql_model.models.hero import Hero, HeroCreate, HeroDelete, HeroRead

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
    hero = HeroFactory().build()
    hero_dict = hero.dict()
    response = client.post("/hero/", json=hero_dict)
    response_hero = Hero.parse_obj(response.json())

    assert response.status_code == 200
    assert response_hero.name == hero.name


def test_api_read_heros(session: Session, client: TestClient):
    heros = HeroFactory().batch(5)
    for hero in heros:
        session.add(hero)
    session.commit()

    response = client.get("/heros/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 5
    for d in data:
        api_hero = Hero.parse_obj(d)
        my_hero = [hero for hero in heros if hero.id == api_hero.id][0]
        for key, value in api_hero.dict(exclude_unset=True).items():
            assert getattr(my_hero, key) == value


def test_api_read_hero(session: Session, client: TestClient):
    hero = HeroFactory().build()
    session.add(hero)
    session.commit()

    response = client.get(f"/hero/{hero.id}")
    data = response.json()
    response_hero = Hero.parse_obj(data)

    assert response.status_code == 200
    for key, value in hero.dict(exclude_unset=True).items():
        assert getattr(response_hero, key) == value


def test_api_read_hero_404(session: Session, client: TestClient):
    hero = HeroFactory().build()
    session.add(hero)
    session.commit()

    response = client.get(f"/hero/999")
    assert response.status_code == 404


def test_api_update_hero(session: Session, client: TestClient):
    hero = HeroFactory().build()
    new_hero = HeroFactory().build()
    session.add(hero)
    session.commit()

    response = client.patch(
        f"/hero/", json={"id": hero.id, **new_hero.dict(exclude={"id"})}
    )
    data = response.json()
    response_hero = Hero.parse_obj(data)

    assert response.status_code == 200
    for key, value in hero.dict(exclude_unset=True).items():
        assert getattr(response_hero, key) == value


def test_api_update_hero_404(session: Session, client: TestClient):
    hero_1 = HeroFactory().build()
    session.add(hero_1)
    session.commit()

    response = client.patch(f"/hero/", json={"name": "Deadpuddle", "id": 999})
    assert response.status_code == 404


def test_delete_hero(session: Session, client: TestClient):
    hero_1 = HeroFactory().build()
    session.add(hero_1)
    session.commit()

    response = client.delete(f"/hero/{hero_1.id}")

    hero_in_db = session.get(Hero, hero_1.id)

    assert response.status_code == 200

    assert hero_in_db is None


def test_delete_hero_404(session: Session, client: TestClient):
    hero_1 = HeroFactory().build()
    session.add(hero_1)
    session.commit()

    response = client.delete(f"/hero/999")
    assert response.status_code == 404


def test_cli_get(mocker):
    hero = HeroFactory().build()
    hero = HeroRead(**hero.dict(exclude_none=True))
    httpx = mocker.patch.object(hero_models, "httpx")
    httpx.get.return_value = mocker.Mock()
    httpx.get.return_value.status_code = 200
    httpx.get.return_value.json.return_value = hero.dict()

    result = runner.invoke(hero_app, ["get", "1"])
    assert result.exit_code == 0
    for key, value in hero.dict(exclude_unset=True).items():
        if type(value) == str:
            assert f"{key}='{value}'" in result.stdout
        elif type(value) == int:
            assert f"{key}={value}" in result.stdout
    assert httpx.get.call_count == 1
    assert httpx.post.call_count == 0
    assert httpx.delete.call_count == 0


def test_cli_get_404(mocker):
    hero = HeroFactory().build()
    hero = HeroRead(**hero.dict(exclude_none=True))
    httpx = mocker.patch.object(hero_models, "httpx")
    httpx.get.return_value = mocker.Mock()
    httpx.get.return_value.status_code = 404
    httpx.get.return_value.text = "Hero not found"
    httpx.get.return_value.json.return_value = hero.dict()

    result = runner.invoke(hero_app, ["get", "999"])
    assert result.exit_code == 1
    assert " ".join(result.exception.args[0].split()) == "404: Hero not found"
    assert httpx.get.call_count == 1
    assert httpx.post.call_count == 0
    assert httpx.delete.call_count == 0


def test_cli_list(mocker):
    heros = HeroFactory().batch(5)
    httpx = mocker.patch.object(hero_models, "httpx")
    httpx.get.return_value = mocker.Mock()
    httpx.get.return_value.status_code = 200
    httpx.get.return_value.json.return_value = heros

    result = runner.invoke(hero_app, ["list"])
    assert result.exit_code == 0

    for hero in heros:
        for key, value in hero.dict(exclude_unset=True).items():
            if type(value) == str:
                assert f"{key}='{value}'" in result.stdout
            elif type(value) == int:
                assert f"{key}={value}" in result.stdout


def test_model_post(mocker):
    hero = HeroFactory().build()
    hero_create = HeroCreate(**hero.dict())

    httpx = mocker.patch.object(hero_models, "httpx")
    httpx.post.return_value = mocker.Mock()
    httpx.post.return_value.status_code = 200
    httpx.post.return_value.json.return_value = hero.dict()
    result = hero_create.post()
    assert result == hero
    assert httpx.get.call_count == 0
    assert httpx.post.call_count == 1
    assert httpx.delete.call_count == 0


def test_model_post_500(mocker):
    hero = HeroFactory().build()
    hero_create = HeroCreate(**hero.dict())

    httpx = mocker.patch.object(hero_models, "httpx")
    httpx.post.return_value = mocker.Mock()
    httpx.post.return_value.status_code = 500
    httpx.post.return_value.json.return_value = hero.dict()
    with pytest.raises(RuntimeError):
        hero_create.post()
    assert httpx.get.call_count == 0
    assert httpx.post.call_count == 1
    assert httpx.delete.call_count == 0


def test_model_read_hero(mocker):
    hero = HeroFactory().build()

    httpx = mocker.patch.object(hero_models, "httpx")
    httpx.get.return_value = mocker.Mock()
    httpx.get.return_value.status_code = 200
    httpx.get.return_value.json.return_value = hero.dict()

    hero_read = HeroRead.get(id=hero.id)
    assert hero_read.name == hero.name
    assert hero_read.secret_name == hero.secret_name
    assert httpx.get.call_count == 1
    assert httpx.post.call_count == 0
    assert httpx.delete.call_count == 0


def test_model_read_hero_404(mocker):
    hero = HeroFactory().build()
    httpx = mocker.patch.object(hero_models, "httpx")
    httpx.get.return_value = mocker.Mock()
    httpx.get.return_value.status_code = 404
    httpx.get.return_value.text = "Hero not found"

    with pytest.raises(RuntimeError) as e:
        HeroRead.get(id=hero.id)
        assert e.value.args[0] == "404: Hero not found"
    assert httpx.get.call_count == 1
    assert httpx.post.call_count == 0
    assert httpx.delete.call_count == 0


def test_model_delete_hero(mocker):
    hero = HeroFactory().build()

    httpx = mocker.patch.object(hero_models, "httpx")
    httpx.delete.return_value = mocker.Mock()
    httpx.delete.return_value.status_code = 200
    httpx.delete.return_value.json.return_value = hero.dict()

    hero_delete = HeroDelete.delete(id=hero.id)
    assert hero_delete == {"ok": True}
    assert httpx.get.call_count == 0
    assert httpx.post.call_count == 0
    assert httpx.delete.call_count == 1


def test_model_delete_hero_404(mocker):
    hero = HeroFactory().build()

    httpx = mocker.patch.object(hero_models, "httpx")
    httpx.delete.return_value = mocker.Mock()
    httpx.delete.return_value.status_code = 404
    httpx.get.return_value.text = "Hero not found"

    with pytest.raises(RuntimeError) as e:
        HeroDelete.delete(id=hero.id)
        assert e.value.args[0] == "404: Hero not found"
    assert httpx.get.call_count == 0
    assert httpx.post.call_count == 0
    assert httpx.delete.call_count == 1


def test_cli_delete_hero(mocker):
    hero = HeroFactory().build()

    httpx = mocker.patch.object(hero_models, "httpx")
    httpx.delete.return_value = mocker.Mock()
    httpx.delete.return_value.status_code = 200
    httpx.delete.return_value.json.return_value = hero.dict()

    result = runner.invoke(hero_app, ["delete", "--hero-id", "1"])
    assert result.exit_code == 0
    assert "{'ok': True}" in result.stdout
    assert httpx.get.call_count == 0
    assert httpx.post.call_count == 0
    assert httpx.delete.call_count == 1


def test_cli_delete_hero_404(mocker):
    hero = HeroFactory().build()

    httpx = mocker.patch.object(hero_models, "httpx")
    httpx.delete.return_value = mocker.Mock()
    httpx.delete.return_value.status_code = 404
    httpx.delete.return_value.text = "Hero not found"
    httpx.delete.return_value.json.return_value = hero.dict()

    result = runner.invoke(hero_app, ["delete", "--hero-id", "999"])
    assert result.exit_code == 1
    assert " ".join(result.exception.args[0].split()) == "404: Hero not found"
    assert httpx.get.call_count == 0
    assert httpx.post.call_count == 0
    assert httpx.delete.call_count == 1
