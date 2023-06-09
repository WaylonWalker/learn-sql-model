from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory

from learn_sql_model.factories.pet import PetFactory
from learn_sql_model.models.hero import Hero
from learn_sql_model.models.pet import Pet


class HeroFactory(ModelFactory[Hero]):
    __model__ = Hero
    __faker__ = Faker(locale="en_US")
    __set_as_default_factory_for_type__ = True
    pet_id = None

    @classmethod
    def name(cls) -> str:
        return (
            cls.__faker__.word(part_of_speech="adjective")
            + "-"
            + cls.__faker__.word(part_of_speech="noun")
        )

    @classmethod
    def secret_name(cls) -> str:
        return (
            cls.__faker__.word(part_of_speech="adjective")
            + "-"
            + cls.__faker__.word(part_of_speech="noun")
        )

    @classmethod
    def age(cls) -> str:
        return cls.__faker__.pyint(min_value=5, max_value=100)

    @classmethod
    def shoe_size(cls) -> str:
        return cls.__faker__.pyint(min_value=5, max_value=14)

    @classmethod
    def pet(cls) -> Pet:
        return PetFactory().build
