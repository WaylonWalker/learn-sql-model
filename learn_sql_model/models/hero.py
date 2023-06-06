from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel, Session, select

from learn_sql_model.config import Config
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

    def post(self, config: Config) -> Hero:
        config.init()
        with Session(config.database.engine) as session:
            db_hero = Hero.from_orm(self)
            session.add(db_hero)
            session.commit()
            session.refresh(db_hero)
            return db_hero


class HeroRead(HeroBase):
    id: int

    @classmethod
    def get(
        cls,
        config: Config,
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
        config: Config,
        where=None,
        offset=0,
        limit=None,
    ) -> Hero:

        with config.database.session as session:
            statement = select(Hero)
            if where != "None":
                from sqlmodel import text

                statement = statement.where(text(where))
            statement = statement.offset(offset).limit(limit)
            heroes = session.exec(statement).all()
        return heroes


class HeroUpdate(SQLModel):
    # id is required to get the hero
    id: int

    # all other fields, must match the model, but with Optional default None
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    shoe_size: Optional[int] = None

    pet_id: Optional[int] = Field(default=None, foreign_key="pet.id")
    pet: Optional[Pet] = Relationship(back_populates="hero")

    def update(self, config: Config) -> Hero:
        with Session(config.database.engine) as session:
            db_hero = session.get(Hero, self.id)
            if not db_hero:
                raise HTTPException(status_code=404, detail="Hero not found")
            hero_data = self.dict(exclude_unset=True)
            for key, value in hero_data.items():
                if value is not None:
                    setattr(db_hero, key, value)
            session.add(db_hero)
            session.commit()
            session.refresh(db_hero)
            return db_hero


class HeroDelete(BaseModel):
    id: int

    def delete(self, config: Config) -> Hero:
        config.init()
        with Session(config.database.engine) as session:
            hero = session.get(Hero, self.id)
            if not hero:
                raise HTTPException(status_code=404, detail="Hero not found")
            session.delete(hero)
            session.commit()
            return {"ok": True}
