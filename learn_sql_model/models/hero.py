from typing import Optional

from fastapi import HTTPException
import httpx
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel, Session, select

from learn_sql_model.config import config
from learn_sql_model.models.pet import Pet


class HeroBase(SQLModel, table=False):
    name: str
    secret_name: str
    x: int
    y: int
    size: int
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

        return Hero.parse_obj(r.json())


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


class Heros(BaseModel):
    heros: list[Hero]

    @classmethod
    def list(
        self,
        where=None,
        offset=0,
        limit=None,
        session: Session = None,
    ) -> Hero:
        # with config.database.session as session:

        def get_heros(session, where, offset, limit):
            statement = select(Hero)
            if where != "None" and where is not None:
                from sqlmodel import text

                statement = statement.where(text(where))
            statement = statement.offset(offset).limit(limit)
            heros = session.exec(statement).all()
            return Heros(heros=heros)

        if session is None:

            r = httpx.get(f"{config.api_client.url}/heros/")
            if r.status_code != 200:
                raise RuntimeError(f"{r.status_code}:\n {r.text}")
            return Heros.parse_obj(r.json())

        return get_heros(session, where, offset, limit)


class HeroUpdate(SQLModel):
    # id is required to update the hero
    id: int

    # all other fields, must match the model, but with Optional default None
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    shoe_size: Optional[int] = None
    x: int
    y: int

    pet_id: Optional[int] = Field(default=None, foreign_key="pet.id")
    pet: Optional[Pet] = Relationship(back_populates="hero")

    def update(self, session: Session = None) -> Hero:
        if session is not None:
            db_hero = session.get(Hero, self.id)
            if not db_hero:
                raise HTTPException(status_code=404, detail="Hero not found")
            for key, value in self.dict(exclude_unset=True).items():
                setattr(db_hero, key, value)
            session.add(db_hero)
            session.commit()
            session.refresh(db_hero)
            return db_hero

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
