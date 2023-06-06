from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship

from learn_sql_model.models.fast_model import FastModel

if TYPE_CHECKING:
    from learn_sql_model.models.hero import Hero


class PetBase(FastModel, table=False):
    name: str = "Jim"
    birthday: Optional[datetime] = None
    hero: "Hero" = Relationship(back_populates="pet")


class Pet(PetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PetCreate(PetBase):
    ...


class PetRead(PetBase):
    id: int


class PetUpdate(PetBase):
    ...


class PetDelete(PetBase):
    id: int
