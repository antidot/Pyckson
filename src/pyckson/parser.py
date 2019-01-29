from pyckson.helpers import is_list_annotation
from pyckson.model.helpers import ModelProviderImpl
from pyckson.parsers.advanced import GenericParser


def parse(cls, value):
    """Takes a class and a dict and try to build an instance of the class

    :param cls: The class to parse
    :param value: either a dict, a list or a scalar value
    """
    if is_list_annotation(cls):
        if not isinstance(value, list):
            raise TypeError('Could not parse {} because value is not a list'.format(cls))
        return [parse(cls.__args__[0], o) for o in value]
    else:
        return GenericParser(cls, ModelProviderImpl()).parse(value)
