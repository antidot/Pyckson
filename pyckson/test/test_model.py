from inspect import Parameter, Signature
from unittest import TestCase

from pyckson.model import PycksonAttribute, ListType, PycksonModel


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


class PycksonModelTest(TestCase):
    def test_should_parse_basic_signature(self):
        param1 = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=int)
        param2 = Parameter('bar', Parameter.POSITIONAL_OR_KEYWORD, annotation=str)
        signature = Signature([param1, param2])

        model = PycksonModel.from_signature(signature, {})

        self.assertEqual(model.get_attribute(python_name='foo').python_name, 'foo')
        self.assertEqual(model.get_attribute(python_name='bar').python_name, 'bar')

    def test_should_ignore_self_parameter(self):
        param1 = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=int)
        param2 = Parameter('self', Parameter.POSITIONAL_OR_KEYWORD)
        signature = Signature([param1, param2])

        model = PycksonModel.from_signature(signature, {})

        self.assertEqual(model.get_attribute(python_name='foo').python_name, 'foo')
        with self.assertRaises(KeyError):
            model.get_attribute(python_name='self')

    def test_should_use_typeinfo_for_lists(self):
        param1 = Parameter('foo', Parameter.POSITIONAL_OR_KEYWORD, annotation=list)
        param2 = Parameter('bar', Parameter.POSITIONAL_OR_KEYWORD, annotation=list)
        signature = Signature([param1, param2])

        model = PycksonModel.from_signature(signature, {'foo': int, 'bar': list})

        self.assertEqual(model.get_attribute(python_name='foo').python_name, 'foo')
        with self.assertRaises(KeyError):
            model.get_attribute(python_name='self')

