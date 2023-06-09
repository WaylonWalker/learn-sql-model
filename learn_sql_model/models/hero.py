from typing import Optional

from fastapi import HTTPException
import httpx
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel, Session, select

from learn_sql_model.config import config, get_config
from learn_sql_model.models.pet import Pet


class HeroBase(SQLModel, table=False):
    name: str
    secret_name: str
    age: Optional[int] = None
    shoe_size: Optional[int] = None

    pet_id: Optional[int] = Field(default=None, foreign_key="pet.id")
    pet: Optional[Pet] = Relationship(back_populates="hero")


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class HeroCreate(HeroBase):
    ...

    def post(self) -> Hero:
        r = httpx.post(
            f"{config.api_client.url}/hero/",
            json=self.dict(),
        )
        if r.status_code != 200:
            raise RuntimeError(f"{r.status_code}:\n {r.text}")


class HeroRead(HeroBase):
    id: int

    @classmethod
    def get(
        cls,
        id: int,
    ) -> Hero:
        with config.database.session as session:
            hero = session.get(Hero, id)
            if not hero:
                raise HTTPException(status_code=404, detail="Hero not found")
        return hero

    @classmethod
    def list(
        self,
        where=None,
        offset=0,
        limit=None,
        session: Session = None,
    ) -> Hero:
        # with config.database.session as session:

        if session is None:
            session = get_config().database.session
        statement = select(Hero)
        if where != "None" and where is not None:
            from sqlmodel import text

            statement = statement.where(text(where))
        statement = statement.offset(offset).limit(limit)
        heroes = session.exec(statement).all()
        return heroes


class HeroUpdate(SQLModel):
    # id is required to update the hero
    id: int

    # all other fields, must match the model, but with Optional default None
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    shoe_size: Optional[int] = None

    pet_id: Optional[int] = Field(default=None, foreign_key="pet.id")
    pet: Optional[Pet] = Relationship(back_populates="hero")

    def update(self) -> Hero:
        r = httpx.patch(
            f"{config.api_client.url}/hero/",
            json=self.dict(),
        )
        if r.status_code != 200:
            raise RuntimeError(f"{r.status_code}:\n {r.text}")


class HeroDelete(BaseModel):
    id: int

    def delete(self) -> Hero:
        r = httpx.delete(
            f"{config.api_client.url}/hero/{self.id}",
        )
        if r.status_code != 200:
            raise RuntimeError(f"{r.status_code}:\n {r.text}")
        return {"ok": True}
