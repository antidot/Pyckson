from pyckson.model.helpers import ModelProviderImpl
from pyckson.parsers.advanced import GenericParser


def parse(cls, value):
    """Takes a class and a dict and try to build an instance of the class

    :param cls: The class to parse
    :param value: either a dict, a list or a scalar value
    """
    return GenericParser(cls, ModelProviderImpl()).parse(value)
