from typing import Dict, Optional

import httpx
import pydantic
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from learn_sql_model.config import config
from learn_sql_model.optional import optional


class HeroBase(SQLModel, table=False):
    name: str
    secret_name: str
    x: int
    y: int
    size: Optional[int]
    flashlight_strength: Optional[int] = 1000
    flashlight_angle: Optional[int] = 0
    lanturn_strength: Optional[int] = 100
    # age: Optional[int] = None
    # shoe_size: Optional[int] = None

    # pet_id: Optional[int] = Field(default=None, foreign_key="pet.id")
    # pet: Optional[Pet] = Relationship(back_populates="hero")

    @pydantic.validator("size", pre=True, always=True)
    def validate_size(cls, v):
        if v is None:
            return 50
        if v <= 0:
            raise ValueError("size must be > 0")
        return v


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
