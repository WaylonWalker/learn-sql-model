from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel, Session, select

from learn_sql_model.config import Config
from learn_sql_model.models.pet import Pet


class newBase(SQLModel, table=False):


class new(newBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class newCreate(newBase):
    ...

    def post(self, config: Config) -> new:
        config.init()
        with Session(config.database.engine) as session:
            db_new = new.from_orm(self)
            session.add(db_new)
            session.commit()
            session.refresh(db_new)
            return db_new


class newRead(newBase):
    id: int

    @classmethod
    def get(
        cls,
        config: Config,
        id: int,
    ) -> new:

        with config.database.session as session:
            new = session.get(new, id)
            if not new:
                raise HTTPException(status_code=404, detail="new not found")
        return new

    @classmethod
    def list(
        self,
        config: Config,
        where=None,
        offset=0,
        limit=None,
    ) -> new:

        with config.database.session as session:
            statement = select(new)
            if where != "None":
                from sqlmodel import text

                statement = statement.where(text(where))
            statement = statement.offset(offset).limit(limit)
            newes = session.exec(statement).all()
        return newes


class newUpdate(SQLModel):
    # id is required to get the new
    id: int

    # all other fields, must match the model, but with Optional default None

    def update(self, config: Config) -> new:
        with Session(config.database.engine) as session:
            db_new = session.get(new, self.id)
            if not db_new:
                raise HTTPException(status_code=404, detail="new not found")
            new_data = self.dict(exclude_unset=True)
            for key, value in new_data.items():
                if value is not None:
                    setattr(db_new, key, value)
            session.add(db_new)
            session.commit()
            session.refresh(db_new)
            return db_new


class newDelete(BaseModel):
    id: int

    def delete(self, config: Config) -> new:
        config.init()
        with Session(config.database.engine) as session:
            new = session.get(new, self.id)
            if not new:
                raise HTTPException(status_code=404, detail="new not found")
            session.delete(new)
            session.commit()
            return {"ok": True}
