from typing import Optional

from sqlmodel import Field

from learn_sql_model.models.fast_model import FastModel


class Hero(FastModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    shoe_size: Optional[int] = None
