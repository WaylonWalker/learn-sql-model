from __future__ import annotations

from typing import Optional

from sqlmodel import Field, SQLModel, select


class FastModel(SQLModel):
    def post(self):
        from learn_sql_model.config import config

        with config.session as session:
            session.add(self)
            session.commit()

    @classmethod
    def get(self, item_id: int = None):
        from learn_sql_model.config import config

        with config.session as session:
            if item_id is None:
                return session.exec(select(self)).all()
            return session.exec(select(self).where(self.id == item_id)).one()


class Hero(FastModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    # new_attribute: Optional[str] = None
    # pets: List["Pet"] = Relationship(back_populates="hero")


class Pet(FastModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = "Jim"


#     age: Optional[int] = None

#     hero_id: int = Field(default=None, foreign_key="hero.id")
#     hero: Optional[Hero] = Relationship(back_populates="pets")
