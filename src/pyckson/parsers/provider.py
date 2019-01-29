try:
    from typing import _ForwardRef as ForwardRef
except ImportError:
    from typing import ForwardRef

from pyckson.const import BASIC_TYPES, PYCKSON_TYPEINFO, PYCKSON_ENUM_OPTIONS, ENUM_CASE_INSENSITIVE, PYCKSON_PARSER, \
    DATE_TYPES, EXTRA_TYPES
from pyckson.helpers import TypeProvider, is_list_annotation, is_set_annotation, is_enum_annotation, \
    is_basic_dict_annotation, is_typing_dict_annotation
from pyckson.parsers.advanced import UnresolvedParser, ClassParser, CustomDeferredParser, DateParser
from pyckson.parsers.base import Parser, BasicParser, ListParser, CaseInsensitiveEnumParser, DefaultEnumParser, \
    BasicDictParser, SetParser, BasicParserWithCast, TypingDictParser
from pyckson.providers import ParserProvider, ModelProvider


class ParserProviderImpl(ParserProvider):
    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider

    def get(self, obj_type, parent_class, name_in_parent) -> Parser:
        if obj_type in BASIC_TYPES:
            return BasicParserWithCast(obj_type)
        if obj_type in EXTRA_TYPES:
            return BasicParser()
        if obj_type in DATE_TYPES:
            return DateParser(parent_class, obj_type)
        if hasattr(obj_type, PYCKSON_PARSER):
            return CustomDeferredParser(obj_type)
        if type(obj_type) is str or type(obj_type) is ForwardRef:
            return UnresolvedParser(TypeProvider(parent_class, obj_type), self.model_provider)
        if obj_type is list:
            type_info = getattr(parent_class, PYCKSON_TYPEINFO, dict())
            if name_in_parent in type_info:
                sub_type = type_info[name_in_parent]
                return ListParser(self.get(sub_type, parent_class, name_in_parent))
            else:
                raise TypeError('list parameter {} in class {} has no subType'.format(name_in_parent,
                                                                                      parent_class.__name__))
        if obj_type is set:
            type_info = getattr(parent_class, PYCKSON_TYPEINFO, dict())
            if name_in_parent in type_info:
                sub_type = type_info[name_in_parent]
                return SetParser(self.get(sub_type, parent_class, name_in_parent))
            else:
                raise TypeError('set parameter {} in class {} has no subType'.format(name_in_parent,
                                                                                     parent_class.__name__))
        if is_list_annotation(obj_type):
            return ListParser(self.get(obj_type.__args__[0], parent_class, name_in_parent))
        if is_set_annotation(obj_type):
            return SetParser(self.get(obj_type.__args__[0], parent_class, name_in_parent))
        if is_enum_annotation(obj_type):
            options = getattr(obj_type, PYCKSON_ENUM_OPTIONS, {})
            if options.get(ENUM_CASE_INSENSITIVE, False):
                return CaseInsensitiveEnumParser(obj_type)
            else:
                return DefaultEnumParser(obj_type)
        if is_basic_dict_annotation(obj_type):
            return BasicDictParser()
        if is_typing_dict_annotation(obj_type):
            if obj_type.__args__[0] != str:
                raise TypeError('typing.Dict key can only be str in class {}'.format(parent_class))
            return TypingDictParser(self.get(obj_type.__args__[1], parent_class, name_in_parent))
        return ClassParser(obj_type, self.model_provider)
