from pyckson.model.helpers import ModelProviderImpl
from pyckson.serializers.advanced import GenericSerializer


def serialize(obj):
    """Takes a object and produces a dict-like representation

    :param obj: the object to serialize
    """
    return GenericSerializer(ModelProviderImpl()).serialize(obj)
