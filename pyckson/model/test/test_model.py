from inspect import Parameter
from unittest import TestCase

from pyckson import listtype
from pyckson.model.builder import PycksonModelBuilder
from pyckson.model.helpers import ModelProviderImpl
from pyckson.parsers.base import ListParser, BasicParser
from pyckson.parsers.provider import ParserProviderImpl
from pyckson.serializers.provider import SerializerProviderImpl


class DummyClass:
    pass


class PycksonAttributeTest(TestCase):
    def test_should_build_simple_parameter(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=int)

        attribute = PycksonModelBuilder(DummyClass,
                                        SerializerProviderImpl(ModelProviderImpl()),
                                        ParserProviderImpl(ModelProviderImpl())).build_attribute(parameter)

        self.assertEqual(attribute.python_name, 'foo')
        self.assertEqual(attribute.attr_type, int)
        self.assertEqual(attribute.optional, False)

    def test_should_build_optional_parameter(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=int, default=None)

        attribute = PycksonModelBuilder(DummyClass,
                                        SerializerProviderImpl(ModelProviderImpl()),
                                        ParserProviderImpl(ModelProviderImpl())).build_attribute(parameter)

        self.assertEqual(attribute.python_name, 'foo')
        self.assertEqual(attribute.attr_type, int)
        self.assertEqual(attribute.optional, True)

    def test_should_camel_case_name(self):
        parameter = Parameter('foo_bar', Parameter.POSITIONAL_OR_KEYWORD, annotation=int)

        attribute = PycksonModelBuilder(DummyClass,
                                        SerializerProviderImpl(ModelProviderImpl()),
                                        ParserProviderImpl(ModelProviderImpl())).build_attribute(parameter)

        self.assertEqual(attribute.python_name, 'foo_bar')
        self.assertEqual(attribute.json_name, 'fooBar')

    def test_should_not_accept_untyped_parameter(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD)

        with self.assertRaises(TypeError):
            PycksonModelBuilder(DummyClass,
                                SerializerProviderImpl(ModelProviderImpl()),
                                ParserProviderImpl(ModelProviderImpl())).build_attribute(parameter)

    def test_should_not_accept_keyword_only_parameter(self):
        parameter = Parameter('foo', Parameter.KEYWORD_ONLY, annotation=int)

        with self.assertRaises(TypeError):
            PycksonModelBuilder(DummyClass,
                                SerializerProviderImpl(ModelProviderImpl()),
                                ParserProviderImpl(ModelProviderImpl())).build_attribute(parameter)

    def test_should_not_accept_positional_only_parameter(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_ONLY, annotation=int)

        with self.assertRaises(TypeError):
            PycksonModelBuilder(DummyClass,
                                SerializerProviderImpl(ModelProviderImpl()),
                                ParserProviderImpl(ModelProviderImpl())).build_attribute(parameter)

    def test_should_not_accept_var_positionalparameter(self):
        parameter = Parameter('foo', Parameter.VAR_POSITIONAL, annotation=int)

        with self.assertRaises(TypeError):
            PycksonModelBuilder(DummyClass,
                                SerializerProviderImpl(ModelProviderImpl()),
                                ParserProviderImpl(ModelProviderImpl())).build_attribute(parameter)

    def test_should_not_accept_var_keyword_parameter(self):
        parameter = Parameter('foo', Parameter.VAR_KEYWORD, annotation=int)

        with self.assertRaises(TypeError):
            PycksonModelBuilder(DummyClass,
                                SerializerProviderImpl(ModelProviderImpl()),
                                ParserProviderImpl(ModelProviderImpl())).build_attribute(parameter)

    def test_should_refuse_unspecified_list(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=list)

        with self.assertRaises(TypeError):
            PycksonModelBuilder(DummyClass,
                                SerializerProviderImpl(ModelProviderImpl()),
                                ParserProviderImpl(ModelProviderImpl())).build_attribute(parameter)

    def test_should_accept_specified_list(self):
        @listtype('foo', int)
        class ListDummyClass:
            pass

        parameter = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=list)

        attribute = PycksonModelBuilder(ListDummyClass,
                                        SerializerProviderImpl(ModelProviderImpl()),
                                        ParserProviderImpl(ModelProviderImpl())).build_attribute(parameter)

        self.assertEqual(type(attribute.parser), ListParser)
        self.assertEqual(type(attribute.parser.sub_parser), BasicParser)


class PycksonModelTest(TestCase):
    def test_should_parse_basic_signature(self):
        class Foo:
            def __init__(self, foo: int, bar: str):
                pass

        model = PycksonModelBuilder(Foo,
                                    SerializerProviderImpl(ModelProviderImpl()),
                                    ParserProviderImpl(ModelProviderImpl())).build_model()

        self.assertEqual(model.get_attribute(python_name='foo').python_name, 'foo')
        self.assertEqual(model.get_attribute(python_name='bar').python_name, 'bar')

    def test_should_ignore_self_parameter(self):
        class Foo:
            def __init__(self, foo: int):
                pass

        model = PycksonModelBuilder(Foo,
                                    SerializerProviderImpl(ModelProviderImpl()),
                                    ParserProviderImpl(ModelProviderImpl())).build_model()

        self.assertEqual(model.get_attribute(python_name='foo').python_name, 'foo')
        with self.assertRaises(KeyError):
            model.get_attribute(python_name='self')

    def test_should_use_typeinfo_for_lists(self):
        @listtype('foo', int)
        @listtype('bar', int)
        class Foo:
            def __init__(self, foo: list, bar: list):
                pass

        model = PycksonModelBuilder(Foo,
                                    SerializerProviderImpl(ModelProviderImpl()),
                                    ParserProviderImpl(ModelProviderImpl())).build_model()

        self.assertEqual(model.get_attribute(python_name='foo').python_name, 'foo')
        with self.assertRaises(KeyError):
            model.get_attribute(python_name='self')
