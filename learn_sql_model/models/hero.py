from typing import Dict

import httpx
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from learn_sql_model.config import config
from learn_sql_model.optional import optional


class HeroBase(SQLModel, table=False):
    name: str
    secret_name: str
    x: int
    y: int
    # size: int
    # age: Optional[int] = None
    # shoe_size: Optional[int] = None

    # pet_id: Optional[int] = Field(default=None, foreign_key="pet.id")
    # pet: Optional[Pet] = Relationship(back_populates="hero")


class Hero(HeroBase, table=True):
    id: int = Field(default=None, primary_key=True)


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
        r = httpx.get(f"{config.api_client.url}/hero/{id}")
        if r.status_code != 200:
            raise RuntimeError(f"{r.status_code}:\n {r.text}")
        return HeroRead.parse_obj(r.json())


class Heros(BaseModel):
    __root__: list[Hero]

    @classmethod
    def list(
        self,
    ) -> Hero:
        r = httpx.get(f"{config.api_client.url}/heros/")
        if r.status_code != 200:
            raise RuntimeError(f"{r.status_code}:\n {r.text}")
        return Heros.parse_obj({"__root__": r.json()})


@optional
class HeroUpdate(HeroBase):
    id: int

    def update(self) -> Hero:
        r = httpx.patch(
            f"{config.api_client.url}/hero/",
            json=self.dict(exclude_none=True),
        )
        if r.status_code != 200:
            raise RuntimeError(f"{r.status_code}:\n {r.text}")


class HeroDelete(BaseModel):
    id: int

    @classmethod
    def delete(self, id: int) -> Dict[str, bool]:
        r = httpx.delete(
            f"{config.api_client.url}/hero/{id}",
        )
        if r.status_code != 200:
            raise RuntimeError(f"{r.status_code}:\n {r.text}")
        return {"ok": True}
