from pyckson.model.model import PycksonModel
from pyckson.parsers.base import Parser
from pyckson.serializers.base import Serializer


class ParserProvider:
    def get(self, obj_type, parent_class, name_in_parent) -> Parser:
        pass


class SerializerProvider:
    def get(self, obj_type, parent_class, name_in_parent) -> Serializer:
        pass


class ModelProvider:
    def get_or_build(self, obj_or_class) -> PycksonModel:
        pass
