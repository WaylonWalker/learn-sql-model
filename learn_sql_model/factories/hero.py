from polyfactory.factories.pydantic_factory import ModelFactory

from learn_sql_model.models.hero import Hero


class HeroFactory(ModelFactory[Hero]):
    __model__ = Hero
