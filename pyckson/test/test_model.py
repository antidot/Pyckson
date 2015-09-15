from inspect import Parameter
from unittest import TestCase
from pyckson.model import PycksonAttribute, ListType


class PycksonAttributeTest(TestCase):
    def test_should_build_simple_parameter(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=int)

        attribute = PycksonAttribute.from_parameter(parameter)

        self.assertEqual(attribute.python_name, 'foo')
        self.assertEqual(attribute.attr_type, int)
        self.assertEqual(attribute.optional, False)

    def test_should_build_optional_parameter(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=int, default=None)

        attribute = PycksonAttribute.from_parameter(parameter)

        self.assertEqual(attribute.python_name, 'foo')
        self.assertEqual(attribute.attr_type, int)
        self.assertEqual(attribute.optional, True)

    def test_should_consider_other_default_values_as_mandatory(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=int, default=0)

        attribute = PycksonAttribute.from_parameter(parameter)

        self.assertEqual(attribute.python_name, 'foo')
        self.assertEqual(attribute.attr_type, int)
        self.assertEqual(attribute.optional, False)

    def test_should_camel_case_name(self):
        parameter = Parameter('foo_bar', Parameter.POSITIONAL_OR_KEYWORD, annotation=int)

        attribute = PycksonAttribute.from_parameter(parameter)

        self.assertEqual(attribute.python_name, 'foo_bar')
        self.assertEqual(attribute.json_name, 'fooBar')

    def test_should_not_accept_untyped_parameter(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD)

        with self.assertRaises(TypeError):
            PycksonAttribute.from_parameter(parameter)

    def test_should_not_accept_keyword_only_parameter(self):
        parameter = Parameter('foo', Parameter.KEYWORD_ONLY, annotation=int)

        with self.assertRaises(TypeError):
            PycksonAttribute.from_parameter(parameter)

    def test_should_not_accept_positional_only_parameter(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_ONLY, annotation=int)

        with self.assertRaises(TypeError):
            PycksonAttribute.from_parameter(parameter)

    def test_should_not_accept_var_positionalparameter(self):
        parameter = Parameter('foo', Parameter.VAR_POSITIONAL, annotation=int)

        with self.assertRaises(TypeError):
            PycksonAttribute.from_parameter(parameter)

    def test_should_not_accept_var_keyword_parameter(self):
        parameter = Parameter('foo', Parameter.VAR_KEYWORD, annotation=int)

        with self.assertRaises(TypeError):
            PycksonAttribute.from_parameter(parameter)

    def test_should_refuse_unspecified_list(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=list)

        with self.assertRaises(TypeError):
            PycksonAttribute.from_parameter(parameter)

    def test_should_accept_specified_list(self):
        parameter = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=list)

        attribute = PycksonAttribute.from_parameter(parameter, sub_type=int)

        self.assertEqual(type(attribute.attr_type), ListType)
        self.assertEqual(attribute.attr_type.sub_type, int)
