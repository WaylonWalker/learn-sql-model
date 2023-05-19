from fastapi import FastAPI

from learn_sql_model.api.hero import hero_router
from learn_sql_model.api.user import user_router

app = FastAPI()

app.include_router(hero_router)
app.include_router(user_router)
