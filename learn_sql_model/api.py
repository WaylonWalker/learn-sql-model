from typing import Union

from fastapi import FastAPI

from learn_sql_model.models.hero import Hero
from learn_sql_model.models.pet import Pet

models = Union[Hero, Pet]

# from learn_sql_model.config import config
# from learn_sql_model.models import Hero

app = FastAPI()
