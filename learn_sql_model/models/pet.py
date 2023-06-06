from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship

from learn_sql_model.models.fast_model import FastModel

if TYPE_CHECKING:
    from learn_sql_model.models.hero import Hero


class Pet(FastModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = "Jim"
    birthday: Optional[datetime] = None
    hero: "Hero" = Relationship(back_populates="pet")
