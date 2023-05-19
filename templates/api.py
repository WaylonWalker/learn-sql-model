from learn_sql_model.api.app import app
from learn_sql_model.models import Hero


@app.post("/hero/")
def create_hero(hero: Hero) -> Hero:
    post(hero)
    return hero


@app.get("/hero/")
def read_heroes(hero: Hero) -> list[Hero]:
    "read all the heros"
    return hero.post()


@app.get("/heros/")
def read_heros() -> list[Hero]:
    "read all the heros"
    return Hero.get()
