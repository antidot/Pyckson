from pyckson.model.helpers import ModelProviderImpl
from pyckson.serializers.advanced import GenericSerializer


def serialize(obj):
    return GenericSerializer(ModelProviderImpl()).serialize(obj)
