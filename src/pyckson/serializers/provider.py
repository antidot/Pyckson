from pyckson.helpers import is_list_annotation, is_set_annotation, is_enum_annotation, is_dict_annotation

try:
    from typing import _ForwardRef as ForwardRef
except ImportError:
    from typing import ForwardRef

from pyckson.const import BASIC_TYPES, PYCKSON_TYPEINFO, PYCKSON_SERIALIZER, DATE_TYPES, EXTRA_TYPES
from pyckson.providers import SerializerProvider, ModelProvider
from pyckson.serializers.advanced import ClassSerializer, GenericSerializer, CustomDeferredSerializer, DateSerializer
from pyckson.serializers.base import BasicSerializer, ListSerializer, EnumSerializer, Serializer, DictSerializer


class SerializerProviderImpl(SerializerProvider):
    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider

    def get(self, obj_type, parent_class, name_in_parent) -> Serializer:
        if obj_type in BASIC_TYPES or obj_type in EXTRA_TYPES:
            return BasicSerializer()
        if obj_type in DATE_TYPES:
            return DateSerializer(parent_class, obj_type)
        if hasattr(obj_type, PYCKSON_SERIALIZER):
            return CustomDeferredSerializer(obj_type)
        if type(obj_type) is str or type(obj_type) is ForwardRef:
            return GenericSerializer(self.model_provider)
        if obj_type is list or obj_type is set:
            type_info = getattr(parent_class, PYCKSON_TYPEINFO, dict())
            if name_in_parent in type_info:
                sub_type = type_info[name_in_parent]
                return ListSerializer(self.get(sub_type, parent_class, name_in_parent))
            else:
                raise TypeError('list parameter {} in class {} has no subType'.format(name_in_parent,
                                                                                      parent_class.__name__))
        if is_list_annotation(obj_type) or is_set_annotation(obj_type):
            return ListSerializer(self.get(obj_type.__args__[0], parent_class, name_in_parent))
        if is_enum_annotation(obj_type):
            return EnumSerializer()
        if is_dict_annotation(obj_type):
            return DictSerializer()
        return ClassSerializer(self.model_provider)
