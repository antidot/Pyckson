from enum import Enum
from typing import List

from pyckson.const import BASIC_TYPES, PYCKSON_TYPEINFO
from pyckson.helpers import TypeProvider
from pyckson.helpers import get_model, is_base_type


def serialize_class(obj):
    model = get_model(obj)
    result = {}
    for attribute in model.attributes:
        value = getattr(obj, attribute.python_name, None)
        if value is None and attribute.optional:
            continue
        elif value is None:
            raise ValueError('attribute {} of {} is None but not marked as optional'.format(attribute.python_name, obj))
        result[attribute.json_name] = attribute.serializer.serialize(value)
    return result


def serialize(obj):
    if is_base_type(obj):
        return obj
    else:
        return serialize_class(obj)


class Serializer:
    def serialize(self, obj):
        pass


class BasicSerializer(Serializer):
    def serialize(self, obj):
        return obj


class ListSerializer(Serializer):
    def __init__(self, sub_serializer: Serializer):
        self.sub_serializer = sub_serializer

    def serialize(self, obj):
        return [self.sub_serializer.serialize(item) for item in obj]


class UnresolvedSerializer(Serializer):
    def __init__(self, type_provider: TypeProvider):
        self.type_provider = type_provider

    def serialize(self, obj):
        return serialize(obj)


class ClassSerializer(Serializer):
    def serialize(self, obj):
        return serialize_class(obj)


class EnumSerializer(Serializer):
    def serialize(self, obj):
        return obj.name


def get_serializer(obj_type, parent_class, name_in_parent) -> Serializer:
    if obj_type in BASIC_TYPES:
        return BasicSerializer()
    if type(obj_type) is str:
        return UnresolvedSerializer(TypeProvider(parent_class, obj_type))
    if obj_type is list:
        type_info = getattr(parent_class, PYCKSON_TYPEINFO, dict())
        if name_in_parent in type_info:
            sub_type = type_info[name_in_parent]
            return ListSerializer(get_serializer(sub_type, parent_class, name_in_parent))
        else:
            raise TypeError('list parameter {} in class {} has no subType'.format(name_in_parent,
                                                                                  parent_class.__name__))
    if issubclass(obj_type, List):
        return ListSerializer(get_serializer(obj_type.__args__[0], parent_class, name_in_parent))
    if issubclass(obj_type, Enum):
        return EnumSerializer()
    return ClassSerializer()
