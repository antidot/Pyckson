from enum import Enum
from typing import List, _ForwardRef, Dict

from pyckson.const import BASIC_TYPES, PYCKSON_TYPEINFO
from pyckson.providers import SerializerProvider, ModelProvider
from pyckson.serializers.advanced import ClassSerializer, GenericSerializer
from pyckson.serializers.base import BasicSerializer, ListSerializer, EnumSerializer, Serializer, DictSerializer


class SerializerProviderImpl(SerializerProvider):
    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider

    def get(self, obj_type, parent_class, name_in_parent) -> Serializer:
        if obj_type in BASIC_TYPES:
            return BasicSerializer()
        if type(obj_type) is str or  type(obj_type) is _ForwardRef:
            return GenericSerializer(self.model_provider)
        if obj_type is list:
            type_info = getattr(parent_class, PYCKSON_TYPEINFO, dict())
            if name_in_parent in type_info:
                sub_type = type_info[name_in_parent]
                return ListSerializer(self.get(sub_type, parent_class, name_in_parent))
            else:
                raise TypeError('list parameter {} in class {} has no subType'.format(name_in_parent,
                                                                                      parent_class.__name__))
        if issubclass(obj_type, List):
            return ListSerializer(self.get(obj_type.__args__[0], parent_class, name_in_parent))
        if issubclass(obj_type, Enum):
            return EnumSerializer()
        if issubclass(obj_type, Dict) or issubclass(obj_type, dict):
            return DictSerializer()
        return ClassSerializer(self.model_provider)
