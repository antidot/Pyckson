from pyckson.model.helpers import ModelProviderImpl
from pyckson.parsers.advanced import GenericParser


def parse(cls, json):
    return GenericParser(cls, ModelProviderImpl()).parse(json)
