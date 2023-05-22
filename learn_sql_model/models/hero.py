from typing import Optional

from sqlmodel import Field, Relationship

from learn_sql_model.models.fast_model import FastModel
from learn_sql_model.models.pet import Pet


class Hero(FastModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    shoe_size: Optional[int] = None

    pet_id: Optional[int] = Field(default=None, foreign_key="pet.id")
    pet: Optional[Pet] = Relationship(back_populates="hero")
