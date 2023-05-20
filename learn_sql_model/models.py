from __future__ import annotations

from typing import Optional

from learn_sql_model.models.fast_model import FastModel
from sqlmodel import Field


class Hero(FastModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    # new_attribute: Optional[str] = None
    # pets: List["Pet"] = Relationship(back_populates="hero")
