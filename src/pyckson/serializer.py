from pyckson.model.helpers import ModelProviderImpl
from pyckson.serializers.advanced import GenericSerializer


def serialize(obj):
    """Takes a object and produces a dict-like representation

    :param obj: the object to serialize
    """
    if isinstance(obj, list):
        return [serialize(o) for o in obj]
    return GenericSerializer(ModelProviderImpl()).serialize(obj)
