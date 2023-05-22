from polyfactory.factories.pydantic_factory import ModelFactory

from learn_sql_model.models.hero import Hero
from learn_sql_model.models.pet import Pet

__relationship__ = [Hero]


class PetFactory(ModelFactory[Pet]):
    __model__ = Pet
    __set_as_default_factory_for_type__ = True
    id = None

    @classmethod
    def name(cls) -> str:
        return cls.__faker__.first_name()
