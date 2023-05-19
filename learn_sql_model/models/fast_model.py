from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, select

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
            from learn_sql_model.config import get_config

            config = get_config()

        self.pre_post()

        with config.session as session:
            session.add(self)
            session.commit()

    @classmethod
    def get(
        self, item_id: int = None, config: "Config" = None
    ) -> Optional["FastModel"]:
        if config is None:
            from learn_sql_model.config import get_config

            config = get_config()

        self.pre_get()

        with config.session as session:
            if item_id is None:
                return session.exec(select(self)).all()
            return session.exec(select(self).where(self.id == item_id)).one()
