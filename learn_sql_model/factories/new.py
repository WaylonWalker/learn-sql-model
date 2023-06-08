from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory

from learn_sql_model.models.new import new


class newFactory(ModelFactory[new]):
    __model__ = new
    __faker__ = Faker(locale="en_US")
    __set_as_default_factory_for_type__ = True
    id = None

    __random_seed__ = 10

