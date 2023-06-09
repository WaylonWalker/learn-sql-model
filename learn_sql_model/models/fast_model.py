from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, select

from learn_sql_model.config import get_config

if TYPE_CHECKING:
    from learn_sql_model.config import Config


class FastModel(SQLModel):
    def pre_post(self) -> None:
        """run before post"""

    def pre_delete(self) -> None:
        """run before delete"""

    @classmethod
    def pre_get(self) -> None:
        """run before get"""

    def post(self, config: "Config" = None) -> None:
        if config is None:
            config = get_config()

        self.pre_post()

        with config.database.session as session:
            session.add(self)
            session.commit()
            session.refresh(self)
        return

    def get(
        self, id: int = None, config: "Config" = None, where=None
    ) -> Optional["FastModel"]:
        if config is None:
            config = get_config()

        self.pre_get()

        with config.database.session as session:
            if id is None:
                statement = select(self.__class__)
                if where is not None:
                    statement = statement.where(where).options()
                results = session.exec(statement).all()
            else:
                print("get by id")
                statement = select(self.__class__).where(self.__class__.id == id)
                results = session.exec(statement).one()
        return results

    def flags(self, config: "Config" = None) -> None:
        if config is None:
            config = get_config()
        flags = []
        for k, v in self.dict().items():
            if v:
                flags.append(f"--{k.replace('_', '-').lower()}")
                flags.append(v)
        return flags

    # TODO
    # update
    # delete
