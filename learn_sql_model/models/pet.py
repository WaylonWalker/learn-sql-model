from typing import Optional

from sqlmodel import Field

from learn_sql_model.models.fast_model import FastModel


class Pet(FastModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = "Jim"


#     age: Optional[int] = None

#     hero_id: int = Field(default=None, foreign_key="hero.id")
#     hero: Optional[Hero] = Relationship(back_populates="pets")
